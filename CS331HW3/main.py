

import math
import functools
import re

def concat(ls):
    acum = []
    for l in ls:
        acum += l
    return acum

def parse(data):
    def clean_sentence(unparsed):
        sentence = unparsed.rstrip().split(' ')
        sentence = [re.sub(r'[^\w]','',w.rstrip()) for w in sentence]
        return [w.lower() for w in sentence if w != '']

    rawlines = data.readlines()
    lines = [list(l.rstrip().split("\t")) for l in rawlines if l.rstrip() != '']
    lines = [[clean_sentence(l[0]),int(l[1])] for l in lines]
    return lines

data = open("./trainingSet.txt")
training_data = parse(data)

vocabulary = sorted(list(set(concat([l[0] for l in training_data]))))

import sys

data = open(sys.argv[1] or "./testSet.txt") # open("./testSet.txt")
test_data = parse(data)

def to_vector(item,vocabulary):
    sentence = item[0]
    class_label = item[1]
    vector = []
    for word in vocabulary:
        characteristic = 1 if word in sentence else 0
        vector.append(characteristic)
    vector.append(class_label)
    return vector

def to_matrix(items,vocabulary):
    return [to_vector(item,vocabulary) for item in items]

vectorized_training_data = to_matrix(training_data,vocabulary)
vectorized_test_data = to_matrix(test_data,vocabulary)

def pp_matrix(mat,vocabulary):
    lines =  [','.join(word for word in vocabulary + ['classlabel'])]
    lines += [','.join(str(bit) for bit in vec) for vec in mat]
    return '\n'.join(line for line in lines)


training_data_formatted = pp_matrix(vectorized_training_data,vocabulary)
test_data_formatted = pp_matrix(vectorized_test_data,vocabulary)


def write_file(filename,content):
    f = open(filename,'w')
    f.write(content)
    f.close()


write_file('./preprocessed_train.txt',training_data_formatted)
write_file('./preprocessed_test.txt',test_data_formatted)


class memoized2(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    def __init__(self, func):
        self.func = func
        self.cache = {}
    def __call__(self, *args):
        try:
            return self.cache[args]
        except KeyError:
            value = self.func(*args)
            self.cache[args] = value
            return value
        except TypeError:
            # uncachable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            return self.func(*args)
    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__
    def __get__(self, obj, objtype):
        """Support instance methods."""
        fn = functools.partial(self.__call__, obj)
        fn.reset = self._reset
        return fn
    def _reset(self):
        self.cache = {}

class Bayes(object):
    def __init__(self,feature_matrix,column_labels):
        self.column_labels = column_labels + ['classlabel']
        self.feature_matrix = feature_matrix

    @memoized2
    def feature_estimate(self,feature_name,feature_value,class_label_value):
        feature_idx = self.column_labels.index(feature_name)
        class_label_name = self.column_labels[-1]
        class_label_idx = self.column_labels.index(class_label_name)
        conditional_selected_rows = [row for row in self.feature_matrix 
                                        if row[feature_idx] == feature_value 
                                        and row[class_label_idx] == class_label_value]   
        class_label_selected_rows = [row for row in self.feature_matrix
                                        if row[class_label_idx] == class_label_value]
        return (len(conditional_selected_rows) + 1)/(len(class_label_selected_rows) + 2)

    @memoized2
    def class_label_estimate(self,value):
        attribute = self.column_labels[-1]
        attribute_idx = self.column_labels.index(attribute)
        selected_rows = [row for row in self.feature_matrix if row[attribute_idx] == value]
        return len(selected_rows)/len(self.feature_matrix)
    
    def prediction_probability(self,feature_vector,class_label_value):
        summed = 0
        for idx in range(len(feature_vector)):
            feature_name = self.column_labels[idx]
            feature_value = feature_vector[idx]
            summand = self.feature_estimate(feature_name,feature_value,class_label_value)
            summed += math.log(summand)
            
        class_label_prob = self.class_label_estimate(class_label_value)
        summed += math.log(class_label_prob)
        return summed


        # prod = 1
        # for idx,observation in enumerate(feature_vector):
        #     feature_name = self.column_labels[idx]
        #     prod *= self.feature_estimate(feature_name,observation,class_label_value)
        # class_label_prob = self.class_label_estimate(class_label_value)
        # prod *= class_label_prob
        # return prod
    
    def predict(self,feature_vector):
        a = self.prediction_probability(feature_vector,0)
        b = self.prediction_probability(feature_vector,1)
        if a >= b: return 0
        return 1



bn = Bayes(vectorized_training_data,vocabulary)
correct_guesses = 0
total_guesses   = 0
for test_case in vectorized_test_data:

    actual = test_case[-1]
    guess  = bn.predict(test_case[:-1])

    if guess == actual:
        correct_guesses += 1
    total_guesses += 1
    accuracy = round(correct_guesses/total_guesses,4)
    print(f'[accuracy={accuracy}] Actual: {actual}, Predicted: {guess}')

# print(vocabulary)
# print(vectorized_test_data)
# print(test_data_formatted)
