from tkinter import END, messagebox
from tkinter.filedialog import askopenfile, askopenfilename

from unicodedata import category

from models.Database import Database


class Controller:
    def __init__(self, model, view):
        """
        Kontrolleri konstruktor
        :param model: main-is loodud mudel
        :param view:  main-is loodud view
        """

        self.model = model
        self.view = view

        # Rippmenüü funktsionaalsus
        self.view.get_combo_categories.bind("<<ComboboxSelected>>", self.combobox_change)


        #Nuppude callback seaded
        self.btn_add_callback()
        self.btn_delete_callback()
        self.btn_edit_callback()


    def btn_add_callback(self):
        self.view.set_btn_add_callback(self.btn_add_click) #Teeb nupu Lisa toimivaks

    def btn_delete_callback(self):
        self.view.set_btn_delete_callback(self.btn_delete_click)

    def btn_edit_callback(self):
        self.view.set_btn_edit_callback(self.btn_edit_click)



    def btn_add_click(self):
        #self.model.save_new_word(self.view.get_txt_word.get())
        #category_select = self.model.save_new_word(self.combobox_change())
        #print(self.view.get_combo_categories.get(), end=" => ")  # Tekst rippmenüüst => Hoonaed
        #print(self.view.get_combo_categories.current())
        if self.view.get_combo_categories.current() > 0:
            category = self.view.get_combo_categories.get().lower()
        else:
            category = self.view.get_txt_category.get().lower()
        word = self.view.get_txt_word.get().lower()
        #print(category)
        if word and category:
            db = Database()
            db.add_record(category, word)
            self.view.get_my_table.destroy()
            self.view.vsb.destroy()
            self.view.create_table()

    def btn_delete_click(self):
        #print('Kustuta')
        id = self.view.get_lbl_id2['text']
        db = Database()
        db.delete_data(id)
        self.view.get_my_table.destroy()
        self.view.vsb.destroy()
        self.view.create_table()

    def btn_edit_click(self):
        #print('Muuda')
        id = self.view.get_lbl_id2['text']
        word = self.view.get_txt_word.get()
        category = self.view.get_combo_categories.get()
        db = Database()
        db.edit_data(id, word, category)
        self.view.get_my_table.destroy()
        self.view.vsb.destroy()
        self.view.create_table()


    def combobox_change(self, event=None):
        """
        Kui valitakse rippmenüüst tegevus, saadakse kätte tekst kui ka index (print lause). Näide kuidas võiks
        rippmenüü antud rakenduses töötada :)
        :param event: vaikimisi pole
        :return: None
        """
        # print(self.view.get_combo_categories.get(), end=" => ") # Tekst rippmenüüst => Hoonaed
        # print(self.view.get_combo_categories.current()) # Rippmenüü index => 1

        if self.view.get_combo_categories.current() > 0:  # Vali kategooria on 0
            self.view.get_txt_category.delete(0, END) # Tühjenda uue kategooria sisestuskast
            self.view.get_txt_category.config(state='disabled')  # Ei saa sisestada uut kategooriat
            self.view.get_txt_word.focus()

        else:
            self.view.get_txt_category.config(state='normal')  # Saab sisestada uue kategooria
            self.view.get_txt_category.focus()




