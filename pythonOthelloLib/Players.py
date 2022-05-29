'''
    Erich Kramer - April 2017
    Apache License
    If using this code please cite creator.

'''

# from Board import Board
from OthelloBoard import OthelloBoard

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    #PYTHON: use obj.symbol instead
    def get_symbol(self):
        return self.symbol
    
    #parent get_move should not be called
    def get_move(self, board):
        raise NotImplementedError()



class HumanPlayer(Player):
    def __init__(self, symbol):
        Player.__init__(self, symbol);

    def clone(self):
        return HumanPlayer(self.symbol)
        
#PYTHON: return tuple instead of change reference as in C++
    def get_move(self, board):
        col = int(input("Enter col:"))
        row = int(input("Enter row:"))
        return  (col, row)



def copy_grid(g):
    return [[g[y][x] for x in range(len(g[y]))] for y in range(len(g))]

# accepts a grid of 'X','O','.' characters, 
#   a player to move symbol, and an opponent symbol,
#   and returns a list of move position, coresponding gamestate pairs.
def successors(grid,player_to_move,opponent):
    assert type(grid) is list

    grid = copy_grid(grid)

    player_positions = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == player_to_move:
                player_positions.append((j,i))

    x_bound,y_bound = len(grid[0]),len(grid)

    successor_grids = []
    for (x,y) in player_positions:

        for dx in [1,0,-1]:
            for dy in [0,-1,1]:
                if dx == 0 and dy == 0: continue

                n_x = x
                n_y = y 
                path = []
                found_opponent = False
                found_valid_move = False
                while n_x >= 0 and n_x < x_bound and n_y >= 0 and n_y < y_bound:
                    
                    path.append((n_x,n_y))

                    tile = grid[n_y][n_x]

                    if tile == opponent:
                        found_opponent = True
                    elif tile == player_to_move:
                        found_opponent = False
                    elif tile == '.':
                        if found_opponent:
                            found_valid_move = True
                            break
                    
                    n_x += dx
                    n_y += dy
                    
                if found_valid_move:
                    new_grid = copy_grid(grid)
                    for (px,py) in path:
                        new_grid[py][px] = player_to_move
                    successor_grids.append((path[-1],new_grid))
                    
    return successor_grids


def minmax_list(xs,mmf):
    mmv,*ys = xs
    for y in ys:
        mmv = mmf(mmv,y)
    return mmv



def gridify(board):
    return copy_grid(board.grid)




class MinimaxPlayer(Player):

    def __init__(self, symbol):
        Player.__init__(self, symbol);
        if symbol == 'X':
            self.oppSym = 'O'
        else:
            self.oppSym = 'X'
    def reconstruct(self,gs):
        rows = len(gs)
        cols = len(gs[0])
        board = OthelloBoard(cols,rows,self.get_symbol(),self.oppSym)
        for i in range(rows):
            for j in range(cols):
                if gs[i][j] == '.': continue
                board.set_cell(j,i,gs[i][j])
        return board

    def minimax_value(self,gs,player_to_move,oppposing_player,max_node = True):
        snd = lambda t: t[1]
        succs = list(map(snd,successors(gs,player_to_move,oppposing_player)))
        if succs == []:
            board = self.reconstruct(gs)
            return self.utility(board)

        recur = lambda gss: self.minimax_value(gss,oppposing_player,player_to_move,not max_node)

        minmax_children = list(map(recur,succs))

        mmf = max if max_node else min
        return minmax_list(minmax_children,mmf)


    def utility(self,board):
        return board.count_score(self.get_symbol())

    def get_move(self,board):
        best = None
        best_score = -1
        for ((row,col),gs) in successors(gridify(board),self.get_symbol(),self.oppSym):
            score = self.minimax_value(gs,self.get_symbol(),self.oppSym)
            if score > best_score:
                best = (col,row)
        assert best != None
        return best
g = [
    ['.','.','.','.'],
    ['.','X','O','.'],
    ['.','O','X','.'],
    ['.','.','.','.']
    ]

# p = MinimaxPlayer('X')
# board = p.reconstruct(g)
# board.display()
# print(p.get_move(board))



