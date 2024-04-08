import datetime
import subprocess
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

class my_window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry('900x400')
        self.window.title('Мастер на все лапки')
        self.window.iconbitmap(default='assets/icons/logo.ico')

        self.window.mainloop()