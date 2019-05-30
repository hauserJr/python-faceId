
from tkinter import *


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("HelloWorld Demo")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

def AddVire(s):
    rootGUI = Tk()
    my_gui = MyFirstGUI(rootGUI)
    rootGUI.geometry("800x480")

    rootGUI.label = Label(s)
    rootGUI.label.pack()


    rootGUI.mainloop()

#rootGUI = Tk()
#rootGUI.title("HelloWorld Demo")
#rootGUI.geometry("800x480")

#rootGUIlabel = Label(rootGUI, text="This is our first GUI!")
#rootGUIlabel.pack()

#rootGUI.mainloop()

