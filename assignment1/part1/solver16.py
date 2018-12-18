#!/bin/python


#Set Of States S : Any arrangement of the numbers 1 to 16 in a 4x4 game board
#Initial State : A 4x4 game board in which numbers 1 to 16 are arranged in the configuration [5,7,8,1][10,2,4,3][6,9,11,12][15,13,14,16] 
#Successor Function : Shifting a specififed row on the board either left or right, or shifting a specified column on the board either up or down
#Goal State G : A 4x4 game board in which numbers 1 to 16 are arranged in the configuration [1,2,3,4][5,6,7,8][9,10,11,12][13,14,15,16] 
#Cost Function : Number of moves taken by the Initial State to obtain a configuration identical to the Goal State
#Heuristic Function : Calculates the distance moved up or down by each number in a column, or the distance moved left or right by each number in a row. This distance is then added to the cost and then the sum is returned.



# solver16.py : Circular 16 Puzzle solver
# Based on skeleton code by D. Crandall, September 2018
#
from Queue import PriorityQueue
from random import randrange, sample
import sys
import string


def index_2d(myList, v, root):
    if(root==0):
        for i, x in enumerate(myList):
            if v in x:
                return (i, x.index(v));
    if(root==1):
        for i, x in enumerate(myList):
            if v in x:
                return i;
    if(root==2):
        for i, x in enumerate(myList):
            if v in x:
                return i;

def bfs(graph, start, end):
    # maintain a queue of paths
    queue = []
    # push the first path into the queue
    queue.append([start])
    while queue:
        # get the first path from the queue
        path = queue.pop(0)
        # get the last node from the path
        node = path[-1]
        # path found
        if node == end:
            return path
        # enumerate all adjacent nodes, construct a new path and push it into the queue
        for adjacent in graph.get(node, []):
            new_path = list(path)
            new_path.append(adjacent)
            queue.append(new_path)


def calculate_heuristic_for_distance(input_matrix,init_matrix,cost):
    graph = {
        '00': ['03', '30', '01', '10'],
        '01': ['00', '02', '11', '31'],
        '02': ['01', '03', '12', '32'],
        '03': ['00', '33', '02', '13'],
        '10': ['00', '20', '11', '13'],
        '11': ['01', '12', '21', '10'],
        '12': ['02', '13', '22', '11'],
        '13': ['03', '12', '23', '10'],
        '20': ['10', '30', '21', '23'],
        '21': ['11', '22', '31', '20'],
        '22': ['12', '23', '32', '21'],
        '23': ['22', '13', '33', '20'],
        '30': ['00', '33', '31', '20'],
        '31': ['30', '32', '21', '01'],
        '32': ['31', '33', '22', '02'],
        '33': ['32', '23', '03', '30'],

    }

    distance=0;
    heuristic=0;
    for row in range(4):
        for column in range(4):
            if(input_matrix[row][column]!=init_matrix[row][column]):
                row1=row;
                col1=column;

                row2,col2=index_2d(init_matrix,input_matrix[row][column],0);
                str1=str(row1)+str(col1);
                str2=str(row2)+str(col2);
                list_returned=[];
                list_returned=bfs(graph,str1,str2);
                heuristic=len(list_returned)-1;
                distance=distance+heuristic;
    return distance+cost;


# shift a specified row left (1) or right (-1)
def shift_row(state, row, dir):
    change_row = state[(row * 4):(row * 4 + 4)]
    return (state[:(row * 4)] + change_row[-dir:] + change_row[:-dir] + state[(row * 4 + 4):],
            ("L" if dir == -1 else "R") + str(row + 1))


# shift a specified col up (1) or down (-1)
def shift_col(state, col, dir):
    change_col = state[col::4]
    s = list(state)
    s[col::4] = change_col[-dir:] + change_col[:-dir]
    return (tuple(s), ("U" if dir == -1 else "D") + str(col + 1))


# pretty-print board state
def print_board(row):
    for j in range(0, 16, 4):
        print '%3d %3d %3d %3d' % (row[j:(j + 4)])


# return a list of possible successor states
def successors(state):
    return [shift_row(state, i, d) for i in range(0, 4) for d in (1, -1)] + [shift_col(state, i, d) for i in range(0, 4)
                                                                             for d in (1, -1)]


# just reverse the direction of a move name, i.e. U3 -> D3
def reverse_move(state):
    return state.translate(string.maketrans("UDLR", "DURL"))


# check if we've reached the goal
def is_goal(state):
    return sorted(state) == list(state)


# The solver! - using BFS right now
def solve(initial_board,init_matrix):
    fringe=PriorityQueue;
    n = 4;
    counter = 0;
    input_matrix = [[0] * n for i in range(n)];
    for x in range(n):
        for y in range(n):
            input_matrix[x][y] = initial_board[counter];
            counter = counter + 1;

    fringe=PriorityQueue();
    priority=calculate_heuristic_for_distance(input_matrix,init_matrix,0)
    fringe.put((priority,[initial_board, "",0]));
    #print("her2")
    #print(fringe.qsize())
    #fringe = [(initial_board, "")]
    while fringe.qsize() > 0:

        temp=[];
        temp=fringe.get();
        state=temp[1][0];
        route_so_far=temp[1][1];
        cost_of_parent=temp[1][2];
        visited.append(state);
        for (succ, move) in successors(state):
            if(succ in visited):
                if is_goal(succ):
                    return (route_so_far + " " + move)
            else:
                n = 4;
                counter = 0;
                input_matrix = [[0] * n for i in range(n)];
                for x in range(n):
                    for y in range(n):
                        input_matrix[x][y] = succ[counter];
                        counter = counter + 1;
                if is_goal(succ):
                    return (route_so_far + " " + move)

                xx = calculate_heuristic_for_distance(input_matrix, init_matrix, cost_of_parent + 4);
                fringe.put((xx, [succ, route_so_far + " " + move, cost_of_parent + 4]));
    return False


# test cases
start_state = []
visited=[];
with open(sys.argv[1], 'r') as file:
    for line in file:
        start_state += [int(i) for i in line.split()]

if len(start_state) != 16:
    print "Error: couldn't parse start state file"

print "Start state: "
print_board(tuple(start_state))

counter=1;
n=4;
init_matrix=[[0] * n for i in range(n)];
for row in range(n):
    #init_matrix.append([]);
    for column in range(n):
        init_matrix[row][column]=counter;
        counter=counter+1;

print "Solving..."
route = solve(tuple(start_state),init_matrix)

print "Solution found in " + str(len(route) / 3) + " moves:" + "\n" + route
