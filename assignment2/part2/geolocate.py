#!/usr/bin/env python3
# Creators : Dhruuv Agarwal

'''
Design:
Used a Dictionary of Dictinary. The key of the first dictionary is the location of the tweets and value is the word list(inner dictionary word:count). We selected the 1st key as location as in Naive Bayes P(w|l). In Naive Bayes we worry about the frequency of the word. Therefore, the inner dictionary key is the word and value is the number of times the word occurred.

Experimentation:
For new words, a lower probability is assigned. So, we tried 10^(-8) to 10^(-5), then we observed that accuracy is dropping. But, in 10^(-6) we found the accuracy to increase. Then we tried finding the relation between probability and size of dataset. Therefore, probability is 1/totalSize. We found this to be empirically correct.
'''


import sys,re,operator
from math import ceil,exp, floor
import numpy as np
from collections import Counter, OrderedDict

## very old yet short list of stop words
stoplist = ['a','about', 'an', 'are' ,'as', 'at', 'be', 'by', 'com','for', 'from','how','in' ,'is', 'it', 'of', 'on','or', 'that','the', 'this','to', 'was', 'what','when','where','who','will','with','the','www','we','so','were','its','but','and','can','i','you','me','now','if','im','careerarc','click','your','our','here','anyone','my','latest','all','p','after','again','apply','up','alert']

## Making structure required from the input. The structure is dictionary with value
## as list of lists for each argument for an id/student

def cleanline(line):
    tmp = []
    for word in line.split():
        tmpword =re.sub(r'\W+','',word.lower())
        
        tmpword = re.sub(r'\b[0-9]+|am|pm\b', '', tmpword)
        #tmpword = re.sub(r'\s\b[0-9]+\b\s*', '', tmpword)
        tmpword = re.sub("\d+", "", tmpword)
        tmpword = re.sub(r'[_]', '', tmpword)
        if tmpword.strip()!='' and tmpword not in stoplist:   tmp.append(tmpword)
    return ' '.join(tmp).rstrip()

def Getinputfromfile(filepath):
    d ={}
    with open(filepath) as fp:
        for line in fp:
            if line.rstrip().count(' ')>1:
                loc,rest = line.rstrip().split(None,1)
                if loc in d:    [d[loc].append(x) for x in cleanline(rest).split()]
                else:   d[loc] = [x for x in cleanline(rest).split()]
    e = {key:dict(Counter(value)) for key,value in d.items()}
    return e

def reduce(inpdict):
    newdict = {}
    listone = []
    for loc,wordlist in inpdict.items():
        for word,times in wordlist.items():
            if times==1:
                if word in listone: listone.remove(word)
                else :  listone.append(word)
   
    for loc,wordlist in inpdict.items():
        tmp = {word:times for word,times in wordlist.items() if word not in listone}
        newdict[loc] = tmp
    return newdict

def topwords(inpdict):
    newdict={}
    for loc,wordlist in inpdict.items():
         #tmp = sorted(wordlist.items(), key=lambda kv: kv[1])
         #tmp = tmp.reverse()
         #tmp=sorted(wordlist, key=wordlist.get, reverse=True)
         tmp=OrderedDict(sorted(wordlist.items(), key=lambda x: x[1]))
         OrderedDict(tmp)

         tmp2 = {v:k for k, v in tmp.items()}
       	 # OrderedDict(tmp2)
         cc_counter=len(tmp2)-5
         for i in tmp2.copy().keys():
             tmp2.pop(i)
             cc_counter=cc_counter-1
             if(cc_counter==0):
                 break
         newdict[loc] = tmp2
    return newdict

def CalcMAP(line, data, size, pclass):
    intermed = {}
    #print("CALC MAP: ",line)
    """
    for loc in pclass:
        val =1
        for word in line.split():
            tmp = data[loc][word]/size[loc] if word in data[loc] else 0.0000001
            val = val*tmp
            #print("val :" , val, word) 
        intermed[loc]=val 
        #print("val :" , val)        
    """
    intermed = {loc:[data[loc][word]/size[loc] if word in data[loc] else 1/total_size for word in line.split()] for loc in pclass}
    
    MAP = {loc:pclass[loc]*np.prod(intermed[loc]) for loc in pclass}
    return MAP


#print (inpdata)
inpdata = Getinputfromfile(sys.argv[1])
#print (inpdata)
inpdata2 = topwords(inpdata)
#print (inpdata2)
print("The top 5 common words in ascending order are:")
for key,value in inpdata2.items():
     print(key,': ', end='')
     for xx in value.values():
        print(xx,' ', end='')
     print()
#sorted_by_value=sorted(inpdata2.items(), key=operator.itemgetter(1))
#print (sorte_by_value)
#print(e)   
words = {key:len(value) for key,value in inpdata.items()}
corpus_sizes = {key:sum(value.values()) for key,value in inpdata.items()}

total_size = sum(corpus_sizes.values())
class_prob = {key:value/total_size for key,value in corpus_sizes.items()}
#print(words,"\n\n",corpus_sizes,"\n\n")
#print(class_prob)
testfile = sys.argv[2]
outfile = sys.argv[3]

f =open(outfile, 'w')

yes = 0
no = 0
with open(testfile) as fp:
        for line in fp:
            
            if line.rstrip().count(' ')>1:
                loc,rest = line.rstrip().split(None,1)
                #print(line.rstrip())
                MAP = CalcMAP(cleanline(line).rstrip(), inpdata, corpus_sizes, class_prob)
                #print(rest,MAP)
                final_pred = max(MAP,key=MAP.get)
                if(final_pred==loc): yes+=1 
                else : no+=1
                f.write(final_pred+' '+line)
f.close()
print("Accuracy: ",(yes/(yes+no))*100)                
