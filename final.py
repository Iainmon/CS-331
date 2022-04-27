
##
##  Bank class helpers
##

def diff_chicks(q1,q2):
    return int(abs(abs(q1.left.chicks - q2.left.chicks) + abs(q1.right.chicks - q2.right.chicks))/2)

def diff_wolves(q1,q2):
    return int(abs(abs(q1.left.wolves - q2.left.wolves) + abs(q1.right.wolves - q2.right.wolves))/2)

def action_rule(q1,q2):
    s = diff_chicks(q1,q2)
    t = diff_wolves(q1,q2)
    ret = int(s + (- t) + (((t**2)*((-8 * s) + (-13 * t) + 33))/4))
    return ret


##
##  Stores number of chicks, wolves, and True or False if the boat is at that bank
#     b_left = bank_from_david_domain((3,3,1))
##  check validity
#     b_left.valid
##  returns a boolean if t's a valid bank state. The State class won't let you construct a state where 
##  you have invalid bank stats

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
        return (self.chicks,self.wolves,int(self.boat))



##
##  Helpers for the state class
##

def antiport(boat):
    assert boat in ['L','R']
    if boat == 'L':
        return 'R'
    return 'L'

def animal_diffs():
    canon =  [(1,0),(2,0),(0,1),(1,1),(0,2)]
    # canon.reverse()
    return canon

##
##  State class, construct via   
#     s = state_from_david_domain((0,0,0),(3,3,1))
##  or if b_left and b_right are valid bank states, and the boat boolean isn't shared, then
#     State(b_left,b_right) is a valid state
##  get list of valid successor states
#     s.successors()
##  check if state is valid
#     s.valid -- true
##  get the rule index of the rule used to transition s1 to s2
#     action_rule(s1,s2) in {1,2,3,4,5}
##  map back to david domain via 
#     s.davidify() -- ((0,0,0),(3,3,1))

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
        # nexts.reverse()
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
    def davidify(self):
      return (self.left.davidify(),self.right.davidify())

def bank_from_david_domain(b):
  if type(b) is Bank:
    return b

  return Bank(b[0],b[1],bool(b[2]))

def state_from_david_domain(b1,b2 = None):
  if type(b1) is State:
    return b1 
  if b2 == None and type(b1) is tuple:
    b2 = b1[1]
    b1 = b1[0]
  return State(bank_from_david_domain(b1),bank_from_david_domain(b2))
  # else:
  #   return State(bank_from_david_domain(b[0][0]),bank_from_david_domain(b[0][1]))
def get_rule(q1,q2):
  return action_rule(state_from_david_domain(q1),state_from_david_domain(q2))

# q1 = ((3,3,1),(0,0,0))
# q2 = ((3,2,0),(0,1,1))

# print(q1)
# print(q2)

# print(state_from_david_domain(q1))
# print(state_from_david_domain(q2))

# print(get_rule(q1,q2))

# print(state_from_david_domain(q1).davidify())
# print(state_from_david_domain(q2).davidify())



def dfs_iain(s,g):
  s = state_from_david_domain(s)
  g = state_from_david_domain(g)
  
  stack=[(s,[s])]
  explored=set()
  n = 0

  while len(stack)>0:
    (v,p)=stack.pop()
    # _v=v[0:2]
    

    if v not in explored:
      if v == g: return (p,n,explored)

      n += 1
      explored.add(v)

      neighbors = [w for w in v.successors() if w not in explored] # expand(v,explored)
      # neighbors.reverse()
      
      for w in neighbors:
        stack.append((w,[w] + p))
  return []
def nth_dfs(s,g,depth):

  # s = state_from_david_domain(s)
  # g = state_from_david_domain(g)
  
  # explored=set()
  # n = 0
  # depth_map = dict()

  paths = dict()
  paths[s] = []
  expanded = set()
  levels = [[s]]
  for i in range(depth):
    frame = []
    for j in range(len(levels[i])):

      st = levels[i][j]
      expanded.add(st)

      for suc in st.successors():
        if suc in frame:
          continue
        paths[suc] = paths[st] + [st]
        frame.append(suc)


    levels.append(frame)
  # for i in range(len(levels)):
    # print('level:',i,'Size:',len(levels[i]),'   start:',s.davidify(),'   goal:',g.davidify())
  return (levels,expanded,paths)# levels[depth - 1]
  



def iddfs_iain(s,g):
  s = state_from_david_domain(s)
  g = state_from_david_domain(g)
  
  depth = 0
  while True:
    (levels,expanded,paths) = nth_dfs(s,g,depth)
    if g in expanded:
      path = paths[g]
      return (path,depth,expanded)
    depth += 1



def english(n):
  if n == 1: return 'Put one chicken in the boat'
  if n == 2: return 'Put two chickens in the boat'
  if n == 3: return 'Put one wolf in the boat'
  if n == 4: return 'Put one wolf and one chicken in the boat'
  if n == 5: return 'Put two wolves in the boat'
  raise Exception('Uh oh!')


# first param True if dfs, otherwise, second param True, third and fourth are states of the encoding ((0,0,0),(3,3,1))
def get_goal_traversal(do_dfs = None, do_iddfs = None, start = None, goal = None):
  if start == None or goal == None:
    raise Exception('Bro look at the function')

  ret_s = ''

  if do_dfs == True:
    (path,n,explored) = dfs_iain(start,goal)
    dp = [p.davidify() for p in path]
    action_hist = []
    for i in range(len(path)):
      if i >= len(dp) - 1:
        break
      s1 = path[i]
      s2 = path[i + 1]
      action = action_rule(s1,s2)

      ret_s += '\n' + english(action) + (', move to left bank.' if s2.boat == 'L' else ', move to right bank.')
    ret_s += '\n' + str(len(explored)) + ' nodes were expanded.'
    return ret_s

  ret_s = ''
  if do_iddfs == True:
    (path,n,explored) = iddfs_iain(start,goal)
    action_hist = []
    for i in range(len(path)):
      if i >= len(path) - 1:
        break
      s1 = path[i]
      s2 = path[i + 1]
      action = action_rule(s1,s2)
      action_hist.append(action)

      ret_s += '\n' + english(action) + (', move to left bank.' if s2.boat == 'L' else ', move to right bank.')

    ret_s += '\n' + str(len(explored)) + ' nodes were expanded.'
    return ret_s


  raise Exception('Bro arg 1 or 2 needs to be tru.')




q1 = ((0,0,0),(3,3,1))
q2 = ((3,3,1),(0,0,0))
get_goal_traversal(True,None,q1,q2)
get_goal_traversal(None,True,q1,q2)


q1 = ((0,0,0),(11,7,1))
q2 = ((11,7,1),(0,0,0))
get_goal_traversal(True,None,q1,q2)
get_goal_traversal(None,True,q1,q2)


# q1 = ((0,0,0),(100,97,1))
# q2 = ((100,97,1),(0,0,0))
# get_goal_traversal(True,None,q1,q2)
# get_goal_traversal(None,True,q1,q2)



