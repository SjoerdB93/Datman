#CallUI.py
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui
from data import Data
import datman
Ui_MainWindow, QtBaseClass = uic.loadUiType("form.ui")



class CallUI(QtBaseClass, Ui_MainWindow):
    def __init__(self):
        QtBaseClass.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.data = Data()
        self.connectActions()
        datman.loadEmpty(self)


    def connectActions(self):
        # Connect File actions
        self.load_button.clicked.connect(lambda: datman.load_file(self))

    def clearLayout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

def setUpWindow():
    app = QtWidgets.QApplication(sys.argv)
    nowWindow = CallUI()
    nowWindow.showMaximized()
    sys.exit(app.exec_())

