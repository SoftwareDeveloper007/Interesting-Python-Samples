from tkinter import *

class Application(object):
    def __init__(self, parent):
        self.x = list(range(5000))
        self.labels = []
        self.parent = parent
        self.navigation_frame = Frame(self.parent)
        self.canvas =  Canvas(self.parent, bg='black', width = 200, height = 500)
        self.mainFrame = Frame(self.canvas)
        self.navigation_frame.pack()
        for i in range(100):
            self.labels.append(Label(self.mainFrame, text=str(i)))
            self.labels[i].grid()
        self.back_button = Button(self.navigation_frame, text='Back', command=lambda: self.move(-2))
        self.quick_nav = Entry(self.navigation_frame, width=3)
        self.quick_nav.bind('<Return>', lambda x: self.move(self.quick_nav.get()))
        self.forward_button = Button(self.navigation_frame, text='Forward', command=lambda: self.move(0))

        temp = divmod(len(self.x), len(self.labels))
        self.pages = temp[0] + (1 if temp[1] else 0)

        self.you_are_here = Label(self.navigation_frame, text='Page 1 of ' + str(self.pages))
        self.current_page = 1
        self.back_button.grid(row=0, column=0)
        self.quick_nav.grid(row=0, column=1)
        self.forward_button.grid(row=0, column=2)
        self.you_are_here.grid(row=0, column=3)
        self.scroll = Scrollbar(self.parent, orient = VERTICAL, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both')
        self.canvas.create_window((4,4), window=self.mainFrame, anchor="nw", tags="frame")

        self.canvas.configure(yscrollcommand = self.scroll.set)
        self.mainFrame.bind("<Configure>", self.update)

    def update(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def move(self, direction):
        if (self.current_page == 1 and direction == -2) or (self.current_page == self.pages and direction == 0):
            return
        if direction in (-2, 0):
            self.current_page += direction + 1
        else:
            try:
                temp = int(direction)
                if temp not in range(1, self.pages+1):
                    return
            except ValueError:
                return
            else:
                self.current_page = temp
        for i in range(len(self.labels)):
            try:
                location = str(self.x[len(self.labels)*(self.current_page - 1) + i])
            except IndexError:
                location = ''
            self.labels[i].config(text=location)
        self.you_are_here.config(text='Page ' + str(self.current_page) + ' of ' + str(self.pages))

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    root.mainloop()