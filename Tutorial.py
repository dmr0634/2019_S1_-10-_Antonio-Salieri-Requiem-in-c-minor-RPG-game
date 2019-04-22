
from tkinter import *

window = Tk()

window.title("")

window.geometry('550x300')

nameLabel1 = Label(window, text="\u2022Press 'E' to pick up items\n\n"
"\u2022Press 'Esc' to open game menu\n\n"
"\u2022Press 'Q' to open character menu\n\n"
"\u2022Press 'Enter' to confirm selected option\n\n"
"\u2022Use W,A,S,D or Arrows to control character",
fg="gray")

nameLabel1.place(relx=.5, rely=.5, anchor="center")
nameLabel1.config(font=("Courier", 19))

txt = Entry(window, width=10)

window.mainloop()

