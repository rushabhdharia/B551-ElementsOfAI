#!/usr/bin/env python3
'''

#Set Of States S : Every possible combination of students to form groups of 1, 2 or 3 students.
#Initial State : No student is assigned to a team yet
#Successor Function : Checks if the groups have 3 team members. If not, it checks whether there are any students who have not yet been assigned to a group and then appends a team member to the group. All this is done by the function "findPossibleTeamMembers()." The successor function then checks if the new group formed was already present in the list of groups or not. If not, it copies the group list to a temp variable and then it appends the new group to the list of groups. The group list is copied using a looping mechanism
#Successor Function For UCS : Checks if the groups have 3 team members. If not, it checks whether there are any students who have not yet been assigned to a group and then appends a team member to the group. All this is done by the function "findPossibleTeamMembers()." The successor function then checks if the new group formed was already present in the list of groups or not. If not, it copies the group list to a temp variable and then it appends the new group to the list of groups.
#Goal State G : Every student is assigned to a team and the course staff's work is minimized
#Cost Function : The amount of work the course staff needs to do in order to assign students to a team. A priority queue used as a fringe, the successor function is run and the time taken to run is calculated. The solve_uniform_cost_search() function takes the minimum time to run and is therefore the most optimal
#Heuristic Function : No heuristic function used

#If you want to run bfs, dfs, gradient descent then use successor function and change s[1] to s in the functions addNewGroup() and successors_ucs().
#The solve_search_all() function searches all the states and finds the best solution



We had problem generating list of successors for this part. So we adapted the functions addGrp, possibleTeamPermutation and the successor function from
https://github.com/BharathaAravind/Artificial-Intelligence-B551/blob/master/Assignment2/problem2/assign.py
Algorithms tried
1. Search all nodes - Optimal answer but slowest of all algorithms
2. Breadth First Search - Not Optimal
3. Depth First Search - Not Optimal
4. Gradient Descent - Not optimal but fastest of all algorithms
5. Uniform Cost Search - Optimal
Therefore Uniform Cost Search is the best algorithm for this problem.
'''
from queue import  PriorityQueue
import sys
import copy

#-----------------------------------------------------------------------------------------------------------------------------
# Code copied from https://github.com/BharathaAravind/Artificial-Intelligence-B551/blob/master/Assignment2/problem2/assign.py
#Add a new group to the given list
def addGrp(s):
	listOfGroups = copy.deepcopy(s[1]) # Reference = https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
	for student in listOfStudents:
		flag = 0
		for groups in listOfGroups:
			if student in groups:
				flag = 1
				break #if student is already present in any group then  don't consider that student as he/she can be only in one group
		if (flag==1):
			continue
		else:
			listOfGroups.append([student])
			break
	return listOfGroups

#Returns possible groups of 1,2 or 3 students
# Assuming grading the assignments take the highest time, we are trying to make more groups with three students
def possibleTeamPermutation(listOfGroups):
	possible_group = listOfGroups[len(listOfGroups)-1]
	list_of_assigned_students = []
	for group in listOfGroups:
		for student in group:
			list_of_assigned_students.append(student)

	#Adding one team member
	list_of_2 = []
	for student in listOfStudents:
		if student not in list_of_assigned_students:
			temp = [possible_group[0], student]
			if(sorted(temp) not in list_of_2):
				list_of_2.append(sorted(temp))

	#Adding a third teammate to the list of two groups
	list_of_3 = []
	for groups in list_of_2:
		for student in listOfStudents:
			if student not in list_of_assigned_students and student not in groups:
				temp = [groups[0],groups[1], student]
				if(sorted(temp) not in list_of_3):
					list_of_3.append(sorted(temp))

	for groups in list_of_2:
		listOfGroups.append(groups)

	for groups in list_of_3:
		listOfGroups.append(groups)

	return listOfGroups

# The successor function which adds a new group by calling addGrp
# Then adds all the possible groups to a list and returns it
def successors_ucs(s):
	successor_list = []
	listOfGroups = addGrp(s)
	possible_groups = possibleTeamPermutation(listOfGroups)
	for newgroups in possible_groups:
		temp = copy.deepcopy(s[1])
		if newgroups not in s:
			temp.append(newgroups)
			successor_list.append(temp)
	return successor_list

#-----------------------------------------------------------------------------------------------------------------------------

def totalTime(s):
	time_to_grade = k*len(s)
	time_incorrect_grp_size = 0
	time_person_requested = 0
	time_person_not_requested = 0
	totalTime = 0

	for group in s:
		for student in group:
			number_of_partners = group_pref[student]['num_of_partners']
			number_of_partners = int(number_of_partners)
			if((number_of_partners != len(group)) and (number_of_partners != 0) ):
				time_incorrect_grp_size += 1
			for person in group_pref[student]['partners']:
				if (person == '_'):
					break
				if person not in group:
					time_person_requested += 1
			for person in group_pref[student]['does_not_want']:
				if person in group:
					time_person_not_requested += 1

	total_time = time_to_grade + time_incorrect_grp_size + time_person_requested*m  + time_person_not_requested*n

	return total_time


def successors(s):
	successor_list = []
	listOfGroups = addGrp(s)
	possible_groups = possibleTeamPermutation(listOfGroups)
	for newgroups in possible_groups:
		tempGroup = [i.copy() for i in s]
		if newgroups not in s:
			tempGroup.append(newgroups)
			successor_list.append(tempGroup)
	return successor_list


def is_goal(s):
	assigned_students = []
	for groups in s:
		for student in groups:
			assigned_students.append(student)

	for student in listOfStudents:
		if student not in assigned_students:
			return False
	return True

#Uniform Cost Search
def solve_uniform_cost_search(s):
	fringe = PriorityQueue()
	fringe.put((1, s))
	while fringe.qsize() > 0:
		for s in successors_ucs(fringe.get()):
			s_time = totalTime(s)
			if is_goal(s):
				return s,s_time
			fringe.put((s_time, s))
	return False

#searches all states and finds the best solution
def solve_search_all(s):
	fringe = [s]
	probable_goal = []
	probable_goal_time = 1000000 #infinity
	while len(fringe) > 0:
		for s in successors(fringe.pop()):
			if is_goal(s):
				s_time = totalTime(s)
				if((probable_goal_time>s_time)):
					probable_goal = s
					probable_goal_time = s_time
			fringe.append(s)
	return probable_goal, probable_goal_time

#gradient descent
def solve_gradient_descent(s):
	fringe = [s]
	probable_goal = []
	probable_goal_time = 1000000 #infinity
	while len(fringe) > 0:
		for s in successors(fringe.pop()):
			if is_goal(s):
				s_time = totalTime(s)
				if((probable_goal_time>s_time)):
					probable_goal = s
					probable_goal_time = s_time
				else:
					return probable_goal, probable_goal_time
			fringe.append(s)
	return probable_goal, probable_goal_time

# Breadth First Search
def solve_bfs(s):
	fringe = [s]
	while len(fringe) > 0:
		for s in successors(fringe.pop(0)):
			if is_goal(s):
				s_time = totalTime(s)
				return s, s_time
			fringe.append(s)
	return False

#Depth First Search
def solve_dfs(s):
	fringe = [s]
	while len(fringe) > 0:
		for s in successors(fringe.pop()):
			if is_goal(s):
				s_time = totalTime(s)
				return s, s_time
			fringe.append(s)
	return False

filename = sys.argv[1]
k = int(sys.argv[2]) #number of mins to grade assignment
wrong_grp_size = 1  # taking 1 min of instructor's time as was assigned to a different group size
m = int(sys.argv[3]) #student assigned to someone they requested not to work with
n = int(sys.argv[4]) #not assigned to someone requested


file = open(filename, "r")
listOfStudents = []
group_pref = {}
for line in file:
	cnt = 1
	for word in line.split():
		if(cnt == 1):
			key = word
			listOfStudents.append(word)
		elif(cnt == 2):
			num_of_partners = word
		elif(cnt == 3):
			partners = word.split(',')
		else:
			does_not_want = word.split(',')
		cnt += 1
	group_pref[key] = {}
	group_pref[key]['num_of_partners'] = num_of_partners
	group_pref[key]['partners'] = partners
	group_pref[key]['does_not_want'] = does_not_want
file.close()

initial_groups = []
solution = solve_uniform_cost_search(initial_groups)

for group in solution[0]:
	str_grp = ' '.join(group)
	print(str_grp)

print(solution[1])
