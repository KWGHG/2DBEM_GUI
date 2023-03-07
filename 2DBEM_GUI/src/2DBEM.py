import os
from asyncio.windows_events import NULL
from PyQt5 import QtWidgets, QtGui, QtCore
from parameters import parametric_airfoil
from potentialbase_panel_method import BEM
from Ui import Ui_mainWindow
from matplotlib.figure import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import sys, Ui
from Subui import Ui_subWindow


class myMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        
        super(myMainWindow ,self).__init__() 
        icon = self.resource_path(os.path.join("src" ,"plane1.png"))
        #print(icon)
        self.setWindowIcon(QtGui.QIcon(icon))
        self.ui = Ui_mainWindow()
        
        self.ui.setupUi(self)
        self.velocity = 0
        self.angle_of_attack = 0
        self.numbers_of_panel = 0
        self.CL = 0
        self.CP = NULL
        self.geometry = np.zeros(0)
        self.filePath = ""
        self.init()
        self.msg()
    def resource_path(self ,relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
            #print("YES " ,base_path)
        else:
            base_path = os.path.abspath("")
            #print("NO" ,base_path)
        return  os.path.join(base_path ,relative_path)

    def init(self): 
        self.ui.Message_Label.setText(" Message ")
        self.ui.Angle_Input.setText("0")
        self.ui.Panels_Input.setText("0")
        self.ui.Velocity_Input.setText("0")
        self.setup_control()
    
    def msg(self):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(2)
        mbox.setText("Airfoil data must be in clockwise from trailing edge")
        mbox.setWindowTitle("Hint")
        mbox.exec_()
    def setup_control(self):
        self.ui.Load.clicked.connect(self.file_load)
        self.ui.PLOT.clicked.connect(self.airfoil_plot)
        self.ui.Velocity_Ok.clicked.connect(self.velocity_onButtonClick)
        self.ui.Angle_Ok.clicked.connect(self.angle_of_attack_onButtonClick)
        self.ui.Panels_Ok.clicked.connect(self.numbers_of_panel_onButtonClick)
        self.ui.Calculation.clicked.connect(self.calculation)
        self.ui.CP_Contour_Plot.clicked.connect(self.CP_plot)
        self.ui.Download.clicked.connect(self.download_Cp)



    def file_load(self):
        self.filePath, filterType = QtWidgets.QFileDialog.getOpenFileName(
            self, "Open file", "./"
        )

    def airfoil_plot(self):
        if self.filePath == "" or self.numbers_of_panel == 0:
            self.ui.Message_Label.setText("Input numbers of panel or loading file ")
        else:
            self.geometry = np.array(parametric_airfoil(self.filePath, self.numbers_of_panel))
            plt.cla()
            fig = plt.figure(figsize=(5, 2))
            ax = fig.add_axes([0.15, 0.25, 0.7, 0.7])
            ax.set_xlim([-0.1, 1.1])

            ax.set_xlabel("x/c")
            ax.plot(self.geometry[:, 0], self.geometry[:, 1], "o--")

            cavans = FigureCanvas(fig)
            graphicscene = QtWidgets.QGraphicsScene()
            graphicscene.addWidget(cavans)
            self.ui.graphicsView.setScene(graphicscene)
            self.ui.graphicsView.show()


    def velocity_onButtonClick(self):
        velocity = float(self.ui.Velocity_Input.text())
        self.velocity = velocity

    def angle_of_attack_onButtonClick(self):
        angle_of_attack = float(self.ui.Angle_Input.text())
        self.angle_of_attack = angle_of_attack

    def numbers_of_panel_onButtonClick(self):
        #if self.filePath == "" or self.numbers_of_panel == 0:
        #    self.ui.Message_Label.setText("Input numbers of panel ")
        #else:
        self.numbers_of_panel = float(self.ui.Panels_Input.text())
        if self.filePath != "":
            self.geometry = np.array(parametric_airfoil(self.filePath, self.numbers_of_panel))
            

    def calculation(self):
        if self.geometry.size == 0 or self.velocity == 0 :
            self.ui.Message_Label.setText(" Please input file ")
        else:
            self.CL, self.CP = BEM(self.velocity, self.angle_of_attack, self.geometry)
            self.ui.CL_Label.setText(str(round(self.CL, 3)))

    def CP_plot(self):
        if self.CL == 0:
            self.ui.Message_Label.setText("Please input file or parameters ")
        else:
            self.subui = Ui_subWindow()
            plt.cla()
            fig = plt.figure(figsize=(9, 2.5))
            ax = fig.add_axes([0.15, 0.25, 0.7, 0.7])
            ax.set_xlim([-0.1, 1.1])

            ax.set_xlabel("x/c")
            ax.plot(self.CP[:, 0], self.CP[:, 1], "o--")
            cavans = FigureCanvas(fig)
            graphicscene = QtWidgets.QGraphicsScene()
            graphicscene.addWidget(cavans)
            self.subui.graphicsView.setScene(graphicscene)
            self.subui.graphicsView.show()

    def download_Cp(self):
        if self.CL == 0:
            self.ui.Message_Label.setText("Please input file or parameters ")
        else:
            file = open("cp.dat", "w")
            rows, columns = self.CP.shape
            for i in range(rows):
                str1 = str(self.CP[i, 0]) + "\t" + str(self.CP[i, 1]) + "\n"
                file.write(str1)
            file.close()


if __name__ == "__main__":
    #print("Work dir:" + os.getcwd())
    app = QtWidgets.QApplication(sys.argv)
    window = myMainWindow()
    window.show()
    sys.exit(app.exec_())
