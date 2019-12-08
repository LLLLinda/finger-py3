from tkinter import *
from tkinter import messagebox
from functools import partial

root=Tk() # create window

#canvas1 = Canvas(root, width = 300, height = 300)
#canvas1.pack()

top = Text(root,width=50, height=10)
top.grid(row = 0, column = 0, sticky=N, columnspan=3)

top.insert(INSERT, " ___\n")
top.insert(INSERT, "|    *    _    __    ___    _   __\n")
top.insert(INSERT, "|--- |  |/ \  /  \| /___\ |/ \\ (__ \n")
top.insert(INSERT, "|    |  |   | \__/| \___  |    ___)\n")
top.insert(INSERT, "                  |\n")
top.insert(INSERT, "              \__/\n\n")
top.configure(state="disabled")



def bug():
    print("hi")

can=False

def press(b):
    if can==True:
        if len(str(b["text"]))==1:
            b.config(text=str(b["text"])+" *")
        else:
            b.config(text=str(b["text"])[0])

def ExitApplication():
    MsgBox = messagebox.askyesnocancel ('Welcome!','Are you sure you want to exit the application',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()
    else:
        messagebox.showinfo('Return','You will now return to the application screen')


def restart():
    MsgBox = messagebox.askquestion ('Exit Application','Start a new game?',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()

def quit():
    MsgBox = messagebox.askquestion ('Exit Application','Are you sure you want to quit?',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()
        
b0 = Button (root, text=0, width=10, height=2, command=bug)
b0.grid(row=1, column=0)

b1 = Button (root, text=0, width=10, height=2, command=ExitApplication)
b1.grid(row=1, column=2)

b2 = Button (root, text=0, width=10, height=2)
b2.grid(row=4, column=0)

b3 = Button (root, text=0, width=10, height=2)
b3.grid(row=4, column=2)


b2.config(command=partial(press,b2))
b3.config(command=partial(press,b3))

can=True


r = Button (root, text='Restart',width=10, height=2, command=restart)
r.grid(row=2, column=1)

q = Button (root, text='Quit',width=10, height=2, command=quit)
q.grid(row=3, column=1)



#canvas1.create_window(150, 150, window=button1)

MsgBox = messagebox.askquestion('Welcome!','How would you like to start the game?\nPress "Yes" to start first,\n"No" to start next',icon = 'warning')
if MsgBox == 'yes':
    print("1")






root.mainloop()