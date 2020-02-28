import tkinter as tk
from backend import pathName, ls, CURRENT_DIR
from config import *
import backend
import os

class App(tk.Frame):
    '''Main App Window with preset frames'''
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.master.title("Financer")
        self.master.resizable(True, True)
        self.master.tk_setPalette(bgColor)
        self.master.geometry(f'{frameWidth}x{frameHeight}')
        self.xPos = int((self.master.winfo_screenwidth() - self.master.winfo_reqwidth()) / 8)
        self.yPos = int((self.master.winfo_screenheight() - self.master.winfo_reqheight()) / 10)
        self.master.geometry("+{}+{}".format(self.xPos, self.yPos))

        self.menuFrame = tk.Frame(
                        self.master,
                        height=frameHeight*0.08,
                        width=frameWidth*1,
                        bg=bgColor
                    )
        self.menuFrame.pack(side='top', pady=5, padx=5)  

        self.listFrame = tk.Frame(self.master,
                                height=frameHeight*0.92,
                                width=frameWidth*0.98,
                                bg=bgColor
                                )
        self.logo = tk.Label(self.menuFrame,
                            text='FILE BROWSER 2019',
                            font=f'AndaleMono 14 bold',
                            background=fgColor,
                            foreground=bgColor
                            )
        self.logo.place(x=0, y=0, relwidth=1)
        self.listFrame.pack(side='left', pady=5, padx=5)  

        global DIR_COUNT
        DIR_COUNT = len(CURRENT_DIR)
        self.scrollbar = tk.Scrollbar(root, takefocus=True)
        self.scrollbar.pack(side='right', fill='y')
    
    def clearFrame(self, *args):
        for frame in args:
            for wdgt in frame.winfo_children():
                if wdgt.winfo_class() == 'Button':
                    wdgt.destroy()

    def permissionPrompt(self):
        backend.Popup(self.master)

class SelectLabel:
    def __init__(self):
        self.text = tk.StringVar()
        self.text.set(pathName(bash=True))
        ent = tk.Entry(
            app.menuFrame,
            state='readonly',
            readonlybackground=fgColor,
            fg=bgColor,
            textvariable=self.text,
            relief='flat',
            font=styleFont,
        )
        ent.place(x=0, y=30, relwidth=1)

    def update(self):
        self.text.set(pathName(bash=True))

class MainList:
    def __init__(self, position):
        self.position= position
        listbox = tk.Listbox(
            app.listFrame,
            background=bgColor,
            foreground=fgColor,
            font=styleFont,
            yscrollcommand=app.scrollbar.set,
            selectmode='browse'
        )
        listbox.place(relheight=1, relwidth=0.2, relx=0+position*0.2)
        app.scrollbar.config(command=listbox.yview)
        try:
            for data in ls():
                if data.__name__() == 'Folder':
                    listbox.insert(0, f'{FolderIcon} {data.name}')
                elif data.__name__() == 'Executable':
                    listbox.insert('end', data.name)
        except PermissionError:
            app.permissionPrompt()

        self.selected =  listbox.curselection()
        listbox.bind("<Double-Button-1>", lambda event: self.command(listbox.get('anchor')))
    
    def __name__(self):
        return f'MainList{self.position}'

    def command(self, item):
        self.update(item)
        DirLabel.update()

    def update(self, item):
        name_list = item.split(f'{FolderIcon} ')
        name = name_list[-1]
        if len(name_list) == 2:
            relativeLen = len(CURRENT_DIR)-DIR_COUNT
            if self.position != relativeLen:
                self.removeList(relativeLen-self.position)
            CURRENT_DIR.append(name)
            self.addList()
        else: print('Executable')

    def addList(self):
        if len(listBoxes) < 5:
            listBoxes.append(MainList(len(listBoxes)))
        else: print('max lists')

    def removeList(self, amount):
        backend.removePath(amount)
        _list = app.listFrame.winfo_children()
        for _ in range(amount):
            listBoxes.pop(-1)
            _list.pop(-1).destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    listBoxes = [MainList(position=0)]
    DirLabel = SelectLabel()
    app.mainloop()