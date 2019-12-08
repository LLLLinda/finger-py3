from tkinter import *
from tkinter import messagebox
from functools import partial
import requests

def comp(state, forward):
    prompt("bot is thinking the next move...")

    b0.config(state="disabled")
    b1.config(state="disabled")
    b2.config(state="disabled")
    b3.config(state="disabled")

    r = requests.post("http://a04f8d4a2199611eaba6906e7112dd5b-1674793614.ap-northeast-1.elb.amazonaws.com:8080/function/one-process", data= state)
    game = str(r.text.strip())

    top.configure(state="normal")
    top.insert(INSERT,"bot made a move:")
    top.insert(INSERT,game[-9:-5])
    top.insert(INSERT,"->")
    top.insert(INSERT,game[-4:])
    top.insert(INSERT,"\n\n")
    top.configure(state="disabled")
    top.see(END)

    b0.config(text=game[-4])
    b1.config(text=game[-3])
    b2.config(text=game[-2])
    b3.config(text=game[-1])

    b2.config(state="normal")
    b3.config(state="normal")

    is0()

    if not (str(b2["text"])=="0" and str(b3["text"])=="0"):
        prompt("It's your turn!\n")


root=Tk()

top = Text(root,width=50, height=10)
top.grid(row = 0, column = 0, sticky=N, columnspan=3)

top.insert(INSERT, " ___\n")
top.insert(INSERT, "|    *    _    __    ___    _   __\n")
top.insert(INSERT, "|--- |  |/ \  /  \| /___\ |/ \\ (__ \n")
top.insert(INSERT, "|    |  |   | \__/| \___  |    ___)\n")
top.insert(INSERT, "                  |\n")
top.insert(INSERT, "              \__/\n\n")
top.configure(state="disabled")


def prompt(s):
    top.configure(state="normal")
    top.insert(INSERT, s+"\n")
    top.configure(state="disabled")
    top.see(END)

ready=False

def press(b):
    if ready==True:
        if b==b2:
            if len(str(b2["text"]))==1:
                if len(str(b3["text"]))==1:
                    is0()
                    b2.config(text=str(b2["text"])+" *")
                else:
                    b3.config(text=str(b3["text"])[0])
                    b2.config(text=(int(b2["text"])+int(b3["text"]))%5)
                    is0(True)

            else:
                b2.config(text=str(b2["text"])[0])
                b0.config(state="disabled")
                b1.config(state="disabled")
        else: #b==b3
            if len(str(b3["text"]))==1:
                if len(str(b2["text"]))==1:
                    is0()
                    b3.config(text=str(b3["text"])+" *")
                else:
                    b2.config(text=str(b2["text"])[0])
                    b3.config(text=(int(b3["text"])+int(b2["text"]))%5)
                    is0(True)
            else:
                b3.config(text=str(b3["text"])[0])
                b0.config(state="disabled")
                b1.config(state="disabled")


def oppo(b):
    if ready==True:
        if len(str(b2["text"]))!=1:
            b2.config(text=str(b2["text"])[0]) 
            b.config(text=(int(b["text"])+int(b2["text"]))%5)
        elif len(str(b3["text"]))!=1:
            b3.config(text=str(b3["text"])[0]) 
            b.config(text=(int(b["text"])+int(b3["text"]))%5)    
        is0(True)

def is0(tobot=False):
    if not GameOver():
        for b in [b0,b1,b2,b3]:
            if len(str(b2["text"]))==1:
                if int(b["text"])==0:
                    b.config(state="disabled")
                else:
                    b.config(state="normal")
        if tobot:
            global game
            game=str(game)+"/"+str(b0["text"])+str(b1["text"])+str(b2["text"])+str(b3["text"])
            comp(game,5)

    else:
        b0.config(state="disabled")
        b1.config(state="disabled")
        b2.config(state="disabled")
        b3.config(state="disabled")

def restart():
    MsgBox = messagebox.askquestion('Restart','Start a new game?',icon = 'warning')
    if MsgBox == 'yes':
       All()

def quit():
    MsgBox = messagebox.askquestion ('Quit','Close applicaton?',icon = 'warning')
    if MsgBox == 'yes':
       root.destroy()
        
b0 = Button (root, text=1, width=10, height=2)
b0.grid(row=1, column=0)

b1 = Button (root, text=1, width=10, height=2)
b1.grid(row=1, column=2)

b2 = Button (root, text=1, width=10, height=2)
b2.grid(row=4, column=0)

b3 = Button (root, text=1, width=10, height=2)
b3.grid(row=4, column=2)

b0.config(command=partial(oppo,b0))
b1.config(command=partial(oppo,b1))
b2.config(command=partial(press,b2))
b3.config(command=partial(press,b3))

r = Button (root, text='Restart',width=10, height=2, command=restart)
r.grid(row=2, column=1)

q = Button (root, text='Quit',width=10, height=2, command=quit)
q.grid(row=3, column=1)

ready=True


def GameOver():
  if str(b0["text"])=="0" and str(b1["text"])=="0":
    prompt("You win!")
    return True
  elif str(b2["text"])=="0" and str(b3["text"])=="0":
    prompt("You lose!")
    return True
  else:
    return False

def All():
    MsgBox = messagebox.askquestion('Welcome!','How would you like to start the game?\n    -  "Yes"  to start FIRST,\n    -  "No"   to start NEXT.',icon = 'warning')
    if MsgBox == 'yes':
        u=1
        prompt("You chose to start FIRST")
    else:
        u=2
        prompt("You chose to start NEXT")

    prompt("Let's play!!\n")

    for b in [b0,b1,b2,b3]:
        b.config(text="1")

    game="1111"

    b0.config(state="disabled")
    b1.config(state="disabled")
    b2.config(state="disabled")
    b3.config(state="disabled")

    if u==1:
        prompt("It's your turn!\n")
        b2.config(state="normal")
        b3.config(state="normal")
    else:
        comp(game,5)



MsgBox = messagebox.askquestion('Welcome!','How would you like to start the game?\n    -  "Yes"  to start FIRST,\n    -  "No"   to start NEXT.',icon = 'warning')
if MsgBox == 'yes':
    u=1
    prompt("You chose to start FIRST")
else:
    u=2
    prompt("You chose to start NEXT")

prompt("Let's play!!\n")


game="1111"

b0.config(state="disabled")
b1.config(state="disabled")
b2.config(state="disabled")
b3.config(state="disabled")

if u==1:
    prompt("It's your turn!\n")
    b2.config(state="normal")
    b3.config(state="normal")
else:
    comp(game,5)



root.mainloop()
