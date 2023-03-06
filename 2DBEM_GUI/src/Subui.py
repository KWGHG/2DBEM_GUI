from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_subWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('oxxo.studio.2')
        self.resize(300, 200)
        self.ui()

    def ui(self):
        self.graphicsView = QtWidgets.QGraphicsView()
        self.graphicsView.setGeometry(QtCore.QRect(20, 380, 511, 211))
        self.graphicsView.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.graphicsView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graphicsView.setObjectName("graphicsView")