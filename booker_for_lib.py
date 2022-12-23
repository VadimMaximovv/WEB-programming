import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import *

its_log = ''

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
        self.newDialog = Book_redactor(id_n)
        self.newDialog.show()

class Menu(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu_for_lib.ui',self)
        self.setWindowTitle('Menu')
        self.all_book_button.clicked.connect(self.event_all_books)
        self.all_user_button.clicked.connect(self.event_all_users)

    def event_all_books(self):
        self.close()
        self.newDialog = All_books()
        self.newDialog.show()

    def event_all_users(self):
        self.close()
        self.newDialog = All_users()
        self.newDialog.show()

class All_books(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('all_books.ui',self)
        self.con = sqlite3.connect("book.db")
        self.setWindowTitle('Список всех книг')
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM books_all").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[1]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}

class All_users(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('all_users.ui',self)
        self.con = sqlite3.connect("book.db")
        self.setWindowTitle('Список всех пользователей')
        cur = self.con.cursor()
        result = cur.execute("SELECT id, user_login, pasport, debt FROM Users").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
        self.close_button.clicked.connect(self.closing)

    def closing(self):
        cur = self.con.cursor()
        cur.execute("UPDATE Users SET debt = NULL, time = NULL WHERE id=?",(self.spinBox.text(),)).fetchone()
        result = cur.execute("SELECT id, user_login, pasport, debt FROM Users").fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        self.modified = {}
        self.con.commit()


class Book_redactor(QDialog):
    def __init__(self,id_n):
        super().__init__()
        self.id_n = id_n
        uic.loadUi('book_redactor.ui',self)
        self.con = sqlite3.connect("book.db")
        cur = self.con.cursor()
        self.setWindowTitle('Информация о книге')
        title_py = str(cur.execute("SELECT title FROM books_all WHERE id=?", (self.id_n,)).fetchone())
        self.line_title.setText(title_py[2:-3:1])
        self.img.setText(title_py[2:-3:1])
        author_py = str(cur.execute("SELECT author FROM books_all WHERE id=?", (self.id_n,)).fetchone())
        self.line_author.setText(author_py[2:-3:1])
        year_py = str(cur.execute("SELECT year FROM books_all WHERE id=?", (self.id_n,)).fetchone())
        self.line_year.setText(year_py[2:-3:1])
        genre_py = str(cur.execute("SELECT title from Genres WHERE id=(SELECT genre FROM books_all WHERE id=?)", (self.id_n,)).fetchone())
        self.genre.setText(genre_py[2:-3:1])
        description_py = str(cur.execute("SELECT description FROM books_all WHERE id=?", (self.id_n,)).fetchone())
        self.line_description.setText(description_py[2:-3:1])
        self.int_quantity_py = cur.execute("SELECT quantity FROM books_all WHERE id=?", (self.id_n,)).fetchone()
        quantity_py = str(self.int_quantity_py)
        quantity_py = quantity_py[1:-2:1]
        self.int_quantity_py = int(quantity_py)
        self.col.setText(quantity_py)
        self.genre_button.clicked.connect(self.choose_genre)
        self.save_button.clicked.connect(self.save_data)
        self.cancel_button.clicked.connect(self.cancel_action)

    def choose_genre(self):
        cur = self.con.cursor()
        genres_all = ['']*21
        for j in range (1,21,1):
            genre = str(cur.execute("SELECT title FROM Genres WHERE id=?", (j,)).fetchone())
            genre = genre[2:-3:1]
            genres_all[j] = genre
        genres_all = str(genres_all)
        genres_all = genres_all.replace(",", "")
        genres_all = genres_all.replace("'", "")
        i, okBtnPressed = QInputDialog.getItem(self, "Выберете жанр", "Выберете жанр",  (genres_all[1:-1].split()), 1, False)
        if okBtnPressed:
            self.genre.setText(i)

    def save_data(self):
        cur = self.con.cursor()
        cur.execute("""UPDATE books_all SET title=?, author=?, year=?, description=?, quantity=? WHERE id=?""",(self.line_title.text(), self.line_author.text(), self.line_year.text(), self.line_description.text(),int(self.col.text()), self.id_n,)).fetchall()
        cur.execute("""UPDATE books_all SET genre=(SELECT id FROM Genres WHERE title=?) WHERE id=?""",(self.genre.text(), self.id_n,)).fetchall()
        self.img.setText(self.line_title.text())
        self.con.commit()
        self.con.close()

    def cancel_action(self):
        self.close()
            
app = QApplication(sys.argv)
ex = MyWidget()
ex.show()
sys.exit(app.exec())
