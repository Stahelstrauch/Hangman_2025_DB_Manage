import os
import sqlite3
import sys
from tkinter import messagebox


class Database:
    db_name = 'databases/hangman_2025.db'
    table = 'words'

    def __init__(self):

        if not os.path.exists(self.db_name):
            self.make_database()

        """Konstruktor"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = None
        self.connect()  # Loo ühendus
        self.cursor = self.conn.cursor()
        self.check_table()

        self.get_categories()

    def make_database(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        try:
            sql = '''CREATE TABLE "words" (
	"id"	INTEGER NOT NULL UNIQUE,
	"word"	TEXT NOT NULL,
	"category"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
)'''
            print("Attempting to create table...")
            self.cursor.execute(sql)
            self.conn.commit()
            messagebox.showinfo('Loodi andmebaas', 'Andmebaas koos tabeliga "words" loodi projekti Hangman_2025_DB_Manage databases kausta!')
        except sqlite3.OperationalError as error:
            print(f'Tabeli loomisel tekkis viga: {error}')
        finally:
            print('Tubli!')


    def check_table(self):
        if self.cursor:
            try:
                sql = 'SELECT name FROM sqlite_master WHERE type="table" and name=?'
                self.cursor.execute(sql, (self.table,))
                result = self.cursor.fetchone()
                if result:
                    print('Tabel word on olemas!')
                    sql = f'select id, word, category from {self.table}'
                    self.cursor.execute(sql)
                    if result:
                        print('Tabelis on veerud olemas')
                    else:
                        print('Veerge ei ole olemas.')
                else:
                    print('Tabelit word pole')
                    #self.close_connection()
            except sqlite3.Error as error:
                print(f'Ei saanud ühendust luua: {error} ')
                sys.exit(1)

    def connect(self):
        """Loob ühenduse andmebaasiga"""
        try:
            if self.conn:
                self.conn.close()  # eelnev ühendus suletakse
                print('Varasem andmebaasi ühendus suleti')
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            print(f'Uus ühendus andmebaasiga {self.db_name} loodud')
        except sqlite3.Error as error:
            print(f'Tõrge andmebaasi ühenduse loomisel:{error}')
            self.conn = None
            self.cursor = None

    def get_categories(self):
        if self.cursor:
            self.cursor.execute("SELECT DISTINCT category FROM words")
            data = self.cursor.fetchall()
            categories = [category[0] for category in data]
            categories.sort()
            categories.insert(0, 'Vali kategooria')
            # print(f'Kategooriad: {categories}.')
            return [category.capitalize() for category in categories]


    def add_record(self, category, word):
        print(f'See jura {word} {category}')
        if self.cursor:
            try:
                sql = f'INSERT INTO words (word, category) VALUES (?, ?)'
                self.cursor.execute(sql, (word, category))
                self.conn.commit() #See lisab reaalselt tabelisse (save)
                print('Sõna on lisatud tabelisse.')
            except sqlite3.Error as error:
                print(f'Sõna lisamisel tuli tõrge: {error}')
            finally:
                self.close_connection()
        else:
            print('Ühendus puudub! Palun loo ühendus andmebaasiga.')


    def read_word(self):
        """Loeb andmebaasist kogu edetabeli"""
        if self.cursor:
            try:
                sql = f'SELECT * FROM words order by category;'
                self.cursor.execute(sql)
                data_word = self.cursor.fetchall() #Kõik kirjed muutujasse data
                return data_word # Tagastab kõik kirjed, mis andmebaasiga seotud on
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return [] #Tagastab tühja listi
            finally:
                self.close_connection() #Igaljuhul sulge ühendus'

    def delete_data(self, id):
        print(id)
        if self.cursor:
            try:
                sql = f'delete from words where id=?'
                self.cursor.execute(sql, (id,))
                self.conn.commit()
                print('Andmed kustutati!')
            except sqlite3.Error as error:
                print(f'Kirjete lugemisel ilmnes tõrge: {error}')
                return []  # Tagastab tühja listi
            finally:
                self.close_connection()  # Igaljuhul sulge ühendus
        else:
            print('Ühendus andmebaasiga puudub. Palun loo ühendus andmebaasiga.')

    def edit_data(self,id, word, category):
        print(id, word,category)
        if self.cursor:
            try:
                sql = f'UPDATE words SET word = ?, category = ? WHERE id=?'
                self.cursor.execute(sql, (word, category, id))
                self.conn.commit()
                print('Andmebaasis parandati sõna: {word} ja kategooria: {category}')
            except sqlite3.Error as error:
                print('Kirjete muutmisel tekkis tõrge {error}')
                return []
            finally:
                self.close_connection()
        else:
            print('Ühendus andmebaasiga puudub!')



    def close_connection(self):
        """Sulgeb andmebaasi ühenduse"""
        try:
            if self.conn:
                self.conn.close()
                print(f'Ühendus andmebaasiga {self.db_name} suletud.')
        except sqlite3.Error as error:
            print(f'Tõrge ühenduse sulgemisel: {error}')

