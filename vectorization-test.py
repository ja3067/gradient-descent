# import tensorflow as tf
import numpy as np
import os

""" def import_from_csv(path, pixel_depth):
    train_database = np.genfromtxt('{}'.format(path), delimiter=",", dtype=int)[1:,:]
    train_labels = train_database[:,0].reshape(42000,1)
    training_labels = np.eye(len(train_labels))[train_labels]
    training_data = np.delete(train_database,0,1)
    return normalize(training_data), training_labels, train_labels

def normalize(image_data, pixel_depth):
    data = (image_data - pixel_depth / 2) / pixel_depth
    return data.astype(np.float32) """

training_data = np.random.rand(200, 200)
correct_index = np.random.choice(10, np.shape(training_data)[0])
training_labels = np.eye(10)[correct_index]

#training_data = np.random.randn(20000, 200)
#training_weights = np.random.randn(10, 200)
#X = np.dot(training_data, training_weights.T)
#training_labels = X / np.sum(X, axis=1).reshape(20000,1)

# training_data, training_labels, correct_index = import_from_csv('/Users/JAustin/Desktop/MNIST/train.csv', 255)

data_size = np.shape(training_data)[0] # 20000
num_params = np.shape(training_data)[1] # 784
num_classes = np.shape(training_labels)[1] # 10

weights = np.random.rand(num_classes, num_params) # or randn
biases = np.random.rand(num_classes, 1)

batch_size = 200
iterations = 1000

# learning_rate = np.array([.01*(1 - x/iterations) for x in range(iterations)]) # linear learning rate
learning_rate = .15*np.exp(-5*np.arange(0,iterations)/iterations) # exponential learning rate
# learning_rate = .01 * np.ones(iterations) # constant learning rate

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=1)[:,None]

def predict(data, batch_size, weights, biases):
    index = np.random.choice(len(data), batch_size, replace=False)
    output = np.dot(data[index], weights.T) + biases.T #np.dot(weights[:,np.newaxis], np.transpose(data[index])) + biases
    return index, softmax(output)

def evaluate(data, labels, weights, biases, batch_size):
    index = np.random.choice(len(data), batch_size, replace=False)
    accuracy = (np.argmax(softmax(np.dot(data[index], weights.T) + biases.T), axis=1)==np.argmax(training_labels[index], axis=1)).sum()*100/batch_size
    print("The accuracy of your model is %s%%!" % accuracy)
    return accuracy, index

def gradient_descent(data, labels, weights, biases, batch_size, iterations, learning_rate):
    for i in range(iterations):
        index, prediction = predict(data, batch_size, weights, biases)
        loss = - np.tensordot(training_labels[index], np.log(prediction), axes=2) # + .1*np.linalg.norm(weights)**2 # cross entropy loss
        print("Loss at step %s is %s" % (i, loss))
        dW = np.zeros_like(weights)
        dB = np.zeros_like(biases)
        for j in range(np.shape(weights)[0]):
            for k in range(np.shape(weights)[1]):
                dW[j,k]=np.sum((prediction - labels[index])[:, j]*data[index][:, k]) / batch_size
                #delta_w[j, k] = np.dot((prediction-labels[index])[:, j], data[index][:, k]) / batch_size
        for j in range(len(biases)):
            dB[j]=np.sum((prediction - labels[index])[:,j]) / batch_size

        weights = weights - learning_rate[i]*dW
        biases = biases - learning_rate[i]*dB

    return weights, biases

new_weights, new_biases = gradient_descent(training_data, training_labels, weights, biases, batch_size, iterations, learning_rate)
accuracy, index = evaluate(training_data, training_labels, new_weights, new_biases, batch_size) # probably should be larger than batch_size