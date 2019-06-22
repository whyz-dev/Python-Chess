from tkinter import *

window = Tk()
window.title("ノーゲーム・ノーライフ")
wall = PhotoImage(file="images/wall.png")

background = Label(window, image=wall)
background.pack()

window.resizable(False, False)

start_button = Button(window, text="Start", bg="#ffffff",fg="#a5008c")
quit_button = Button(window, text="Quit", bg="#ffffff",fg="#a5008c")

start_button.place(x=320, y=100, width=80, height=30)
quit_button.place(x=320, y=200, width=80, height=30)

window.mainloop()