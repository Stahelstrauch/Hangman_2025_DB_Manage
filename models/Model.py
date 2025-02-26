import sqlite3
from tkinter import messagebox

from models.Database import Database



class Model:
    def __init__(self):
        self.database = Database()
        self.__categories = self.database.get_categories()
        self.data_word = self.database.read_word()







    @property
    def categories(self):
        return self.__categories