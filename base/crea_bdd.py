import sqlite3

bdd = sqlite3.connect('résa.bibli.squlite3')

def table_exist():
  
  cursor = bdd.cursor()
  
  cursor.execute("CREATE TABLE IF NOT EXISTS Users   (id INTEGER PRIMARY KEY AUTOINCREMENT,nom_prenom TEXT NON NULL)")

  cursor.execute("CREATE TABLE IF NOT EXISTS Books (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NON NULL,author TEXT NON NULL)")

  cursor.execute("CREATE TABLE IF NOT EXISTS Reservations (id INTEGER PRIMARY KEY AUTOINCREMENT,user_id INTEGER, book_id INTEGER, date_emprunt TIMESTAMP, date_rendue TIMESTAMP)")
  
  bdd.commit()