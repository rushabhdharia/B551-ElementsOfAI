#!/usr/bin/env python3
#
# ./ocr.py : Perform optical character recognition, usage:
#     ./ocr.py train-image-file.png train-text.txt test-image-file.png
#
# Authors: (Nahush Raichura(nraichur), Rushabh dharia(rdharia), Sethu Prakasam(sprakas))
# (based on skeleton code by D. Crandall, Oct 2018)
#
##Algorithms and Code Description
'''
---> Simplified Algorithm
-in the Simple HMM algorithm we first take the keys from the train image dictionary
-now for every test image pixel we compare it with the train image pixel to calculate the probability
-the elements are check for "*", " " and none
-the weightage given to star is 0.6, for a blank space is 0.3 and 0.1 for everything else
-these probability weightages are taken after trying a handful of combinations and getting the best results with 0.6,.3,0.1
-the total probability is then divided by 350 because the test images have a total of 350 pixel
-we then calculate the average of the weighted sum of probabilities and then find the corresponding letter from the TRAIN_LETTERS data
-the character we find from the TRAIN_LETTER data-set is then appended as an answer and returned to the print function to print the final answer

--->Viterbi Algorithm
-We first make dictioaries of the transition probabilities
-Then we have created a 2dimensional array structure using multi dimensional list\
-the row of the structure includes the test sets from the images and the column has the characters from the train data set
-we start the viterbi algorithm by filling up the first column with the initial probabilities of each character
-the next rows are then filled with the emission probabilities
-the formula for the next emission probability is transition probability times the previous states probability
-then we backtrack each element from the last column to the first column
-the backtracking path is then appended to a string and returned to the string function for printing

-The Final answer is then given by comparing each character between the two algorithms 
-if both the algorithms have the same character at that position then the final answer will have that character at the same position
-however if simple and and viterbi recognizes the same character differently then the character predicted by viterbi is taken into consideration
 
'''

from PIL import Image, ImageDraw, ImageFont
import sys,math
def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size), result = im.size , []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result
def load_training_letters(fname,TRAIN_LETTERS):
    return { TRAIN_LETTERS[i]: load_letters(fname)[i] for i in range(0, len(TRAIN_LETTERS) ) }
def calculate_transition_probability(file_name,TRAIN_LETTERS):
    ##input of all the available data
    with open(file_name) as f:list_of_lines=[line.strip() for line in f]
    no_of_letters = 0
    for x in range(len(list_of_lines)):
        for y in range(len(list_of_lines[x])):no_of_letters = no_of_letters+1
    ##
    for x in range(len(list_of_lines)):
        ##making a dictionary of all the letters from the text training data with frequency count of each word
        if(list_of_lines[x]!=""):
            for y in range(len(list_of_lines[x])):
                if(list_of_lines[x][y] in dictionary_of_letters.keys()):dictionary_of_letters[list_of_lines[x][y]]=(dictionary_of_letters[list_of_lines[x][y]]+1)/no_of_letters
                else:dictionary_of_letters[list_of_lines[x][y]]=1/no_of_letters
        ##
        ##making a dictionary with the keys observed->new letter
        for y in range(len(list_of_lines[x])-1): ## to avoid the space in the word
            observed_new=""
            observed_new=observed_new+list_of_lines[x][y]+"->"+list_of_lines[x][y+1]
            if observed_new in dictionary_of_transition_probability.keys():dictionary_of_transition_probability[observed_new]=dictionary_of_transition_probability[observed_new]+1
            else:dictionary_of_transition_probability[observed_new]=1
        ##
        ##making a dictionary of 2 consecutive words in the train string text
        for y in range(len(list_of_lines[x])-1):
            temp=list_of_lines[x][y]+list_of_lines[x][y+1]
            if temp in dictionary_of_transition_probability2.keys():dictionary_of_transition_probability2[temp]=dictionary_of_transition_probability2[temp]+1
            else:dictionary_of_transition_probability2[temp]=1
        ##
        ##here we make a dictionary of new keys which are present in the lines from the train_text data
        for y in range(len(list_of_lines[x])):
            if(list_of_lines[x][y] in dictionary_of_letters_new.keys()):dictionary_of_letters_new[list_of_lines[x][y]]=dictionary_of_letters_new[list_of_lines[x][y]]+1
            else:dictionary_of_letters_new[list_of_lines[x][y]]=1
        ##
    ##making a new dictionary which is based on the condition that if the dictionary consist the character which is present in the training text input then we increase the dictionary value by 1 or else make a new key and set the fequency as 1
    for x in range(0,len(list_of_lines)):
        if list_of_lines[x]=="":pass
        else:
            if list_of_lines[x][0] in dictionary_of_letters2.keys():dictionary_of_letters2[list_of_lines[x][0]]+=1
            else :dictionary_of_letters2[list_of_lines[x][0]] = 1
    ##

    for x in dictionary_of_letters2.keys():
        dictionary_of_letters2[x]=dictionary_of_letters2[x]/len(list_of_lines)
    ##print(dictionary_of_letters2)

    for x in range(0,len(TRAIN_LETTERS)):
        if TRAIN_LETTERS[x] in dictionary_of_letters2.keys():pass
        else:dictionary_of_letters2[TRAIN_LETTERS[x]]=math.pow(10,-9)
    ##print(dictionary_of_letters2)
    for x in range(len(TRAIN_LETTERS)):
        ##calculate the probability from the train_letters if the sequence observed->new is not available in the dictionary we assign it a very small probability value in this case 10^-9
        for y in range(len(TRAIN_LETTERS)):
            observed_new=""
            observed_new=observed_new+TRAIN_LETTERS[y]+"->"+TRAIN_LETTERS[x]
            if observed_new in dictionary_of_transition_probability.keys() and TRAIN_LETTERS[y] in dictionary_of_letters.keys():dictionary_of_transition_probability[observed_new]=dictionary_of_transition_probability[observed_new]/dictionary_of_letters[TRAIN_LETTERS[y]]
            else:dictionary_of_transition_probability[observed_new]=math.pow(10,-9)
        ##
        ##if the train train letters are not present in the dictionary we assign them a very low probability 10^-9
        if(TRAIN_LETTERS[x] not in dictionary_of_letters.keys()):dictionary_of_letters[TRAIN_LETTERS[x]]=math.pow(10,-9)
        ##
    ##calculating the probability
    ##if the string is not present in the dictionary then we assign it a probability of 10^-9 to that key in the dictionary
    for x in dictionary_of_letters_new.keys():
        for y in dictionary_of_letters_new.keys():
            string=x+y
            if string in dictionary_of_transition_probability2.keys() and string in dictionary_of_letters_new.keys():dictionary_of_transition_probability2[string]=dictionary_of_transition_probability2[string]/float((dictionary_of_letters_new[x]+dictionary_of_letters2[y]))
            else:dictionary_of_transition_probability2[string]=math.pow(10,-9)
    ##
    ##making the final dictionary used for computations
    ## checking in dictionary if the string is not there then we assign a vert low probability to it in this case 10^-9
    for x in TRAIN_LETTERS:
        for y in TRAIN_LETTERS:
            string=x+y
            if string in dictionary_of_transition_probability2.keys():dictionary_of_transition_probability3[string]=dictionary_of_transition_probability2[string]
            else:dictionary_of_transition_probability3[string]=math.pow(10,-9)
            if string not in dictionary_of_transition_probability2.keys():dictionary_of_transition_probability2[string]=math.pow(10,-9)
    ##
def simple_HMM(test_from_image,train_from_image):
    ans=""
    for x in range(len(test_from_image)):## for each letter in the test image
        weight_list,max,temp=[],-9999999999999999,0
        ##calculating the probability from each character observed in the image recognition
        for y in train_from_image.keys():
            stars,blank,none=0,0,0
            for xx in range(CHARACTER_HEIGHT):
                for yy in range(CHARACTER_WIDTH):
                    if(train_from_image[y][xx][yy]==test_from_image[x][xx][yy]=="*"):stars=stars+1
                    elif(train_from_image[y][xx][yy]==test_from_image[x][xx][yy]==" "):blank=blank+1
                    else:none=none+1
            weight_list.append((0.6*stars+0.3*blank+0.1*none)/350)
        ##
        ##finding out the highest likely word from the weight list and hence finding out the coressponding letter to it and appending it to the final answer
        for y in range(len(weight_list)):
            if weight_list[y]>max:max,temp=weight_list[y],y
        ans=ans+list(train_from_image)[temp]
        ##
    final_answer_list.append(ans)
    return ans
def viterbi_HMM(test_from_image,train_from_image,TRAIN_LETTERS):
    list1,list2,ans=[],[],""
    ##calculating the probability for each TRAIN_LETTER
    for x in range(len(TRAIN_LETTERS)):
        star,blank,none=0,0,0
        for xx in range(CHARACTER_HEIGHT):
            for yy in range(CHARACTER_WIDTH):
                if (test_from_image[0][xx][yy]==train_from_image[TRAIN_LETTERS[x]][xx][yy]=="*"):star=star+1
                elif(test_from_image[0][xx][yy]==train_from_image[TRAIN_LETTERS[x]][xx][yy]==" "):blank=blank+1
                else:none=none+1
        list2.append(math.log(0.7*star+0.2*blank+0.1*none)/350)##take log of probability to avoid large computations
    list1.append(list2)
    ##
    ##calculating probabiliry for each character in the test image and then finding the highest probability character from the dictionary and then appending as ans and then returning the final ans
    for x in range(1,len(test_from_image)):
        list2=[]
        for y in range(len(TRAIN_LETTERS)):
            temp,temp1=0,0
            for z in range(len(TRAIN_LETTERS)):
                temp3,string=0,TRAIN_LETTERS[y]+TRAIN_LETTERS[z]
                temp3=list1[x-1][z]+math.log(dictionary_of_transition_probability3[string])
                if(temp3>temp):temp,temp1=temp3,z
            star,blank,none = 0,0,0
            for xx in range(CHARACTER_HEIGHT):
                for yy in range(CHARACTER_WIDTH):
                    if (test_from_image[x][xx][yy] == train_from_image[TRAIN_LETTERS[y]][xx][yy] == "*"):star = star + 1
                    elif (test_from_image[x][xx][yy] == train_from_image[TRAIN_LETTERS[y]][xx][yy] == " "):blank = blank + 1
                    else:none = none + 1
            list2.append(temp+math.log((0.6*star+0.3*blank+0.1*none)/350))
        list1.append(list2)
    ##
    ##get the highest probability and the index of the corresponding element from the TRAIN_LETTER, and append it as the answer
    for x in range(len(test_from_image)):
        min,temp=-9999999999,0
        for y in range(len(TRAIN_LETTERS)):
            if(list1[x][y]>min):min,temp=list1[x][y],y
        ans=ans+TRAIN_LETTERS[temp]
    final_answer_list.append(ans)
    return ans
    ##
# main program
TRAIN_LETTERS,CHARACTER_WIDTH,CHARACTER_HEIGHT="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' ",14,25
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
dictionary_of_letters,dictionary_of_letters2,dictionary_of_letters_new,dictionary_of_transition_probability,dictionary_of_transition_probability2,dictionary_of_transition_probability3,list_of_keys,list_of_values,train_letters,test_letters,final_answer_list,ultimate_answer={},{},{},{},{},{},[],[],load_training_letters(train_img_fname,TRAIN_LETTERS),load_letters(test_img_fname),[],[]
calculate_transition_probability(train_txt_fname,TRAIN_LETTERS)
print("Simple: %s\nViterbi: %s" % (simple_HMM(test_letters,train_letters),viterbi_HMM(test_letters,train_letters,TRAIN_LETTERS)))
for x in range(len(final_answer_list[0])):
    flag=0
    if(final_answer_list[0][x]==final_answer_list[1][x]):
        flag=1
        ultimate_answer.append(final_answer_list[0][x])
    if(flag!=1):
        flag=1
        ultimate_answer.append(final_answer_list[1][x])
print("Final Answer:")
for x in range(len(ultimate_answer)):
    print(ultimate_answer[x], end="")
print()
