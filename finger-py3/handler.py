from random import choice
def handle(user_choice):
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

    # generate dictionary and list of states for comp and user
    comp_states_dict = generate_states('comp', start_index=0)
    user_states_dict = generate_states('user', start_index=len(comp_states_dict))
    comp_states_list = list(comp_states_dict.values())
    user_states_list = list(user_states_dict.values())
    all_states_list = comp_states_list + user_states_list

    # connect all the states together
    build_links(comp_states_dict, user_states_dict)
    build_links(user_states_dict, comp_states_dict)

    # set score (score is mainly for user states)
    # 1. set for win step
    for state in user_states_list:
        if not state.next:
            state.score = 100
            state.win = True
        elif state.myleft == -1:
            state.score = 90
    #    elif state.myleft == 0 and state.myright == 1:
    #        state.score = 90
    for state in comp_states_list:
        for child in state.next:
            if child.score > 50:
                state.score = child.score
                break
        
    # 2. set for lose step (after setting win to avoid seemingly win state)
    for state in comp_states_list:
        if not state.next:
            state.score = 0
            state.lose = True
        elif state.myleft == -1:
            state.score = 10
    #    elif state.myleft == 0 and state.myright == 1:
    #        state.score = 10
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

    user_choice = convert_side(user_choice)
    current_state = comp_states_dict[user_choice]
    if current_state.lose:
        return "You win"
    
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
        print("You lose..")
    return current_state.get_state('str')
