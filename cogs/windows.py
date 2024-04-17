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

        self.old_name = ''

        self.price = 0
        self.sum = 0

        self.create_frames()
        self.secret()

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
            self.sql = self.new_connect.execute_sql(f"select * from tovar")
            for row in self.sql:
                self.db_name = row[1]
                self.db_price = row[2]
                self.table_tov.insert('', END, values=[self.db_name, self.db_price])
        elif table == self.table_buy:
            self.sql = self.new_connect.execute_sql(f'select T.name, T.price, TB.kol, TB.sum from tovar_buy TB inner join tovar T on TB.id_tovar = T.id')
            for row in self.sql:
                self.db_name = row[0]
                self.db_price = row[1]
                self.db_kol = row[2]
                self.db_sum = row[3]
                self.table_buy.insert('', END, values=[self.db_name, self.db_price])
        elif table == self.table_sell:
            self.sql = self.new_connect.execute_sql(f'select T.name, T.price, TS.kol, TS.sum from tovar_sell TS inner join tovar T on TS.id_tovar = T.id')
            for row in self.sql:
                self.db_name = row[0]
                self.db_price = row[1]
                self.db_kol = row[2]
                self.db_sum = row[3]
                self.table_sell.insert('', END, values=[self.db_name, self.db_price])

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

    # удаление товара
    def del_tovar(self):
        self.new_connect = connect_db(name_db)
        if self.tovar_name.get() != '':
            self.check = self.new_connect.execute_sql(f"select * from tovar where name='{self.tovar_name.get()}'")
            if len(self.check.fetchall()) == 0:
                messagebox.showerror('Ошибка', 'Такого товара не существует!')
            else:
                otvet = messagebox.askyesno('Уведомление', 'Вы точно желаете удалить данный товар?')
                if otvet:
                    self.sql = self.new_connect.execute_sql(f"delete from tovar where name='{self.tovar_name.get()}'")
                    self.new_connect.close_db()
                    self.update_tables(self.table_tov)
        else:
            messagebox.showerror('Ошибка', 'Товар не выбран!')
    
    # обновление товара
    def update_tovar(self):
        self.new_connect = connect_db(name_db)
        if self.tovar_name.get() != '':
            self.check = self.new_connect.execute_sql(f"select * from tovar where name='{self.old_name}'")
            if len(self.check.fetchall()) == 0:
                messagebox.showerror('Ошибка', 'Такого товара не существует!')
            else:
                self.replay = self.new_connect.execute_sql(f"select * from tovar where name='{self.tovar_name.get()}' and price='{self.tovar_price.get()}'")
                if len(self.replay.fetchall()) > 0:
                    messagebox.showerror('Ошибка', 'Такой товар уже существует!')
                else:
                    otvet = messagebox.askyesno('Увемдоление', 'Вы точно хотите удалить данный товар?')
                    if otvet:
                        self.new_connect.execute_sql(f"update tovar set name='{self.tovar_name.get()}' and price='{self.tovar_price.get()}' where name='{self.old_name}'")
                        self.new_connect.close_db()
                        self.update_tables(self.table_tov)
        else:
            messagebox.showerror('Ошибка', 'Товар не выбран!')

    def buy(self):
        if self.buy_tovar.get() != '' and self.sum > 0:
            print(self.price)
            self.new_connect = connect_db(name_db)
            self.sql = self.new_connect.execute_sql(f"se;ect * from tovar where name = '{self.buy_tovar.get()}'")
            for row in self.sql:
                self.id_tovar = row[0]
                self.new_connect.execute_sql(f"insert into tovar_buy (id_tovar, price, kol, sum) values ('{self.id_tovar}', '{self.price}', '{self.tovar_kol.get()}', '{self.sum}')")
            self.new_connect.close_db()
            self.update_tables(self.table_buy)
        else:
            messagebox.showerror('Ошибка', 'Вы не выбрали товар или не ввели количество')

    def set_sum(self):
        if self.tovar_kol.get() < 0:
            messagebox.showerror('Ошибка', 'Количествло не может быть отрицательным!')
            self.tovar_kol.set(0)
        self.sum = self.tovar_kol.get()*self.price
        self.lb_sum.configure(text=f'Сумма: {self.sum} руб.')

    def combobox_tovar(self):
        self.new_connect = connect_db(name_db)
        self.sql = self.new_connect.execute_sql(f"select * from tovar where name='{self.buy_tovar.get()}'")

        for row in self.sql:
            self.price = row[2]
        self.new_connect.close_db()
        self.lb_price.configure(text=f'Цена: {self.price} руб.')
        self.set_sum()

    def kol_up(self):
        self.tovar_kol.set(self.tovar_kol.get()+1)
        self.set_sum()

    def kol_down(self):
        if self.tovar_kol.get() > 0:
            self.tovar_kol.set(self.tovar_kol.get()-1)
            self.set_sum()

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
        self.btn_del_tovar = Button(self.frame1, text='Удалить товар', command=self.del_tovar)
        self.btn_del_tovar.place(x=600, y=100)
        self.btn_update_tovar = Button(self.frame1, text='Изменить товар', command=self.update_tovar)
        self.btn_update_tovar.place(x=600, y=140)

        self.update_tables(self.table_tov)
        self.table_tov.bind('<<TreeviewSelect>>', lambda event: self.select_tovar(self.tovar_name, self.tovar_price))

    # вкладка 'Купить'
    def frame_buy(self):
        self.table_buy = Treeview(self.frame2, columns=['tovar', 'price', 'kol', 'sum'], show='headings')
        self.table_buy.heading('tovar', text = 'Товар', command=lambda:self.sort_name('tovar', False, self.table_buy))
        self.table_buy.heading('price', text = 'Цена', command=lambda:self.sort_number('price', False, self.table_buy))
        self.table_buy.heading('kol', text = 'Количество', command=lambda:self.sort_number('kol', False, self.table_buy))
        self.table_buy.heading('sum', text = 'Сумма', command=lambda:self.sort_number('sum', False, self.table_buy))
        
        self.table_buy.column('tovar', width=150, anchor='c')
        self.table_buy.column('price', width=150, anchor='c')
        self.table_buy.column('kol', width=150, anchor='c')
        self.table_buy.column('sum', width=150, anchor='c')
        self.table_buy.place(x = 10, y = 10)

        self.update_tables(self.table_buy)

        self.tovar_list = []
        self.new_connect = connect_db(name_db)
        self.sql = self.new_connect.execute_sql(f'select * from tovar')
        for row in self.sql:
            self.tovar_list.append(row[1])
        self.new_connect.close_db()

        self.lb_name = Label(self.frame2, text='Выберите товар:', font='Arial 12', background='lightblue')
        self.lb_name.place(x=10, y=250)
        self.buy_tovar = Combobox(self.frame2, values=self.tovar_list, state='readonly')
        self.buy_tovar.place(x=10, y=300)
        self.buy_tovar.bind('<<ComboboxSelected>>', lambda event: self.combobox_tovar())

        self.tovar_kol = IntVar()
        self.lb_kol = Label(self.frame2, text='Введите количество:', font='Arial 12', background='lightblue')
        self.lb_kol.place(x=200, y=250)
        self.buy_kol = Entry(self.frame2, textvariable=self.tovar_kol)
        self.buy_tovar.place(x=200, y=300, width=100)

        self.lb_price = Label(self.frame2, text='Цена 0 руб.', font='Arial 12', background='lightblue')
        self.lb_price.place(x=10, y=340)

        self.lb_sum = Label(self.frame2, text='Итого 0 руб.', font='Arial 12', background='lightblue')
        self.lb_sum.place(x=200, y=340)

        self.btn_send_buy = Button(self.frame2, text='Купить', command=self.buy)
        self.btn_send_buy.place(x=400, y=300)

        self.btn_up = Button(self.frame2, text='+',)
        self.btn_up.place(x=300, y=300, width=25, height=23)
        self.btn_down = Button(self.frame2, text='-',)
        self.btn_down.place(x=325, y=300, width=25, height=23)

    # вкладка 'Продать'
    def frame_sell(self):
        self.table_sell = Treeview(self.frame3, columns=['tovar', 'price', 'kol', 'sum'], show='headings')
        self.table_sell.heading('tovar', text='Товар')
        self.table_sell.heading('price', text='Цена')
        self.table_sell.heading('kol', text='Количество')
        self.table_sell.heading('sum', text='Сумма')

        self.table_sell.column('tovar', width=150, anchor='c')
        self.table_sell.column('price', width=150, anchor='c')
        self.table_sell.column('kol', width=150, anchor='c')
        self.table_sell.column('sum', width=150, anchor='c')

        self.update_tables(self.table_sell)

        self.tovar_sell_list = []
        self.new_connect = connect_db(name_db)
        self.sql = self.new_connect.execute_sql(f"select * from tovar")
        for row in self.sql:
            self.tovar_sell_list.append(row[1])
        self.new_connect.close_db()

        self.lb_name = Label(self.frame3, text='Выберите товар:', font='Arial 12', background='lightblue')
        self.lb_name.place(x=10, y=250)
        self.sell_tovar = Combobox(self.frame3, values=self.tovar_sell_list, state='readonly')
        self.sell_tovar.place(x=10, y=300)

        self.lb_price2 = Label(self.frame3, text='Установите наценку:', font='Arial 12', background='lightblue')
        self.lb_price2.place(x=170, y=250)
        self.price2_tovar = Combobox(self.frame3, values=['10%', '15%', '20%', '25%', '30%'], state='readonly')
        self.price2_tovar.place(x=170, y=300, width=50)
        self.price2_tovar.current(0)
        self.price2_tovar.place(x=170, y=300, width=50)

        self.sell_tovar_kol = IntVar()
        self.lb_kol = Label(self.frame3, text='Введите количество:', font='Arial 12', background='lightblue')
        self.lb_kol.place(x=200, y=250)
        self.sell_kol = Entry(self.frame3, textvariable=self.tovar_kol)
        self.sell_kol.place(x=350, y=300, width=100)

        self.btn_up = Button(self.frame3, text='🔺',)
        self.btn_up.place(x=450, y=300, width=25, height=23)
        self.btn_down = Button(self.frame3, text='🔻',)
        self.btn_down.place(x=475, y=300, width=25, height=23)

        self.lb_sell_price = Label(self.frame3, text='Итого: 0 руб.', font='Arial 12', background='lightblue')
        self.lb_sell_price.place(x=10, y=340)

        self.lb_sell_sum = Label(self.frame3, text='Итого: 0 руб.', font='Arial 12', background='lightblue')
        self.lb_sell_sum.place(x=350, y=340)

        self.lb_kol_info = Label(self.frame3, text='Товаров на складе: 0.', font='Arial 12', background='lightblue')
        self.lb_kol_info.place(x=650, y=50)

        self.btn_send_sell = Button(self.frame3, text='Продать')
        self.btn_send_sell.place(x=550, y=300)