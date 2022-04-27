


# def minmax_list(xs,mmf):
#     mmv,*ys = xs
#     for y in ys:
#         mmv = mmf(mmv,y)
#     return mmv

# def minimax_value(gs,max_node = True):
#     if gs.is_terminal(): return gs.utility()

#     recur = lambda gss: minimax_value(gss,not max_node)

#     succs = gs.successors()
#     minmax_children = list(map(recur,succs))

#     mmf = max if max_node else min
#     return minmax_list(minmax_children,mmf)



def print_grid(g):
    print(''.join('-' for _ in range(len(g[0])*5)))
    for row in g:
        print(row)
    # print(''.join('-' for _ in range(len(g[0])*5)))


def copy_grid(g):
    return [[g[y][x] for x in range(len(g[y]))] for y in range(len(g))]

def successors(grid,player_to_move,opponent):
    # grid = gs.to_grid()
    assert type(grid) is list
    # print('using:')
    # print_grid(grid)
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
                    elif tile == ' ':
                        if found_opponent:
                            found_valid_move = True
                            break
                        # break
                    
                    n_x += dx
                    n_y += dy
                    
                if found_valid_move:
                    new_grid = copy_grid(grid)
                    for (px,py) in path:
                        new_grid[py][px] = player_to_move
                    successor_grids.append(new_grid)
                    
                    # print('Positions: ',player_positions)
                    # print('Path: ',path)
                    # print_grid(new_grid)

    return successor_grids




g = [
    [' ',' ',' ',' '],
    [' ','X','O',' '],
    [' ','O','X',' '],
    [' ',' ',' ',' ']
    ]


# print('using:')
print_grid(g)
# for gs in successors(g,'X','O'):
#     print_grid(gs)
g2 = successors(g,'X','O')[0]
print_grid(g2)
# g3 = successors(g2,'O','X')
# print_grid(g3[0])
# print_grid(g3[1])

for gs in successors(g2,'O','X'):
    print_grid(gs)