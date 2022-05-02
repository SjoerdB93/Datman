import plotting_tools
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
import CallUI
from pathlib import Path
import os
from data import Data

def select_data_button(self):
    if not self.selection_button.isChecked():
        delete_selected(self)
        self.plot_figure()

def delete_selected(self):
    key_list = []
    for key in self.datadict:
        if key.endswith("_selected"):
            key_list.append(key)
    for key in key_list:
        del(self.datadict[key])

def load_files(self):
    files = get_path(self)
    open_selection(self, files)

def normalize_data(self):
    delete_selected(self)
    for key, item in self.datadict.items():
        item.ydata = normalize(item.ydata)
    self.plot_figure()

def shift_vertically(self):
    delete_selected(self)
    shifter = 1
    shift_value = 10000
    for key, item in self.datadict.items():
        item.ydata = [value * shifter for value in item.ydata]
        shifter *= shift_value
    self.plot_figure()

def center_data(self):
    delete_selected(self)
    for key, item in self.datadict.items():
        max_value = max(item.ydata)
        middle_index = item.ydata.index(max_value)
        middle_value = item.xdata[middle_index]
        item.xdata = [coordinate - middle_value for coordinate in item.xdata]
    self.plot_figure()

def normalize(ydata):
    max_y = max(ydata)
    new_y = [value / max_y for value in ydata]
    return new_y

def translate_y(self):
    for key, item in self.datadict.items():
        translate_value = float(self.translate_y_entry.text())
        item.ydata = [value + translate_value for value in item.ydata]
    self.plot_figure()

def translate_x(self):
    for key, item in self.datadict.items():
        translate_value = float(self.translate_x_entry.text())
        print(translate_value)
        item.xdata = [value + translate_value for value in item.xdata]
    self.plot_figure()

def multiply_y(self):
    for key, item in self.datadict.items():
        multiply_value = float(self.multiply_y_entry.text())
        item.ydata = [value * multiply_value for value in item.ydata]
    self.plot_figure()

def multiply_x(self):
    for key, item in self.datadict.items():
        multiply_value = float(self.multiply_x_entry.text())
        item.xdata = [value * multiply_value for value in item.xdata]
    self.plot_figure()

def cut_data(self):
    for key, item in self.datadict.items():
        xdata = item.xdata
        ydata = item.ydata
        new_x = []
        new_y = []
        if f"{key}_selected" in self.datadict:
            selected_item = self.datadict[f"{key}_selected"]
            for index, (valuex, valuey) in enumerate(zip(xdata, ydata)):
                if valuex < min(selected_item.xdata) or valuex > max(selected_item.xdata):
                    new_x.append(valuex)
                    new_y.append(valuey)
            item.xdata = new_x
            item.ydata = new_y
    delete_selected(self)
    self.plot_figure()


def open_selection(self, files):
    for file in files:
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


def get_path(self, documenttype="Text file (*.txt);;All Files (*)"):
    dialog = QFileDialog
    options = dialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    path = QFileDialog.getOpenFileNames(self, "Open files", "",
                                        documenttype, options=options)[0]
    return path
