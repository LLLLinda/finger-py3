import requests

def comp(state, forward):
  r = requests.post("http://a04f8d4a2199611eaba6906e7112dd5b-1674793614.ap-northeast-1.elb.amazonaws.com:8080/function/one-process", data= state)
  return r.text.strip()



#setup
public=[]
haveMod=True
strict=False #maintains opponent's "01" or "10" value, does not support haveMod==False 

def tostr(i,j,k,l): #convert digits into a state
  return str(i)+str(j)+str(k)+str(l)

def Overflow(v): #handle >5 condition under haveMod
  if haveMod==True:
    return v % 5
  else:
    if v>=5: 
      return 0
    else:
      return v

for i in range(5): #generate list of all states under haveMod
  for j in range(5):
    if (i<=j) and not((i==0) and (j==0)): 
      for k in range(5):
        for l in range(5):
          if (k<=l) and not((k==0) and (l==0)):
            state=[tostr(i,j,k,l)]

            if (k!=0):
              if (i!=0):
                state.append(tostr(Overflow(i+k),j,k,l))
              if (j!=0) and (i!=j):
                if not haveMod or (not strict) or (strict and (not(i==0 and j==1) or (k==4))):
                  state.append(tostr(i,Overflow(j+k),k,l))
              if (l!=0):
                state.append(tostr(i,j,k,Overflow(l+k)))

            if (l!=0):
              if (i!=0) and (k!=l) and (Overflow(i+k)!=Overflow(i+l)):
                state.append(tostr(Overflow(i+l),j,k,l))
              if (j!=0) and (k!=l) and (i!=j) and (Overflow(j+k)!=Overflow(j+l)):
                if not haveMod or (not strict) or (strict and (not(i==0 and j==1) or (k==0 and l==1) or (l==4))):
                  state.append(tostr(i,Overflow(j+l),k,l))
              if (k!=0) and (k!=l):
                state.append(tostr(i,j,Overflow(k+l),l))

            for a in range(k+l):
              if (((haveMod==True) and (a<=(k+l-a)% 5)) or ((haveMod==False) and (a<=(k+l-a)))) and	not((a==k) and (Overflow(k+l-a)==l)):
                if a!=0 or Overflow(k+l-a)!=0:
                  state.append(tostr(i,j,a,Overflow(k+l-a)))
            
            public.append(state)

#functions
def swap(state,a,b): #swap specified digits a, b of state s
  state=list(state)
  temp=state[a]
  state[a]=state[b]
  state[b]=temp
  state="".join(state)
  return state

def turn(state): #swap first 2 digits with last 2 to indicate turn end
  '''enhanced functionality for function path:\n
   only processes last 4 digits if len(state)>4'''
  if len(state)<=4:
    prev=""
  else:
    prev=state[:-4]
  state=state[-4:]

  state=swap(state,0,2)
  state=swap(state,1,3)
  return prev+state

def argm(state): #arrangement for digits to locate state
  f=""
  if state[0]>state[1]: 
    f="1"
  else: 
    f="0"

  if state[2]>state[3]: 
    f=f+"1"
  else: 
    f=f+"0"

  return f

def convert(state,f): #convert a state by arrangement for state search
  if f[0]=="1": state=swap(state,0,1)
  if f[1]=="1": state=swap(state,2,3)
  return state

def comb(state): #all combinations of a given state
  return [convert(state, f) for f in ["00","01","10","11"]]

def isloop(state, game): #tells if a game has encountered a loop
  g=game.split("/")
  for i in range(len(g)-1):
    if g[i] in comb(state) and i%2==game.count("/")%2:
      return True
  return False

def locate(state): #locate state number for a SORTED state
  if state[:2]=="01": h=0; t=13
  elif state[:2]=="02": h=14; t=27
  elif state[:2]=="03": h=28; t=41
  elif state[:2]=="04": h=42; t=55
  elif state[:2]=="11": h=56; t=69
  elif state[:2]=="12": h=70; t=83
  elif state[:2]=="13": h=84; t=97
  elif state[:2]=="14": h=98; t=111
  elif state[:2]=="22": h=112; t=125
  elif state[:2]=="23": h=126; t=139
  elif state[:2]=="24": h=140; t=153
  elif state[:2]=="33": h=154; t=167
  elif state[:2]=="34": h=168; t=181
  elif state[:2]=="44": h=182; t=195
  else: 
    return print("Cannot identify state", state, "! Did you forget to swap state order?")

  for target in range(h,t+1):
    if public[target][0]==state: break
  
  return(target)

#don't change the above...

def m1(state):
  nz0=False
  nz1=False
  nz2=False
  nz3=False
  allowA=False

  print("I) Choose from below... ")
  if state[2]!="0":
    nz2=True
    print("<1> - use L hand (value: ",state[2],")", sep="")
  if state[3]!="0":
    nz3=True
    print("<2> - use R hand (value: ",state[3],")", sep="")
  if sum([int(x) for x in list(state[2:])])!=1:
    allowA=True
    print("<3> - rearrange")
  print("<0> - quit game")
  
  valid=False
  while not valid:
    x=input("\nYour move: ")
    if (x=="1" and not nz2) or (x=="2" and not nz3) or (x=="3" and not allowA) or (x not in ["0","1","2","3"]):
      print("invalid input!")
      continue
    else:
      if x=="0":
        return -1
      valid=True

  print()

  if x!="3":
    if x=="1": print("II) Use L hand (value: ",state[2],") to tap...", sep="")
    if x=="2": print("II) Use R hand (value: ",state[3],") to tap...", sep="")
    if state[0]!="0":
      nz0=True
      print("<1> - oponent L hand (value: ",state[0],")", sep="")
    if state[1]!="0":
      nz1=True
      print("<2> - oponent R hand (value: ",state[1],")", sep="")
    if x=="1" and nz3==True:
      print("<3> - own R hand (value: ",state[3],")", sep="")
    if x=="2" and nz2==True:
      print("<3> - own L hand (value: ",state[2],")", sep="")
    print("<0> - return")

    valid=False
    while not valid:
      y=input("\nYour move: ")
      if (y=="1" and not nz0) or (y=="2" and not nz1) or (y=="3" and (not nz2 or not nz3)) or (y not in ["0","1","2","3"]):
        print("invalid input!")
        continue
      else:
        valid=True
    print("\n")

    if y=="0":
      return 0
    else:
      if x=="1":
        if y=="1":
          return str(Overflow(int(state[0])+int(state[2])))+state[1:]
        elif y=="2":
          return state[0]+str(Overflow(int(state[1])+int(state[2])))+state[2:]
        else:
          return state[:3]+str(Overflow(int(state[3])+int(state[2])))
      else:
        if y=="1":
          return str(Overflow(int(state[0])+int(state[3])))+state[1:]
        elif y=="2":
          return state[0]+str(Overflow(int(state[1])+int(state[3])))+state[2:]
        else:
          return state[:2]+str(Overflow(int(state[2])+int(state[3])))+state[3]

  else:
    print("II) Choose new arrangement...")
    swap=False
    arrg=[]
    if int(state[2])>int(state[3]):
      swap=True
      k=int(state[3])
    else:
      k=int(state[2])
    l=int(state[2])+int(state[3])-k
    count=0
    for a in range(k+l):
      if (a<=(k+l-a)% 5) and not((a==k) and (Overflow(k+l-a)==l)):
        if a!=0 or Overflow(k+l-a)!=0:
          count+=1
          if not swap: 
            print("<",count,"> - ",a," ",Overflow(k+l-a), sep="")
            arrg.append(str(a)+str(Overflow(k+l-a)))
          else: 
            print("<",count,"> - ",Overflow(k+l-a)," ",a, sep="")
            arrg.append(str(Overflow(k+l-a))+str(a))
    print("<0> - return")

    valid=False
    while not valid:
      y=input("\nYour move: ")
      if (y not in [str(i) for i in range(count+1)]):
        print("invalid input!")
        continue
      else:
        valid=True
    print("\n")

    if y=="0":
      return 0
    else:
      return state[:2]+arrg[int(y)-1]

def m2(state):
  print("Choose from below...")

  options=[convert(path, argm(state)) for path in public[locate(convert(state, argm(state)))][1:]]
  for i in range(len(options)):
    print("<",i+1,"> - ", options[i], sep="")
  print("<0> - quit game")

  valid=False
  while not valid:
    y=input("\nYour move: ")
    if (y not in [str(i) for i in range(len(options)+1)]):
      print("invalid input!")
      continue
    else:
      if y=="0":
        return -1
      valid=True
  print("\n")

  return options[int(y)-1]

def player(game, mode):
  if len(game)<=4:
    prev=""
    state=game
  else:
    prev=game[:-4]
    state=game[-4:]
  
  print(prev,">", sep="")
  print("Comp: ",state[0],"\t",state[1])
  print("You : ",state[2],"\t",state[3],"\n")
  r=0
  while type(r)!=type(""):
    if mode==1:
      r=m1(state)
    else:
      r=m2(state)
    if r==-1:
      return -1

  return prev+state+"/"+r

def GameOver(game):
  if len(game)<=4:
    state=game
  else:
    state=game[-4:]
  
  if state[2:]=="00":
    print("You lose!")
    return True
  elif state[:2]=="00":
    print("You win!")
    return True
  else:
    return False

def play():
  print("Let's play!!")
  u=0
  while u not in [1,2]:
    u=int(input("You want to go...\n<1> - first, or \n<2> - second? "))
    if u not in [1,2]: print("invalid input!\n")
  print()

  mode=0
  while mode not in [1,2]:
    mode=int(input("Your preferred game mode... \n<1> - step-by-step moves or \n<2> - show all possible moves? "))
    if mode not in [1,2]: print("invalid input!\n")
  print()

  game="1111"
  while not GameOver(game):
    if u==1:
      game=player(game,mode)
      if game==-1:
        return -1
      elif GameOver(game): 
        break
      else:
        game=comp(game,5)
        print("The computer made a move:",game[-9:-5], "->",game[-4:],"\n")
    else:
      game=comp(game,5)
      print("The computer made a move:",game[-9:-5], "->", game[-4:],"\n")
      if GameOver(game):
        break
      else:
        game=player(game,mode)
        if game==-1:
          return -1

  return 0

def wrap():
  print(" ___")
  print("|    *    _    __    __     _   __")
  print("|--- |  |/ \  /  \| /___\ |/ \\ (__ ")
  print("|    |  |   | \__/| \___  |    ___)")
  print("                  |")
  print("              \__/")

  d=0
  while d!=2:
    d=0
    print()
    play()
    while d not in [1,2]:
      d=int(input("\nWould you like to... \n<1> - start a new game \n<2> - quit? "))
      if d not in [1,2]: print("invalid input!\n")
      print()

wrap()
