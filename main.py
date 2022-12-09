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
        # cur.execute("select  column_name from information_schema.columns where table_name = 'task';")
        # arr = cur.fetchall()
        # length = len(arr)
        # self.tableWidget.setColumnCount(length-2)
        lable_up = ('id','Описание задачи','начало','срок','конец','назначающий','выполняющий','приоритет','статус')
        self.tableWidget.setColumnCount(len(lable_up))
        self.tableWidget.setHorizontalHeaderLabels(lable_up)

        cur.execute("select post from staff;")
        post = cur.fetchall()[0][0]
        if post == 'clerk':

            cur.execute("select task_id, description, start_date, deadline_date, end_date, appointing, executor, priority, task_status from task;")
            arr = cur.fetchall()
            self.tableWidget.setRowCount(len(arr))
            row = 0
            for a in arr:
                column = 0
                for r in a:
                    if column == 2 or column == 3 or column == 4:
                        cellinfo = QtWidgets.QDateTimeEdit(r)
                        self.tableWidget.setCellWidget(row, column, cellinfo)
                    elif column == 8 or column == 0:
                        r = str(r)
                        cellinfo = QtWidgets.QTableWidgetItem(r)
                        self.tableWidget.setItem(row, column, cellinfo)
                    else:
                        cellinfo = QtWidgets.QTableWidgetItem(r)
                        self.tableWidget.setItem(row, column, cellinfo)
                    column+=1
                row+=1
        else:
            pass



        self.pushButton_2.clicked.connect(self.check_add) #добавить
        self.pushButton_3.clicked.connect(self.check_chenge) #изменить
        self.pushButton_4.clicked.connect(self.check_drop) #удалить
        self.pushButton_5.clicked.connect(self.check_find) #найти
    def check_chenge(self):
        print('check_chenge')
        array = []

        if self.lineEdit_6.text() is not None:
            array.append(f"task_name = '{self.lineEdit_6.text()}'")
        if self.lineEdit_5.text() is not None:
            array.append(f"description = '{self.lineEdit_5.text()}'")
        if self.dateTimeEdit.text() is not None:
            pass
        if self.dateTimeEdit_2.text() is not None:
            pass
        if self.dateTimeEdit_3.text() is not None:
            pass
        if self.lineEdit.text() is not None:
            array.append(f"appointing = '{self.lineEdit.text()}'")
        if self.lineEdit_2.text() is not None:
            array.append(f"executor = '{self.lineEdit_2.text()}'")
        if self.lineEdit_4.text() is not None:
            if (self.lineEdit_4.text() == "True") or (self.lineEdit_4.text() == "true"):
                task_status = True
            else:
                task_status = False
            array.append(f"task_status = '{str(task_status)}'")
        if self.lineEdit_3.text() is not None:
            array.append(f"priority = '{self.lineEdit_3.text()}'")
        for arg in array:
            if self.lineEdit_7.text() is not None:
                print(arg)
                cur.execute(f"UPDATE task set {arg} where task_id = {self.lineEdit_7.text()}")
                con.commit()
    def check_drop(self):
        print('check_drop')
    def check_find(self):
        print('check_find')
    def check_add(self):
        id_task = self.lineEdit_7.text()
        name_company = self.lineEdit_6.text()
        description = self.lineEdit_5.text()
        start_date = self.dateTimeEdit.text()
        start_date = start_date[6:10]+'-'+start_date[3:5]+'-'+start_date[0:2]+' 00:00:00.000000'
        deadline_date = self.dateTimeEdit_2.text()
        deadline_date = deadline_date[6:10]+'-'+deadline_date[3:5]+'-'+deadline_date[0:2]+' 00:00:00.000000'
        end_date = self.dateTimeEdit_3.text()
        end_date = end_date[6:10]+'-'+end_date[3:5]+'-'+end_date[0:2]+' 00:00:00.000000'
        appointing = self.lineEdit.text()
        executor = self.lineEdit_2.text()
        task_status = self.lineEdit_4.text()
        if task_status == 'True' or 'true':
            task_status = True
        else:
            task_status = False
        priority = self.lineEdit_3.text()
        cur.execute(f"insert into task(id_task, task_name, description, start_date, deadline_date, end_date, appointing, executor, priority, task_status) values"
                    f" ('{id_task}','{name_company}', '{description}', '{start_date}', '{deadline_date}', '{end_date}', '{appointing}', '{executor}','{priority}',{task_status})")
        con.commit()
        print(description, start_date, deadline_date, end_date, appointing, executor, priority)

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
        #
        #             cur.execute(f"SELECT first_name FROM staff WHERE login = '{row[0]}';")
        #             first_name = cur.fetchall()
        #             cur.execute(f"SELECT last_name FROM staff WHERE login = '{row[0]}';")
        #             last_name = cur.fetchall()
        #
        #             cur.execute(f"set role {row[0]};")
        #             con.commit()
        #             cur.execute("select current_user;")
        #             print(f'Пользователь {cur.fetchall()[0][0]}')
        #             self.lineEdit.text()
        #             self.close()
        #             self.twoWindow = TwoWindow()
        #             self.twoWindow.show()
        #
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