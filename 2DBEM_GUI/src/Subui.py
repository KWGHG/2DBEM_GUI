from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_subWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.ui()

    def ui(self):
        self.graphicsView = QtWidgets.QGraphicsView()
        self.graphicsView.setWindowTitle("-CP Plot")
        self.graphicsView.setGeometry(QtCore.QRect(550, 380, 1000, 300))
        self.graphicsView.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.graphicsView.setFrameShadow(QtWidgets.QFrame.Plain)
        self.graphicsView.setObjectName("graphicsView")