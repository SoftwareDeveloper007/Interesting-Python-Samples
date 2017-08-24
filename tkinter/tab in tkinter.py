import tkinter
from tkinter import *
from ttk import *
import ttk
import tkinter as tk

root = Tk()
root.title("Model_A")
#root.resizable(0,0)

#root.grid()
#root.geometry("1200x800")
# start of Notebook (multiple tabs)
notebook = ttk.Notebook(root)
notebook.pack(fill=BOTH, expand=True)

#Child Frames
ContainerOne = Canvas(notebook)
ContainerOne.pack(fill=BOTH, expand=True)
ContainerTwo = Canvas(notebook)
ContainerTwo.pack(fill=BOTH, expand=True)
ContainerThree = Canvas(notebook)
ContainerThree.pack(fill=BOTH, expand=True)
ContainerFour = Canvas(notebook)
ContainerFour.pack(fill=BOTH, expand=True)

#Create the pages
notebook.add(ContainerOne, text='Mode A')
notebook.add(ContainerTwo, text='Mode B')
notebook.add(ContainerThree, text='Mode C')
notebook.add(ContainerFour, text='Mode D')

frame = Frame(ContainerOne, width=1200, height=800)
scroll = Scrollbar(root)
frame.pack(side=LEFT, fill=BOTH, expand=True)
scroll.pack(side=RIGHT, fill=Y)

ContainerOne.configure(yscrollcommand=scroll.set, background="black", scrollregion=(0,0,100,1000))
scroll.configure(command=ContainerOne.yview)
#Component Selection

componentComb = Combobox(frame, state="readonly", values=("A", "B", "C"))
componentComb.pack()
componentComb.set("Main Selection")



root.mainloop()