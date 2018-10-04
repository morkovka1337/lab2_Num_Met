import math
import pylab
from matplotlib import mlab
from matplotlib.figure import Figure
from new_label import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from main import MyWin
#######################################
class Math_Part(Ui_MainWindow):

    def bilding(self, n, u, h, a, b, eps):
        ax = self.figure.add_subplot(111)
        item = self.comboBox.currentText()
        self.tableWidget.setRowCount(n+1)
        cnt1, cnt2 = 0, 0
        if item != "Test":
            ax.clear()
            for i in range(n + 1):
                for j in range(12):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str("")))
        for i in range(n + 1):
            self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
        def abs_solution(x, const):
            return math.exp(7*x) * const
        def f(x, u):
            if item == "Test":
                return 7*u
            if item == "Main 1":
                return ((1/(1 + 3*x + x**2)) * (u**2) + u - (u**3) * math.sin(10 * x))
            if item == "Main 2":
                pass

        def loc_err(step_u, two_step_u):
            return ((two_step_u - step_u) * ((16.0) / 15.0))

        # def step_func1(step, x, u):
        #     return f(x, u)

        # def step_func2(step, x, u):
        #     return f(x + step / 2, u + (step / 2) * step_func1(step, x, u))

        # def step_func3(step, x, u):
        #     return f(x + step / 2, u + (step / 2) * step_func2(step, x, u))

        # def step_func4(step, x, u):
        #     return f(x + step, u + step * step_func3(step, x, u))

        def next_point_x(step, x):
            return x + step

        def next_point_u(u, x, step):
            k1 = f(x, u)
            k2 = f(x + step / 2, u + (step / 2) *k1)
            k3 = f(x + step / 2, u + (step / 2) * k2)
            k4 = f(x + step, u + step * k3)
            return u + (step / 6) * (k1 + 2 * k2 + 2 * k3 + k4)

        ##################################################
        def new_point(step, x, u, number_r):
            nonlocal h

            new_u = next_point_u(u, x, step)
            new_x = next_point_x(step, x)

            add_u = next_point_u(u, x, step / 2)
            add_x = next_point_x(step / 2, x)

            add_u = next_point_u(add_u, add_x, step / 2)
            add_x = next_point_x(step / 2, add_x)

            S = loc_err(new_u, add_u)

            self.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(add_u)))
            self.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(add_x)))
            self.tableWidget.setItem(number_r, 5, QtWidgets.QTableWidgetItem(str(h)))
            self.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(S)))
            # print("####", h)
            self.tableWidget.setItem(number_r, 12, QtWidgets.QTableWidgetItem(str(new_u - add_u)))
            if self.checkBox.isChecked():
                print("S####: ", S)
                print("exp###: ", eps / 16, eps)
                print("####", h)
                if abs(S) >= eps / 16 and abs(S) <= eps:
                    print("save point")
                    return new_x, new_u
                if abs(S) < eps / 16:
                    print("save point, but change step")
                    h *= 2
                    nonlocal cnt2
                    cnt2 += 1
                    self.tableWidget.setItem(number_r, 10, QtWidgets.QTableWidgetItem(str(cnt2)))
                    return new_x, new_u
                if abs(S) > eps:
                    print("Fail")
                    h /= 2
                    nonlocal cnt1
                    cnt1 += 1
                    self.tableWidget.setItem(number_r, 9, QtWidgets.QTableWidgetItem(str(cnt1)))
                    return new_point(h, x, u, number_r)
            else: return new_x, new_u
        ax.axis([-10, 20, -10, 20])
        const = u
        x = 0.0
        color = '-b' if self.checkBox.isChecked() else '-g'
        abs_x, abs_u= x, abs_solution(x, const)
        for i in range(n):
            old_x, old_u = x, u
            self.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(old_u)))
            self.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(old_x)))
            x, u = new_point(h, old_x, old_u, i + 1)
            ax.plot([old_x, x], [old_u, u], color)
            if item == "Test":
                old_abs_x, old_abs_u = abs_x, abs_u
                self.tableWidget.setItem(i, 7, QtWidgets.QTableWidgetItem(str(old_abs_u)))
                self.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(old_abs_x)))
                self.tableWidget.setItem(i, 11, QtWidgets.QTableWidgetItem(str(abs(old_abs_u - old_u))))
                abs_x = x
                abs_u = abs_solution(abs_x, const)
                ax.plot([old_abs_x, abs_x], [old_abs_u, abs_u], '-r')
            self.progressBar.setProperty("value", 100*(i/n))
        if item == "Test":
            self.tableWidget.setItem(i, 11, QtWidgets.QTableWidgetItem(str(abs(abs_u - u))))
            self.tableWidget.setItem(n, 7, QtWidgets.QTableWidgetItem(str(abs_u)))
            self.tableWidget.setItem(n, 8, QtWidgets.QTableWidgetItem(str(abs_x)))
        self.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem(str(u)))
        self.tableWidget.setItem(n, 2, QtWidgets.QTableWidgetItem(str(x)))
        ax.grid(True)
        self.canvas.draw()