import numpy as np
import matplotlib.pyplot as plt

def import_from_csv(path, pixel_depth, length, class_num):
    train_database = np.genfromtxt('{}'.format(path), delimiter=",", dtype=int)[1:,:]
    train_labels = train_database[:,0].reshape(length,)
    training_labels = np.eye(class_num)[train_labels]
    training_data = np.delete(train_database,0,1)
    return normalize(training_data, pixel_depth), training_labels, train_labels

def normalize(image_data, pixel_depth):
    data = (image_data - pixel_depth / 2) / pixel_depth
    return data.astype(np.float32)

training_data, training_labels, correct_index = import_from_csv('/Users/JAustin/Desktop/MNIST/train.csv', 255, 42000, 10)

test_labels = np.eye(10)[np.genfromtxt('{}'.format('/Users/JAustin/Desktop/MNIST/results_net4.csv'), delimiter=",", dtype=int)[1:, 1]]
test_data = normalize(np.genfromtxt('{}'.format('/Users/JAustin/Desktop/MNIST/test.csv'), delimiter=",", dtype=int)[1:, :], 255)


#training_data = np.random.rand(20000, 784)
#correct_index = np.random.choice(10, np.shape(training_data)[0])
#training_labels = np.eye(10)[correct_index]

#training_data = np.random.rand(10000, 784)
#training_weights = np.random.rand(10, 784)
#X = np.dot(training_data, training_weights.T)
#training_labels = X / np.sum(X, axis=1).reshape(10000,1)


data_size = np.shape(training_data)[0] # 20000
num_params = np.shape(training_data)[1] # 784
num_classes = np.shape(training_labels)[1] # 10

weights = np.random.rand(num_classes, num_params) # or randn
biases = np.random.rand(num_classes, 1)

batch_size = 256
iterations = 2000

momentum_rate = .9
threshold = .3


# learning_rate = np.array([.01*(1 - x/iterations) for x in range(iterations)]) # linear learning rate
learning_rate = .3*np.exp(-5*np.arange(0,iterations)/iterations) # exponential learning rate
# learning_rate = .01 * np.ones(iterations) # constant learning rate

def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=1)[:,None]

def predict(data, batch_size, weights, biases):
    index = np.random.choice(len(data), batch_size, replace=False)
    output = np.dot(data[index], weights.T) + biases.T #np.dot(weights[:,np.newaxis], np.transpose(data[index])) + biases
    return index, softmax(output)

def evaluate(data, labels, weights, biases, batch_size):
    index = np.random.choice(len(data), batch_size, replace=False)
    accuracy = (np.argmax(softmax(np.dot(data[index], weights.T) + biases.T), axis=1)==np.argmax(labels[index], axis=1)).sum() * 100 / batch_size
    print("The accuracy of your model is %s%%!" % accuracy)
    return accuracy, index

def conditional_evaluate(data, labels, weights, biases, batch_size, threshold):
    index = np.random.choice(len(data), batch_size, replace=False)
    prediction = np.argmax(softmax(np.dot(data[index], weights.T) + biases.T), axis=1)
    accuracy = (np.argmax(softmax(np.dot(data[index], weights.T) + biases.T), axis=1) == np.argmax(labels[index],axis=1)).sum() * 100 / batch_size
    unsure = np.where(np.max(softmax(np.dot(data[index], weights.T) + biases.T), axis=1) < threshold)[0]
    print("The accuracy of your model is %s%%! The model is unsure about %s%%" % (accuracy, len(unsure)*100/batch_size))
    return accuracy, index, unsure, prediction

def check(data, prediction, index, dim=28, test_labels = None):
    img = data[index].reshape(dim, dim)
    print('The model thinks this number is a %s.' % prediction[index])
    if not test_labels is None: print('The provided labels think this number is a %s' % test_labels[index])
    plt.imshow(img)

def check_unsure(arr):
    for i in range(len(arr)):
        check(test_data, prediction, arr[i], test_labels = test_labels)
        plt.figure(i+1)

def gradient_descent(data, labels, weights, biases, batch_size, iterations, learning_rate, momentum_rate):
    weight_momentum = np.zeros_like(weights)
    bias_momentum = np.zeros_like(biases)
    gamma = momentum_rate
    for i in range(iterations):
        temp_weights = weights - gamma*weight_momentum
        temp_biases = biases - gamma*bias_momentum
        index, prediction = predict(data, batch_size, temp_weights, temp_biases)
        loss = - np.tensordot(labels[index], np.log(prediction), axes=2) / batch_size # + .1*np.linalg.norm(weights)**2 # cross entropy loss
        if i % 50 == 0: print("Loss at step %s is %s" % (i, loss))
        if i % 1000 == 0: conditional_evaluate(test_data, test_labels, weights, biases, len(test_data), threshold)
        error_arr = prediction - labels[index]
        dW = np.sum(error_arr[..., None] * data[index][:, None, :], axis=0) / batch_size
        dB = np.sum(error_arr, axis=0)[:, None] / batch_size
        weight_momentum = gamma*weight_momentum + learning_rate[i]*dW
        bias_momentum = gamma*bias_momentum + learning_rate[i]*dB
        weights -= weight_momentum
        biases -= bias_momentum

    return weights, biases

new_weights, new_biases = gradient_descent(training_data, training_labels, weights, biases, batch_size, iterations, learning_rate, momentum_rate)
accuracy, index, unsure, prediction = conditional_evaluate(training_data, training_labels, new_weights, new_biases, batch_size, threshold) # probably should be larger than batch_size

conditional_evaluate(test_data, test_labels, weights, biases, len(test_data), threshold)

