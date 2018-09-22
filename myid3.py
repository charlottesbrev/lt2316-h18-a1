# Module file for implementation of ID3 algorithm.

# You can add optional keyword parameters to anything, but the original
# interface must work with the original test file.
# You will of course remove the "pass".

import os, sys, math
import numpy
# You can add any other imports you need.

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

    def all_positive(self, Examples):
       for x in Examples:
          if x < 0:
             return false
       return true

    def all_negative(self, ):
       for x in Examples:
          if x > 0:
             return false
       return true

    def most_common_attribute_value(self, Examples, Target_Attribute):
       pass
       # ?????????????????????????????
       # how do we find the most common attribte value?
       #most_common = least_common_value
       #for e in Example:
       #   if is_more_common(e, some_value)
       #      most_common = e
       #return most_common

    def best_classified_attribute(self, Examples, Attributes):
       # ???????????????????????????????
       # what is meant with a best classified attribute?
       pass

    def most_common_target_value(self, Examples, v_i):
       # ???????????????????????????????
       # what is meant with a most common target value?
       # do we need more arguments?
       pass

    def subset_with_value(self, Examples, A, v_i):
       out = []
       for e in Examples:
       # ???????????????????????????
       # how should we determine what to add to the returning set 'out'?
       # do we need 'A' for something or not?
          if e == v_i:
              out.append(e)
       return out

    def subtract_from_set(self, Attribute, A):
       out = []
       for a in Attribute:
          if not exist(a, A):
             out.append(a)
       return out

    def ID3(self, Examples, Target_Attribute, Attributes):
        # Create a root node for the tree
        Root = {}
        # If all examples are positive, return the single-node tree Root, with label = +.
        if all_positive(Examples):
           Root.label = '+'
           return Root
        # If all examples are negative, return the single-node tree Root, with label = -.
        if all_negative(Examples):
           Root.label = '-'
           return Root
        # If number of predicting attributes is empty, then Return the single node tree Root,
        # with label = most common value of the target attribute in the examples.
        if Attributes is None:
           Root.label = most_common_attribute_value(Examples, Target_Attribute)
           return Root
        # Otherwise Begin
        #    A = The Attribute that best classifies examples.
        #    Decision Tree attribute for Root = A
           A = best_classified_attribute(Examples, Attributes)
           Root.decision_tree_attribute = A
        #    For each possible value, v_i, of A
           for v_i in A:
        #       Add a new tree branch below Root, corresponding to the test A = v_i.
              tree_branch = ...
        #       Let Examples(v_i) be the subset of examples that have the value v_i for A
        #       If Examples(v_i) is empty
        #          Then below this new branch add a leaf node with label = most common target value in the examples
        #       Else
        #          below this new branch add the subtree ID3(Examples(v_i), Target_Attribute, Attributes - {A})
              if test(A, v_i):
                 Root.branches += ...
              # ????????????????????????????
              # I don't know what test should do...
              # should we just compare A to v_i? but is not v_i the elements of A?
              sub = subset_with_value(Examples, A, v_i)
              if sub is empty:
                 tree_branch.leaf = ...
                 tree_branch.leaf.label = most_common_target_value(Examples, v_i)
              else:
                 NewAttribute = subtract_from_set(Attribute, A) # Attribute - {A}
                 # ???????????????????????????????
                 # should all elements in A be excluded from Attribute in the row above?
                 tree_branch.subtree = ID3(self, sub, Target_Attribute, NewAttribute)

        # End
        return Root

    def split(self, split, y):
       split_set = set(split)
       ret_list = []
       for e in split_set:
          cur_list = []
          for i in range(len(y)):
             if e == split[i]:
                cur_list.append(y[i])
          ret_list.append(cur_list)
       return ret_list

    # entropy
    def ent(self, y):
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


    def ent_aft(self, y, splits):
       n = len(y)
       E_after = 0
       for s in splits:
          E_s = self.ent(s)
          E_after = E_after + len(s)/n * E_s
       return E_after

    #      class: like                                in code: y
    # attributes: cheese, sauce, spicy, vegetables    in code: attrs
    #     values: mozza
    def train(self, X, y, attrs, prune=False):
       # B = like
       B = ['no', 'yes', 'yes', 'no', 'no', 'yes', 'yes', 'yes']
       # A = cheeese
       A = ['mozza', 'gouda', 'mozza', 'jarls', 'mozza', 'gouda', 'jarls', 'mozza']
       self.split(A, B)
       split_sauce = self.split(A, B)
       print(split_sauce)
       E_aft = self.ent_aft(B, split_sauce)
       IG_aft = self.ent(B) - E_aft
       print("IG %f" % (IG_aft, ))

       # A = sauce
       A = ['hllnds', 'tomato', 'tomato', 'bbq', 'bbq', 'tomato', 'hllnds', 'tomato']
       split_sauce = self.split(A, B)
       print(split_sauce)
       E_aft = self.ent_aft(B, split_sauce)
       IG_aft = self.ent(B) - E_aft
       print("IG %f" % (IG_aft, ))

       # A = spicy
       A = ['yes', 'no', 'yes', 'no', 'yes', 'yes', 'yes', 'no']
       self.split(A, B)
       split_sauce = self.split(A, B)
       print(split_sauce)
       E_aft = self.ent_aft(B, split_sauce)
       IG_aft = self.ent(B) - E_aft
       print("IG %f" % (IG_aft, ))

       # A = vegetables
       A = ['no', 'no', 'no', 'no', 'yes', 'yes', 'yes', 'yes']
       self.split(A, B)
       split_sauce = self.split(A, B)
       print(split_sauce)
       E_aft = self.ent_aft(B, split_sauce)
       IG_aft = self.ent(B) - E_aft
       print("IG %f" % (IG_aft, ))

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
