import sys
import math
# Импортируем наш интерфейс из файла
from new_label import *
from numpy import float64
from PyQt5 import QtWidgets, QtGui, QtCore
from MyMplCanc import MtMplCanv
import Math_Part
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import PyQt5
from MyMplCanc import MtMplCanv
from matplotlib.figure import Figure
from widg import *
class MyWin(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.secWin = None
        self.figure = Figure()

        # добавление шаблона размещения на виджет
        self.companovka_for_mpl = QtWidgets.QVBoxLayout(self.Widget)
        # получение объекта класса холста с нашим рисунком
        self.canvas = MtMplCanv(self.figure)
        # Размещение экземпляра класса холста в шаблоне размещения
        self.companovka_for_mpl.addWidget(self.canvas)
        # получение объекта класса панели управления холста
        self.toolbar = NavigationToolbar(self.canvas, self)
        # Размещение экземпляра класса панели управления в шаблоне размещения
        self.companovka_for_mpl.addWidget(self.toolbar)
        # Здесь прописываем событие нажатия на кнопку
        self.pushButton.clicked.connect(self.MyFunction)

    def MyFunction(self):
        u0 = float64(self.textEdit_3.toPlainText())
        h = float64(self.textEdit_4.toPlainText())
        # x0 = float(self.textEdit_5.toPlainText())
        n = int(self.textEdit_6.toPlainText())
        eps = float64(self.textEdit_7.toPlainText())
        a = float64(self.textEdit_8.toPlainText())
        b = float64(self.textEdit_9.toPlainText())
        d = float64(self.textEdit_2.toPlainText())
        if self.comboBox.currentText() == "Test":
            self.label.setText("du/dx = 7*u\nu(0) = u0")
        if self.comboBox.currentText() == "Main 1":
            self.label.setText("du/dx = (1/(1 + 3*x + x^2)) * u^2 + u - u^3 * sin(10*x)\nu(0) = u0")
        self.secWin = second_window(self)
        Math_Part.Math_Part.bilding(self, n, u0, h, a, b, eps, self.secWin, d)
        self.secWin.show()
       
class second_window(QtWidgets.QMainWindow, Ui_MainWindow_new):
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
    

        
if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    try: 
        sys.exit(app.exec_())
    except SystemExit:
        ...