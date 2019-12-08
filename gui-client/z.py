from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from functools import partial
import requests
from requests.exceptions import Timeout

def comp(state, forward):
    prompt("bot is thinking the next move...")

    b0.config(state="disabled")
    b1.config(state="disabled")
    b2.config(state="disabled")
    b3.config(state="disabled")
    ls.config(state="disabled")

    r = requests.post(url, data= state)
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

    is0()

    if not (str(b2["text"])=="0" and str(b3["text"])=="0"):
        prompt("It's your turn!\n")


root=Tk()
root.title('Fingers')

top = Text(root,width=50, height=10)
top.grid(row = 1, column = 0, sticky=N, columnspan=3)

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
        
        ls.set("")

        if tobot:
            global game
            game=str(game)+"/"+str(b0["text"])+str(b1["text"])+str(b2["text"])+str(b3["text"])
            comp(game,5)
        else:
            swap=False
            arrg=[]
            if int(b2["text"])>int(b3["text"]):
                swap=True
                k=int(b3["text"])
            else:
                k=int(b2["text"])
            l=int(b2["text"])+int(b3["text"])-k
            count=0
            for a in range(k+l):
                if (a<=(k+l-a)% 5) and not((a==k) and ((k+l-a)%5==l)):
                    if a!=0 or (k+l-a)%5!=0:
                        count+=1
                        if not swap: 
                            arrg.append(str(a)+"   "+str((k+l-a)%5))
                        else: 
                            arrg.append(str((k+l-a)%5)+"   "+str(a))
            if len(arrg)==0:
                ls.config(state="disabled")
            else:
                ls.config(state="readonly")
                ls.config(values=arrg)
            

    else:
        b0.config(state="disabled")
        b1.config(state="disabled")
        b2.config(state="disabled")
        b3.config(state="disabled")
        ls.config(state="disabled")

def restart():
    MsgBox = messagebox.askquestion('Restart','Start a new game?')
    if MsgBox == 'yes':
       All()

def quit():
    MsgBox = messagebox.askquestion ('Quit','Close applicaton?')
    if MsgBox == 'yes':
       root.destroy()
        
dum= Label(root, text = "\nbot") 
dum.grid(row=2, column=1)

dum1= Label(root, text = "\n\nArrange...") 
dum1.grid(row=6, column=1)

dum2= Label(root, text = "you\n\n") 
dum2.grid(row=8, column=1)

b0 = Button (root, text=1, width=10, height=2)
b0.grid(row=3, column=0)

b1 = Button (root, text=1, width=10, height=2)
b1.grid(row=3, column=2)

b2 = Button (root, text=1, width=10, height=2)
b2.grid(row=7, column=0)

b3 = Button (root, text=1, width=10, height=2)
b3.grid(row=7, column=2)

b0.config(command=partial(oppo,b0))
b1.config(command=partial(oppo,b1))
b2.config(command=partial(press,b2))
b3.config(command=partial(press,b3))

r = Button (root, text='Restart',width=10, height=2, command=restart)
r.grid(row=4, column=1)

q = Button (root, text='Quit',width=10, height=2, command=quit)
q.grid(row=5, column=1)

ls= ttk.Combobox(root, state="readonly", width=10, height=2)
ls.grid(row=7, column=1)

def selected(event):
  b2.config(text=ls.get()[0])
  b3.config(text=ls.get()[-1])
  ls.config(values=[])
  is0(True)

ls.bind("<<ComboboxSelected>>", selected)


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
    MsgBox = messagebox.askquestion('Welcome!','How would you like to start the game?\n    -  "Yes"  to start FIRST,\n    -  "No"   to start NEXT.')
    if MsgBox == 'yes':
        u=1
        prompt("You chose to start FIRST")
    else:
        u=2
        prompt("You chose to start NEXT")

    prompt("Let's play!!\n")

    for b in [b0,b1,b2,b3]:
        b.config(text="1")
    
    ls.set("")

    game="1111"

    b0.config(state="disabled")
    b1.config(state="disabled")
    b2.config(state="disabled")
    b3.config(state="disabled")

    if u==1:
        prompt("It's your turn!\n")
        is0()
    else:
        comp(game,5)


from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
url = askstring('Configuration', 'Please enter Server URL of the bot:')

if url=="":
    root.destroy()
else:
    try:
        response = requests.get(url, data="1111", timeout=5)
    except Timeout:
        showinfo("Error", 'Connection timeout, now quitting application.')
        root.destroy()
    else:
        if response.status_code!=200:
            showinfo("Error", "Connection error, now quitting application.")
            root.destroy()
        else:
            showinfo("Success", "Connect successful.")





MsgBox = messagebox.askquestion('Welcome!','How would you like to start the game?\n    -  "Yes"  to start FIRST,\n    -  "No"   to start NEXT.')
if MsgBox == 'yes':
    u=1
    prompt("\nYou chose to start FIRST")
else:
    u=2
    prompt("\nYou chose to start NEXT")

prompt("Let's play!!\n")


game="1111"

b0.config(state="disabled")
b1.config(state="disabled")
b2.config(state="disabled")
b3.config(state="disabled")

if u==1:
    prompt("It's your turn!\n")
    is0()
else:
    comp(game,5)



root.mainloop()
