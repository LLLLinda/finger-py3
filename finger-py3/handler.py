def handle(req):
    # generate dictionary and list of states for comp and user
    comp_states_dict = generate_states('comp', start_index=0)
    user_states_dict = generate_states('user', start_index=len(comp_states_dict))
    comp_states_list = list(comp_states_dict.values())
    user_states_list = list(user_states_dict.values())
    all_states_list = comp_states_list + user_states_list

    # connect all the states together
    build_links(comp_states_dict, user_states_dict)
    build_links(user_states_dict, comp_states_dict)

    # build graph
    g = Graph(directed=True)
    g.add_vertices(len(all_states_list))
    for i in range(len(g.vs)):
        state = all_states_list[i]
        if state.next:
            for j in range(len(state.next)):
                g.add_edge(state.index, state.next[j].index)

    # set score (score is mainly for user states)
    # 1. set for win step
    for state in user_states_list:
        if not state.next:
            state.score = 100
            state.win = True
        elif state.myleft == -1:
            state.score = 90
        elif state.myleft == 0 and state.myright == 1:
            state.score = 90
        
    # 2. set for lose step (after setting win to avoid seemingly win state)
    for state in comp_states_list:
        if not state.next:
            state.score = 0
            state.lose = True
        elif state.myleft == -1:
            state.score = 10
        elif state.myleft == 0 and state.myright == 1:
            state.score = 10
    for state in user_states_list:
        for child in state.next:
            if child.score < 50:
                state.score = child.score
                break

    def convert_side(string):
        chars = [char for char in string]
        new_string = []
        i = 0
        while i < len(chars):
            if chars[i] == '-':
                num = chars[i]+chars[i+1]
                i += 2
            else:
                num = chars[i]
                i += 1
            new_string.append(num)
        new_string[0], new_string[1], new_string[2], new_string[3] = new_string[2], new_string[3], new_string[0], new_string[1]
        return ''.join(new_string)

    end = False
    current_state = user_states_dict['1111']
    print("Rule:")
    print("Type in your choice as a string,", end=' ')
    print("your fingers go first,", end=' ')
    print("smaller one at the front.")
    print("'-1' means dead hand.")
    print("Type in 'q' if you want to quit.\n")
    print("Game started!")
    while not end:
        current_state.print_state(form='sqr')
        possible_choices = [state.get_state(form='str') for state in current_state.next]
        
        user_choice = input("Type in your choice:")
        if user_choice == 'q':
            print("Quit game.")
            break
        user_choice = convert_side(user_choice)
        while user_choice not in possible_choices:
            user_choice = input("Invalid choice, type in again:")
            if user_choice == 'q':
                print("Quit game.")
                break
            user_choice = convert_side(user_choice)
        
        current_state = comp_states_dict[user_choice]
        if current_state.lose:
            print("You win")
            break
        
        max_next = None
        max_score = 0
        for state in current_state.next:
            if state.score >= max_score:
                max_score = state.score
                max_next = state
                
        candidates = []
        for state in current_state.next:
            if state.score == max_score:
                candidates.append(state)
                
        current_state = choice(candidates)
        if current_state.win:
            current_state.print_state(form='sqr')
            print("You lose...")
            break


class State:
    def __init__(self, r, index=0, myl=1, myr=1, opl=1, opr=1, \
                 lose=False, win=False, score=50):
        self.role = r
        self.index = index
        self.myleft = myl
        self.myright = myr
        self.opleft = opl
        self.opright = opr
        self.next = list()
        self.prev = list()
        self.name = str(self.myleft)+str(self.myright)+str(self.opleft)+str(self.opright)
        self.lose = lose
        self.win = win
        self.footprint = 0
        self.score = score
        
    def info(self, show_next=True, show_prev=True):
        print("No.%d," %self.index, self.role)
        self.print_state()
        print("score %d" %self.score)
        if show_next:
            if self.next:
                print("Next state:")
                for child in self.next:
                    print(child.role, end=' ')
                    child.print_state()
        if show_prev:
            if self.prev:
                print("Previous state:")
                for parent in self.prev:
                    print(parent.role, end=' ')
                    parent.print_state()
    
    def print_state(self, form='str', view='me'):
        if form == 'str':
            if view == 'me':
                print(str(self.myleft)+str(self.myright)+str(self.opleft)+str(self.opright))
            elif view == 'op':
                print(str(self.opleft)+str(self.opright)+str(self.myleft)+str(self.myright))
        elif form == 'sqr':
            if view == 'me':
                print(self.opleft, self.opright)
                print(self.myleft, self.myright)
            elif view == 'op':
                print(self.myleft, self.myright)
                print(self.opleft, self.opright)
    
    def get_state(self, form='int'):
        if form == 'int':
            return self.myleft, self.myright, self.opleft, self.opright
        if form == 'str':
            return str(self.myleft)+str(self.myright)+str(self.opleft)+str(self.opright)
        else:
            print("form should be 'int' or 'str'")
    
    def set_index(self, index):
        self.index = index
    
    def reset_footprint(self):
        self.footprint = 0
    
    def add_next(self, state):
        k,l,i,j = state.get_state()
        a,b,c,d = self.get_state()
        if i==a and j==b and k==c and l==d:
            return
        if state not in self.next:
            self.next.append(state)
            
    def add_prev(self, state):
        k,l,i,j = state.get_state()
        a,b,c,d = self.get_state()
        if [a,b,c,d] == [i,j,k,l]:
            return
        if state not in self.prev:
            self.prev.append(state)

def generate_states(role, start_index):
    states = dict()
    myindex = start_index
    
    # all hands alive
    for j in range(1,5):
        for i in range(0, j+1):
            for l in range(1,5):
                for k in range(0,l+1):
                    state = State(r=role, index=myindex, myl=i, myr=j, opl=k, opr=l)
                    states[state.name] = state
                    myindex += 1
                    
    # only one of my hands dead                
    for j in range(0,5):
        for l in range(1,5):
            for k in range(0,l+1):
                state = State(r=role, index=myindex, myl=-1, myr=j, opl=k, opr=l)
                states[state.name] = state
                myindex += 1
    
    # only one of op hands dead
    for l in range(0,5):
        for j in range(1,5):
            for i in range(0, j+1):
                state = State(r=role, index=myindex, myl=i, myr=j, opl=-1, opr=l)
                states[state.name] = state
                myindex += 1
    
    # only one of my hands and only one of op hands dead
    for j in range(0,5):
        for l in range(0,5):
            if j == 0 and l == 0:
                continue
            state = State(r=role, index=myindex, myl=-1, myr=j, opl=-1, opr=l)
            states[state.name] = state
            myindex += 1
    
    # I lose
    for l in range(1,5):
        for k in range(-1,l+1):
            state = State(r=role, index=myindex, myl=-1, myr=-1, opl=k, opr=l)
            states[state.name] = state
            myindex += 1
    
    return states

def to_string(sth):
    string = ''
    if isinstance(sth, list):
        for x in sth:
            string += str(x)
    else:
        string = str(sth)
    return string

def remove_duplicate(mylist):
    unrepeat = []
    [unrepeat.append(x) for x in mylist if x not in unrepeat]
    return unrepeat  

def build_links(mystates, opstates):
    for key in mystates.keys():
        state = mystates[key]
        i,j,k,l = state.get_state()
        
        # both side both hands dead
        if (i == -1 and j == -1) or (k == -1 and l == -1):
            continue
        
        # both side one hand alive
        elif i == -1 and k == -1:
            new = (j+l)%5
            if j != 0 and new == 0:
                new = -1
            
            op_key = to_string([k,new,i,j])
            state.add_next(opstates[op_key])
            opstates[op_key].add_prev(state)
        
        # only my side one hand alive
        elif i == -1 and k != -1:
            if j == 0:
                op_key = to_string([k,l,i,j])
                state.add_next(opstates[op_key])
                opstates[op_key].add_prev(state)
            else:
                pairs = [[(j+k)%5, l], [(j+l)%5, k]]
                for x in range(len(pairs)):
                    if j != 0 and pairs[x][0] == 0:
                            pairs[x][0] = -1
                    elif pairs[x][0] > pairs[x][1]:
                        pairs[x][0], pairs[x][1] = pairs[x][1], pairs[x][0]
                unrepeat = remove_duplicate(pairs)
                for x, y in unrepeat:
                    op_key = to_string([x,y,i,j])
                    state.add_next(opstates[op_key])
                    opstates[op_key].add_prev(state)
        
        # my side both hands alive
        else:
            # add to op (two cases)
            # case1: op side one hand alive
            if k == -1:
                if i == 0:
                    new = [(j+l)%5]
                elif j == 0:
                    new = [(i+l)%5]
                else:
                    new = [(i+l)%5, (j+l)%5]
                for x in range(len(new)):
                    if new[x] == 0:
                        new[x] = -1
                unrepeat = remove_duplicate(new)
                for x in unrepeat:
                    op_key = to_string([k,x,i,j])
                    state.add_next(opstates[op_key])
                    opstates[op_key].add_prev(state)
            
            # case2: op side both hand alive
            else:
                if i == 0:
                    pairs = [[(j+k)%5, l], [(j+l)%5, k]]
                elif j == 0:
                    pairs = [[(i+k)%5, l], [(i+l)%5, k]]
                else:
                    pairs = [[(i+k)%5, l], [(j+k)%5, l], 
                             [(i+l)%5, k], [(j+l)%5, k]]
                for x in range(len(pairs)):
                    if pairs[x][0] == 0:
                            pairs[x][0] = -1
                    elif pairs[x][0] > pairs[x][1]:
                        pairs[x][0], pairs[x][1] = pairs[x][1], pairs[x][0]
                unrepeat = remove_duplicate(pairs)
                for x, y in unrepeat:
                    op_key = to_string([x,y,i,j])
                    state.add_next(opstates[op_key])
                    opstates[op_key].add_prev(state)

            # add to myself
            pairs = [[(i+j)%5, i], [(i+j)%5, j]]
            for x in range(len(pairs)):
                if pairs[x][0] > pairs[x][1]:
                    pairs[x][0], pairs[x][1] = pairs[x][1], pairs[x][0]
            unrepeat = remove_duplicate(pairs)
            for new1, new2 in unrepeat:
                op_key = to_string([k,l,new1,new2])
                state.add_next(opstates[op_key])
                opstates[op_key].add_prev(state)

            # rearrange
            sum = i + j
            pairs = []
            for x in range(int(sum/2)+1):
                pairs.append([x, (sum-x)%5])
            for x in range(len(pairs)):
                if pairs[x][0] > pairs[x][1]:
                    pairs[x][0], pairs[x][1] = pairs[x][1], pairs[x][0]
            unrepeat = remove_duplicate(pairs)
            for new1, new2 in pairs:
                if new1 == i and new2 == j:
                    continue
                elif new1 == 0 and new2 == 0:
                    continue
                op_key = to_string([k,l,new1,new2])
                state.add_next(opstates[op_key])
                opstates[op_key].add_prev(state)
        
def print_all_states_info(states_list, index_list=False, show_prev=False, show_next=False):
    if index_list:
        for idx in states_list:
            state = all_states_list[idx]
            state.info(show_prev=show_prev, show_next=show_next)
    else:
        for state in states_list:
            state.info(show_prev=show_prev, show_next=show_next)
            
def print_all_states(states_list, index_list=True, view='user', form='str'):
    for idx in states_list:
        state = all_states_list[idx]
        if state.role == view:
            state.print_state(view='me', form=form)
        else:
            state.print_state(view='op', form=form)


#Mitch Dec 03

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
def show(mode=0): #show all states, 0 = readable, 1 = plain txt, 2 = csv
  for x in range(len(states)):
    if mode==0: 
      print(" "*(3-len(str(x))), x, "   ", states[x][0], " ---", sep="", end="")
    elif mode==1:
      print(states[x][0], " ", sep="", end="")
    elif mode==2:
      print(states[x][0],sep="", end="")

    for y in range(1, len(states[x])):
      if mode==0 or mode==1:
        print(" ",states[x][y], sep="", end="")
      elif mode==2:
        print(",",states[x][y], sep="", end="")
    
    if mode==0 or mode==1:
      print()
    else:
      print("\\n")

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
  if state.isnumeric()==True:
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
  while state[-4:].isnumeric()==False:
    state=state[:-5]
  state=state[:-5]
  return state

#recursive computation  
def think(steps, forward): #create list of list for derived state from a path function result
  if forward>=2:
    for i in range(len(steps)):
      if steps[i][-4:].isnumeric()==True:
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
            if type(steps[j][1][0])==type([]) or steps[j][1][0][-4:].isnumeric() or steps[j][1][0][-4:]=="loop":
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
      if steps[i][-4:].isnumeric()==False:
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
  leaf=[[i[:len(state)+5],[0,0,0,0,0]] for i in path(state)]
  tree=think([foresee(x) for x in path(state)],forward)
  dive(tree, leaf)
  #draw(tree)
  #for i in range(len(leaf)):
    #print(leaf[i])
  #return leaf

#def decision(leaf):
  #must win
  for i in range(len(leaf)):
    if leaf[i][1][0]==leaf[i][1][1] and leaf[i][1][1]!=0:
      return leaf[i][0]

  #win & 0 lose
  a=[]
  for i in range(len(leaf)):
    if leaf[i][1][1]>leaf[i][1][2] and leaf[i][1][2]==0:
      if len(a)==0 or leaf[i][1][1]>a[1]:
        a=[i,leaf[i][1][1]]
  if len(a)>0:
    return leaf[a[0]][0]

  #more win than lose
  a=[]
  for i in range(len(leaf)):
    if leaf[i][1][1]>leaf[i][1][2]:
      if len(a)==0 or leaf[i][1][1]-leaf[i][1][2]>a[1]:
        a=[i,leaf[i][1][1]]
  if len(a)>0:
    return leaf[a[0]][0]

  #most loops only
  a=[]
  for i in range(len(leaf)):
    if leaf[i][1][1]==0 and leaf[i][1][2]==0 and leaf[i][1][3]>0:
      if len(a)==0 or leaf[i][1][3]>a[1]:
        a=[i,leaf[i][1][1]]
  if len(a)>0:
    return leaf[a[0]][0]

  #return random item from leaf
  a=[]
  b=[]
  import random
  for i in range(len(leaf)):
    if leaf[i][1][0]==0:
      b.append(i)
    else:
      a.append(i)
  if len(a)>0:
    return leaf[a[random.randrange(0,len(a))]][0]
  else:
    return leaf[b[random.randrange(0,len(b))]][0]
  
  #return "x"

#for i in range(len(states)):
  #l=decision(comp(states[i][0],5))
  #if l=="x": print(i)


### wrap() components

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
      if (y=="1" and not nz0) or (y=="2" and not nz1) or (y=="3" and not nz2 and not nz3) or (y not in ["0","1","2","3"]):
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

  options=[convert(path, argm(state)) for path in states[locate(convert(state, argm(state)))][1:]]
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
  print("You : ",state[2],"\t",state[3])
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
        game=comp(game,5) #did you forget to use turn for the computer to think?
    else:
      game=comp(game,5)
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
    print()
    play()
    while d not in [1,2]:
      d=int(input("\nWould you like to... \n<1> - start a new game \n<2> - quit? "))
      if d not in [1,2]: print("invalid input!\n")
      print()
