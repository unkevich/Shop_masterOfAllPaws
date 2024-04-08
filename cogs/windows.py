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

    def secret(self):
        self.canva = Canvas(self.frame1, width=900, height=200, bg='lightblue', highlightthickness=0)
        self.canva.place(x=0, y=250)

        self.img_m = PhotoImage(file='assets/images/magazin.png')
        self.img_del = PhotoImage(file='assets/images/delivery.png')
        self.img_tov = PhotoImage(file='assets/images/tovar.png')

        self.image_magazin = self.canva.create_image(800,60,image=self.img_m)
        self.image_delivery = self.canva.create_image(60,60,image=self.img_del,state='hidden')
        self.image_tovar = self.canva.create_image(750,100,image=self.img_tov,state='hidden')

        self.canva.tag_bind(self.image_magazin, '<Button-1>', lambda event: self.secret_move())
    
    def secret_move(self):
        self.canva.itemconfig(self.image_delivery, state='normal')
        self.canva.itemconfig(self.image_tovar, state='hidden')
        self.x, self.y = self.canva.coords(self.image_delivery)
        if self.x < 800:
            self.canva.move(self.image_delivery, 10, 0)
            self.canva.after(20, self.secret_move)
        else:
            self.canva.itemconfig(self.image_delivery, state='hidden')
            self.canva.coords(self.image_delivery, 60, 60)
            self.canva.itemconfig(self.image_tovar, state='normal')
    
    # сортировка по названию
    def sort_name(self, col, reverse, table):
        data = [(table.set(child, col), child) for child in table.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            table.move(child, '', index)
        table.heading(col, command=lambda: self.sort_number(col, not reverse, table))
    
    # сортировка по номеру
    def sort_number(self, col, reverse, table):
        data = [(float(table.set(child, col)), child) for child in table.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            table.move(child, '', index)
        table.heading(col, command=lambda: self.sort_number(col, not reverse, table))

    # обновление таблиц
    def update_tables(self, table):
        for row in table.get_children():
            table.delete(row)
        self.new_connect = connect_db(name_db)
        if table == self.table_tov:
            self.sql = self.new_connect.execute_sql(f'select * from tovar')
            for row in self.sql:
                self.db_name = row[1]
                self.db_price = row[2]
                self.table_tov.insert('', END, values=[self.db_name, self.db_price])

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
        self.btn_new_tovar = Button(self.frame1, text='Добавить новый товар', command=self.create_tovar)
        self.btn_new_tovar.place(x=600, y=60)
        self.btn_del_tovar = Button(self.frame1, text='Удалить товар')
        self.btn_del_tovar.place(x=600, y=100)
        self.btn_update_tovar = Button(self.frame1, text='Изменить товар')
        self.btn_update_tovar.place(x=600, y=140)

        self.update_tables(self.table_tov)
        self.table_tov.bind('<<TreeviewSelect>>', lambda event: self.select_tovar(self.tovar_name, self.tovar_price))

    def select_tovar(self, tovar_name, tovar_price):
        for row in self.table_tov.selection():
            tovar_name.set(self.table_tov.item(row)['values'][0])
            tovar_price.set(self.table_tov.item(row)['values'][1])

    # добавление товара
    def create_tovar(self):
        if self.tovar_name.get() != '' or self.tovar_price.get() != '':
            self.new_connect = connect_db(name_db)
            self.replay = self.new_connect.execute_sql(f"select * from tovar where name='{self.tovar_name.get()}'")
            if len(self.replay.fetchall()) > 0:
                messagebox.showerror('Ошибка', 'Такой товар уже существует!')
            else:
                self.new_connect.execute_sql(f"insert into tovar (name, price) values ('{self.tovar_name.get()}', '{self.tovar_price.get()}')")
            self.new_connect.close_db()
            self.update_tables(self.table_tov)

    # вкладка 'Купить'
    def frame_buy(self):
        pass

    # вкладка 'Продать'
    def frame_sell(self):
        pass