#!/usr/bin/env python3
###################################
# CS B551 Fall 2018, Assignment #3
#
# Your names and user ids: 
# Rushabh Dharia - rdharia, Nahush Raichura - nraichur, Sethu Prakasam -sprakas
# (Based on skeleton code by D. Crandall)
#
#
####
# Put your report here!!
'''
Training:
The trained data is stored in the following dictionaries
dict_of_s - Stores the probability of a part of speech to occur in a sentence.
transition_prob - Stores the transition from the past POS state Si to current POS state Si+1. P(Si+1| Si)
emission_prob - Stores the emission of observation Wi in state Si. P(Wi | Si)
transiton_prob2 - Stores the transition to state Si+2 given states Si and Si+1. P(Si+2| Si, Si+1) 
start_p - Stores the probability of a part of speech to start a sentence

list pos[] stores all the parts of speech considered in the training data

Simplified Model:
Estimated the most probable tag Si for each word Wi using the emission probability
If the new word encountered is not in the training set then the part of speech is considered noun by default.

Viterbi:
A table V is created. Columns are the words and rows are the parts of speech. 
For column 0:
We calculate the occurrence of each Part of Speech tag by multiplying the starting probability (using the start_p dictionary) and the emission probability and set it's previous value to 1

For other columns:
We calculate the max prob of occurrence of a part of speech tag by multiplying the previous row by the transition probability from the previous state to the next state(Comparing all the states to get the max value).
Then we set that element's probability to the max probability found above and set it's prev to the previous state which gave the maximum probability.

After creating the above table we backtrack to get the list of hidden parameters(parts of speech) for the observed parameters(words of the sentence).

Things we tried:
If a word is not present in the training set then
1. We gave preference to noun:  words correct- 95.71%,  sentences correct- 58.10%
2. Gave all parts of speech the equal probability : words correct - 94.30%,  sentences correct- 50.95%
3. Gave each part of speech the probability of its occurence depending on the training data : words coreect - 95.33%,  sentences correct- 56.20%
4. Gave probability of each part of speech equal to emission probability: words correct - 95.21%, sentences correct - 56.30%

As we can see if a word is not encountered selecting that word as a noun is the safest bet.

Complex MCMC:
We used Gibbs Sampling.
The initial sample considered is all tags are set to noun
We created 500 samples and burnt the first 100 samples

For every sample
a. If it the first word in the sentence then we muliplied the starting probability of the first label with the emission prob P(Wi|Si)
b. If it is the last word of the sentence we multiplied the emission prob P(Wi|Si) with transition prob P(Si, Si-1) and transition prob P(Si|Si-1, Si-2)
c. If it is the second last word of the sentence we multiplied the emission prob P(Wi|Si) with transition prob P(Si, Si-1) and transition prob P(Si|Si-1, Si-2) and transition prob P(Si+1, Si)
d. For all other words of the sentence  we multiplied the emission prob P(Wi|Si) with transition prob P(Si, Si-1) and transition prob P(Si|Si-1, Si-2) and transition prob P(Si+1, Si) and transition prob P(Si+2|Si+1, Si)

All these probabilities are stored in a list prob[]

Then we used the numpy function np.random.choice to select a part of speech tag and append it to the new sample till tags for all the samples are created.

After 100 iterations we check every 5 recently generated samples to see if they converge(i.e. if they are the same).If they converge then we halt the sample creation and return the most recently created sample

Posterior:
For simple we calculate the logs of the emission probabilities P(Wi|Si) and return their sum.

For HMM we calculate the logs of the emission probabilities P(Wi|Si), transition Prob P(Si|Si-1) and the starting probability of the first label.
Then we add all of them

For Complex we calculate the log of the emission prob emission probabilities P(Wi|Si), transition Prob P(Si|Si-1) and transition prob P(Si|Si-1,Si-2) and add all of them

Assumptions:
1. For posterior: If we encounter a new word we set it's emission/transition probabilities to 0.0000000000001. We directly calculated its log which is -36.841361487904734 and used that instead of calculating it's log everytime

2. Similarly for MCMC, if we encounter a new word we set it's emission/transition probabilities to 0.0000000000001.

Results:
For bc.test
==> So far scored 2000 sentences with 29442 words.
                   Words correct:     Sentences correct: 
   0. Ground truth:      100.00%              100.00%
         1. Simple:       92.91%               43.15%
            2. HMM:       95.71%               58.10%
        3. Complex:       90.80%               38.15%

For bc.test.tiny
==> So far scored 3 sentences with 42 words.
                   Words correct:     Sentences correct: 
   0. Ground truth:      100.00%              100.00%
         1. Simple:       95.24%               66.67%
            2. HMM:      100.00%              100.00%
        3. Complex:       83.33%                0.00%
'''
####

import random
import math
import numpy as np
import sys

# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#

dict_of_s = {} #prob of pos
transition_prob = {} #transition prob
transition_prob2 = {} # transition prob for complex
emission_prob = {} #emission prob
pos = []
start_p = {} #starting prob

class Solver:
	# Calculate the log of the posterior probability of a given sentence
	#  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
	def posterior(self, model, sentence, label):

		if model == "Simple":
			total = 0
			for i in range(0, len(sentence)):
				sum1 = math.log(dict_of_s[label[i]])
				if sentence[i] in emission_prob[label[i]]:
					sum2 = math.log(emission_prob[label[i]][sentence[i]])
				else: 
					sum2 = -36.841361487904734 #0.0000000000001
				total +=  sum1 + sum2
			return total

		elif model == "Complex":
			sum1 = math.log(start_p[label[0]])
			sum2 = 0

			total = sum1 
			sum1 = 0
			sum3=0
			if (len(label)>=2):
				for i in range(len(sentence)-1):
					if label[i+1] in transition_prob[label[i]]:
						sum3 = math.log(transition_prob[label[i]][label[i+1]])
					else:
						sum3 = -36.841361487904734

			for i in range(len(sentence)):             
				if sentence[i] in emission_prob[label[i]]:
					sum1 += math.log(emission_prob[label[i]][sentence[i]])
				else:
					sum1 += -36.841361487904734

			sum2 = 0
			for i in range(len(sentence)-2):
				key = label[i+2]+"->"+label[i+1]+label[i]
				if key in transition_prob2:
					sum2 += math.log(transition_prob2[key])
				else:
					sum2 += -36.841361487904734

			total += sum1 + sum2+sum3
			return total

		elif model == "HMM":
			sum1 = math.log(start_p[label[0]])
			if sentence[0] in emission_prob[label[0]]:
				sum2 = math.log(emission_prob[label[0]][sentence[0]])
			else:
				sum2 = -36.841361487904734 #0.0000000000001
			total = sum1 + sum2
			for i in range(1, len(sentence)):
				if sentence[i] in emission_prob[label[i]]:
					sum1 = math.log(emission_prob[label[i]][sentence[i]])
				else:
					sum1 = -36.841361487904734 #0.0000000000001
				if label[i] in transition_prob[label[i-1]]:
					sum2 = math.log(transition_prob[label[i-1]][label[i]])
				else:
					sum2 = -36.841361487904734
				total += sum1 + sum2 
			return total
		else:
			print("Unknown algo!")

	# Do the training!
	#
	def train(self, data):
		global dict_of_s
		global transition_prob
		global emission_prob
		global pos
		global start_p
		
		total_for_start = 0

		file = open("bc.train", 'r')
		for line in file:
			i = 0
			line2 = line.split(' ')
			for word in line2:
				word = word.lower()
				if i == 1:
					if word not in start_p:
						start_p[word] = 0
					total_for_start += 1
					start_p[word] += 1
				if i%2 == 0:
					w = word
				else:
					if word not in emission_prob:
						emission_prob[word] = {}
						pos.append(word)
					if w not in emission_prob[word]:
						emission_prob[word][w] = 0
					emission_prob[word][w] += 1
				i += 1  

		for key in start_p:
			start_p[key] /= total_for_start

		list_for_wisi = []
		for key in emission_prob:
			total = 0
			for val in emission_prob[key]:
				total += emission_prob[key][val]
			list_for_wisi.append(total)

		count1 = 0
		for key in emission_prob:
			for val in emission_prob[key]:
				emission_prob[key][val]/=list_for_wisi[count1]
			count1+=1       
		
		a = 0
		total = 0
		for i in data:
			for j in i:
				a+=1
				prev = None
				prev2 = None
				if a%2==0:
					for k in j:
						if k not in dict_of_s:
							dict_of_s[k] = 0
						if k not in transition_prob:
							transition_prob[k] = {}
						
						dict_of_s[k] += 1
						total += 1

						if prev:
							if k not in transition_prob[prev]:
								transition_prob[prev][k] = 0
							transition_prob[prev][k] += 1

						prev2 = prev
						prev = k


	   
		for k in dict_of_s:
			dict_of_s[k] /= total

		list_for_si = []
		for si in transition_prob:
			total = 0
			for k in transition_prob[si]:
				total += transition_prob[si][k]
			list_for_si.append(total)

		count = 0
		for si in transition_prob:
			for k in transition_prob[si]:
				transition_prob[si][k] /= list_for_si[count]
			count+=1


		# Transition Probabilities
		# P(Si+2|Si+1, Si)
		for line in data:
			for i in range(len(line[1])-2):
				key = line[1][i+2] +"->"+ line[1][i+1] + line[1][i]
				if key in transition_prob2:
					transition_prob2[key] += 1
				else:
					transition_prob2[key] = 1

		deno_dict = {}
		for line in data:
			for i in range(len(line[1])-1):
				key = line[1][i+1] + line[1][i]
				if key in deno_dict:
					deno_dict[key] += 1
				else:
					deno_dict[key] = 1

		for key in transition_prob2.keys():
			a, b = key.split("->")
			transition_prob2[key] /= deno_dict[b]

		pos.remove('')
		pass

	# Functions for each algorithm. Right now this just returns nouns -- fix this!
	#
	def simplified(self, sentence):
		global emission_prob
		list_simp = []
		for word in sentence:
			maxi = 0
			part_of_speech = "noun"
			for k in emission_prob:
				if word in emission_prob[k] and maxi<emission_prob[k][word]:
					maxi = emission_prob[k][word]
					part_of_speech = k
			list_simp.append(part_of_speech)
		return list_simp

	def stopping_condition(self, list_sampler):
		check = 1
		for i in range(1, len(list_sampler)):
			#print(list_sampler[0])
			if list_sampler[0] != list_sampler[i]:
				check = 0
				break       
		return check

	def complex_mcmc(self, sentence):
		global pos
		burning_iteration = 100
		total_iterations = 500
		samples = []
		sample_checker = []
		counter = 0
		sample = ["noun"] * len(sentence)

		for i in range(total_iterations):
			final_sample = []

			for j in range(len(sentence)):            
				word = sentence[j]
				prob = [0] * len(pos)
			
				for k in range(len(pos)):
						current_prob2=pos[k]
						prob0 = start_p[pos[k]]
					
						if pos[k] in emission_prob and word in emission_prob[pos[k]]:    
							prob1 = emission_prob[pos[k]][word]
						else:
							prob1 = 0.0000000000001
						
						if j!=0:
							if sample[j-1] in transition_prob and current_prob2 in transition_prob[sample[j-1]]:
								prob2 = transition_prob[sample[j-1]][current_prob2]
							else:
								prob2 = 0.0000000000001

						if j!=0:
							key = pos[k]+"->"+sample[j-1]+sample[j-2]
							if key in transition_prob2:
								prob3 = transition_prob2[key]
							else:
								prob3 = 0.0000000000001

						if j!=0 and j!=len(sentence)-1 and j!=len(sentence)-2:
							key = sample[j+2]+"->"+sample[j+1]+pos[k]
							if key in transition_prob2:
								prob5 = transition_prob2[key]
							else:
								prob5 = 0.0000000000001


						if j!=0 and j!= len(sentence)-1: 
							if sample[j+1] in transition_prob and pos[k] in transition_prob[sample[j+1]]:
								prob4 = transition_prob[sample[j+1]][pos[k]]
							else:
								prob4 = 0.0000000000001

						if j == 0:
							prob[k] = prob0 * prob1
						elif j == len(sentence)-1:
							prob[k] = prob1 * prob2 *prob3
						elif j==len(sentence)-2:
							prob[k] = prob1 * prob2 *prob3*prob4
						else:
							prob[k] = prob1 * prob2 * prob3 * prob4 *prob5   

				sum_of_prob = sum(prob)
				for l in range(len(prob)):
					prob[l] /= sum_of_prob

				tag = np.random.choice(pos, 1, p=prob)
				final_sample.append(tag[0])

			sample = final_sample


			if i > burning_iteration:
				samples.append(sample)
				sample_checker.append(sample)
				counter+=1
				if counter>5:
					sample_checker.pop(0)
					if self.stopping_condition(sample_checker):
						break
		return samples[len(samples)-1]


	def hmm_viterbi(self, sentence):
		global start_p
		global emission_prob
		global transition_prob

		#---------------------------------------------------------------------------------------------------
		#Code Adapted from https://en.wikipedia.org/wiki/Viterbi_algorithm
		V = [{}]
		for parts in pos:
			if sentence[0] in emission_prob[parts]:
				V[0][parts] = {"prob": start_p[parts] * emission_prob[parts][sentence[0]], "prev": None}
			else:
				V[0][parts] = {"prob": 0, "prev": None}
		check = 0
		for i in V[0]:
			if V[0][i]['prob']:
				check = 1
			
		if check == 0:
			V[0]['noun']['prob'] = 1

		
		for q in range(1, len(sentence)):
			V.append({})
			check = 0
			for parts in pos:
				max_pos_prob = V[q-1][pos[0]]["prob"] * transition_prob[pos[0]][parts]
				prev_pos_selected = pos[0]
				for prev_pos in pos[1:]:
					if parts in transition_prob[prev_pos]:
						prob = V[q-1][prev_pos]["prob"] * transition_prob[prev_pos][parts]
					else:
						prob = 0
					if prob > max_pos_prob:
						max_pos_prob = prob
						prev_pos_selected = prev_pos
				
				if sentence[q] in emission_prob[parts]:
					max_prob = max_pos_prob * emission_prob[parts][sentence[q]]
				else:
					max_prob = 0
				V[q][parts] = {"prob": max_prob, "prev": prev_pos_selected}

			for i in V[q]:
				if V[q][i]['prob']:
					check = 1

			if check == 0: #if transition probabilities fails
#Gives preference to noun:  words correct- 95.71%,  sentences correct- 58.10%
				V[q]['noun']['prob'] = 1

# Uncomment to give all parts of speech the equal probability : words correct - 94.30%,  sentences correct- 50.95%
				# for parts in pos:
				#   V[q][parts]['prob'] = 1/12

# Uncomment to give each part of speech the probability of its occurence depending on the training data : words correct - 95.33%,  sentences correct- 56.20%
				# for parts in pos:
				#   V[q][parts]['prob'] = dict_of_s[parts]

# Uncomment to select the probability of part of speech equal to emission probability words correct - 95.21%, sentences correct - 56.30%
				# for parts in pos:
				#   V[q][parts]['prob'] = transition_prob[V[q][parts]['prev']][parts]

		opt = []
		max_prob = max(value["prob"] for value in V[-1].values())
		previous = None

		for st, data in V[-1].items():
			if data["prob"] == max_prob:
				opt.append(st)
				previous = st
				break

		for t in range(len(V) - 2, -1, -1):
			opt.insert(0, V[t+1][previous]["prev"])
			previous = V[t+1][previous]["prev"]

		#---------------------------------------------------------------------------------------------------
		return opt

	# This solve() method is called by label.py, so you should keep the interface the
	#  same, but you can change the code itself. 
	# It should return a list of part-of-speech labelings of the sentence, one
	#  part of speech per word.
	#
	def solve(self, model, sentence):
		if model == "Simple":
			return self.simplified(sentence)
		elif model == "Complex":
			return self.complex_mcmc(sentence)
		elif model == "HMM":
			return self.hmm_viterbi(sentence)
		else:
			print("Unknown algo!")

 