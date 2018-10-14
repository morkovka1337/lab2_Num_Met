import math
import decimal
import pylab
from numpy import float64
from matplotlib import mlab
from matplotlib.figure import Figure
from new_label import Ui_MainWindow
from widg import Ui_MainWindow_new
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtGui, QtCore
from main import MyWin, second_window
#######################################
class Math_Part(Ui_MainWindow):
    def bilding(self, n, u, h, a, b, eps, secwin, d):
        ax = self.figure.add_subplot(111)
        item = self.comboBox.currentText()
        flag = False
        x = 0.0
        x0, u0 = 0.0, u
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(n)
        secwin.label.setText("Начальное х0 = " + str(x))
        secwin.label_2.setText("Начальное u0 = " + str(u))
        secwin.label_3.setText("Коэффициент a = " + str(a))
        secwin.label_4.setText("Коэффициент b = " + str(b))
        secwin.label_5.setText("выход за границу = " + str(d))
        secwin.label_6.setText("Макс. число шагов N = " + str(n))
        secwin.label_7.setText("Шаг h = " + str(h))
        secwin.label_8.setText("Контроль ЛП = " + str(eps))
        secwin.label_9.setText("Task - " + str(item))
        secwin.tableWidget.setRowCount(n + 1)
        cnt_g, cnt_l = 0, 0
        cnt_l_list, cnt_g_list = [], []
        xlist, ulist, L_Elist, Mark_list, hlist = [], [], [], [], []
        xlist.append(x)
        ulist.append(u)
        hlist.append(h)

        for i in range(n + 1):
            secwin.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i)))
        def abs_solution(x, const):
            return math.exp(7*x) * const
        def sol_const(u):
            return (u)
        def f(x, u):
            if item == "Test":
                return 7*u
            if item == "Main 1":
                return ((1/(1 + 3*x + x**2)) * (u**2) + u - (u**3) * math.sin(10 * x))
   
            if item == "Main 2":
                pass

        def loc_err(step_u, two_step_u):
            return ((two_step_u - step_u) * ((16.0) / 15.0))

        def next_point_x(step, x):
            return x + step

        def next_point_u(u, x, step):
            k1 = f(x, u)
            k2 = f(x + step / 2, u + (step / 2) *k1)
            k3 = f(x + step / 2, u + (step / 2) * k2)
            k4 = f(x + step, u + step * k3)
            return (u + ((step / 6) * (k1 + 2 * k2 + 2 * k3 + k4)))

        ##################################################
        def new_point(step, x, u, number_r):
            nonlocal h
            nonlocal cnt_g
            nonlocal cnt_l
            nonlocal flag
            new_u = next_point_u(u, x, step)
            new_x = next_point_x(step, x)

            add_u = next_point_u(u, x, step / 2)
            add_x = next_point_x(step / 2, x)

            add_u = next_point_u(add_u, add_x, step / 2)
            add_x = next_point_x(step / 2, add_x)

            S = loc_err(new_u, add_u)

            secwin.tableWidget.setItem(number_r, 3, QtWidgets.QTableWidgetItem(str(add_u)))
            secwin.tableWidget.setItem(number_r, 4, QtWidgets.QTableWidgetItem(str(add_x)))
            secwin.tableWidget.setItem(number_r, 7, QtWidgets.QTableWidgetItem(str(abs(S))))
            secwin.tableWidget.setItem(number_r, 6, QtWidgets.QTableWidgetItem(str(new_u - add_u)))
            if self.checkBox.isChecked():
                if abs(S) >= eps / 16 and abs(S) <= eps:
                    print("save point")
                    hlist.append(h)
                    Mark_list.append(abs(S))
                    return new_x, new_u
                if abs(S) < eps / 16:
                    print("save point, but change step")
                    h *= 2
                    nonlocal cnt_g
                    cnt_g += 1
                    cnt_g_list.append(cnt_g)
                    hlist.append(h)
                    Mark_list.append(abs(S))
                    return new_x, new_u
                if abs(S) > eps:
                    print("Fail")
                    h /= 2
                    nonlocal cnt_l
                    cnt_l += 1
                    cnt_l_list.append(cnt_l)
                    return new_point(h, x, u, number_r)
            else:
                hlist.append(h)
                Mark_list.append(abs(S))
                return new_x, new_u
        if self.checkBox_2.isChecked():
            ax.clear()
        ax.axis([-10, 20, -10, 20])
        const = sol_const(u)
        xlist.append(x)
        ulist.append(u)
        abs_x, abs_u= x, abs_solution(x, const)
        #ax.plot([0, 0], [0, 0], '-b', label = ("number", x0, u0))
        #ax.plot([0, 0], [0, 0], 'r--', markersize = 0.5, label = ("absolute", x0, u0))
        for i in range(n):
            old_x, old_u = x, u
            secwin.tableWidget.setItem(i, 1, QtWidgets.QTableWidgetItem(str(old_u)))
            secwin.tableWidget.setItem(i, 2, QtWidgets.QTableWidgetItem(str(old_x)))
            secwin.tableWidget.setItem(i, 5, QtWidgets.QTableWidgetItem(str(h)))
            secwin.tableWidget.setItem(i, 12, QtWidgets.QTableWidgetItem(str(cnt_g)))
            secwin.tableWidget.setItem(i, 11, QtWidgets.QTableWidgetItem(str(cnt_l)))

            if x > d:
                self.progressBar.setValue(n)
                break
            x, u = new_point(h, old_x, old_u, i + 1)

            
            xlist.append(x)
            ulist.append(u)
            ax.plot([old_x, x], [old_u, u], '-b')
            if item == "Test":
                old_abs_x, old_abs_u = abs_x, abs_u
                secwin.tableWidget.setItem(i, 8, QtWidgets.QTableWidgetItem(str(old_abs_u)))
                secwin.tableWidget.setItem(i, 9, QtWidgets.QTableWidgetItem(str(old_abs_x)))
                L_Elist.append(abs(old_abs_u - old_u))
                secwin.tableWidget.setItem(i, 10, QtWidgets.QTableWidgetItem(str(abs(old_abs_u - old_u))))
                abs_x = x
                abs_u = abs_solution(abs_x, const)
                ax.plot([old_abs_x, abs_x], [old_abs_u, abs_u], 'r--', markersize = 0.5)
            self.progressBar.setValue(i + 1)
        if item == "Test":
            secwin.tableWidget.setItem(i, 10, QtWidgets.QTableWidgetItem(str(abs(abs_u - u))))
            secwin.tableWidget.setItem(n, 8, QtWidgets.QTableWidgetItem(str(abs_u)))
            secwin.tableWidget.setItem(n, 9, QtWidgets.QTableWidgetItem(str(abs_x)))
        secwin.tableWidget.setItem(n, 1, QtWidgets.QTableWidgetItem(str(u)))
        secwin.tableWidget.setItem(n, 2, QtWidgets.QTableWidgetItem(str(x)))
        secwin.tableWidget.setItem(n, 5, QtWidgets.QTableWidgetItem(str(h)))
        secwin.tableWidget.setItem(n, 12, QtWidgets.QTableWidgetItem(str(cnt_g)))
        secwin.tableWidget.setItem(n, 11, QtWidgets.QTableWidgetItem(str(cnt_l)))
        secwin.label_10.setText("Max U = " + str(max(ulist)))
        secwin.label_11.setText("Max x = " + str(max(xlist)))
        secwin.label_12.setText("Max h = " + str(max(hlist)))
        secwin.label_13.setText("Min h = " + str(min(hlist)))
        if item == "Test":
            secwin.label_14.setText("Max Гл. Погр. = " + str(round(max(L_Elist), 9)))
            secwin.label_16.setText("Min Гл. Погр. = " + str(round(min(L_Elist), 9)))
        else:
            secwin.label_14.setText("Max Гл. Погр. = " + "--")
            secwin.label_16.setText("Min Гл. Погр. = " + "--")

        secwin.label_17.setText("Max ОЛП = " + str(round(max(Mark_list), 9)))
        secwin.label_18.setText("Min ОЛП = " + str(round(min(Mark_list), 9)))
        if self.checkBox.isChecked():
            secwin.label_19.setText("Общ кол-во увел. = " + str(max(cnt_g_list)))
            secwin.label_20.setText("Общ кол-во уменьш. = " + str(max(cnt_l_list)))
        ax.grid(True)
        ax.legend((["number", x0, u0], ["absolute", x0, u0]))
        self.canvas.draw()