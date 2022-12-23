import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *

its_log=''

class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('booker.ui',self)
        self.setWindowTitle('Booker for user')
        self.main_button.clicked.connect(self.event_menu)
        self.book_button1.clicked.connect(lambda:self.event_book_info(1))
        self.book_button2.clicked.connect(lambda:self.event_book_info(2))
        self.book_button3.clicked.connect(lambda:self.event_book_info(3))
        self.book_button4.clicked.connect(lambda:self.event_book_info(4))
        self.book_button5.clicked.connect(lambda:self.event_book_info(5))
        self.book_button6.clicked.connect(lambda:self.event_book_info(6))
        self.book_button7.clicked.connect(lambda:self.event_book_info(7))
        self.book_button8.clicked.connect(lambda:self.event_book_info(8))
        self.book_button9.clicked.connect(lambda:self.event_book_info(9))
        self.book_button10.clicked.connect(lambda:self.event_book_info(10))
        
    def event_menu(self):
        self.newDialog = Menu()
        self.newDialog.show()

    def event_book_info(self, id_n):
        self.newDialog = Book_info(id_n)
        self.newDialog.show()

class Menu(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui',self)
        self.setWindowTitle('Menu')
        self.Dprofile_button.clicked.connect(self.event_profile)

    def event_profile(self):
        self.close()
        self.newDialog = Profile('', '', 'Долгов нет')
        self.newDialog.show()

class Profile(QDialog):
    def __init__(self, it_log, it_pasport, it_dolg):
        super().__init__()
        self.it_log = it_log
        self.it_pasport = it_pasport
        self.it_dolg = it_dolg
        uic.loadUi('user_profile.ui',self)
        self.setWindowTitle('Профиль')
        self.acc_button.clicked.connect(self.event_enter)
        self.name_label.setText('Логин:\t\t' + self.it_log)
        self.pasport_label.setText('Паспорт:\t' + self.it_pasport)
        self.img.setText(it_dolg)
            
    def event_enter(self):
        self.close()
        self.newDialog = Enter_in_acc()
        self.newDialog.show()

class Enter_in_acc(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('enter_in_acc.ui',self)
        self.con = sqlite3.connect("book.db")
        self.setWindowTitle('Вход в аккаунт')
        self.reg_button.clicked.connect(self.registration)
        self.ok_button.clicked.connect(self.enter_to_acc)

    def enter_to_acc(self):
        cur = self.con.cursor()
        all_id = str(cur.execute("SELECT id FROM Users ORDER BY id DESC LIMIT 1").fetchone())
        all_id = int(all_id[1:-2:1])
        for i in range(2, all_id+1, 1):
            new_login = str(cur.execute("SELECT user_login FROM Users WHERE id=?", (i,)).fetchone())
            new_login = new_login[2:-3:1]
            new_pas = str(cur.execute("SELECT password FROM Users WHERE id=?", (i,)).fetchone())
            new_pas = new_pas[2:-3:1]
            if str(self.login_edit.text()) == new_login and str(self.pas_edit.text()) == new_pas:
                self.status.setText('Вход прошел успешно')
                global its_log
                its_log = new_login
                new_pasport = str(cur.execute("SELECT pasport FROM Users WHERE id=?", (i,)).fetchone())
                new_pasport = new_pasport[2:-3:1]
                new_dolg = str(cur.execute("SELECT debt FROM Users WHERE id=?", (i,)).fetchone())
                if new_dolg=='(None,)':
                    new_dolg = 'Долгов нет'
                else:
                    new_dolg = new_dolg[1]
                    new_dolg = str(cur.execute("SELECT title FROM books_all WHERE id=?", (new_dolg,)).fetchone())
                    new_dolg = new_dolg[2:-3:1]
                self.close()
                self.newDialog = Profile(its_log, new_pasport, new_dolg)
                self.newDialog.show()
                break
            else:
                self.status.setText('Неправильный логин или пароль')

    def registration(self):
        i, okBtnPressed = QInputDialog.getText(self, "Регистрация", "Введите ваш логин")
        if okBtnPressed:
            self.login_py = str(i)
        i, okBtnPressed = QInputDialog.getText(self, "Регистрация", "Введите ваши пасспортные данные")
        if okBtnPressed:
            self.pasport_py = str(i)
        i, okBtnPressed = QInputDialog.getText(self, "Регистрация", "Введите ваш пароль")
        if okBtnPressed:
            self.password_py = str(i)
        cur = self.con.cursor()
        self.id_user = str(cur.execute("SELECT id FROM Users ORDER BY id DESC LIMIT 1").fetchone())
        self.id_user = self.id_user[1:-2:1]
        self.id_user = int(self.id_user) + 1
        cur.execute(f"INSERT INTO Users (id, user_login, pasport, password) VALUES (?, ?, ?, ?)",(self.id_user, self.login_py, self.pasport_py, self.password_py)).fetchall()
        self.con.commit()

class Book_info(QDialog):
    def __init__(self,id_n):
        super().__init__()
        self.id_n = id_n
        uic.loadUi('Book_info.ui',self)
        self.con = sqlite3.connect("book.db")
        cur = self.con.cursor()
        self.setWindowTitle('Информация о книге')
        title_py = str(cur.execute("SELECT title FROM books_all WHERE id=?", (self.id_n,)).fetchone())
        self.book_title.setText('Название: \t' + title_py[2:-3:1])
        self.img.setText(title_py[2:-3:1])
        author_py = str(cur.execute("SELECT author FROM books_all WHERE id=?", (self.id_n,)).fetchone())
        self.book_author.setText('Автор: \t\t' + author_py[2:-3:1])
        year_py = str(cur.execute("SELECT year FROM books_all WHERE id=?", (self.id_n,)).fetchone())
        self.book_year.setText('Год: \t\t' + year_py[2:-3:1])
        genre_py = str(cur.execute("SELECT title from Genres WHERE id=(SELECT genre FROM books_all WHERE id=?)", (self.id_n,)).fetchone())
        self.book_genre.setText('Жанр: \t\t' + genre_py[2:-3:1])
        description_py = str(cur.execute("SELECT description FROM books_all WHERE id=?", (self.id_n,)).fetchone())
        self.book_description.setText('Описание: \t' + description_py[2:-3:1])
        self.int_quantity_py = cur.execute("SELECT quantity FROM books_all WHERE id=?", (self.id_n,)).fetchone()
        quantity_py = str(self.int_quantity_py)
        quantity_py = quantity_py[1:-2:1]
        self.int_quantity_py = int(quantity_py)
        self.book_quantity.setText('Количество: ' + quantity_py)
        self.order_button.clicked.connect(self.order)
        if self.int_quantity_py == 0:
            self.order_button.setEnabled(False)

    def order(self):
        cur = self.con.cursor()
        debt_check = str(cur.execute("SELECT debt FROM Users WHERE user_login=?", (its_log,)).fetchone())
        if (debt_check == 'None' or debt_check == '(None,)') and its_log!='' and self.int_quantity_py > 0:
            debt = str(cur.execute("SELECT id FROM books_all WHERE id=?", (self.id_n,)).fetchone())
            debt = int(debt[1:-2:1])
            cur.execute("""UPDATE Users SET debt=? WHERE user_login=?""",(debt, its_log,)).fetchall()
            self.int_quantity_py -= 1
            cur.execute("""UPDATE books_all SET quantity=? WHERE id=?""",(self.int_quantity_py, self.id_n,)).fetchall()
            self.con.commit()
            self.con.close()
        self.order_button.setEnabled(False)
        quantity_py = str(self.int_quantity_py)
        self.book_quantity.setText('Количество: ' + quantity_py)

app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec())
