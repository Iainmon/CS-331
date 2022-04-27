

import sys
sys.setrecursionlimit(100000)


def diff_chicks(q1,q2):
    return int(abs(abs(q1.left.chicks - q2.left.chicks) + abs(q1.right.chicks - q2.right.chicks))/2)

def diff_wolves(q1,q2):
    return int(abs(abs(q1.left.wolves - q2.left.wolves) + abs(q1.right.wolves - q2.right.wolves))/2)

# def diff_chicks(q1,q2):
#     return abs((q1.left.chicks + q2.right.chicks) - (q2.left.chicks + q2.right.chicks))

# def diff_wolves(q1,q2):
#     return abs((q1.left.wolves + q1.right.wolves) - (q2.left.wolves + q2.right.wolves))

def action_rule(q1,q2):
    
    s = diff_chicks(q1,q2)
    t = diff_wolves(q1,q2)
    ret = int(s + (- t) + (((t**2)*((-8 * s) + (-13 * t) + 33))/4))
    # print(q1,q2,s,t,ret)
    return ret

class Bank:
    def __init__(self,chicks,wolves,boat):
        self.chicks = chicks 
        self.wolves = wolves
        self.boat = boat

    @property
    def valid(self):
        return ((self.chicks >= self.wolves) or self.chicks == 0) and self.chicks >= 0 and self.wolves >= 0
    
    def __str__(self):
        return f'[{self.chicks} | {self.wolves}]'
    def __repr__(self):
        return str(self)
    def __eq__(self,other):
        return self.chicks == other.chicks and self.wolves == other.wolves and self.boat == other.boat
    def davidify(self):
        return (self.chicks,self.wolves)

def antiport(boat):
    assert boat in ['L','R']
    if boat == 'L':
        return 'R'
    return 'L'

def animal_diffs():
    # res = []
    # for j in range(2 + 1):
    #     res += [(i,j) for i in range(2 + 1) if i + j >= 1 and i + j <= 2]
    # return res
    canon =  [(1,0),(2,0),(0,1),(1,1),(0,2)]
    # canon.reverse()
    return canon

class State:
    sucs = dict()
    def __init__(self,left_state,right_state):
        self.left = left_state
        self.right = right_state
        assert self.left.boat == (not self.right.boat)

    @property
    def boat(self):
        assert self.left.boat == (not self.right.boat)
        if self.left.boat:
            return 'L'
        return 'R'

    @property
    def valid(self):
        return self.left.valid and self.right.valid
    @property
    def chicks(self):
        return self.left.chicks + self.right.chicks
    @property
    def wolves(self):
        return self.left.wolves + self.right.wolves

    def successors(self):
        # if self in State.sucs.keys():
        #     return State.sucs[self]
        nexts = []
        new_boat = antiport(self.boat)
        for (diff_chicks,diff_wolves) in animal_diffs():
            if new_boat == 'R':
                diff_chicks *= -1
                diff_wolves *= -1

            new_left  = Bank(self.left.chicks  + diff_chicks, self.left.wolves  + diff_wolves, not self.left.boat)
            new_right = Bank(self.right.chicks - diff_chicks, self.right.wolves - diff_wolves, not self.right.boat)

            new = State(new_left,new_right)
            if new.valid:
                nexts += [new]
        nexts.reverse()
        # State.sucs[self] = nexts
        return nexts
    def __str__(self):
        if self.boat == 'L':
            return f'{self.left} <>    {self.right}'
        else:
            return f'{self.left}    <> {self.right}'
    def __repr__(self):
        return str(self)
    def __eq__(self,other):
        return self.left == other.left and self.right == other.right
    def __hash__(self):
        return hash(str(self))


# def dfs(start,goal,found):
#     # if start == goal:
#     #     return [start]
#     if start == goal:
#         print('Explored: ', len(found))
#         return [goal]
#     found.append(start)
#     new_found = []
#     for child in start.successors():
#         if child not in found:
#             if child == goal:
#                 return [start] + dfs(child,goal,found + new_found)
#             p = [start] + dfs(child,goal,found )
#             if p[-1] == goal:
#                 return p
#             new_found.append(child)

#     # for child in start.successors():
#     #     if child in found:
#     #         continue
        
#     #     p = [start]
#     #     q = p + dfs(child,goal,found)

#     #     if q[-1] == goal:
#     #         return q
#     #     else:
#     #         found.append(child)
#     #         q = p + dfs(child,goal,found)
#     #         if q[-1] == goal:
#     #             return q

#     # return []

#     # found = found + new_found
#     # for child in start.successors():
#     #     if child in new_found:
#     #         continue
#     #     p = dfs(child,goal,found)

#     #     if [] == p:
#     #         continue
#     #     if p[-1] == goal:
#     #         return [start] + p
        
#     #     found.append(child)
#     return []
#     #         if p[-1] == goal:
#     #             return p
#     # return 

#     # if start == goal:
#     #     return [goal]
#     # if start in found:
#     #     return 
#     # for child in start.successors():
#     #     if child in found:
#     #         continue
#     #     found_ 
#     #     return 
def concat(lss):
    ls = []
    for l in lss:
        ls += l
    return ls
def unions(ss):
    return set(concat([list(s) for s in ss]))

# def expand_s_(state,n):
#     if n == 0:
#         return set([state])
#     if n == 1:
#         return set(state.successors())
#     uns = set()
#     for s in state.successors():
#         for ss in expand(s,n-1):
#             uns.add(ss)
#     return uns


def expand_list(state,n):
    if n <= 0: return []
    if n == 1: return state.successors()
    states = []
    [states.append(s) for s in concat(expand_list(c,n-1) for c in state.successors()) if s not in states]
    return states

def expand(state,n):
    return set(expand_list(state,n))

def iddfs(start,goal):

    j = 0
    ret = []
    found = set()
    while ret == []:

        expanded = set()
        
        paths = dict()
        paths[start] = []

        for k in range(j):
            for state in set(expand_list(start,k)).union({start}):
                for s in state.successors():
                    paths[s] = [state] + paths[state]
                
        found = expand(start,j)
        for i in range(j):


            
            
            level = []

            for state in found:
                path = [state] + paths[state]
                for si in expand(state,j + 1 + i):
                    paths[si] = path
                    if si not in level:
                        level.append(si)
            print(j,i,len(level))
            # for s in list(found):
            #     if s in level:
            #         expanded.remove(s)
            #     found.remove(s)
            #     expanded.add(s)
            
            
            for s in level:
                if s in expanded:
                    expanded.remove(s)
                    found.add(s)

            for si in level:
                found.add(si)
                if si == goal and ret == []:
                    ret = [goal] + paths[goal]
                    
                

            if ret != []:
                print('----------')
                print('Path length:       ',len(paths[goal]))
                print('Path length:       ',len(ret))
                print('Accessed states:   ',len(found))
                print('Expanded states:   ',len(expanded))
                print('----------')
                break
        if ret != []:
            break
        # print('Depth:        ',i)
        # print('Old states:   ',len(found))


        j += 1

    return (ret,found)


def dfs(start,goal):
    paths = dict()
    paths[start] = []
    front = [start]
    explored = set()
    res_path = []
    while True:

        curr = front.pop()

        if curr not in explored:

            if curr == goal:
                # res_path = paths[curr]
                # explored.add(curr)
                break


            path = [curr] + paths[curr]


            # seen = set(paths.keys()) # explored.union(front)
            children = curr.successors()
            children.reverse()
            f = False
            a = None
            for child in children:
                if curr == child:
                    continue
 
                if child in explored:
                    continue
                if child == goal:
                    paths[goal] = [curr] + paths[curr]
                    f = True
                    a = goal
                paths[child] = [curr] + paths[curr]
                front.append(child)
            if f:
                front.append(a)
            explored.add(curr)




    print('Start:          ', start)
    print('Goal :          ', goal)
    print('Front:          ', len(front))
    print('Path length:    ', len(paths[goal]))
    print('Nodes explored: ', len(explored))
    print('Nodes explored: ', len(explored.union(front)))
    print('Nodes explored: ', len(explored.union(front)))
    print('Nodes explored: ', len(paths.keys()))

    return (res_path,explored)




start, goal = State(Bank(0,0,False),Bank(3,3,True)), State(Bank(3,3,True),Bank(0,0,False))
iddfs(start,goal)
# for i in range(len(t)):
#     if i == 0:
#         print(t[i])
#         continue
#     print(t[i],action_rule(t[i-1],t[i]))


start, goal = State(Bank(0,0,False),Bank(11,7,True)), State(Bank(11,7,True),Bank(0,0,False))
iddfs(start,goal)
start, goal = State(Bank(0,0,False),Bank(100,97,True)), State(Bank(100,97,True),Bank(0,0,False))
iddfs(start,goal)

# t = iddfs(start,goal)
# for i in range(len(t)):
#     if i == 0:
#         print(t[i])
#         continue
#     print(t[i],action_rule(t[i-1],t[i]))

assert False


left  = Bank(3,3,True)
right = Bank(0,0,False)
initial = State(left,right)
goal = State(right,left)
sucs = initial.successors()
# print(initial)
# print(sucs)

# start, goal = State(Bank(3,3,True),Bank(0,0,False)), State(Bank(3,2,False),Bank(0,1,True))
# t1 = find_bfs(start,goal)
# print('Start: ', start)
# print('Goal: ', goal)
# for t in t1:
#     print(t)

start, goal = State(Bank(0,0,False),Bank(3,3,True)), State(Bank(3,3,True),Bank(0,0,False))

(t,vs) = dfs(start,goal)


# print('Start: ', start)
# print('Goal: ', goal)
# for i in range(len(t)):
#     if i == 0:
#         print(t[i])
#         continue
#     print(t[i],action_rule(t[i-1],t[i]))
# print('Path length', len(t))
print('-----------------')
start, goal = State(Bank(0,0,False),Bank(11,7,True)), State(Bank(11,7,True),Bank(0,0,False))
visited = []

(t,vs) = dfs(start,goal)

# for i in range(len(t)):
#     if i == 0:
#         print(t[i])
#         continue
#     print(t[i],action_rule(t[i-1],t[i]))

# print('Start: ', start)
# print('Goal: ', goal)
# # for i in range(len(t)):
# #     if i == 0:
# #         print(t[i])
# #         continue
# #     print(t[i],action_rule(t[i-1],t[i]))
# print('Path length', len(t))
# print(t)
