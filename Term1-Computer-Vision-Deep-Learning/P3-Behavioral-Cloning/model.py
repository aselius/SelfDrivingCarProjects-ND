"""This consists of the training procedures

This includes the training steps through Keras layers and will output
a model.h5 in order to for drive.py to be used in autonomous mode.abs

"""
import h5py
import json
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import pickle
import tensorflow as tf
from tqdm import tqdm
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adam, RMSprop
from keras.utils import np_utils
from keras import backend as K
np.random.seed(42)

pickle_file = 'cam_data.pickle'

with open(pickle_file, 'rb') as f:
    pickle_data = pickle.load(f)
    X_train = pickle_data['train_data']
    y_train = pickle_data['train_label']
    X_valid = pickle_data['valid_data']
    y_valid = pickle_data['valid_label']
    X_test = pickle_data['test_data']
    y_test = pickle_data['test_label']
    del pickle_data
#squash to 0-1 or -0.5 - 0.5
#going with -0.5/0.5 for now for 0 mean
def squash(data):
    data = data/255 - 0.5
    return data

X_train = squash(X_train.astype('float32'))
X_valid = squash(X_valid.astype('float32'))
X_test = squash(X_test.astype('float32'))

print("size of training data features:", X_train.shape)
print("size of training data labels:", y_train.shape)
print("size of validation data features:", X_valid.shape)
print("size of validation data labels:", y_valid.shape)
print("size of test data features:", X_test.shape)
print("size of test data labels:", y_test.shape)

nb_classes = 1
nb_epoch = 10
batch_size = 32
input_shape = X_train.shape[1:]
print(input_shape, 'input shape')

# load model if already compiled

try:
    with open('model.json', 'r') as J:
        model = model_from_json(json.load(J))

    print("found existing models. importing...\n")
    model.compile('adam', 'mse6')
    model.load_weights('model.h5')
    print("model import success...\n")
except:
    #model parameters
    nb_first_filter = 16
    nb_second_filter = 8
    nb_third_filter = 4
    nb_fourth_filter = 2
    pool_size = (2,2)
    kernel_size = (3,3)
    
    #initiate the model
    model = Sequential()
    
    model.add(Convolution2D(
            nb_first_filter, kernel_size[0], kernel_size[1],
            border_mode='valid', input_shape=input_shape))
    model.add(Activation('relu'))
    
    model.add(Convolution2D(
            nb_second_filter, kernel_size[0], kernel_size[1]))
    model.add(Activation('relu'))

    model.add(Convolution2D(
            nb_third_filter, kernel_size[0], kernel_size[1]))
    model.add(Activation('relu'))

    model.add(MaxPooling2D(pool_size=pool_size))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Activation('relu'))
    model.add(Dense(16))
    model.add(Dropout(0.5))
    model.add(Dense(nb_classes))
    
model.summary()

model.compile(loss='mean_squared_error',
              optimizer=Adam(),
              metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch,
          verbose=1, validation_data=(X_valid, y_valid))
score = model.evaluate(X_test, y_test, verbose=0)

print('Test score:', score[0])
print('Test accuracy:', score[1])

if 'model.json' in os.listdir():
    print("The file already exists, overwrite? Y/n \n")
    user_input = input()
    
    if user_input == 'y' or 'Y':
        json_string = model.to_json()
        
        with open('model.json', 'w') as outfile:
            json.dump(json_string, outfile)
            model.save('./model.h5')
            print("overwrite complete")
            
    else:
        print("Aborting..")
else:
    json_string = model.to_json()
    
    with open('model.json', 'w') as outfile:
        json.dump(json_string, outfile)
        model.save('./model.h5')
        print("Save complete.")
