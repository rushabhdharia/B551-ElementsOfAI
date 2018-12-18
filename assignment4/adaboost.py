#!/usr/bin/env python3
import sys
import time
import numpy as np
import math
from collections import defaultdict, Counter
import random
import json

def read_data(fname):
    file = open(fname, 'r');
    data = [x.strip().split() for x in file.readlines()]
    ##splitting the id and the data into  two different parts as we dont need the image name just storing it
    id = [x[0] for x in data]
    dataset = [x[1:] for x in data]
    return id,dataset

def training_adaboost(data,iterations):
    ignore, N, permutations, h, weight=0,len(data),[], [], []
    for i in range(iterations): permutations.append((random.randint(1, 192),random.randint(1, 192))) ##we generate random pairs to compare with, the number of random pairs are equal to the number of iterations we run
    W = [1.0/float(N) for i in range(N)] ##initalizingthe weight vector to 0
    for k in range(0,iterations):
        indice, correct, wrong = permutations[k], defaultdict(int), defaultdict(int)
        for x in data:
            if (x[indice[0]] >= x[indice[1]]):correct[x[0]] += 1
            else:wrong[x[0]] += 1
        #https://stackoverflow.com/questions/6987285/python-find-the-item-with-maximum-occurrences-in-a-list
        if len(correct)==0: pred=min(wrong,key=wrong.get), max(wrong,key=wrong.get)
        elif len(wrong)==0: pred=max(correct, key=correct.get), min(correct, key=correct.get)
        else: pred=max(correct,key=correct.get), max(wrong,key=wrong.get)
        h.append(pred)
        error, predictions = 0, []
        for i in range(N):
            predictions.append(pred[0] if data[i][indice[0]] >= data[i][indice[1]] else pred[1])
            if (predictions[i] != data[i][0]):error = error + W[i]
        if (error >= 1):ignore+=1 ##ignoring error greater than 1 super rare case python was throwing error here
        else:
            for i in range(N):
                if (predictions[i] == data[i][0]):W[i] = W[i] * (error/(1 - error ))
            temp=float(sum(W))
            W = [float(w)/temp for w in W] ## here we are normalizing the W vector by dividing it with len(W)
            weight.append(math.log((1 - error )/error)) ## appending the error in weight list
    return h, weight, permutations,ignore

def testing_adaboost(data,h,w,i,ignore,iterations,results,temp_list,temp_list2,temp_list3,temp_list4):
    ##we initialize two list of the classifiers the real ones and the inverted ones which works the same
    for x in temp_list:
        ans, iterr = defaultdict(int), iterations-ignore[x] ## this is to run the loop till the length iterr if some weights are ignored in the training and the count of that has been kept in the model file
        for y in range (iterr):
            ##for the testing data we check the pixel values by using the same indices we used in training and then increase the count of answer dictionary with the weight vector obtained from training
            if data[i[x][y][0]] >= data[i[x][y][1]]:ans[h[x][y][0]] += w[x][y]
            else:ans[h[x][y][1]] += w[x][y]
        results.append(max(ans,key=ans.get))
    if Counter(results).most_common()[0][1] == Counter(results).most_common()[1][1]:
        ## if the result is not present in the first temp_list check for the orientation pairs in the second list ie.. temp_list2
        try:return results[temp_list3.index((Counter(results).most_common()[0][0],Counter(results).most_common()[1][0]))]
        except:return results[temp_list4.index((Counter(results).most_common()[0][0],Counter(results).most_common()[1][0]))]
    else:
        return Counter(results).most_common()[0][0]

def main_adaboost(task, file1, file2):
    iterations=6000##changing this will change the time of the program training as well as the accuracy the max value is 192*192
    id, dataset=read_data(file1)
    if task == 'train':
        seggregated_data, h, w, i, ignore, temp_list = defaultdict(list), {}, {}, {}, {}, []
        print("Training classifiers...")
            ## if we dont consider strong classifiers remove this and directly send the data to the training function we were getting only 31% accuracy, since it was a weak classifier
            ## so we take combinations of each of 0,90,180,270 pairs
            ## 0->90, 0->180, 0->270 if not 0 then check for 90, if not 0 then check for 180, if not 0 then check for 270
            ## 90->180, 90->270 if not 90 then check for 180, if not 90 then check for 180
            ## 180->270 if not 180 then 270
            ## like this we have generated 6 pairs of classifiers which are equivalent to the inversions as well which means 90->0 and so on for all the pairs ie.. if not 90 then check for 0
        temp_list=[(0,90),(0,180),(0,270),(90,180),(90,270),(180,270)]
        for x in dataset:
            for temp in temp_list:
                if int(x[0]) in temp:seggregated_data[temp].append(x)
        for temp in temp_list: h[temp], w[temp], i[temp], ignore[temp] = training_adaboost(seggregated_data[temp],iterations)
        #converting the data to json writable and readable key-value format
        h,w,i,ignore={str(k): v for k, v in h.items()}, {str(k): v for k, v in w.items()}, {str(k): v for k, v in i.items()}, {str(k): v for k, v in ignore.items()}
        json_format_key_value = {"h": h, "w": w, "i": i, "ignore": ignore}
        with open('adaboost_model.txt', 'w') as file: file.write(json.dumps(json_format_key_value)) ##writing the json output format in the file
    if task == 'test':
        id,data = read_data(file1)
        with open(file2, 'r') as f:datastore = json.load(f)
        h, w, i, ignore, count, f2 = datastore['h'], datastore['w'], datastore['i'], datastore['ignore'], 0, open("adaboost_output.txt", 'w')
        print("Testing..........")
        temp_list, temp_list2, temp_list3, temp_list4=['(0, 90)', '(0, 180)', '(0, 270)', '(90, 180)', '(90, 270)', '(180, 270)'], ['(90, 0)', '(180, 90)', '(270, 180)', '(270, 0)', '(270, 90)', '(180, 0)'], [('0', '90'), ('0', '180'), ('0', '270'), ('90', '180'), ('90', '270'),('180', '270')], [('270', '180'), ('270', '90'), ('180', '90'), ('270', '0'),('180', '0'), ('90', '0')]
        for x in data:
            answer = testing_adaboost(x,h,w,i,ignore,iterations,[],temp_list,temp_list2,temp_list3,temp_list4)
            f2.write(id[data.index(x)] + " " + str(answer) + "\n")
            if int(x[0]) == int(answer):count += 1
        print("Accuracy:", (float(count) / float(len(data))) * 100)
main_adaboost(sys.argv[1], sys.argv[2], sys.argv[3])
