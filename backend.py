import os
import tkinter as tk

currentLs = []
CURRENT_DIR = ['/Users']

def pathName(bash=False):
    if bash:
        return str('/'.join(CURRENT_DIR)).replace(' ', r'\ ')
    return '/'.join(CURRENT_DIR)

def ls():
    currentLs = []
    for num, f in enumerate(os.listdir(pathName())):
        if os.path.isfile(os.path.join(pathName(), f)):
            currentLs.append(Executable(name=f, position=num))
        else:
            currentLs.append(Folder(name=f, position=num))
    return currentLs

def addPath(name):
    CURRENT_DIR.append(name)

def removePath(amount):
    for _ in range(amount):
        CURRENT_DIR.pop(-1)

class dataType:
    def __init__(self, name, position):
        self.name = name
        self.position = position

class Folder(dataType):
    def __init__(self, name, position):
        dataType.__init__(self, name, position)

    def __name__(self):
        return 'Folder'

    def buttonCommand(self):
        CURRENT_DIR.append(self.name),

class Executable:
    def __init__(self, name, position):
        dataType.__init__(self, name, position)

    def __name__(self):
        return 'Executable'

    def buttonCommand(self):
        pass

class Popup(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.overrideredirect(True)
        self.withdraw()
        self.deiconify()
        parent.update()
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.title('ERROR')
        self.parent = parent
        self.buttonbox()
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.geometry("+%d+%d" % (parent.winfo_width()/2,
                                  parent.winfo_height()/2))
        self.geometry('200x75')
        self.configure(bg='green')
        self.wm_attributes('-modified', 0.1)

    def buttonbox(self):
        l = tk.Label(self, text="PERMISSION DENIED", font='Helvetica 14 bold', bg='green', fg='black')
        l.pack(side='top', pady=5)
        self.a = tk.Button(self,
                    name='ok',
                    text="Ok",
                    fg='white',
                    highlightthickness=30,
                    highlightbackground='black',
                    command=self.ok,
                    default='active')
        self.a.place(width=92, height=30, x=5, y=40)
        self.bind('<Return>',lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.ok())

    def ok(self):
        self.parent.focus_set()
        self.destroy()

if __name__ == '__main__':
    root= tk.Tk()
    root.overrideredirect(1)
    app = Popup(root)
    app.mainloop()