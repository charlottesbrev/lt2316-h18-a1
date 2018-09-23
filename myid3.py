# Module file for implementation of ID3 algorithm.

# You can add optional keyword parameters to anything, but the original
# interface must work with the original test file.
# You will of course remove the "pass".

import os, sys, math
import numpy
# You can add any other imports you need.

class Node:
    def __init__(self, y, H):
       self.y = y
       self.H = H
       self.SplitAttrib = None
       self.Children = []

class DecisionTree:
    def __init__(self, load_from=None):
        # Fill in any initialization information you might need.
        #
        # If load_from isn't None, then it should be a file *object*,
        # not necessarily a name. (For example, it has been created with
        # open().)
        print("Initializing classifier.")
        if load_from is not None:
            print("Loading from file object.")

    def ID3(self, X, y, attribute_names):
        # Create a root node for the tree
        # If all examples are positive, return the single-node tree Root, with label = +.
        # If number of predicting attributes is empty, then Return the single node tree Root,
        # with label = most common value of the target attribute in the examples.
        # Otherwise Begin
        #    A = The Attribute that best classifies examples.
        #    Decision Tree attribute for Root = A
        #    For each possible value, v_i, of A
        #       Add a new tree branch below Root, corresponding to the test A = v_i.
        #       Let Examples(v_i) be the subset of examples that have the value v_i for A
        #       If Examples(v_i) is empty
        #          Then below this new branch add a leaf node with label = most common target value in the examples
        #       Else
        #          below this new branch add the subtree ID3(Examples(v_i), Target_Attribute, Attributes - {A})
        # End

        # Create a root node for the tree
        Root = Node(y, self.ent(y))
        # If all examples are positive/negative, return the single-node tree Root, with label = +/-.
        y_set = set(y)
        if len(y_set) <= 1:
           # Root.label = orsak ???
           return Root
        # If number of predicting attributes is empty, then Return the single node tree Root,
        # with label = most common value of the target attribute in the examples.
# !!!!!!!!!!!!!!!!!!!
        if len(attribute_names) == 0:
           Root.label = most_common_attribute_value(X, y)
           return Root
        # Otherwise Begin
        #    A = The Attribute that best classifies examples.
        #    Decision Tree attribute for Root = A
# !!!!!!!!!!!!!!!!!!!
        # 1 splitta på alla attribut...
        # 2 ta reda på vilket som har högst IG
        H_y = self.entropy(y)
        best_split_y = None
        best_split_attribute_name = None
        max_IG = 0
        for attribute_name in attribute_names:
            split_data = X[attribute_name]
            split_y = self.split(split_data, y)
            H = self.entropy_after_split(y, split_y)
            IG = H_y - H
            if IG >= max_IG:
               best_split_y = split_y
               best_split_attribute_name = attribute_name
               max_IG = IG
        # 3 använd detta som split attribut
        Root.SplitAttrib = best_split_attribute_name
        #    For each possible value, v_i, of A
        for v_y in best_split_y:
        #       Add a new tree branch below Root, corresponding to the test A = v_i.
        #       Let Examples(v_i) be the subset of examples that have the value v_i for A
        #       If Examples(v_i) is empty
        #          Then below this new branch add a leaf node with label = most common target value in the examples
        #       Else
        #          below this new branch add the subtree ID3(Examples(v_i), Target_Attribute, Attributes - {A})
              if v_y == []:
# !!!!!!!!!!!!!!!!!!!
                 child_node = Node(v_y, self.entropy(v_y))
                 #child_node.label = most_common_target_value(X, v_y)
                 Root.Children.append(child_node)
              else:
# !!!!!!!!!!!!!!!!!!!
                 attribute_names.remove(best_split_attribute_name) # Attributes - {A}
                 Root.Children.append(self.ID3(self, X, y, attribute_names))
        # End
        return Root

    def split(self, split_attr, y):
        split_set = set(split_attr)
        ret_list = []
        for e in split_set:
           cur_list = []
           for i in range(len(y)):
              if e == split_attr[i]:
                 cur_list.append(y[i])
           ret_list.append(cur_list)
        return ret_list

    # entropy
    def entropy(self, y):
       set_y = set(y)
       n = len(y)
       E = 0
       for s in set_y:
          c = 0
          for e in y:
             if s == e:
                c = c + 1
          if c != 0:
             E = E - c/n*math.log(c/n, 2)
       return E


    def entropy_after_split(self, y, splits):
       n = len(y)
       E_after = 0
       for s in splits:
          E_s = self.entropy(s)
          E_after = E_after + len(s)/n * E_s
       return E_after

    #      class: like                                in code: y
    # attributes: cheese, sauce, spicy, vegetables    in code: attrs
    #     values: mozza
    def train(self, X, y, attrs, prune=False):
       print(X)
       # B = like
       B = ['no', 'yes', 'yes', 'no', 'no', 'yes', 'yes', 'yes']
       # A = cheeese
       A = ['mozza', 'gouda', 'mozza', 'jarls', 'mozza', 'gouda', 'jarls', 'mozza']
       self.split(A, B)
       split_sauce = self.split(A, B)
       E_aft = self.entropy_after_split(B, split_sauce)
       IG_aft = self.entropy(B) - E_aft
       #print(split_sauce)
       #print("IG %f" % (IG_aft, ))

       # A = sauce
       A = ['hllnds', 'tomato', 'tomato', 'bbq', 'bbq', 'tomato', 'hllnds', 'tomato']
       split_sauce = self.split(A, B)
       E_aft = self.entropy_after_split(B, split_sauce)
       IG_aft = self.entropy(B) - E_aft
       #print(split_sauce)
       #print("IG %f" % (IG_aft, ))

       # A = spicy
       A = ['yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'no']
       self.split(A, B)
       split_sauce = self.split(A, B)
       E_aft = self.entropy_after_split(B, split_sauce)
       IG_aft = self.entropy(B) - E_aft
       #print(split_sauce)
       #print("IG %f" % (IG_aft, ))

       # A = vegetables
       A = ['no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'yes']
       self.split(A, B)
       split_sauce = self.split(A, B)
       E_aft = self.entropy_after_split(B, split_sauce)
       IG_aft = self.entropy(B) - E_aft
       #print(split_sauce)
       #print("IG %f" % (IG_aft, ))

        # Doesn't return anything but rather trains a model via ID3
        # and stores the model result in the instance.
        # X is the training data, y are the corresponding classes the
        # same way "fit" worked on SVC classifier in scikit-learn.
        # attrs represents the attribute names in columns order in X.
        #
        # Implementing pruning is a bonus question, to be tested by
        # setting prune=True.
        #
        # Another bonus question is continuously-valued data. If you try this
        # you will need to modify predict and test.
       pass

    def predict(self, instance):
        # Returns the class of a given instance.
        # Raise a ValueError if the class is not trained.
        pass

    def test(self, X, y, display=False):
        # Returns a dictionary containing test statistics:
        # accuracy, recall, precision, F1-measure, and a confusion matrix.
        # If display=True, print the information to the console.
        # Raise a ValueError if the class is not trained.
        result = {'precision':None,
                  'recall':None,
                  'accuracy':None,
                  'F1':None,
                  'confusion-matrix':None}
        if display:
            print(result)
        return result

    def __str__(self):
        # Returns a readable string representation of the trained
        # decision tree or "ID3 untrained" if the model is not trained.
        return "ID3 untrained"

    def save(self, output):
        # 'output' is a file *object* (NOT necessarily a filename)
        # to which you will save the model in a manner that it can be
        # loaded into a new DecisionTree instance.
        pass
