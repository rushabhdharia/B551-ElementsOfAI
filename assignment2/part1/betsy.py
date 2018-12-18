#!/usr/bin/env python3
import copy
import sys
import time

max_player = ''
min_player = ''
n = ''
counter_max = 0
blockcol = []

def printable_board(board):
    print("\n".join([ " ".join([ str(board[row][col]) for col in range(0,len(board)-3)]) for row in range(0,len(board))]))

def boardstring(board):
    print(''.join(a for i in board for a in i))

def da_move_calculator(board, player):
    N = len(board)
    expanded = board+board
    width = N-3 
    #c = [[]]
    c = []
    for i in range(0, N):
        board2 = []
        for j in range(0, N-3):
            board2.append('.')
        c.append(board2)
    #c = [['.'] for i in range(N) for j in range(N-3)]
    
    player2 = 'x' if player == 'o' else 'o'
    first_player2 = ['.' for x in range(0,width)]
    last_player2 = ['.' for x in range(0,width)]
    
    first_empty = ['.' for x in range(0,width)]
    count_other = 0     
    
    for y in range(0,width):
        for x in range(2*N-1,N-1,-1):
            #print(x)
            
            if first_empty[y] == '.' and expanded[x][y] == '.' :   first_empty[y]=x-N
            if last_player2[y] == '.' and expanded[x][y] == player2 : last_player2[y] = x-N              
            if expanded[x][y] == player2 : 
                first_player2[y] = x-N                
                count_other +=1               
            if expanded[x][y] == '.': 
                c[x-N][y] ='.'
                continue
            
            past = x+1
            if past<2*N and c[past-N][y]!='.' and c[past-N][y]!= player2 and c[past-N][y]>1:
                c[x-N][y] = c[past-N][y]-1
                continue
            
            if expanded[x][y] == player: 
                c[x-N][y] =0
                continue
            count = 0
            for i in range(x-1,0,-1):
                
                if expanded[i][y] == player:
                    c[x-N][y] = x-i-count 
                    break
                if expanded[i][y] == '.':   count +=1
            #print(expanded[x][y],player2)    
            
            # when after all this we still dont have value it means there is no 
            # element of player, but if other is there, then handle
            if c[x-N][y]=='.' and expanded[x][y] == player2:
                #print("sxsx")
                c[x-N][y]=player2
    #print(first_player2)
    #print(last_player2)
    row_moves = []        
    for r in range(N-1,-1,-1):
        row_sum= 0
        for col in range(0,width):
            if c[r][col]=='.':
                row_sum += first_empty[col]-r+1
            elif c[r][col]==player2:
                row_sum += r-first_empty[col]+1 if first_empty[col] !='.' else 100000
            else:
                row_sum +=c[r][col]
        row_moves.append(row_sum)
    maindiagonal = [0,0]    
    for r in range(N-4,-1,-1):
        col =[N-r-4,r]
        for i in [0,1]:
            if c[r][col[i]]=='.':   maindiagonal[i] += abs(first_empty[col[i]]-r)+1
            elif c[r][col[i]] == player2:    
                maindiagonal[i] += r-first_empty[col[i]]+1 if first_empty[col[i]]!='.' else 100000
            else:   
                #print(c)
                maindiagonal[i] += c[r][col[i]]
    colmoves=[]
    for y in range(0,width):
        if(last_player2[y]=='.') :
            #print("sd\n",board)
            if first_empty[y] != '.': colmoves.append(first_empty[y] + 1)
            else : colmoves.append(0)
            continue
        if last_player2[y]-first_player2[y] >2:
            colmoves.append(100000) 
            continue
        if last_player2[y]-first_player2[y]<3 :
            #print(first_empty[y])
            #print(c)
            val = 0
            if first_empty[y] != '.' : val += first_empty[y] + 1
            if first_player2[y]< N-3 : val+= abs(first_player2[y]-(N-3))                 
            colmoves.append(val) 
            continue
    p_block = []
    for y in range(0,width):
        if colmoves[y]>10000:
            p_block.append(y)
    
    #print(colmoves)
    #print(maindiagonal)
    #print(row_moves)
    #printable_board(c)
    return (min(min(colmoves),min(maindiagonal), min(row_moves[3:])), count_other)
    
    #print(c)           
    """
def da_heuristic2(board):
    #print(player1)
    min_player1_move,p1_list = da_move_calculator(board,player1)
    player2 = 'x' if player1 == 'o' else 'o'
    min_player2_move,p2_list = da_move_calculator(board,player2)
    #print(player," moves needed : ",min_player1_move)
    #print(player2," moves needed : ",min_player2_move)
    #[blockcol.append(x) for x in p1_list if x in p2_list] 
    #print(min_player2_move-min_player1_move)
    #if min_player2_move==0: return -10000
    return min_player2_move-min_player1_move
    """
def da_heuristic2(move1,move2):
    return move2-move1
"""
Heuristic 3: (Main Heuristic)

move_caclulate: 
calculates : moves required for column and row and diagonal cases both for player 1(me) and player 2.
Then heuristic we first tried subtracting min moves required for player1, and then for player2, To know which is in favor and by how much

After this we tried putting weights on these values. high value on player1, makes final value to be more positive so it favours player1 more.
Thus that makes it to attack more.
Same for defense.
This weight we introduced to adapt to situations.
All this was possible because the move calculator does well in predicting the moves required for each. 
"""
def da_heuristic3(move1,move2,count1,count2):
    fullval = n*(n+3)/2
    rem1 = fullval- count1
    rem2 = fullval- count2
    if count1==0 or count2==0 or count1==count2:
        return (move2)-(move1)
    if rem2!=0: 
        ratio = rem1/rem2
        if ratio>1 and rem2!=0: return (ratio*move2)-(move1*1)
    return (1*move2)-(move1*1)

def da_heuristic4(move1,move2,count1,count2):
    fullval = n*(n+3)/2
    rem1 = fullval- count1
    rem2 = fullval- count2
    if count1==0 or count2==0 or count1==count2:
        return (move2)-(move1)
    if rem2!=0: 
        ratio = rem1/rem2
        if ratio>2 and rem2!=0: return (move1*1)
    return (1*move2)-(move1*1)    
"""
Heurisitic 1 early

nr_heuristic1():

-This heuristic function gives +1 to the max player and -1 to the min player.

-This heuristic function tries to break the sequence of the min player and then maximizing itself.

-Every row, column and diagonal in the board is calculated using this weighted values given to each row, column and diagonal

-For example-: Consider the board: (the maximizing player

X . .                         ->row1=+1

X . .                         ->row2=+1

O O .                      ->row3=-2

X X .                       ->row4=+2

O X .                       ->row5=0

X O .                       ->row6=0

 Col 1=2

Col 2=0

Col 3=0

Diag1=+1

Diag2=-1

Heuristic=row1+row2+row3+row4+row5+row6+col1+col2+col3+diag1+diag2=4

-The more positive heuristic favors more of the maximizing player which is X in this case.

-We ran a few test cases and the heuristic always favored the maximizing player, however the problem with this heuristic is that it does not show the most optimistic move so if the heuristic value is 3 and 4 and the move with heuristic 3 is more favorable the heuristic with 4, the alpha beta decision function will still take the heuristic with value 4 so it takes a longer path to win. Running the heuristic in the competition we always used to lose with people who handled the above case
"""
def nr_heuristic1(board):
    global n
    heuristic = 0
    main_counter = 1
    counter_row_x = 0
    counter_row_o = 0
    for x in board:
        if main_counter > n:
            break
        for y in range(len(x)):
            if x[y] == 'x':
                heuristic = heuristic + 1
                counter_row_x = counter_row_x + 1
            if x[y] == 'o':
                heuristic = heuristic - 1
                counter_row_o = counter_row_o + 1

        main_counter = main_counter + 1
        counter_row_x = 0
        counter_row_o = 0

    main_counter = 1
    counter_col_x = 0
    counter_col_o = 0
    for x in range(n):
        for y in range(n + 3):
            if main_counter > n:
                break
            if board[y][x] == 'x':
                heuristic = heuristic + 1
                counter_col_x = counter_col_x + 1
            if board[y][x] == 'o':
                heuristic = heuristic - 1
                counter_col_o = counter_col_o + 1
        main_counter = main_counter + 1
        counter_col_x = 0
        counter_col_o = 0

    main_counter = 0
    counter_diag1_x = 0
    counter_diag1_o = 0
    start = 0
    for y in range(n + 1):
        for x in range(n):
            if board[start][x] == 'x':
                heuristic = heuristic + 1
                counter_diag1_x = counter_diag1_x + 1
            if board[start][x] == 'o':
                heuristic = heuristic - 1
                counter_diag1_o = counter_diag1_o + 1
            start = start + 1
        break
        main_counter = main_counter + 1
        start = start - (n - 1)
        counter_diag1_x = 0
        counter_diag1_o = 0

    # for diagonal left to right -- down to up
    main_counter = 0
    start = n - 1
    counter_diag2_x = 0
    counter_diag2_o = 0
    for y in range(n + 1):
        for x in range(n):
            if board[start][x] == 'x':
                heuristic = heuristic + 1
                counter_diag2_x = counter_diag2_x + 1

            if board[start][x] == '0':
                heuristic = heuristic - 1
                counter_diag2_o = counter_diag2_o + 1

            start = start - 1
        break
        main_counter = main_counter + 1
        start = n + y
        counter_diag2_x = 0
        counter_diag2_o = 0

    # print heuristic
    return heuristic


def drop(col, current_player, board1):
    global counter_max
    counter_max+=1
    current_board = copy.deepcopy(board1)
    select = -1
    for i in range(len(current_board)):
        if i == 0 and current_board[i][col] != '.':
            break  # cannot add a pebble here
        if current_board[i][col] == '.':
            select = i
    if select != -1:
        current_board[select][col] = current_player
    return current_board


def rotate(col, board1):
    board = copy.deepcopy(board1)
    no_of_row = len(board1)
    temp = board[no_of_row - 1][col]
    for i in range(no_of_row - 1, 0, -1):
        board[i][col] = board[i - 1][col]

    board[0][col] = '.'
    board = drop(col, temp, board)
    return board


def successors(board, current_player):
    global n
    global counter_max
    total = (n + (n+3))/2
    list1 = []
    for i in range(n):
        #if i not in blockcol:   list1.append(rotate(i, board))
        if board[0][i]=='.' :#and counter_max < total:
            list1.append(drop(i, current_player, board))
        if board[n+2][i]!='.':   list1.append(rotate(i, board))
        
        #list1.append(rotate(i, board))
    return list1


def terminal(s, depth):
    if depth == 0:
        return 1
    return 0


def min_value(s, alpha, beta, depth):
    global min_player
    depth -= 1
    mv1,count2 = da_move_calculator(s,player1) 
    player2 = 'x' if player1 == 'o' else 'o'
    mv2,count1 = da_move_calculator(s,player2)
    if(mv1==0): return 10000
    if(mv2==0): return -10000  
    if terminal(s, depth):
        #print("terminal depth min fn")
        return da_heuristic4(mv1,mv2,count1,count2)
    for s2 in successors(s, min_player):
        val = max_value(s2, alpha, beta, depth)
        #print("beta: ",beta," max val: ", val)
        beta = min(beta, val)
        if alpha >= beta:
            return beta
    return beta


def max_value(s, alpha, beta, depth):
    global max_player
    depth -= 1
    mv1,count2 = da_move_calculator(s,player1) 
    player2 = 'x' if player1 == 'o' else 'o'
    mv2,count1 = da_move_calculator(s,player2)
    if(mv1==0): return 10000
    if(mv2==0): return -10000
    if terminal(s, depth):
        #print("terminal depth max fn depth")
        #printable_board(s)
        #print(da_heuristic2(s))
        
    #    return da_heuristic2(s)
        return da_heuristic4(mv1,mv2,count1,count2)
    for s2 in successors(s, max_player):
        val = min_value(s2, alpha, beta, depth)
        #print("alpha: ",alpha," min val: ", val)
        alpha = max(alpha, val)
        
        if alpha >= beta:
            return alpha
    return alpha


def successors2(main_succ, board):
    global n
    global max_player
    for i in range(n):
        temp = rotate(i, board)
        if temp == main_succ:
            decision = i+1
            return -decision
        temp = drop(i, max_player, board)
        if temp == main_succ:
            decision = i+1
            return decision


def alpha_beta_decision(initial_board, depth):
    global max_player
    alpha = -1000000
    for s in successors(initial_board, max_player):
            a = min_value(s, alpha, 1000000, depth)
            if alpha < a:
                alpha = a
                main_suc = s
    decision = successors2(main_suc, initial_board)
    return main_suc, decision


def main():
    global n
    global max_player
    global min_player
    global player1
    
    start = time.time()
    n = int(sys.argv[1])
    max_player = sys.argv[2]
    player1 = sys.argv[2]
    if max_player == 'x':
        min_player = 'o'
    else:
        min_player = 'x'
    state_of_board = sys.argv[3]
    time_limit = int(sys.argv[4])
        
    initial_board = []
    for i in range(0, len(state_of_board), n):
        board = []
        for j in range(0, n):
            board.append(state_of_board[i + j])
        initial_board.append(board)
        
    #printable_board(initial_board)
    #val = da_move_calculator(initial_board, player1)
    
    #da_heuristic2(initial_board)
    #print(da_move_calculator(initial_board,max_player))
    #print(da_move_calculator(initial_board,min_player))
    depth = 2
    
    while True:
        mainsuc, decision = alpha_beta_decision(initial_board, depth)
        
        str = ''
    
        for i in mainsuc:
            for j in i:
                str += j
        print(decision, " ", str)
        depth += 1
        if time.time() > start + time_limit:
            break
    
    #print(da_move_calculator(mainsuc,max_player))
    #print(da_move_calculator(mainsuc,min_player))
    #print()
    #printable_board(mainsuc)
    """
    if decision < 0:
        print("I'd recommend rotating column ", abs(decision))
    else:
        print("I'd recommend dropping a pebble in column ", decision)
    """
    
    
    return


if __name__ == '__main__':
    main()
