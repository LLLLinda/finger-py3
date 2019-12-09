#setup
states=[]
haveMod=True
strict=True #maintains opponent's "01" or "10" value, does not support haveMod==False 

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
            
            states.append(state)

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

#output

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
    return

  for target in range(h,t+1):
    if states[target][0]==state: break
  
  return(target)

def path(state, prune=False): #list all possible paths from ANY game state & attach result
  '''processes last 4 digits if len(state)>4'''
  doPrune=False

  if len(state)<=4:
    prev=""
  else:
    prev=state[:-4]
  state=state[-4:]
  
  if prev.count("/")%2==1:
    output= [prev+state+"/"+convert(turn(path), argm(state)) for path in states[locate(turn(convert(state, argm(state))))][1:]]
  else:
    output= [prev+state+"/"+convert(path, argm(state)) for path in states[locate(convert(state, argm(state)))][1:]]
  
  for i in range(len(output)):
    state=output[i][-4:]
    if state[:2]=="00":
      if output[i].count("/")%2==1:
        output[i]=output[i]+"/wins"
        if prune:
          doPrune=True
          break
      else:
        output[i]=output[i]+"/impr"
    elif state[2:]=="00": 
      if output[i].count("/")%2==1:
        output[i]=output[i]+"/impr"
      else:
        output[i]=output[i]+"/lose"
        if prune:
          doPrune=True
          break
    elif isloop(state, output[i][:-4]):
      output[i]=output[i]+"/loop"

  if prune==True and doPrune==True:
    output=[output[i]]

  return output

def foresee(state): #simple heuristics for immediate state
  if len(state)<=4:
    prev=""
  else:
    prev=state[:-4]
  state=state[-4:]
  if state.isdigit()==True:
    if prev.count("/")%2==0: #going to be my turn
      if ((state[0]=="0" or state[1]=="0") and #win if 0Xab where X+a/b=>0 or (X+a/b=6 and a,b!=0/1,4) or (X=1 and a,b!=0,1)
          (Overflow(sum([int(x) for x in list(state[:2])])+int(state[2]))==0 or 
          Overflow(sum([int(x) for x in list(state[:2])])+int(state[3]))==0 or
          ((sum([int(x) for x in list(state[:2])])+int(state[2])==6 or
            sum([int(x) for x in list(state[:2])])+int(state[3])==6) and 
            state[2:] not in ["04","40","14","41"]) or 
          (sum([int(x) for x in list(state[:2])])==1 and sum([int(x) for x in list(state[2:])])!=1))):
        state=state+"/wins"
      elif ((state[0]=="1" or state[1]=="1") and #win if 1Xab and a,b!=0/1,4 where X+a=>0 or X+b=>0
          state[2:] not in ["04","40","14","41"] and
          ((Overflow(sum([int(x) for x in list(state[:2])])-1+int(state[2]))==0 and
           int(state[2])!=0) or 
          (Overflow(sum([int(x) for x in list(state[:2])])-1+int(state[3]))==0 and
           int(state[3])!=0))):
        state=state+"/wins"
      elif sum([int(x) for x in list(state[2:])])==1: #otherwise lose if ??01
        state=state+"/lose"
    else:
      if ((state[2]=="0" or state[3]=="0") and
          (Overflow(sum([int(x) for x in list(state[2:])])+int(state[0]))==0 or 
          Overflow(sum([int(x) for x in list(state[2:])])+int(state[1]))==0 or
          ((sum([int(x) for x in list(state[2:])])+int(state[0])==6 or
          sum([int(x) for x in list(state[2:])])+int(state[1])==6) and    
          state[:2] not in ["04","40","14","41"]) or
          (sum([int(x) for x in list(state[2:])])==1 and sum([int(x) for x in list(state[:2])])!=1))):
        state=state+"/lose"
      elif ((state[2]=="1" or state[3]=="1") and
          state[:2] not in ["04","40","14","41"] and
          ((Overflow(sum([int(x) for x in list(state[2:])])-1+int(state[0]))==0 and
           int(state[0])!=0) or 
          (Overflow(sum([int(x) for x in list(state[2:])])-1+int(state[1]))==0 and
           int(state[1])!=0))):
        state=state+"/lose"
      elif sum([int(x) for x in list(state[:2])])==1:
        state=state+"/wins"
  return prev+state

def extract(state): #remove any suffix to the state
  while state[-4:].isdigit()==False:
    state=state[:-5]
  state=state[:-5]
  return state

#recursive computation  
def think(steps, forward): #create list of list for derived state from a path function result
  if forward>=2:
    for i in range(len(steps)):
      if steps[i][-4:].isdigit()==True:
        steps[i]=[steps[i][-4:], think([foresee(x) for x in path(steps[i], True)], forward-1)]
  return steps

def draw(steps, depth=1): #draw the derived states from the above think function
  '''Leave depth as 1!!!'''
  for i in range(len(steps)):
    if type(steps[i])!=type([]):
      steps[i]=foresee(steps[i])
      print("\t"*(depth-1), steps[i])
    else:
      print("\t"*(depth-1), steps[i][0])
      draw(steps[i][1], depth+1)

def exclude(steps): #(de)notate moves that will cause the opponent player to win immediately
  avoidable=False
  #strip=False
  for i in range(len(steps)):
    if type(steps[i])==type([]): #if there exists a turn following the next
      if len(steps[i][1])==1 and type(steps[i][1][0])!=type([]) and (steps[i][1][0][-4:]=="wins" or steps[i][1][0][-4:]=="lose"):
        #if the turn after next has only one choice AND there is no other choice following AND it is either a win or lose
        for j in range(len(steps)):
          if type(steps[j])==type([]):
            if type(steps[j][1][0])==type([]) or steps[j][1][0][-4:].isdigit() or steps[j][1][0][-4:]=="loop":
              #any other path with undetermined outcome or loop after the next turn will do
              avoidable=True
        if avoidable:
          steps[i][0]=steps[i][0]+"xxxx"
          #we will delete this path and all its subsequent choices when using dive procedure
      else:
        exclude(steps[i][1])
    #elif steps[i][1][0][-4:]=="wins" or steps[i][1][0][-4:]=="lose":
      #strip=True?


def dive(steps, leaf): #process results from the above think function
  i=0
  while i < len(steps):
    if type(steps[i])!=type([]):
      order=[x[0] for x in leaf].index(steps[i][:len(leaf[0][0])])
      leaf[order][1][0]+=1
      if steps[i][-4:].isdigit()==False:
        if steps[i][-4:]=="wins":
          if steps[i].count("/")%2==1:
            impr=False
            for j in range(len(steps)):
              if type(steps[j])==type([]) or steps[j][-4:]!="wins":
                impr=True
                break
            if impr:
              steps[i]=steps[i]+"/xxxx"
              leaf[order][1][0]-=1
            else:
              leaf[order][1][1]+=1
          else:  
            leaf[order][1][1]+=1
          #leaf[order][1][1]+=1/10**(steps[i].count("/")-2)
          #leaf[order][1][1]=round(leaf[order][1][1]+1/steps[i].count("/"),3)
        elif steps[i][-4:]=="lose":
          if steps[i].count("/")%2==0:
            impr=False
            for j in range(len(steps)):
              if type(steps[j])==type([]) or steps[j][-4:]!="lose":
                impr=True
                break
            if impr:
              steps[i]=steps[i]+"/xxxx"
              leaf[order][1][0]-=1
            else:
              leaf[order][1][2]+=1
          else:
            leaf[order][1][2]+=1
          #leaf[order][1][2]+=1/10**(steps[i].count("/")-2)
          #leaf[order][1][2]=round(leaf[order][1][2]+1/steps[i].count("/"),3)
        elif steps[i][-4:]=="loop":
          leaf[order][1][3]+=1
      else:
        leaf[order][1][4]+=1
      i+=1
    else: #this part won't work anymore
      if steps[i][0][-4:]=="xxxx":
        del steps[i] 
      else:
        dive(steps[i][1], leaf)
        i+=1
  return leaf

def comp(state, forward): #wrap-up function for computing the next step
  if len(state)<=4:
    prev=""
  else:
    prev=state[:-4]
  state=turn(state[-4:])

  leaf=[[i[:len(state)+5],[0,0,0,0,0]] for i in path(state)]
  tree=think([foresee(x) for x in path(state)],forward)
  dive(tree, leaf)
  print("State tree:")
  draw(tree)
  print("\nResult statistics:")
  print("path: TotalPath, Wins, Loses, Loops, Unsettled")
  for i in range(len(leaf)):
    print(leaf[i])
  #return leaf

#def decision(leaf):
  #must win
  for i in range(len(leaf)):
    if leaf[i][1][0]==leaf[i][1][1] and leaf[i][1][1]!=0:
      return prev+turn(state)+"/"+turn(leaf[i][0][-4:])

  #win & 0 lose
  import random
  a=[]
  for i in range(len(leaf)):
    if leaf[i][1][0]==leaf[i][1][1] and leaf[i][1][1]!=0:
      a.append(i)
  if len(a)>0:
    return prev+turn(state)+"/"+turn(leaf[a[random.randrange(0,len(a))]][0][-4:])

  #more win than lose
  a=[]
  for i in range(len(leaf)):
    if leaf[i][1][1]>leaf[i][1][2]:
      if len(a)==0 or leaf[i][1][1]-leaf[i][1][2]>a[1]:
        a=[i,leaf[i][1][1]]
  if len(a)>0:
    return prev+turn(state)+"/"+turn(leaf[a[0]][0][-4:])

  #most loops only
  a=[]
  for i in range(len(leaf)):
    if leaf[i][1][1]==0 and leaf[i][1][2]==0 and leaf[i][1][3]>0:
      if len(a)==0 or leaf[i][1][3]>a[1]:
        a=[i,leaf[i][1][1]]
  if len(a)>0:
    return prev+turn(state)+"/"+turn(leaf[a[0]][0][-4:])

  #return random item from leaf
  a=[]
  b=[]
  for i in range(len(leaf)):
    if leaf[i][1][0]==0:
      b.append(i)
    else:
      a.append(i)
  if len(a)>0:
    return prev+turn(state)+"/"+turn(leaf[a[random.randrange(0,len(a))]][0][-4:])
  else:
    return prev+turn(state)+"/"+turn(leaf[b[random.randrange(0,len(b))]][0][-4:])
  
  #return "x"

#for i in range(len(states)):
  #l=decision(comp(states[i][0],5))
  #if l=="x": print(i)



def handle(req):
  return comp(str(req), 5)
