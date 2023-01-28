from dataclasses import dataclass
import email
from json import load
import string
from turtle import delay
from matplotlib.pyplot import cla
from matplotlib.style import use
import pymysql
#pymysql.install_as_MySQLdb()
import pstats
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

import mysql.connector as con
import time
import datetime


from PyQt5.uic import loadUiType

ui,_=loadUiType('library.ui')

class MainApp(QMainWindow , ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.sheetkey=0
        self.setWindowTitle("Library Management System")
        self.setupUi(self)
        self.handle_ui_changes()
        self.handle_buttons()
        self.showcategory()
        self.showauthor()
        self.showpublisher()
        self.show_category_combobox()
        self.show_author_combobox()
        self.show_publisher_combobox()
        self.showallbooks()

    def handle_ui_changes(self):
        self.hide_themes()
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.tabBar().setVisible(False)
        self.pushButton_15.setEnabled(False)
        
        self.showalldata()


    def handle_buttons(self):
        self.pushButton_5.clicked.connect(self.Dark_Blue_Theme)
        self.pushButton_23.clicked.connect(self.hide_themes)
        self.pushButton.clicked.connect(self.opendaytodaytab)
        self.pushButton_2.clicked.connect(self.openbookstab)
        self.pushButton_3.clicked.connect(self.openusertab)
        self.pushButton_4.clicked.connect(self.opensettingstab)
        self.pushButton_7.clicked.connect(self.addnewbook)


        self.pushButton_16.clicked.connect(self.addcategory)
        self.pushButton_17.clicked.connect(self.addauthor)
        self.pushButton_18.clicked.connect(self.addpublisher)

        self.pushButton_12.clicked.connect(self.Search_Books)
        self.pushButton_10.clicked.connect(self.Edit_Books)
        self.pushButton_11.clicked.connect(self.Delete_Books)
        self.pushButton_13.clicked.connect(self.Add_New_User)
        self.pushButton_14.clicked.connect(self.Login)
        self.pushButton_15.clicked.connect(self.Edit_User)
        self.pushButton_6.clicked.connect(self.adddata)
        
        

    def show_themes(self):
        self.groupBox_3.show()

    def hide_themes(self):
        self.groupBox_3.hide()

    # opening tabs
    def Add_New_User(self):
        self.db = con.connect(host='localhost' , user='root' , password ='Mayjon@1372' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_13.text()
        email = self.lineEdit_14.text()
        password = self.lineEdit_15.text()
        password2 = self.lineEdit_16.text()

        if username !="" or email !="":
            if password == password2 :
                self.cur.execute('INSERT INTO users (user_name , user_email , user_password) VALUES (%s , %s , %s)' , (username , email , password))

                self.db.commit()
                self.statusBar().showMessage('New User Added')
                self.label_42.setText('Added')

            else:
                self.label_42.setText('Password mismatch')
        else:
                self.label_42.setText('fields empty')

    def Login(self):
        self.db = con.connect(host='localhost' , user='root' , password ='Mayjon@1372' , db='library')
        self.cur = self.db.cursor()

        username = self.lineEdit_25.text()
        password = self.lineEdit_26.text()

        sql = ' SELECT * FROM users where user_name= %s'

        self.cur.execute(sql,[(username)])
        data = self.cur.fetchall()
        if data:
            for row in data  :
                if username == row[1] and password == row[3]:
                    print('user match')
                    self.statusBar().showMessage('Valid Username & Password')
                    self.pushButton_15.setEnabled(True)

                    self.lineEdit_21.setText(row[1])
                    self.lineEdit_22.setText(row[2])
                    self.lineEdit_23.setText(row[3])
                    self.lineEdit_24.setText(row[3])
                    self.label_43.setText("Login-ed")

                else:
                    self.label_43.setText("Invalid username or password")


        else:
            self.label_43.setText("Account doesn't exist")

    def Edit_User(self):

        username = self.lineEdit_21.text()
        email = self.lineEdit_22.text()
        password = self.lineEdit_23.text()
        password2 = self.lineEdit_24.text()

        original_name = self.lineEdit_25.text()
        if username!="" or email!="":
            if password == password2 :
                self.db = con.connect(host='localhost', user='root', password='Mayjon@1372', db='library')
                self.cur = self.db.cursor()

                print(username)
                print(email)
                print(password)

                self.cur.execute('''
                    UPDATE users SET user_name=%s , user_email=%s , user_password=%s WHERE user_name=%s
                ''', (username , email , password , original_name))

                self.db.commit()
                self.statusBar().showMessage('User Data Updated Successfully')
                self.label_44.setText("Updated")
                time.sleep(2)
                self.label_44.setText("")
                self.label_43.setText("")
                self.pushButton_15.setEnabled(False)
                self.lineEdit_21.setText("")
                self.lineEdit_22.setText("")
                self.lineEdit_23.setText("")
                self.lineEdit_24.setText("")
                self.lineEdit_25.setText("")
                self.lineEdit_26.setText("")


            else:
                self.label_44.setText("Password mis-match")
        else:
                self.label_44.setText("fields empty")




    def opendaytodaytab(self):
        self.tabWidget.setCurrentIndex(0)

    def openbookstab(self):
        self.tabWidget.setCurrentIndex(1)

    def openusertab(self):
        self.tabWidget.setCurrentIndex(2)

    def opensettingstab(self):
        self.tabWidget.setCurrentIndex(3)

    # setting books tab

    def addnewbook(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db="library")
        self.cur=self.db.cursor()

        title=self.lineEdit_2.text()
        code=self.lineEdit_3.text()
        category=self.comboBox_2.currentText()
        author=self.comboBox_3.currentText()
        publisher=self.comboBox_4.currentText()
        price=self.lineEdit_4.text()
        description=self.plainTextEdit.toPlainText()

        if title!="" or code!="" :
            self.cur.execute('INSERT INTO book (book_name,book_description,book_code,book_category,book_author,book_publisher,book_price) VALUES (%s , %s , %s , %s , %s , %s , %s)' ,(title , description ,code , category , author , publisher , price))
            self.db.commit()
            self.statusBar().showMessage('New Book Added')

            self.lineEdit_2.setText("")
            self.lineEdit_3.setText("")
            self.comboBox_2.setCurrentText("")
            self.comboBox_3.setCurrentText("")
            self.comboBox_4.setCurrentText("")
            self.lineEdit_4.setText("")
            self.plainTextEdit.setPlainText("")

            self.showallbooks()
        else:
            self.statusBar().showMessage('fields empty')








    def Search_Books(self):

        self.db = con.connect(host='localhost' , user='root' , password ='Mayjon@1372' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_12.text()

        sql = ' SELECT * FROM book WHERE book_name = %s'
        self.cur.execute(sql , [(book_title)])

        data = self.cur.fetchone()
        if data:
            self.lineEdit_10.setText(data[1])
            self.plainTextEdit_3.setPlainText(data[2])
            self.lineEdit_11.setText(data[3])
            self.comboBox_11.setCurrentText(data[4])
            self.comboBox_9.setCurrentText(data[5])
            self.comboBox_10.setCurrentText(data[6])
            self.lineEdit_9.setText(str(data[7]))
            print(data)
        else:
            self.statusBar().showMessage('no Book with this Title')


    def Edit_Books(self):
        self.db = con.connect(host='localhost' , user='root' , password ='Mayjon@1372' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_10.text()
        book_description = self.plainTextEdit_3.toPlainText()
        book_code = self.lineEdit_11.text()
        book_category = self.comboBox_11.currentText()
        book_author = self.comboBox_9.currentText()
        book_publisher = self.comboBox_10.currentText()
        book_price = self.lineEdit_9.text()


        search_book_title = self.lineEdit_12.text()

        self.cur.execute('UPDATE book SET book_name=%s ,book_description=%s ,book_code=%s ,book_category=%s ,book_author=%s ,book_publisher=%s ,book_price=%s WHERE book_name = %s', (book_title,book_description,book_code,book_category,book_author,book_publisher , book_price , search_book_title))

        self.db.commit()
        self.statusBar().showMessage('book updated')
        self.showallbooks()
        

   

    def Delete_Books(self):
        self.db = con.connect(host='localhost' , user='root' , password ='Mayjon@1372' , db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_12.text()

        warning = QMessageBox.warning(self , 'Delete Book' , "are you sure you want to delete this book" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            sql = ' DELETE FROM book WHERE book_name = %s '
            self.cur.execute(sql , [(book_title)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted')

            self.showallbooks()

    # setting user tab

    def addnewuser(self):
        pass

    def login(self):
        pass

    def edituser(self):
        pass

    # setting settings tab

    def addcategory(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()
        categoryname=self.lineEdit_27.text()
        self.cur.execute("INSERT INTO category (category_name) VALUES (%s)",(categoryname,) )
        self.db.commit()
        self.statusBar().showMessage("New Category Added")
        self.lineEdit_27.setText("")
        self.showcategory()

        #self.cursor()

        
        
        
    def addauthor(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()
        authorname=self.lineEdit_28.text()
        self.cur.execute("INSERT INTO authors (author_name) VALUES (%s)",(authorname,) )
        self.db.commit()
        self.statusBar().showMessage("New Author Added")
        self.lineEdit_28.setText("")
        self.showauthor()

    def addpublisher(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()
        publishername=self.lineEdit_29.text()
        self.cur.execute("INSERT INTO publisher (publisher_name) VALUES (%s)",(publishername,) )
        self.db.commit()
        self.statusBar().showMessage("New Publisher Added")
        self.lineEdit_29.setText("")
        self.showpublisher()

    def showcategory(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()
        self.cur.execute("select category_name from category")
        data=self.cur.fetchall()

        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row , form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row,column,QTableWidgetItem(str(item)))
                    column+=1

                row_position=self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    def showauthor(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()
        self.cur.execute("select author_name from authors")
        data=self.cur.fetchall()

        if data:
            self.tableWidget_4.setRowCount(0)
            self.tableWidget_4.insertRow(0)
            for row , form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_4.setItem(row,column,QTableWidgetItem(str(item)))
                    column+=1

                row_position=self.tableWidget_4.rowCount()
                self.tableWidget_4.insertRow(row_position)

    def showpublisher(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()
        self.cur.execute("select publisher_name from publisher")
        data=self.cur.fetchall()

        if data:
            self.tableWidget_5.setRowCount(0)
            self.tableWidget_5.insertRow(0)
            for row , form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_5.setItem(row,column,QTableWidgetItem(str(item)))
                    column+=1

                row_position=self.tableWidget_5.rowCount()
                self.tableWidget_5.insertRow(row_position)

    def adddata(self):
        username=self.lineEdit_30.text()
        booktitle=self.lineEdit.text()
        type=self.comboBox.currentText()
        days=int(self.spinBox.text())+1
        frommm=datetime.date.today()
        duee=frommm + datetime.timedelta(days=days)
        print()
        

        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()
        self.cur.execute('select * from users where user_name=%s',(username,))
        dataname=self.cur.fetchone()
        

        self.cur.execute('select * from book where book_name=%s',(booktitle,))
        databook=self.cur.fetchone()
        

        
        if dataname:
            email=dataname[2]
            if databook:
                category=databook[4]
                print("book exist")
                print(category)
                if type=="Rent":
                    self.cur.execute('INSERT INTO dayoperations (user_name,user_email,book_name,category,fromm,days,due) VALUES (%s , %s , %s, %s , %s , %s, %s)',(username,email,booktitle,category,frommm,str(days),duee))
                    self.db.commit()
                    self.label_45.setText("Record Added")
                elif type=="Retrieve":
                    self.cur.execute('DELETE FROM dayoperations where user_name=%s AND book_name=%s',(username,booktitle))
                    self.db.commit()
                    self.label_45.setText("Record Removed")

                self.showalldata()
            else:
                self.label_45.setText("Invalid Book")
        else:
            self.label_45.setText("Invalid User")

    def showalldata(self):
        self.db = con.connect(host='localhost', user='root', password='Mayjon@1372', db='library')
        self.cur = self.db.cursor()

        self.cur.execute(''' 
            SELECT user_name,user_email,book_name,category,fromm,days,due FROM dayoperations
        ''')

        data = self.cur.fetchall()

        print(data)

        self.tableWidget1.setRowCount(0)
        self.tableWidget1.insertRow(0)
        for row , form in enumerate(data):
            for column , item in enumerate(form):
                self.tableWidget1.setItem(row , column , QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget1.rowCount()
            self.tableWidget1.insertRow(row_position)
        




    def showallbooks(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()
        self.cur.execute("SELECT book_code,book_name,book_author,book_publisher,book_category,book_price FROM book")
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, item in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                column += 1

            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)

        self.db.close()


    def show_category_combobox(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()

        self.cur.execute("select category_name from category")
        data=self.cur.fetchall()
        for item in data:
            self.comboBox_2.addItem(item[0])
            self.comboBox_11.addItem(item[0])

    def show_author_combobox(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()

        self.cur.execute("select author_name from authors")
        data=self.cur.fetchall()
        for item in data:
            self.comboBox_3.addItem(item[0])
            self.comboBox_9.addItem(item[0])
        
    def show_publisher_combobox(self):
        self.db=con.connect(host="localhost",user="root",password="Mayjon@1372",db='library')
        self.cur=self.db.cursor()

        self.cur.execute("select publisher_name from publisher")
        data=self.cur.fetchall()
        for item in data:
            self.comboBox_4.addItem(item[0])
            self.comboBox_10.addItem(item[0])

    def Dark_Blue_Theme(self):
        if self.sheetkey==0:
            style = open('themes/darkblue.css' , 'r')
            style = style.read()
            self.setStyleSheet(style)
            self.sheetkey=1
        else:
            self.sheetkey=0
            self.setStyleSheet("")
            
   





def main():
    app=QApplication(sys.argv)
    window=MainApp  ()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()

        