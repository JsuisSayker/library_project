import sqlite3
import base.crea_bdd as crea_bdd
import datetime

cursor = crea_bdd.bdd.cursor()
crea_bdd.table_exist()


#This function is used to make a new database
def new_bdd():
    cursor.execute('DELETE FROM Users')
    cursor.execute('DELETE FROM Books')
    cursor.execute('DELETE FROM Reservations')

    list_nom = [{
        "nom_prenom": "Alexis Limouzin"
    }, {
        "nom_prenom": "Tuan Henry"
    }, {
        "nom_prenom": "Killian Trouve"
    }, {
        "nom_prenom": "Matisse de Cornuaud Marcheteau"
    }, {
        "nom_prenom": "Théo Domengie"
    }, {
        "nom_prenom": "Hansouman Sow"
    }, {
        "nom_prenom": "Coline Guilmard"
    }, {
        "nom_prenom": "Julien Lejealle"
    }, {
        "nom_prenom": "Lea Perrot"
    }, {
        "nom_prenom": "Remi Vanicat"
    }, {
        "nom_prenom": "Elouan Caro"
    }]

    crea_bdd.table_exist()
    for nom in list_nom:
        cursor.execute("INSERT INTO Users (nom_prenom) VALUES (:nom_prenom)",
                       nom)
    crea_bdd.bdd.commit()

    list_book = [{
        "title": "La Volonté de puissance",
        "author": "Elisabeth Förster-Nietzsche"
    }, {
        "title": "Sami et Julie en classe de découverte",
        "author": "Loïc Audrain"
    }, {
        "title": "Apprendre à développer avec JavaScript",
        "author": "Christian Vigouroux"
    }, {
        "title": "Psychologie de la connerie",
        "author": "Jean-François Marmion "
    }, {
        "title": "L'Art difficile de rester assise sur une balançoire",
        "author": "Emmanuelle Urien"
    }, {
        "title": "Programmer Pour les Nuls",
        "author": "Wallace Wang"
    }]

    for book in list_book:
        cursor.execute(
            "INSERT INTO Books (title,author) VALUES (:title,:author)", book)
    crea_bdd.bdd.commit()


class Base:
    def __init__(self, bdd):
        pass

#Take the user_id and the book_id for making the reservation

    def reservation(self, id, book):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        dico = {"id": id, "book": book}
        cursor.execute(
            "INSERT INTO Reservations (user_id,book_id) VALUES       (:id,:book)",
            dico)
        bdd.commit()

#Make a list with all the books inside

    def list_all_books(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute("SELECT title,author FROM Books")
        return cursor.fetchall()

#return the title of the books which are reserve

    def list_books(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute(
            "SELECT Books.title FROM Books INNER JOIN Reservations ON Books.id == Reservations.book_id"
        )
        return cursor.fetchall()

#Make a list with all the reservation

    def list_taken(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute(
            "SELECT user_id FROM Reservations WHERE user_id IS NOT NULL")
        for user_id in self.get_reservation():
            cursor.execute(
                "SELECT Books.title, Books.author FROM Books INNER JOIN Reservations ON Books.id == Reservations.book_id"
            )
        return cursor.fetchall()

#Make a list with all the books not reserve

    def list_not_taken(self):
        lst_all_books = self.list_all_books()
        lst_books_taken = self.list_taken()
        lst_books_not_taken = []
        print(lst_all_books, lst_books_taken)
        for books in lst_all_books:
            if books not in lst_books_taken:
                lst_books_not_taken.append(books)
            else:
                print("toto")
        return lst_books_not_taken

#Get a list with the id of all the books

    def get_book_id(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute("SELECT id FROM Books")
        return cursor.fetchall()

#take the title and transform it into is id

    def sweep_id(self, title):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute("SELECT id FROM Books WHERE title = :reservation",
                       {"reservation": title})
        return cursor.fetchone()[0]

#take the name and transform it into is id

    def sweep_name(self, nom_prenom):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute("SELECT id FROM Users WHERE nom_prenom = :identifiant",
                       {"identifiant": nom_prenom})
        return cursor.fetchone()[0]

#Take the id of one of the members and transform it into his name

    def get_name(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute("SELECT id FROM Users")
        for id in self.get_book_id():
            cursor.execute("SELECT nom_prenom FROM Users")
        return cursor.fetchall()

#Take the user_id where are in Reservations

    def get_reservation(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute("SELECT user_id FROM Reservations")
        return cursor.fetchall()

#return the loan and return date, for the client

    def client_pov(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        self.list_books()
        for reserve in self.list_taken():
            date_now = datetime.datetime.now()
            date_later = date_now + datetime.timedelta(days=20)
            print(date_later)
            cursor.execute(
                "UPDATE Reservations SET date_emprunt = ? ,date_rendue = ?;",
                (date_now, date_later))
            cursor.execute("SELECT date_emprunt,date_rendue FROM Reservations")
        return cursor.fetchall()

#Make alist with the  reserve books, for the bookseller

    def library_emprunt(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        for reserve in self.list_taken():
            print('Livre emprunté :')
            cursor.execute(
                "SELECT Books.title FROM Books INNER JOIN Reservations ON Books.id == Reservations.book_id"
            )
            return cursor.fetchall()
        return []

#return the loan, and return date

    def library_date(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        for reserve in self.list_taken():
            date_now = datetime.datetime.now()
            date_later = date_now + datetime.timedelta(days=20)
            cursor.execute(
                "UPDATE Reservations SET date_emprunt = ? ,date_rendue = ?;",
                (date_now, date_later))
            cursor.execute("SELECT date_emprunt,date_rendue FROM Reservations")
        return cursor.fetchmany()

#Make a list with the name of all the people who reserve a book

    def library_client(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        for reserve in self.list_taken():
            print('Emprunter par :')
        cursor.execute("SELECT user_id FROM Reservations")
        for user_id in self.get_reservation():
            cursor.execute(
                "SELECT Users.nom_prenom FROM Users INNER JOIN Reservations ON Reservations.user_id == Users.id "
            )
        return cursor.fetchall()


#Delete all the reservation

    def reservation_clear(self):
        bdd = sqlite3.connect('résa.bibli.squlite3')
        cursor = bdd.cursor()
        cursor.execute('DELETE FROM Reservations')
        bdd.commit()

base = Base(crea_bdd.bdd)
print('Books id :')
print(base.get_book_id())
print('User id :')
print(base.get_name())
#base.reservation_clear()#execute this command if you want to clear all the reservations
print('Les livres réservés sont :')
print(base.list_books())
print('Voici le point de vue du libraire :')
print(base.library_emprunt())
print(base.library_date())
print(base.library_client())
