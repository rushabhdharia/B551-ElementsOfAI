#!/usr/bin/env python3

'''
Code Adapted from https://machinelearningmastery.com/implement-decision-tree-algorithm-scratch-python/

'''
import numpy as np
import sys
import json
import pandas as pd

#Cost function used to evaluate splits in the training data. Gives an idea of how good a split is.
def gini_index(groups, classes):
   num_inst = float(sum(len(group) for group in groups))
   gini = 0.0
   
   for group in groups:
      size = float(len(group))
      if size == 0:
         continue
      score = 0.0
      for class_val in classes:
         prop = [s[0] for s in group].count(class_val) / size
         score += prop*prop
      gini += (1.0 - score) * (size/num_inst)
   
   return gini

#Splits data based on an attribute and an attribute value
def test_split(index, value, sample):
   left = []
   right = []

   for i in sample:
      if i[index] < value:
         left.append(i)
      else:
         right.append(i)

   return left, right

# Selects the best split
def get_split(sample):
   class_values = list(set(i[0] for i in sample))
   b_index, b_value, b_score, b_groups = 999, 999, 999, None
   index = 1
   count = len(sample[0])
   while index < count:
      groups = test_split(index, 128, sample) #sample[0][index]
      g = gini_index(groups, class_values)
      if g < b_score:
         b_index, b_value, b_score, b_groups = index, 128, g, groups
      index+=1
   return {'index': b_index, 'value' :b_value, 'groups' : b_groups}

# Creates a terminal node
def to_terminal(group):
   outcomes = [s[0] for s in group]
   return max(set(outcomes), key = outcomes.count)

# Creates children for a node
def split(node, max_depth, min_size, depth):
   left, right = node['groups']
   del(node['groups'])

   if not left or not right:
      node['left'] = node['right'] = to_terminal(left+right)
      return

   if depth >= max_depth:
      node['left'], node['right'] = to_terminal(left), to_terminal(right)
      return

   if len(left) <= min_size:
      node['left'] = to_terminal(left)
   else:
      node['left'] = get_split(left)
      split(node['left'], max_depth, min_size, depth+1)

   if len(right) <= min_size: 
      node['right'] = to_terminal(left)
   else:
      node['right'] = get_split(right)
      split(node['right'], max_depth, min_size, depth+1) 

# Builds a Decision Tree
def build_tree(sample, max_depth, min_size):
   root = get_split(sample)
   split(root, max_depth, min_size, 1)
   return root

# Makes a prediction based on the decision tree
def predict(node, row):
   if row[node['index']] < node['value']:
      if isinstance(node['left'], dict):
         return predict(node['left'], row)
      else:
         return node['left']
   else:
      if isinstance(node['right'], dict):
         return predict(node['right'], row)
      else:
         return node['right']

# Used to create a subsample
def subsample():
   x=np.random.randint(training_data.shape[0], size=int(training_data.shape[0]/80))
   y=np.random.randint(training_data.shape[1], size=int(training_data.shape[1]/8))
   z=np.append(0,y)   
   return training_data[x,:][:,z], z

# Builds a random forest
def forest_train(num_trees):
   max_depth = 30
   min_size = 1
   trees = []
   list_z = []

   for i in range(num_trees):
      sample,z = subsample()
      tree = build_tree(sample, max_depth, min_size)
      trees.append(tree)
      list_z.append(z)

   return trees, list_z

# Makes predictions based on random forest
def forest_test(num_trees, trees, list_z):
   total = {}
   right_pred = 0
   f_op = open("output.txt", "w")

   for i in range(num_trees): 
      tree = trees[i]
      index = 0
      for row in testing_data[:][:,list_z[i]]:
         prediction=predict(tree,row)
         temp=[]
         temp.append(prediction)
         total[index]=total.get(index,[])+temp
         index+=1

   total_count = len(total.values())
   k=0
   for key_t in total:
   	max1 = max(total[key_t], key=total[key_t].count)
   	f_op.write(names[k])
   	f_op.write(" ")
   	f_op.write(str(max1))
   	f_op.write("\n")
   	# print(names[k], max1)
   	k += 1
   	if testing_data[key_t][0] == max1:
   		right_pred += 1

   return right_pred, total_count


def forest_f(arg1, text1, text2):
   global training_data
   global testing_data
   global names
   num_trees = 50

   if(arg1== "train"): 
      file1 = open(text1)
      data_train = []
      for line in file1:
         temp = []
         for row in line.split()[1:]:
            temp.append(int(row))
         data_train.append(temp)
      training_data = np.array(data_train)
      
      trees, list_z = forest_train(num_trees)
      data = {}
      data['trees'] = trees
      data['list_z'] = list_z
      
      df = pd.DataFrame(data)

      df.to_json(path_or_buf=text2)


   else:
      file2 = open(text1)
      data_test = []
      names = []
      for line in file2:
         names.append(line.split()[0])
         temp2 = []
         for row in line.split()[1:]:
            temp2.append(int(row))
         data_test.append(temp2)
      testing_data = np.array(data_test)

      # with open('', 'r') as fp:
      df = pd.read_json(path_or_buf = text2)
      data = df.to_dict('dict')
      trees = data['trees']# read from file
      list_z = data['list_z']# read from file

      right_pred,total_count = forest_test(num_trees, trees, list_z)

      accuracy = float(right_pred) * 100/total_count

      print("Accuracy = {}".format(accuracy))
   pass

if __name__ == '__main__':
   main()
