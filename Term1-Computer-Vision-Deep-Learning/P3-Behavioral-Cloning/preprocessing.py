""" Preprocessing Step

This will be used to translate the csv and pngs into a workable NumPy
Array using Pickle. This utilized not just the central camera, but also
the 

"""

import csv
import pickle
import matplotlib.pyplot as plt
import numpy as np
import os
from tqdm import tqdm

## import csv
csv_path = "./driving_log.csv"

data = []
with open(csv_path) as file:
    reader = csv.reader(file)
    for i in reader:
        data.append(i)

csv_size = len(data)
print("%d data points imported" % csv_size)

## define a image conversion function
# data 0,1,2th column in a row are center, left and right images

features = ()
labels = ()

def crop_image(image):
    """crops the image down to 18x80

    and uses the red channel from rgb
    """
    image = image[65:135:4, 0:-1:4, 0]
    return image

def flatten_image(image):
    """flattens the image data into one list
    """
    image = image.flatten().tolist()
    return image

def import_image(data_row_column):
    """imports the image data from path data
    """
    img = plt.imread(data_row_column.strip())
    return img

## store the images in a 3xn array i imagine to keep the consistency in angles per frame
## store the angles as labels
## flatten images

for i in tqdm(range(int(len(data))), unit='items'):
    for j in range(3):
        cropped_image = crop_image(import_image(data[i][j]))
        features += (flatten_image(cropped_image),)
        labels += (float(data[i][3]),)

features = np.array(features).reshape(len(features), 18, 80, 1)
print("shape of features array is", features.shape)
labels = np.array(labels)
print("shape of labels array is", labels.shape)

## split train and validation using train test split
from sklearn.model_selection  import train_test_split

# split the dataset into training data and test data
X_train, X_test, y_train, y_test = train_test_split(
    features,
    labels,
    test_size=0.20,
    random_state=42)

# split the training set into train and validation sets
X_train, X_valid, y_train, y_valid = train_test_split(
    X_train,
    y_train,
    test_size=0.20,
    random_state=42)

## output the result (X_train, X_val, y_train, y_val) in pickle for further analysis
output_file = 'cam_data.pickle'
iterate = True

while iterate:
    if not os.path.isfile(output_file):
        print('Pickle file not found. Saving data to pickle file.')
        try:
            with open(output_file, 'wb') as pfile:
                pickle.dump(
                    {
                        'train_data': X_train,
                        'train_label': y_train,
                        'valid_data': X_valid,
                        'valid_label': y_valid,
                        'test_data': X_test,
                        'test_label': y_test
                    },
                    pfile, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print('Unable to save pickle file :', e)
            raise
        print('Save complete')
        iterate = False
    else:
        print('pickle file with default output name found. please enter an alternate name')
        output_file = input("Alternate name: ")
