import plotting_tools
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
from pathlib import Path
import os
from data import Data

def delete_selected(self):
    key_list = []
    for key in self.datadict:
        if key.endswith("_selected"):
            key_list.append(key)
    for key in key_list:
        del(self.datadict[key])

def load_file(self):
    file = get_path()


    if file != "":
        delete_selected(self)
        path = os.path.dirname(file)
        filename = Path(file).name
        self.data.filename = filename
        os.chdir(path)
        data = get_data(file)
        data.filename = filename
        if filename not in self.datadict:
            self.datadict[filename] = data
            self.open_item_list.addItem(filename)
        layout = self.graphlayout
        self.clearLayout(self.graphlayout)
        self.figurecanvas = plotting_tools.plotGraphOnCanvas(self, layout,
                                                             title=filename, scale="log", marker=None)
        self.figurecanvas[1].canvas.mpl_connect('button_press_event', self.on_press)
        self.figurecanvas[1].canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.figurecanvas[1].canvas.mpl_connect('button_release_event', self.on_release)




def get_data(path):
    data = Data()
    seperator = "\t"
    data_array = [[], []]
    with (open(path, 'r')) as file:
        for line in file:
            line = line.split(seperator)
            data_array[0].append(float(line[0]))
            data_array[1].append(float(line[1]))
    data.xdata = data_array[0]
    data.ydata = data_array[1]
    return data


def loadEmpty(self):
    verticalscan_canvas = plotting_tools.PlotWidget(xlabel="X value", ylabel="Y Value",
                                                    title="Plot")
    create_layout(self, verticalscan_canvas, self.graphlayout)


def create_layout(self, canvas, layout):
    toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(canvas)
    layout.addWidget(toolbar)


def get_path(documenttype="Text file (*.txt);;All Files (*)"):
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    path = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()", "", documenttype, options=options)[0]
    return path
