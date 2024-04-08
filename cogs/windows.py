import datetime
import subprocess
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *
from .data.config import *
from .data.connect import connect_db

class my_window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('900x400')
        self.window.title('Мастер на все лапки')
        self.window.iconbitmap(default='assets/icons/logo.ico')

        self.create_frames()

        self.window.mainloop()

    def create_frames(self):
        self.notebook = Notebook()
        style = Style()
        style.configure('TFrame', background='lightblue')
        self.notebook.pack(expand=True, fill=BOTH)

        self.frame1 = Frame(self.notebook)
        self.frame2 = Frame(self.notebook)
        self.frame3 = Frame(self.notebook)

        self.frame1.pack(fill=BOTH, expand=True)
        self.frame2.pack(fill=BOTH, expand=True)
        self.frame3.pack(fill=BOTH, expand=True)

        self.notebook.add(self.frame1, text='Товары')
        self.notebook.add(self.frame2, text='Купить')
        self.notebook.add(self.frame3, text='Продать')

        self.frame_tovar()
        self.frame_buy()
        self.frame_sell()

    # вклад 'Товары'
    def frame_tovar(self):
        # таблица товаров
        self.table_tov = Treeview(self.frame1, columns=['tovar', 'price'], show='headings')
        self.table_tov.heading('tovar', text='Товар')
        self.table_tov.heading('price', text='Цена')
        self.table_tov.column('tovar', width=150, anchor='c')
        self.table_tov.column('price', width=150, anchor='c')
        self.table_tov.place(x=10, y=10)
        # текст названия
        self.tovar_name = StringVar()
        self.lb_name = Label(self.frame1, text='Наименование товара:', background='lightblue', font='Arial 12')
        self.lb_name.place(x=350, y=20)
        # текстовое поля для ввода названия
        self.entry_price = Entry(self.frame1, textvariable=self.tovar_name, font='Arial 12')
        self.entry_price.place(x=350, y=60)
        # текст цены
        self.tovar_price = DoubleVar()
        self.lb_name = Label(self.frame1, text='Цена товара:', background='lightblue', font='Arial 12')
        self.lb_name.place(x=350, y=100)
        # текстовое поля для ввода цены
        self.entry_price = Entry(self.frame1, textvariable=self.tovar_price, font='Arial 12')
        self.entry_price.place(x=350, y=140)
        # кнопки
        self.btn_new_tovar = Button(self.frame1, text='Добавить новый товар')
        self.btn_new_tovar.place(x=600, y=60)
        self.btn_del_tovar = Button(self.frame1, text='Удалить товар')
        self.btn_del_tovar.place(x=600, y=100)
        self.btn_update_tovar = Button(self.frame1, text='Изменить товар')
        self.btn_update_tovar.place(x=600, y=140)

    # вкладка 'Купить'
    def frame_buy(self):
        pass

    # вкладка 'Продать'
    def frame_sell(self):
        pass