############################################################
#                                                          #
#  Code for Lab 1: Your First Fully Connected Layer  #
#                                                          #
############################################################


import tensorflow as tf
import os
import os.path
import numpy as np
import pandas as pd
#sess = tf.Session()

data = pd.read_csv("https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data", sep=",",
                   names=["sepal_length", "sepal_width", "petal_length", "petal_width", "iris_class"])
#

np.random.seed(0)
data = data.sample(frac=1).reset_index(drop=True)#shuffles data but keeps indices in place

#
all_x = data[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']] #keep just those columns
#

all_y = pd.get_dummies(data.iris_class) #make 3 y columns with 0 or 1 for each class
#

n_x = len(all_x.columns)# 4 features
n_y = len(all_y.columns)# 3 classes

train_x, test_x = np.split(all_x,[100])

train_y, test_y = np.split(all_y,[100])


