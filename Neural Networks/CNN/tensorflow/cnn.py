import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

import constants
import helper_methods

ap = argparse.ArgumentParser()
ap.add_argument('-ind', '--individual', required=False) #This is if the user wishes to train/validate on each CNN indivudally
args = vars(ap.parse_args())

#Import in the data set of images
data = constants.processImgs()

#Get the shape of the images and define their width, height, depth (RGB)
imgShape = data[0].shape

imgWidth = imgShape[0]
imgHeight = imgShape[1]
imgDepth = imgShape[2]

#data
collectiveData = tf.placeholder('float', [None, imgWidth, imgHeight, imgDepth])
ballData = tf.placeholder('float',[None, imgWidth, imgHeight, imgDepth])
bottleData = tf.placeholder('float',[None, imgWidth, imgHeight, imgDepth])
canData = tf.placeholder('float',[None, imgWidth, imgHeight, imgDepth])
paperData = tf.placeholder('float',[None, imgWidth, imgHeight, imgDepth])
backgroundData = tf.placeholder('float',[None, imgWidth, imgHeight, imgDepth])

#labels
collectiveLabels = tf.placeholder('float', [None, constants.class_count])
ballLabels = tf.placeholder('float',[None, 1])
bottleLabels = tf.placeholder('float',[None, 1])
canLabels = tf.placeholder('float',[None, 1])
paperLabels = tf.placeholder('float',[None, 1])
backgroundLabels = tf.placeholder('float',[None, 1])

#Define the 1D array that will hold tensor for the image
tensorShape = int(imgWidth * imgHeight * imgDepth)

weights, bias = {}, {}

#Now we can create the individual CNN's for each object in the data set

#Ball CNN
weights['ballWeight'] = tf.Variable(tf.random_normal([7,7,3,constants.FILTERCOUNT])) #This is the 'kernel' variable, but unlike keras it takes a matrix (height, width, in-channels, out-channels)
bias['ballBias'] = tf.Variable(tf.random_normal([constants.FILTERCOUNT]))
ballConv = tf.nn.conv2d(input=ballData, filter=weights['ballWeight'], strides=[1,1,1,1], padding=constants.PADDING)
ballActivation = tf.nn.relu(ballConv + bias['ballBias'])
weights['ballOutputWeight'] = tf.Variable(tf.random_normal([tensorShape, 1]))
bias['ballOutputBias'] = tf.Variable(tf.random_normal([1]))
ballOutput = tf.reshape(ballActivation, shape=[-1, tensorShape])
ballPrediction = tf.matmul(ballOutput, weights['ballOutputWeight']) + bias['ballOutputBias']

#This is for training on individual components, so the loss/optimization is done solely on this object
# ballLoss = tf.nn.sigmoid_cross_entropy_with_logits(logits=ballPrediction, labels=ballLabels)
# ballOptimizer = tf.train.AdamOptimizer(learning_rate=constants.learningrate).minimize(ballLoss)


#Bottle CNN
weights['bottleWeight'] = tf.Variable(tf.random_normal([7,7,3,constants.FILTERCOUNT])) #This is the same as the 'filter' variable (height, width, in-channels, out-channels)
bias['bottleBias'] = tf.Variable(tf.random_normal([constants.FILTERCOUNT]))
bottleConv = tf.nn.conv2d(input=bottleData, filter=weights['bottleWeight'], strides=[1,1,1,1], padding=constants.PADDING)
bottleActivation = tf.nn.relu(bottleConv + bias['bottleBias'])
weights['bottleOutputWeight'] = tf.Variable(tf.random_normal([tensorShape, 1]))
bias['bottleOutputBias'] = tf.Variable(tf.random_normal([1]))
bottleOutput = tf.reshape(bottleActivation, shape=[-1, tensorShape])
bottlePrediction = tf.matmul(ballOutput, weights['bottleOutputWeight']) + bias['bottleOutputBias']

# bottleLoss = tf.nn.sigmoid_cross_entropy_with_logits(logits=bottlePrediction, labels=bottleLabels)
# bottleOptimizer = tf.train.AdamOptimizer(learning_rate=constants.learningrate).minimize(bottleLoss)


#Can CNN
weights['canWeight'] = tf.Variable(tf.random_normal([7,7,3,constants.FILTERCOUNT])) #This is the same as the 'filter' variable (height, width, in-channels, out-channels)
bias['canBias'] = tf.Variable(tf.random_normal([constants.FILTERCOUNT]))
canConv = tf.nn.conv2d(input=canData, filter=weights['canWeight'], strides=[1,1,1,1], padding=constants.PADDING)
canActivation = tf.nn.relu(canConv + bias['canBias'])
weights['canOutputWeight'] = tf.Variable(tf.random_normal([tensorShape, 1]))
bias['canOutputBias'] = tf.Variable(tf.random_normal([1]))
canOutput = tf.reshape(canActivation, shape=[-1, tensorShape])
canPrediction = tf.matmul(ballOutput, weights['canOutputWeight']) + bias['canOutputBias']

# canLoss = tf.nn.sigmoid_cross_entropy_with_logits(logits=canPrediction, labels=canLabels)
# canOptimizer = tf.train.AdamOptimizer(learning_rate=constants.learningrate).minimize(canLoss)


#Paper CNN
weights['paperWeight'] = tf.Variable(tf.random_normal([7,7,3,constants.FILTERCOUNT])) #This is the same as the 'filter' variable (height, width, in-channels, out-channels)
bias['paperBias'] = tf.Variable(tf.random_normal([constants.FILTERCOUNT]))
paperConv = tf.nn.conv2d(input=paperData, filter=weights['paperWeight'], strides=[1,1,1,1], padding=constants.PADDING)
paperActivation = tf.nn.relu(paperConv + bias['paperBias'])
weights['paperOutputWeight'] = tf.Variable(tf.random_normal([tensorShape, 1]))
bias['paperOutputBias'] = tf.Variable(tf.random_normal([1]))
paperOutput = tf.reshape(paperActivation, shape=[-1, tensorShape])
paperPrediction = tf.matmul(paperOutput, weights['paperOutputWeight']) + bias['paperOutputBias']

# paperLoss = tf.nn.sigmoid_cross_entropy_with_logits(logits=paperPrediction, labels=paperLabels)
# paperOptimizer = tf.train.AdamOptimizer(learning_rate=constants.learningrate).minimize(paperLoss)


#Background CNN
weights['backgroundWeight'] = tf.Variable(tf.random_normal([7,7,3,constants.FILTERCOUNT]))
bias['backgroundBias'] = tf.Variable(tf.random_normal([constants.FILTERCOUNT]))
backgroundConv = tf.nn.conv2d(input=backgroundData, filter=weights['backgroundWeight'], strides=[1,1,1,1], padding=constants.PADDING)
backgroundActivation = tf.nn.relu(backgroundConv + bias['backgroundBias'])
weights['backgroundOutputWeight'] = tf.Variable(tf.random_normal([tensorShape, 1]))
bias['backgroundOutputBias'] = tf.Variable(tf.random_normal([1]))
backgroundOutput = tf.reshape(backgroundActivation, shape=[-1, tensorShape])
backgroundPrediction = tf.matmul(backgroundOutput, weights['backgroundOutputWeight']) + bias['backgroundOutputBias']



#Now that all the individual CNN's are formed, the predicitons from these join to make the final NN
stackedPredictions = tf.stack([ballPrediction, bottlePrediction, canPrediction, paperPrediction, backgroundPrediction])
rawPredictions = stackedPredictions[:, :, 0]

weights['final'] = tf.Variable(tf.random_normal([5,5])) #5 classes of objects
bias['final'] = tf.Variable(tf.random_normal([5]))
finalPrediction = tf.matmul(rawPredictions, weights['final']) + bias['final']
finalLoss = tf.nn.sigmoid_cross_entropy_with_logits(logits=finalPrediction, labels=collectiveLabels)
finalOptimizer = tf.train.AdamOptimizer(learning_rate=constants.learningrate).minimize(finalLoss)

"""
Need to now split our data for training/validation
The data split can be used for individual training as well
"""

groupLabels = constants.createLabels()
print(groupLabels.shape)

#Now for the learning/training of the model, as well as the validation
with tf.Session() as sess:
    trainingAcc = 0.0
    trainingData, trainingLabels, validationData, validationLabels = helper_methods.separateTraining(validationSplit=0.8)
    for epoch in range(constants.EPOCHCOUNT):
        print(f"Epoch #{epoch}:")
        batchData, batchLabels = helper_methods.getBatchData(constants.BATCHSIZE, trainingData, trainingLabels)

        #This is for the collective group (5 object optimization)
        finalOptimizer.run(feed_dict={collectiveData: batchData, collectiveLabels: batchLabels})