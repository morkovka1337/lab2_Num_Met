import sys
import math
# Импортируем наш интерфейс из файла
from new_label import *
from PyQt5.QtWidgets import QApplication, QMainWindow
from MyMplCanc import MtMplCanv
import Math_Part
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtWidgets, QtGui, QtCore
from MyMplCanc import MtMplCanv
from matplotlib.figure import Figure
class MyWin(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
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

    # Пока пустая функция которая выполняется
    # при нажатии на кнопку
    def MyFunction(self):
        u0 = float(self.textEdit_3.toPlainText())
        h = float(self.textEdit_4.toPlainText())
        #x0 = float(self.textEdit_5.toPlainText())

        n = int(self.textEdit_6.toPlainText())
        eps = float(self.textEdit_7.toPlainText())
        a = float(self.textEdit_8.toPlainText())
        b = float(self.textEdit_9.toPlainText())
        #self.tableWidget.insertRow(0)
        Math_Part.Math_Part.bilding(self, n, u0, h, a, b, eps)
        #self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("hi"))


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())