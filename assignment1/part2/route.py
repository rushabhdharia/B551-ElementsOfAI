#!/bin/env/python3

#Set Of States S : The list of cities and towns, the highways that connect them, and the distance an individual covers while traveling through these routes
#Initial State : The city or town from which an individual has to reach the Goal State
#Successor Function : Checks if a particular node is visited or not. If not visited, the node which is the name of the city or town is appended to a list and the iterator moves forward. This continues until the iterator reaches the goal which is the city whose distance from the initial state needs to be found.
#Successor Function For DLS : Checks if the nodes in a particular level are visited or not. If not visited, that particular level is appended in the list and the iterator moves to the next level. This continues until the iterator reaches the level in which the goal node is present.
#Goal State G : The city or town and individual has to reach when traveling from the Initial State
#Cost Function : Sum of distances of all the cities or towns an individual needs to pass through in order to reach the Goal State, starting from the Initial State
#Heuristic Function : This function is only used in the A* search function. This function involves a heuristic for each of the three parameters namely, distance, time and segments. This function is the summation of the respective parameter and the haversine great circle distance between the start city and the end city.

#Time is (distance)/(speed). In order to underestimate the time, we need to overestimate the speed. Therefore, the average speed in the heuristic for time is assumed to be 100mph. If the speed is zero, then the average speed is assumed to be 50mph. If the speed is not mentioned then the average speed is assumed to be 40mph.
#We have considered Haversine distance equivalent to the number of segments. For instance, if the Haversine Distance is 3000, it means that the number of segments are 3000 with the cost of each segment being 1. 

#For any point A to B traveled on a map, the largest distance will be 4000 miles on Earth. This always underestimates the number of segments between any state and the goal state


import sys
from queue import PriorityQueue
from math import radians, cos, sin, asin, sqrt


# if speed = 0  speed = 50mph

def is_goal(node):
    if (node == end_city):
        return True
    return False


# ------------------------------------------------------------------------
# The below code is copied from
# https://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 3956  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


# --------------------------------------------------------------------------

def dist_ab(citya, cityb):
    count = 0
    #print(citya,cityb);
    for i in list_of_connections[citya]['neighbors']:
        if (cityb == i):
            return_val = int(list_of_connections[citya]['length'][count])
            return return_val
        count += 1


def time_ab(citya, cityb):
    count = 0
    for i in list_of_connections[citya]['neighbors']:
        if (cityb == i):
            dist = int(list_of_connections[citya]['length'][count])
            speed = int(list_of_connections[citya]['speed_limit'][count])
            if (speed == 0):
                speed = 50
            return_val = dist / speed
            return return_val
        count += 1


def successors_astar(node):
    list1 = []

    for i in list_of_connections[node]['neighbors']:
        list1.append(i);
        #if([node,i] not in parent):
        #parent.append([i, node])
        if is_goal(i):
            break;
    #print (list1);
    return list1

def dist_tillstart(s, start_city):
    counter = 1

    dist=0;
   # print s;
    #print parent;
    while(1):
        for i in parent:
            if(s==i[0]):
                #city found take its parent in pr
                pr=i[1];
                #calculate distance between its parents
                dist=dist+dist_ab(i[0],i[1]);
                s=i[1];
                break;
        if (i[1] == start_city):
            break;
    return dist;

def time_tillstart(s,start_city):
    counter = 1
    time3 = 0;
    while (1):


        for i in parent:
            if (s == i[0]):
                # city found take its parent in pr
                pr = i[1];
                time3=time3+time_ab(i[0],i[1]);
                s = i[1];
                break;
        if (i[1] == start_city):
            break;
    return time3;

def cost_tillstart(s,start_city):
    counter = 1
    cost = 0;
    while (1):

        for i in parent:
            if (s == i[0]):
                # city found take its parent in pr
                pr = i[1];
                #time3 = time3 + time_ab(i[0], i[1]);
                cost=cost+1;
                s = i[1];
                break;
        if (i[1] == start_city):
            break;
    return cost;


#def segments_tillstart(s,start_city):




def astar(start_city, end_city, list_of_connections):
    fringe = PriorityQueue()
    start_lat = list_of_cities[start_city]['lat']
    start_long = list_of_cities[start_city]['long']
    end_lat = list_of_cities[end_city]['lat']
    end_long = list_of_cities[end_city]['long']
    heu_of_start = haversine(start_long, start_lat, end_long, end_lat)
    fringe.put((heu_of_start,[start_city, heu_of_start, 0]))
    #visited.append([start_city, heu_of_start])
    visited.append(start_city);
    #parent.append([start_city, -1])
    while fringe.qsize()>0:
        temp=fringe.get();
        #print(temp[1])
        node=temp[1][0];

        check_heu=temp[1][1];
        #print(check_heu,node)
        for s in successors_astar(node):
            try:
                if(sys.argv[4]=='distance'):
                    lat1 = list_of_cities[s]['lat']
                    long1 = list_of_cities[s]['long']
                    if (s not in visited):
                        parent.append([s, node])
                        visited.append(s)
                        distab = dist_tillstart(s, start_city)
                        heu = haversine(long1, lat1, end_long, end_lat) + distab
                        #     #fringe.get(count)
                        fringe.put((heu, [s, heu, distab]))
                if(sys.argv[4]=='time'):
                    lat1 = list_of_cities[s]['lat']
                    long1 = list_of_cities[s]['long']
                    if (s not in visited):
                        parent.append([s, node])
                        visited.append(s)
                        timeab = time_tillstart(s, start_city)
                        heu = (haversine(long1, lat1, end_long, end_lat)/100) + timeab
                        fringe.put((heu, [s, heu, timeab]))
                if(sys.arg[4]=='segments'):
                    lat1 = list_of_cities[s]['lat']
                    long1 = list_of_cities[s]['long']
                    if (s not in visited):
                        parent.append([s, node])
                        visited.append(s)
                        costab = cost_tillstart(s, start_city)
                        heu = (haversine(long1, lat1, end_long, end_lat)/4000) + costab
                        fringe.put((heu, [s, heu, costab]))

            except:
                if (sys.argv[4] == 'distance'):
                    if (s not in visited):
                        parent.append([s, node])
                        visited.append(s)
                        distab = dist_ab(s,node);
                        heu = check_heu - distab
                        fringe.put((heu, [s, heu, distab]))
                if(sys.argv[4]=='time'):
                    if (s not in visited):
                        parent.append([s, node])
                        visited.append(s)
                        timeab = time_ab(s, node);
                        heu = check_heu - timeab
                        fringe.put((heu, [s, heu, timeab]))
                if(sys.argv[4]=='segments'):
                    if (s not in visited):
                        parent.append([s, node])
                        visited.append(s)
                        costab = 1;
                        heu = check_heu - costab
                        fringe.put((heu, [s, heu, costab]))


            if is_goal(s):
                #print ("reached");
                #print(dist_tillstart(s,start_city));
                return node

    return False

def successors(node):
    list1 = []
    for i in list_of_connections[node]['neighbors']:
        if i not in visited:
            parent.append([i, node])
            list1.append(i)
            if is_goal(i):
                break
    return list1


def successors_dls(node, level, dls_level, parent_dls, visited_dls):
    list1 = []
    for i in list_of_connections[node]['neighbors']:
        if i not in visited_dls:
            # print(dls_level)
            for j in dls_level:
                # print(node,j[0],j[1],level)
                if (node == j[0] and j[1] <= level):
                    break
            abc = int(j[1]) + 1
            if (abc == level + 1):
                return list1
            dls_level.append([i, abc])
            list1.append(i)
            parent_dls.append([i, node])
            if is_goal(i):
                print (list1)
                return list1

    return list1


def uniform():
    fringe = PriorityQueue()
    fringe.put((1, [start_city, 0]))
    while fringe.qsize() > 0:
        temp = fringe.get()[1]
        route = temp[0]
        cost = temp[1]
        visited.append(route)
        for s in successors(route):
            if (cost_function == 'distance'):
                path_cost = cost + dist_ab(s, route)
            elif (cost_function == 'time'):
                path_cost = cost + time_ab(s, route)
            elif (cost_function == 'segments'):
                path_cost = cost + 1
            if is_goal(s):
                return route
            fringe.put((path_cost, [s, path_cost]))
    return False


def bfs():
    fringe = [start_city]
    while len(fringe) > 0:
        route = fringe.pop(0)
        visited.append(route)
        for s in successors(route):
            if is_goal(s):
                return route
            fringe.append(s)
    return False


def dfs():
    fringe = [start_city]
    while len(fringe) > 0:
        route = fringe.pop()
        visited.append(route)
        for s in successors(route):
            if is_goal(s):
                return route
            fringe.append(s)
    return False


def dls(iteration):
    fringe = [start_city]
    dls_level = []
    visited_dls = []
    dls_level.append([start_city, 0])
    parent_dls = []
    parent_dls.append([start_city, -1])
    while len(fringe) > 0:
        route = fringe.pop()
        visited_dls.append(route)
        for s in successors_dls(route, iteration, dls_level, parent_dls, visited_dls):
            if is_goal(s):
                return route, parent_dls
            fringe.append(s)
    return False, []


def ids(start_city, end_city, list_of_connections):
    found = False
    iteration = 0
    parent_dls = []
    while (not found):
        result, parent_dls = dls(iteration)
        if result == False:
            iteration += 1
        else:
            found = True

    return parent_dls





file = open("city-gps.txt", "r")

list_of_cities = {}

for line in file:
    cnt = 1
    for word in line.split():
        if (cnt == 1):
            city = word
        elif (cnt == 2):
            latitude = float(word)
        elif (cnt == 3):
            longitude = float(word)
        cnt += 1

    list_of_cities[city] = {}
    list_of_cities[city]['lat'] = latitude
    list_of_cities[city]['long'] = longitude

file.close()

file = open("road-segments.txt", "r")
list_of_connections = {}

for line in file:
    cnt = 1
    for word in line.split():
        if (cnt == 1):
            city1 = word
        elif (cnt == 2):
            city2 = word
        elif (cnt == 3):
            length = word
        elif (cnt == 4):
            speed_limit = word
        elif (cnt == 5):
            name_of_highway = word
        cnt += 1
    if (city1 not in list_of_connections):
        list_of_connections[city1] = {}
    if (city2 not in list_of_connections):
        list_of_connections[city2] = {}
    if ('neighbors' not in list_of_connections[city1]):
        list_of_connections[city1]['neighbors'] = []
        list_of_connections[city1]['length'] = []
        list_of_connections[city1]['speed_limit'] = []
        list_of_connections[city1]['name_of_highway'] = []
    list_of_connections[city1]['neighbors'].append(city2)
    list_of_connections[city1]['length'].append(length)
    list_of_connections[city1]['speed_limit'].append(speed_limit)
    list_of_connections[city1]['name_of_highway'].append(name_of_highway)

    if ('neighbors' not in list_of_connections[city2]):
        list_of_connections[city2]['neighbors'] = []
        list_of_connections[city2]['length'] = []
        list_of_connections[city2]['speed_limit'] = []
        list_of_connections[city2]['name_of_highway'] = []

    list_of_connections[city2]['neighbors'].append(city1)
    list_of_connections[city2]['length'].append(length)
    list_of_connections[city2]['speed_limit'].append(speed_limit)
    list_of_connections[city2]['name_of_highway'].append(name_of_highway)

file.close()

start_city = sys.argv[1]
end_city = sys.argv[2]

visited = []
parent = []
parent.append([start_city, -1])

routing_algo = sys.argv[3]
cost_function = sys.argv[4]
ans_list = []

if (routing_algo == "bfs"):
    solution = bfs()
    if (cost_function == 'segments'):
        optimal = "yes"
    else:
        optimal = "no"
elif (routing_algo == "uniform"):
    solution = uniform()
    optimal = "yes"
elif (routing_algo == "dfs"):
    solution = dfs()
    optimal = "no"
elif (routing_algo == "ids"):
    parent = ids(start_city, end_city, list_of_connections)
    if (cost_function == 'segments'):
        optimal = "yes"
    else:
        optimal = "no"

elif (routing_algo == "astar"):
    astar(start_city, end_city, list_of_connections)
    optimal = "yes"

counter = 1;
while (1):
    for i, j in parent:
        if (end_city == i):
            counter = counter + 1;
            ans_list.append(i)
            end_city = j
        # print(i,j);
    if (start_city == end_city):
        break;

ans_list.append(start_city)
ans_list.reverse()

total_dist = 0
time = 0
for i in range(len(ans_list) - 1):
    city1 = ans_list[i]
    city2 = ans_list[i + 1]
    count = 0
    for j in list_of_connections[city1]['neighbors']:
        if city2 == j:
            try: 	
            	speed = int(list_of_connections[city1]['speed_limit'][count])
            except:
                temp = list_of_connections[city1]['speed_limit'][count]
                list_of_connections[city1]['speed_limit'][count] = 40
                speed = 40
                list_of_connections[city1]['name_of_highway'][count] = temp
            if (speed == 0):
                speed = 50
            dist = int(list_of_connections[city1]['length'][count])
            time += dist / speed
            total_dist += dist
        count += 1

print()
print("Travel Time = %.4f" % time, "hours")
print("Total miles to Travel =", total_dist)
print("Source =", start_city)
print("Destination =", end_city)
print()

for i in range(len(ans_list) - 1):
    city1 = ans_list[i]
    city2 = ans_list[i + 1]
    count = 0
    for j in list_of_connections[city1]['neighbors']:
        if city2 == j:
            highway_name = list_of_connections[city1]['name_of_highway'][count]
            length_of_highway = list_of_connections[city1]['length'][count]
            speed_limit_on_highway = list_of_connections[city1]['speed_limit'][count]
            break
        count += 1
    print("From ", ans_list[i], " take highway ", highway_name, " to reach to ", ans_list[i + 1])
    print("Speed Limit on ", highway_name, "is ", speed_limit_on_highway)

print()

print(optimal, end = " ")
print(total_dist, end = " ")
print("%.4f" % time, end = " ")

for i in ans_list:
    print(i, end = " ")

