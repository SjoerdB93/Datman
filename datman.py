import plotting_tools
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path
import os
import data


def load_file(self):
    file = get_path()
    if file != "":
        path = os.path.dirname(file)
        filename = Path(file).name
        self.data.filename = filename
        os.chdir(path)
        data = get_data(file)
        self.data.xdata = data[0]
        self.data.ydata = data[1]
        self.sort_data()
        layout = self.graphlayout
        self.clearLayout(self.graphlayout)
        self.figurecanvas = plotting_tools.plotGraphOnCanvas(self, layout, self.data.xdata, self.data.ydata,
                                                             title=filename, scale="log", marker=None)
        self.figurecanvas[1].canvas.mpl_connect('button_press_event', self.on_press)
        self.figurecanvas[1].canvas.mpl_connect('motion_notify_event', self.on_hover)
        self.figurecanvas[1].canvas.mpl_connect('button_release_event', self.on_release)



def get_data(path):
    seperator = "\t"
    data = [[], []]
    with (open(path, 'r')) as file:
        for line in file:
            line = line.split(seperator)
            data[0].append(float(line[0]))
            data[1].append(float(line[1]))
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
