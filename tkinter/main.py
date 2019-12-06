from tkinter import *
from tkinter import ttk

#%%
class App:

    def __init__(self, master):

        frame = Frame(master, padx=10, pady=10, bg="#ECECEC")
        frame.pack()

        self.v = IntVar()

        self.preset1 = ttk.Radiobutton(frame, text="Preset 1", variable=self.v, value=1)
        self.preset1.pack(anchor=W)
        self.preset2 = ttk.Radiobutton(frame, text="Preset 2", variable=self.v, value=2)
        self.preset2.pack(anchor=W)

        self.next = ttk.Button(frame, text='Next', command=lambda: print(self.v.get()))
        self.next.pack(side='left')
        self.quit = ttk.Button(frame, text='quit', command=frame.quit)
        self.quit.pack(side='left')



root = Tk()

app = App(root)

root.mainloop()
root.destroy()

#%%


#%%

























#%% Check Button
master = Tk()

var = IntVar()

c = ttk.Checkbutton(master, text="Expand", variable=var)
c.pack()

ttk.Button(text="print selection", command=lambda: print(var.get())).pack()

mainloop()

#%%

master = Tk()

listbox = Listbox(master)
listbox.pack()

listbox.insert(END, "a list entry")

for item in ["one", "two", "three", "four"]:
    listbox.insert(END, item)

mainloop()

#%% RadioButton

master = Tk()






master.mainloop()
master.destroy()

#%%

root = Tk()

ttk.Style().configure("TButton", padding=10, relief="flat", background='black', foreground='black')

btn = ttk.Button(text="Sample")
btn.pack()

root.mainloop()


#%%
def callback():
    print("called the callback!")

root = Tk()

# create a menu
menu = Menu(root)
root.config(menu=menu)

filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New", command=callback)
filemenu.add_command(label="Open...", command=callback)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=callback)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=callback)

mainloop()

#%%

class One:

    def __init__(self):
        self.A = 1
        self.B = 2
        print("abc")

    def printok(self):
        print("ok")


class Two(One):
    b = 5
    def __init__(self):
        super().__init__()
        self.b = 10


#%%
a = Two()

 #%%
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

class Student(Person):
  pass

x = Student()
#%%