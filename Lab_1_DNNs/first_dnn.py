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


sess = tf.Session()

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

groundTruth = np.argmax(test_y.values,1)#array with index of +1 label for each row e.g [0,1,0,2,1,0,2,2,1,1,0,1]

x = tf.placeholder(tf.float32, shape=[None, n_x])
y = tf.placeholder(tf.float32, shape=[None, n_y])
w = tf.Variable(tf.zeros([n_x,n_y]))
b = tf.Variable(tf.zeros([n_y]))

n_1 = 10 #number of nodes of hidden layer 1
n_2 = 20
n_3 = 10

weights = {
        'w_1': tf.Variable(tf.truncated_normal([n_x, n_1], stddev=0.1)),
        'w_2': tf.Variable(tf.truncated_normal([n_1, n_2], stddev=0.1)),
        'w_3': tf.Variable(tf.truncated_normal([n_2, n_3], stddev=0.1)),
        'w_y': tf.Variable(tf.truncated_normal([n_3, n_y], stddev=0.1))
}

bias = {
        'b_1': tf.Variable(tf.constant(0.1, shape=[n_1])),
        'b_2': tf.Variable(tf.constant(0.1, shape=[n_2])),
        'b_3': tf.Variable(tf.constant(0.1, shape=[n_3])),
        'b_y': tf.Variable(tf.constant(0.1, shape=[n_y]))
}


h_1 = tf.nn.relu(tf.matmul(x, weights['w_1']) + bias['b_1'])
h_2 = tf.nn.relu(tf.matmul(h_1, weights['w_2']) + bias['b_2'])
h_3 = tf.nn.relu(tf.matmul(h_2, weights['w_3']) + bias['b_3'])
predictions_fcn = tf.matmul(h_3, weights['w_y']) + bias['b_y']#dont relu, have to change this!!!

logs_path = "./logs/lab_1/"
g = tf.get_default_graph()

with g.as_default():
    with tf.name_scope('loss'):
        cost_fcn = tf.losses.softmax_cross_entropy(onehot_labels=y, logits=predictions_fcn, scope="Cost_Function")
        tf.summary.scalar('loss', cost_fcn)
    with tf.name_scope('accuracy'):
        #sum( np.equal(myPrediction,groundTruth)) / (len(groundTruth)*1.0)
        accuracy = tf.equal(tf.argmax(predictions_fcn,1),tf.argmax(groundTruth,1))
        accuracy = tf.reduce_sum(tf.cast(accuracy, tf.float32))
        tf.summary.scalar('accuracy', accuracy)

        
merged = tf.summary.merge_all()
train_writer = tf.summary.FileWriter(logs_path + '/train')
test_writer = tf.summary.FileWriter(logs_path + '/test')

optimizer = tf.train.AdagradOptimizer(0.1).minimize(cost_fcn)
sess.run(tf.global_variables_initializer()) 

for epoch in range(3000):
    [_, summary_train] = sess.run([optimizer, merged], feed_dict={x: train_x, y: train_y})
    [myPrediction,summary_test] = sess.run( [predictions_fcn, merged], feed_dict={x: test_x, y: test_y})
    myPrediction = myPrediction.tolist()
    myPrediction = np.argmax(myPrediction,1)

    [accuracy,summary_test] = sess.run( [accuracy, merged], feed_dict={x: test_x, y: test_y})
    
    train_writer.add_summary(summary_train, epoch)
    test_writer.add_summary(summary_test, epoch)

    if epoch % 100 == 0:
        print('Accuracy at epoch:%d =' %epoch,accuracy )


        
        
        


'''Perceptron code
prediction = tf.nn.softmax(tf.matmul(x,w) + b)

cost = tf.reduce_mean(-tf.reduce_sum(y * tf.log(prediction), axis=1))

optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(cost)
sess.run(tf.global_variables_initializer()) 

for epoch in range(1000):
    sess.run([optimizer], feed_dict={x: train_x, y: train_y})
    myPrediction = sess.run(prediction, feed_dict={x: test_x, y: test_y}).tolist()
    myPrediction = np.argmax(myPrediction,1)
    if epoch % 1000 == 0:
        print('Accuracy at epoch:%d =' %epoch,sum(np.equal(myPrediction,groundTruth))/len(groundTruth))
'''
    
    
    
  







#print(a)
#print(b)


#printsum(sum(np.equal(myPrediction2,test_y


    

    