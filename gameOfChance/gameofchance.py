#!/usr/bin/env python3
import sys

def calculate_ex1(die_to_reroll, die2, die3):
	expected_value = 0
	list_die = [1,2,3,4,5,6]
	if(die2 == die3):
		list_die.remove(die2)
		expected_value += 25/6 - (die2*3)/6
	for i in range(len(list_die)):
		expected_value += (list_die[i]+die2+die3)/6
	return expected_value

def calculate_ex2(die_to_reroll1, die_to_reroll2, die3):
	expected_value = 25/36 - (die3*3)/36 # expected value that both die are equal to the third die * 25
	expected_value += 21*2/6 + die3 
	return expected_value

def calculate_ex3():
	expected_value = 21*3/6 #https://www.quora.com/If-you-roll-a-die-n-times-what-is-the-expected-value-for-the-sum-of-the-faces
	expected_value += 25*6/216 # all 3 are same
	expected_value -= 21*3/216 # all 3 are same
	return expected_value

def main():
	#input
	die1 = int(sys.argv[1])
	die2 = int(sys.argv[2])
	die3 = int(sys.argv[3])

	# If all are same then it's the maximum expected value
	if(die1==die2 and die2==die3):
		none = 25
		print("Don't Reroll")
		sys.exit()
	
	#calculate all expected values
	none = die1+die2+die3
	a = calculate_ex1(die1, die2, die3)
	b = calculate_ex1(die2, die1, die3)
	c = calculate_ex1(die3, die1, die2)
	ab = calculate_ex2(die1, die2 ,die3)
	bc = calculate_ex2(die2, die3, die1)
	ac = calculate_ex2(die1, die3, die2)
	abc = calculate_ex3()

	#Printing all probabilities
	# print("a = ", a)
	# print("b = ", b)
	# print("c = ", c)
	# print("ab = ", ab)
	# print("bc = ", bc)
	# print("ac = ", ac)
	# print("abc = ", abc)
	
	max_ev = max(a,b,c,ab,bc,ac,abc)
	if (max_ev == a):
		print("Reroll the 1st Die")
	elif (max_ev == b):
		print("Reroll the 2nd Die")
	elif (max_ev == c):
		print("Reroll the 3rd Die")
	elif (max_ev == ab):
		print("Reroll the 1st and 2nd Dice")
	elif (max_ev == bc):
		print("Reroll the 2nd and 3rd Dice")
	elif (max_ev == ac):
		print("Reroll the 1st and 3rd Dice")
	elif (max_ev == abc):
		print("Reroll all the dice")
	
if __name__ == '__main__':
	main()
