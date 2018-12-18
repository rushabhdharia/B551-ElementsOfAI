#!/usr/bin/env python3
# a0.py : Solve the N-Rooks/N-Queens/N-Knights problem!
#
# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.
#
# The N-queens problem is: Given an empty NxN chessboard, place N queens on the board so that no queens
# can take any other, i.e. such that no two queens share the same row, column or diagonal
#
# The N-Knights problem is: Given an empty NxN chessboard, place N knights on the board so that no knight 
# can take any other.
#
# Note: Some of the code has been referred from the code provided in nrooks-2.py

import sys

# Check if knight doesn't attack the knights placed already
def knight_restricted(board, row, col):
	for i in range(0,N):
		for j in range(0,N):
			if(board[i][j]==1):
				if(row==i-2):
					if(col==j-1 or col==j+1):
						return 1
				if(row==i-1):
					if(col==j-2 or col==j+2):
						return 1
				if(row==i+1):
					if(col==j-2 or col==j+2):
						return 1
				if(row==i+2):
					if(col==j-1 or col==j+1):
						return 1		
	return 0

# Count # of pieces in given row
def count_on_row(board, row):
	sum = 0
	for i in range(N):
		if not (board[row][i]=='X'):
			sum += board[row][i]
	return sum

#checks if there is a piece already present on the diagonal
def check_diagonal(board, row, col):
	for i in range(N):
		for j in range(N):
			if(board[i][j]==1):
				if (abs(i-row) == abs(j-col)):
					return 0
	return 1

# Count # of pieces in given column
def count_on_col(board, col):
	sum = 0
	for i in range(N):
		if not (board[i][col]=='X'):
			sum += board[i][col]
	return sum

# Count total # of pieces on board
def count_pieces(board):
	sum = 0
	for i in range(N):
		for j in range(N):
			if not (board[i][j]=='X'):
				sum += board[i][j]
	return sum

# Return a string with the board rendered in a human-friendly format
def printable_board(board):
	str = ""
	for row in board:
		for col in row:
			if col == 'X': 
				str += 'X '
			elif col:   
				if (problem == "nrook"):
					str += "R "
				elif(problem=="nqueen"):
					str += "Q "
				elif(problem=="nknight"):
					str += "K "
			else:
				str += "_ "
		str += "\n"	
	return str

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
	return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors_nknight(board):
	list1 = []
	c = count_pieces(board)
	for r in range(0, N):
		if(c<N):
			if not (board[r][c]=='X'):
				if not(knight_restricted(board,r,c)):
					list1.append(add_piece(board, r, c))
	return list1


def successors_nqueen(board):
	list1 = []
	c = count_pieces(board)
	for r in range(0, N):
		if(c<N):
			if not (count_on_row(board,r)): #if there is already a queen present in the row then skip this row
					if (check_diagonal(board,r,c)):
						if not (board[r][c]=='X'):
							list1.append(add_piece(board, r, c))
	return list1

def successors_nrook(board):
	list1 = []
	c = count_pieces(board)
	for r in range(0, N):
		if(c<N):
			if not (count_on_row(board,r)):
				if not (board[r][c]=='X'):
					list1.append(add_piece(board, r, c))
	return list1

# check if board is a goal state
def is_goal(board):
	return count_pieces(board) == N and \
		all( [ count_on_row(board, r) <= 1 for r in range(0, N) ] ) and \
		all( [ count_on_col(board, c) <= 1 for c in range(0, N) ] )

def is_goal_nknight(board):
	if (count_pieces(board)==N):						
		return 1

# Solve n-rooks!
def solve_nrook(initial_board):
	fringe = [initial_board]
	while len(fringe) > 0:
		for s in successors_nrook( fringe.pop() ): 												
			printable_board(s)
			if is_goal(s):
				return(s)
			fringe.append(s)
	return False

# Solve n-queens!
def solve_nqueen(initial_board):
	fringe = [initial_board]
	while len(fringe) > 0:
		for s in successors_nqueen( fringe.pop() ): 
			printable_board(s)
			if is_goal(s):
				return(s)
			fringe.append(s)
	return False

# Solve n-knights!
def solve_nknight(initial_board):
	fringe = [initial_board]
	while len(fringe) > 0:
		for s in successors_nknight( fringe.pop() ):
			printable_board(s)
			if is_goal_nknight(s):
				return(s)
			fringe.append(s)
	return False

problem = sys.argv[1] # nrook/nqueen/nknight problem
N = int(sys.argv[2]) # This is N, the size of the board. It is passed through command line arguments.
unavial_pos = int(sys.argv[3]) #Used to store the number of unavailable positions on the chessboard

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0 for i in range(N)] for i in range(N)] #https://stackoverflow.com/questions/2739552/2d-list-has-weird-behavor-when-trying-to-modify-a-single-value

# to add the unavialable positions on the initial board
for x in range(0, 2*unavial_pos, 2):
	a = int(sys.argv[x+4])
	b = int(sys.argv[x+5])
	initial_board[a-1][b-1]= 'X'

print ("Starting from initial board:\n" + printable_board(initial_board) + "\n\nLooking for solution...\n")

if(problem=="nrook"):
	solution = solve_nrook(initial_board)
	
elif(problem=="nqueen"):
	solution = solve_nqueen(initial_board)

elif(problem=="nknight"):
	solution = solve_nknight(initial_board)

print (printable_board(solution) if solution else "Sorry, no solution found. :(")