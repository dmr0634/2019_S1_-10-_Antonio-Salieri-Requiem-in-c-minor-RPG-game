from tkinter import *

window = Tk()

window.title("Welcome to LikeGeeks app")

window.geometry('800x400')

lbl = Label(window, text="Use W,A,S,D or Arrows to control character movement. ")
lb2 = Label(window, text="Press 'E' to pick up items ")
lb3 = Label(window, text="Press 'Q' to open character menu")
lb4 = Label(window, text="Press 'ESC' to open game menu")
lb5 = Label(window, text="Press 'Enter' to confitm selected option")

lbl.grid(column=6, row=10)
lb2.grid(column=6, row=11)
lb3.grid(column=6, row=12)
lb4.grid(column=6, row=13)
lb5.grid(column=6, row=14)

def clicked():
    lbl.configure(text="Button was clicked !!")
    lbl.configure(text="")
    lb2.configure(text="")
    lb3.configure(text="")
    lb4.configure(text="")
    lb5.configure(text="")

btn = Button(window, text="next", command=clicked)

btn.grid(column=1, row=0)

window.mainloop()
