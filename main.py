import sys

from PyQt5.QtWidgets import QTableWidgetItem

import input_menu
import body_menu
import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
import registration_menu
class TwoWindow(QtWidgets.QMainWindow, body_menu.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.oneWindow = None
        self.pushButton.clicked.connect(self.check)
        lable_up = ('id', 'компания', 'Описание задачи','начало','срок','конец','назначающий','выполняющий','приоритет','статус')
        self.tableWidget.setColumnCount(len(lable_up))
        self.tableWidget.setHorizontalHeaderLabels(lable_up)

        self.pushButton_2.clicked.connect(self.check_add)  # добавить
        self.pushButton_2.clicked.connect(self.open_table)
        self.pushButton_3.clicked.connect(self.check_chenge)  # изменить
        self.pushButton_3.clicked.connect(self.open_table)
        self.pushButton_4.clicked.connect(self.check_drop)  # удалить
        self.pushButton_4.clicked.connect(self.open_table)
        self.pushButton_5.clicked.connect(self.find_client_table)  # найти

        cur.execute("select post from staff;")
        post = cur.fetchall()[0][0]
        if post == 'clerk':
            self.open_table()
        else:
            self.pushButton_4.disconnect(self)

        self.pushButton_6.clicked.connect(self.employee_report) #отчет по сотруднику
        self.pushButton_7.clicked.connect(self.client_report) #отчет по заданию
        self.label_14.setText(" ") #отчет по сотруднику
        self.label_15.setText(" ") #отчет по заданию

    def employee_report(self):
        cur.execute("select post from staff;")
        post = cur.fetchall()[0][0]
        cur.execute(f"set role postgres;")
        cur.execute(f"select save_csv('{self.lineEdit_8.text()}','2000-10-19 10:23:54.000000', '2099-10-19 10:23:54.000000');")
        con.commit()
        cur.execute(f"set role {post};")
        self.label_14.setText("Выполненно")
    def client_report(self):
        cur.execute("select post from staff;")
        post = cur.fetchall()[0][0]
        cur.execute(f"set role postgres;")
        cur.execute(f"select save_csv_task({int(self.lineEdit_9.text())});")
        con.commit()
        cur.execute(f"set role {post};")
        self.label_15.setText("Выполненно")






    def open_table(self):
        cur.execute(
            "select task_id, task_name, description, start_date, deadline_date, end_date, appointing, executor, priority, task_status from task;")
        arr = cur.fetchall()
        self.tableWidget.setRowCount(len(arr))
        row = 0
        for a in arr:
            column = 0
            for r in a:
                if column == 3 or column == 4 or column == 5:
                    cellinfo = QtWidgets.QDateTimeEdit(r)
                    self.tableWidget.setCellWidget(row, column, cellinfo)
                elif column == 9 or column == 0:
                    r = str(r)
                    cellinfo = QtWidgets.QTableWidgetItem(r)
                    self.tableWidget.setItem(row, column, cellinfo)
                else:
                    cellinfo = QtWidgets.QTableWidgetItem(r)
                    self.tableWidget.setItem(row, column, cellinfo)

                column += 1
            row += 1

    def find_client_table(self):
        if self.lineEdit_7.text() == '*':
            self.open_table()
        else:
            if self.lineEdit_6.text() != '':
                cur.execute(
                    f"select task_id, task_name, description, start_date, deadline_date, end_date, appointing, executor, priority, task_status from task where task_name = '{self.lineEdit_6.text()}';")
            if self.lineEdit.text() != '':
                cur.execute(
                    f"select task_id, task_name, description, start_date, deadline_date, end_date, appointing, executor, priority, task_status from task where appointing = '{self.lineEdit.text()}';")
            if self.lineEdit_2.text() != '':
                cur.execute(
                    f"select task_id, task_name, description, start_date, deadline_date, end_date, appointing, executor, priority, task_status from task where executor = '{self.lineEdit.text()}';")
            arr = cur.fetchall()
            self.tableWidget.setRowCount(len(arr))
            row = 0
            for a in arr:
                column = 0
                for r in a:
                    if column == 3 or column == 4 or column == 5:
                        cellinfo = QtWidgets.QDateTimeEdit(r)
                        self.tableWidget.setCellWidget(row, column, cellinfo)
                    elif column == 9 or column == 0:
                        r = str(r)
                        cellinfo = QtWidgets.QTableWidgetItem(r)
                        self.tableWidget.setItem(row, column, cellinfo)
                    else:
                        cellinfo = QtWidgets.QTableWidgetItem(r)
                        self.tableWidget.setItem(row, column, cellinfo)

                    column += 1
                row += 1
    def check_chenge(self):
        array = []
        if self.lineEdit_6.text() != '':
            array.append(f"task_name = '{self.lineEdit_6.text()}'")
        if self.lineEdit_5.text() != '':
            array.append(f"description = '{self.lineEdit_5.text()}'")
        if self.dateTimeEdit.text() != '':
            array.append(f"start_date = '{self.dateTimeEdit.text()}'")
        if self.dateTimeEdit_2.text() != '':
            array.append(f"deadline_date = '{self.dateTimeEdit_2.text()}'")
        if self.dateTimeEdit_3.text() != '':
            array.append(f"end_date = '{self.dateTimeEdit_2.text()}'")
        if self.lineEdit.text() != '':
            array.append(f"appointing = '{self.lineEdit.text()}'")
        if self.lineEdit_2.text() != '':
            array.append(f"executor = '{self.lineEdit_2.text()}'")
        if self.lineEdit_4.text() != '':
            if (self.lineEdit_4.text() == "True") or (self.lineEdit_4.text() == "true"):
                task_status = True
            else:
                task_status = False
            array.append(f"task_status = {str(task_status)}")
        if self.lineEdit_3.text() != '':
            array.append(f"priority = '{self.lineEdit_3.text()}'")
        for arg in array:
            if self.lineEdit_7.text() != '':
                cur.execute(f"UPDATE task set {arg} where task_id = {self.lineEdit_7.text()}")
                con.commit()

    def check_drop(self):
        if self.lineEdit_7.text() != '':
            cur.execute(f"DELETE from task where task_id = {self.lineEdit_7.text()}")
            con.commit()
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
        if id_task or name_company or description or appointing or executor != "":
            cur.execute(f"insert into task(id_task, task_name, description, start_date, deadline_date, end_date, appointing, executor, priority, task_status) values"
                        f" ('{id_task}','{name_company}', '{description}', '{start_date}', '{deadline_date}', '{end_date}', '{appointing}', '{executor}','{priority}',{task_status})")
            con.commit()

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
        # self.lineEdit.text()
        # self.close()
        # self.twoWindow = TwoWindow()
        # self.twoWindow.show()
        cur.execute("SELECT login FROM staff")
        rows = cur.fetchall()
        for row in rows:
            if self.lineEdit.text() == row[0]:
                cur.execute(f"SELECT password FROM staff WHERE login = '{row[0]}';")
                pas = cur.fetchall()
                cur.execute(f"SELECT password = (crypt('{self.lineEdit_2.text()}', '{pas[0][0]}')) AS pswmatch FROM staff where login = '{row[0]}' ;")
                if (cur.fetchall()[0][0]) is True:

                    cur.execute(f"SELECT first_name FROM staff WHERE login = '{row[0]}';")
                    first_name = cur.fetchall()
                    cur.execute(f"SELECT last_name FROM staff WHERE login = '{row[0]}';")
                    last_name = cur.fetchall()

                    cur.execute(f"set role {row[0]};")
                    con.commit()
                    cur.execute("select current_user;")
                    print(f'Пользователь {cur.fetchall()[0][0]}')
                    self.lineEdit.text()
                    self.close()
                    self.twoWindow = TwoWindow()
                    self.twoWindow.show()
                    self.twoWindow.label.setText(f"Пользователь: {first_name[0][0]} {last_name[0][0]}")

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
                cur.execute(f"insert into staff(staff_id, task_id, first_name, last_name, post, login,password) values (6, 6, '{self.lineEdit_1.text()}','{self.lineEdit_2.text()}','{self.lineEdit_3.text()}', '{self.lineEdit_4.text()}', crypt('{self.lineEdit_5.text()}', 'zaxar'));")
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