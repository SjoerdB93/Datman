# CallUI.py
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
import plotting_tools
from data import Data
import datman
import pywinauto
import numpy as np

Ui_MainWindow, QtBaseClass = uic.loadUiType("form.ui")


class CallUI(QtBaseClass, Ui_MainWindow):
    def __init__(self):
        QtBaseClass.__init__(self)
        Ui_MainWindow.__init__(self)
        self.figurecanvas = None
        self.datadict = {}
        print(self.datadict)
        self.setupUi(self)
        self.clicked = False
        self.data = Data()
        self.connectActions()
        datman.loadEmpty(self)

    def connectActions(self):
        # Connect File actions
        self.load_button.clicked.connect(lambda: datman.load_files(self))
        self.cut_data_button.clicked.connect(lambda: datman.cut_data(self))
        self.remove_button.clicked.connect(self.remove_sample)
        self.save_button.clicked.connect(self.save_data)
        self.normalize_button.clicked.connect(lambda: datman.normalize_data(self))
        self.shift_vertically_button.clicked.connect(lambda: datman.shift_vertically(self))
        self.center_button.clicked.connect(lambda: datman.center_data(self))
        self.selection_button.clicked.connect(lambda: datman.select_data_button(self))

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_press(self, event):
        self.clicked = True
        self.startx = event.xdata

    def on_hover(self, event):
        if self.clicked == True and self.selection_button.isChecked():
            self.stopx = event.xdata

    def remove_sample(self):
        datman.delete_selected(self)
        if self.open_item_list.currentItem() is not None:
            key_to_remove = self.open_item_list.currentItem().text()
            del (self.datadict[key_to_remove])
            self.open_item_list.takeItem(self.open_item_list.currentRow())
            self.plot_figure()

    def sort_data(self, x, y):
        bar_list = {"x": x, "y": y}
        sorted = self.sort_bar(bar_list)
        return sorted["x"], sorted["y"]
        self.data.xdata = sorted["x"]
        self.data.ydata = sorted["y"]

    def sort_bar(self, bar_list):
        sorted_x = []
        sorted_x.extend(bar_list['x'])
        sorted_x.sort()
        sorted_y = []
        for x in sorted_x:
            sorted_y.append(bar_list['y'][bar_list['x'].index(x)])
        return {"x": sorted_x, "y": sorted_y}

    def save_data(self):
        datman.delete_selected(self)
        if len(self.datadict) == 1:
            for key, item in self.datadict.items():
                xdata = item.xdata
                ydata = item.ydata
            path = self.saveFileDialog()
            filename = path[0]
            if filename[-4:] != ".txt":
                filename = filename + ".txt"
            array = np.stack([xdata, ydata], axis=1)
            np.savetxt(filename, array, delimiter="\t")
        elif len(self.datadict) > 1:
            path = self.saveFileDialog()[0]
            for key, item in self.datadict.items():
                xdata = item.xdata
                ydata = item.ydata
                filename = item.filename
                filename = filename.split(".")[0]
                filename = f"{path}{filename}_edited.txt"
                array = np.stack([xdata, ydata], axis=1)
                np.savetxt(filename, array, delimiter="\t")

    def saveFileDialog(self, documenttype="Text file (*.txt)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", self.data.filename[:-4],
                                               documenttype, options=options)
        return fileName

    def saveFile(self, horizontal=True):
        pass

    def on_release(self, event):
        self.clicked = False
        self.select_data()
        # self.plot_figure()

    def plot_figure(self, layout=None, filename="Test"):
        if layout == None:
            layout = self.graphlayout
        self.clearLayout(layout)
        self.figurecanvas = plotting_tools.plotGraphOnCanvas(self, layout,
                                                             title=filename, scale="log", marker=None)
        self.figurecanvas[1].canvas.mpl_connect('button_press_event', self.on_press)
        self.figurecanvas[1].canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.figurecanvas[1].canvas.mpl_connect('button_release_event', self.on_release)

    def select_data(self):
        datman.delete_selected(self)
        selected_dict = {}
        startx = min(self.startx, self.stopx)
        stopx = max(self.startx, self.stopx)
        for key, item in self.datadict.items():
            xdata = item.xdata
            ydata = item.ydata
            xdata, ydata = self.sort_data(xdata, ydata)
            start_index = 0
            stop_index = len(xdata)
            found_start = False
            found_stop = False

            for index, value in enumerate(xdata):
                if value > startx and not found_start:
                    start_index = index
                    found_start = True
                if value > stopx and not found_stop:
                    stop_index = index
                    found_stop = True
            selected_data = Data()
            selected_data.xdata = xdata[start_index:stop_index]
            selected_data.ydata = ydata[start_index:stop_index]
            if len(selected_data.xdata) > 0 and (found_start or found_stop) == True:
                selected_dict[f"{key}_selected"] = selected_data
        if len(selected_dict) > 0:
            self.datadict.update(selected_dict)
            self.clearLayout(self.graphlayout)
            self.plot_figure()


def setUpWindow():
    app = QtWidgets.QApplication(sys.argv)
    nowWindow = CallUI()
    nowWindow.showMaximized()
    sys.exit(app.exec_())
