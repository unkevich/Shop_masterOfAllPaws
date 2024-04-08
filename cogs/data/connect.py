import sqlite3
from tkinter import messagebox

class connect_db:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()
    
    def execute_sql(self, sql_txt):
        try:
            self.sql_txt = sql_txt
            return self.cursor.execute(self.sql_txt)
        except:
            messagebox.showerror('Ошибка', 'Невозможно получить данные!')
    
    def close_db(self):
        self.connector.commit()
        self.cursor.close()
        self.connector.close()