from matplotlib.colors import LogNorm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



def plotGraphOnCanvas(self, layout, title = "", scale="log", marker = None, revert = False):
    canvas = PlotWidget(xlabel="Detector position (pixels)", ylabel="Intensity (arb. u)",
                        title = "Horizontal Scan")
    figure = canvas.figure
    for key, item in self.datadict.items():
        X = item.xdata
        Y = item.ydata
        plotgGraphFigure(X, Y, canvas, filename=key, revert=revert, title=title)
    layout.addWidget(canvas)
    figurecanvas = [figure, canvas]
    self.toolbar = NavigationToolbar(canvas, self)
    layout.addWidget(self.toolbar)
    return figurecanvas

def plotgGraphFigure(X, Y, canvas, filename="", xlim=None, title="", scale="log",marker=None, linestyle="solid",
                     revert = False):
    fig = canvas.theplot
    fig.plot(X, Y, label=filename, linestyle=linestyle, marker=marker)
    if revert:
        fig.invert_xaxis()
    canvas.theplot.set_title(title)
    canvas.theplot.set_xlim(xlim)
    canvas.theplot.set_yscale(scale)
    fig.legend()





class PlotWidget(FigureCanvas):
    def __init__(self, parent=None, xlabel=None, ylabel='Intensity (arb. u)', title="", scale="linear"):
        super(PlotWidget, self).__init__(Figure())
        self.setParent(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.theplot = self.figure.add_subplot(111)
        self.theplot.set_title(title)
        self.theplot.set_xlabel(xlabel)
        self.theplot.set_ylabel(ylabel)
        self.figure.set_tight_layout(True)