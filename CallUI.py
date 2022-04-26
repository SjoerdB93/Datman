#CallUI.py
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
import plotting_tools
from data import Data
import datman
import numpy as np
Ui_MainWindow, QtBaseClass = uic.loadUiType("form.ui")



class CallUI(QtBaseClass, Ui_MainWindow):
    def __init__(self):
        QtBaseClass.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.clicked = False
        self.data = Data()
        self.connectActions()
        datman.loadEmpty(self)


    def connectActions(self):
        # Connect File actions
        self.load_button.clicked.connect(lambda: datman.load_file(self))
        self.cut_data_button.clicked.connect(self.cut_data)
        self.save_button.clicked.connect(self.save_data)

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_press(self, event):
        self.clicked = True
        self.startx = event.xdata

    def on_hover(self, event):
        if self.clicked == True:
            self.stopx = event.xdata

    def sort_data(self):
        bar_list = {"x": self.data.xdata, "y": self.data.ydata}
        sorted = self.sort_bar(bar_list)
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
        path = self.saveFileDialog()
        filename = path[0]
        if filename[-4:] != ".txt":
            filename = filename + ".txt"
        array = np.stack([self.data.xdata, self.data.ydata], axis=1)
        np.savetxt(filename, array, delimiter="\t")

    def saveFileDialog(self, documenttype="Text file (*.txt)"):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", self.data.filename[:-4],
                                               documenttype, options=options)
        return fileName

    def saveFile(self, horizontal = True):
        pass

    def on_release(self, event):
        self.clicked = False
        self.select_data()
        self.plot_figure()

    def plot_figure(self):
        layout = self.graphlayout
        self.clearLayout(layout)

        self.figurecanvas = plotting_tools.plot_multiple(self, layout, self.data.xdata, self.data.ydata,
                                                         X2 = self.data.xdata_selected, Y2 = self.data.ydata_selected, title=self.data.filename,
                                                         scale="log", marker=None)
        self.figurecanvas[1].canvas.mpl_connect('button_press_event', self.on_press)
        self.figurecanvas[1].canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.figurecanvas[1].canvas.mpl_connect('button_release_event', self.on_release)


    def cut_data(self):
        new_x = []
        new_y = []
        if self.data.xdata_selected != [] and self.data.ydata_selected != []:
            for index, (valuex, valuey) in enumerate(zip(self.data.xdata, self.data.ydata)):
                if valuex < min(self.data.xdata_selected) or valuex > max(self.data.xdata_selected):
                    new_x.append(valuex)
                    new_y.append(valuey)
            self.data.xdata = new_x
            self.data.ydata = new_y
        self.data.xdata_selected = []
        self.data.ydata_selected = []
        self.plot_figure()


    def select_data(self):
        selected_data = [[], []]
        found_start = False
        found_stop = False
        print(self.data.xdata)
        for index, value in enumerate(self.data.xdata):
            if value > self.startx and not found_start:
                start_index = index
                found_start = True
            if value > self.stopx and not found_stop:
                stop_index = index
                found_stop = True
        print(f"len is {len(self.data.xdata[start_index:stop_index])}")
        print(start_index)
        print(stop_index)
        self.data.xdata_selected = self.data.xdata[start_index:stop_index]
        self.data.ydata_selected = self.data.ydata[start_index:stop_index]


def setUpWindow():
    app = QtWidgets.QApplication(sys.argv)
    nowWindow = CallUI()
    nowWindow.showMaximized()
    sys.exit(app.exec_())

