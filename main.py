import sys
from datetime import datetime

import input_menu
import body_menu
import psycopg2
import hashlib

from PyQt5 import QtCore, QtGui, QtWidgets

import registration_menu


class TwoWindow(QtWidgets.QMainWindow, body_menu.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.oneWindow = None
        self.pushButton.clicked.connect(self.check)
        cur.execute("select  column_name from information_schema.columns where table_name = 'task';")
        arr = cur.fetchall()
        length = len(arr)
        self.tableWidget.setColumnCount(length-2)
        lable_up = ('номер','Название компании','Описание задачи','начало','срок','конец','назначающий','выполняющий','приоритет','статус')

        self.tableWidget.setHorizontalHeaderLabels(lable_up)

        cur.execute("select  * from task;")
        arr = cur.fetchall()

        # cellinfo = QtWidgets.QTableWidgetItem('cellinfo')
        # print(type(cellinfo))
        # print(cellinfo)
        # self.tableWidget.setItem(0, 0, cellinfo)
        self.tableWidget.setRowCount(len(arr))


        row = 0
        for a in arr:
            column = 0
            print(a)

            for r in a:

                print(column)
                if column == 0:
                    pass
                    r = str(r)
                    cellinfo = QtWidgets.QTableWidgetItem(r)
                    self.tableWidget.setItem(row, column, cellinfo)
                elif column == 3:
                    cellinfo = QtWidgets.QDateTimeEdit(r)
                    self.tableWidget.setCellWidget(row, column, cellinfo)
                elif column == 4:
                    cellinfo = QtWidgets.QDateTimeEdit(r)
                    self.tableWidget.setCellWidget(row, column, cellinfo)
                elif column == 5:
                    cellinfo = QtWidgets.QDateTimeEdit(r)
                    self.tableWidget.setCellWidget(row, column, cellinfo)
                elif column == 9:
                    # r = str(r)
                    # cellinfo = QtWidgets.QTableWidgetItem(r)
                    # self.tableWidget.setItem(row, column, cellinfo)
                    pass
                elif column == 10:
                    r = str(r)
                    cellinfo = QtWidgets.QTableWidgetItem(r)
                    self.tableWidget.setItem(row, column-1, cellinfo)

                elif column == 11:
                    # r = str(r)
                    # cellinfo = QtWidgets.QTableWidgetItem(r)
                    # self.tableWidget.setItem(row, column, cellinfo)
                    pass
                else:
                    cellinfo = QtWidgets.QTableWidgetItem(r)
                    self.tableWidget.setItem(row, column, cellinfo)
                column+=1
            print(row)
            row+=1

    def check(self):
        self.close()
        self.oneWindow = OneWindow()
        self.oneWindow.show()

class OneWindow(QtWidgets.QMainWindow, input_menu.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.twoWindow = None
        self.pushButton.clicked.connect(self.check)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_2.clicked.connect(self.check_2)

    def check(self):
        self.lineEdit.text()
        self.close()
        self.twoWindow = TwoWindow()
        self.twoWindow.show()
        # cur.execute("SELECT login FROM staff")
        # rows = cur.fetchall()
        # for row in rows:
        #     if self.lineEdit.text() == row[0]:
        #         cur.execute(f"SELECT password FROM staff WHERE login = '{row[0]}';")
        #         pas = cur.fetchall()
        #         cur.execute(f"SELECT password = (crypt('{self.lineEdit_2.text()}', '{pas[0][0]}')) AS pswmatch FROM staff where login = '{row[0]}' ;")
        #         if (cur.fetchall()[0][0]) is True:
        #             self.lineEdit.text()
        #             self.close()
        #             self.twoWindow = TwoWindow()
        #             self.twoWindow.show()
        #             cur.execute(f"SELECT first_name FROM staff WHERE login = '{row[0]}';")
        #             first_name = cur.fetchall()
        #             cur.execute(f"SELECT last_name FROM staff WHERE login = '{row[0]}';")
        #             last_name = cur.fetchall()
        #             self.twoWindow.label.setText(f"Пользователь: {first_name[0][0]} {last_name[0][0]}")

    def check_2(self):
        self.lineEdit.text()
        self.close()
        self.treeWindow = TreeWindow()
        self.treeWindow.show()
class TreeWindow(QtWidgets.QMainWindow, registration_menu.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.treeWindow = None
        self.pushButton_2.clicked.connect(self.check)
        self.lineEdit_5.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_6.setEchoMode(QtWidgets.QLineEdit.Password)

    def check(self):
        if self.lineEdit_1.text() \
                and self.lineEdit_2.text() \
                and self.lineEdit_3.text() \
                and self.lineEdit_4.text() \
                and self.lineEdit_5.text() \
                and self.lineEdit_6.text() is not None:
            if self.lineEdit_5.text() == self.lineEdit_6.text():
                cur.execute(f"insert into staff(task_id, first_name, last_name, post, login,password) values (1, '{self.lineEdit_1.text()}','{self.lineEdit_2.text()}','{self.lineEdit_3.text()}', '{self.lineEdit_4.text()}', crypt('{self.lineEdit_5.text()}', 'zaxar'));")
                con.commit()
                cur.execute(f"create USER {self.lineEdit_4.text()};")
                con.commit()


        self.close()
        self.twoWindow = TwoWindow()
        self.twoWindow.show()
        self.twoWindow.label.setText(f"Пользователь: {self.lineEdit_1.text()} {self.lineEdit_2.text()}")

def main():
    global con
    con = psycopg2.connect(
        database="practica2",
        user="postgres",
        password="pass",
        host="127.0.0.1",
        port="5432"
    )
    global cur
    cur = con.cursor()



    app = QtWidgets.QApplication(sys.argv)
    window = OneWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()