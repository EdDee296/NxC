from tkinter import *
from tkinter import ttk

class MyWindow:
    def __init__(self, window):
        self.window = window
        self.canvas = Canvas(self.window)
        self.frame = Frame(self.canvas)
        self.scrollbar = Scrollbar(self.window, command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.frame.bind("<Configure>", self.update_scrollregion)

        self.create_layer()

    def create_layer(self):
        layer = ttk.Combobox(self.frame, values=[], width=10)
        layer.place(x=127.0, y=269.0)

        arg = ttk.Combobox(self.frame, values=[], width=7)
        arg.place(x=125.0, y=304.0)

    def update_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

window = Tk()
MyWindow(window)
window.mainloop()