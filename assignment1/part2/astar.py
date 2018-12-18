#!/bin/env/python3
import sys
from Queue import PriorityQueue
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
                        heu = haversine(long1, lat1, end_long, end_lat) + timeab
                        fringe.put((heu, [s, heu, timeab]))
                if(sys.arg[4]=='segments'):
                    lat1 = list_of_cities[s]['lat']
                    long1 = list_of_cities[s]['long']
                    if (s not in visited):
                        parent.append([s, node])
                        visited.append(s)
                        costab = cost_tillstart(s, start_city)
                        heu = haversine(long1, lat1, end_long, end_lat) + costab
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
print(start_city,end_city)
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
#    print(solution,visited);
    #sys.exit(1);

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
            speed = int(list_of_connections[city1]['speed_limit'][count])
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

print(optimal),
print(total_dist),
print("%.4f" % time),

for i in ans_list:
    print(i),

