from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten
from tensorflow.keras.models import Sequential
import tensorflow as tf
import os
import cv2
import imghdr
from matplotlib import pyplot as plt
import numpy as np


def limit():
    # 1 is puppy, 0 is kitten
    gpus = tf.config.experimental.list_physical_devices(
        'GPU')  # Listing all physical devices
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(
            gpu, True)  # Limit memory growth

    device = tf.config.list_physical_devices('GPU')


def printImg(data_dir):
    # Print image
    img = cv2.imread(os.path.join(data_dir, 'kitten', '2.png'))
    print(img.shape)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.show()


def checkImg(data_dir, image_exts):
    for image_class in os.listdir(data_dir):
        for image in os.listdir(os.path.join(data_dir, image_class)):
            image_path = os.path.join(data_dir, image_class, image)
            try:
                img = cv2.imread(image_path)
                tip = imghdr.what(image_path)
                if tip not in image_exts:
                    print('Image not in ext list {}'.format(image_path))
                    os.remove(image_path)
            except Exception as e:
                print('Issue with image {}'.format(image_path))
                # os.remove(image_path)
    print("Done!")


def getBatch(data_dir):
    data = tf.keras.utils.image_dataset_from_directory(data_dir)
    data_iterator = data.as_numpy_iterator()
    batch = data_iterator.next()  # Get a batch of images from the dataset
    return batch, data


def checkLabels(batch):
    # Check labels of images
    fig, ax = plt.subplots(ncols=4, figsize=(20, 20))
    for idx, img in enumerate(batch[0][:4]):
        ax[idx].imshow(img.astype(int))
        ax[idx].title.set_text(batch[1][idx])
    plt.show()


def scale(data):
    # Scale the images
    scaled_data = data.map(lambda x, y: (x/255, y))
    scaled_data.as_numpy_iterator().next()
    batch = scaled_data.as_numpy_iterator().next()
    return scaled_data


def splitData(scaled_data):
    # Split the scaled_data into training, validation and test sets
    train_size = int(len(scaled_data)*.7)
    val_size = int(len(scaled_data)*.2)
    test_size = int(len(scaled_data)*.1)+1
    # print(len(scaled_data), train_size, val_size, test_size)
    train = scaled_data.take(train_size)
    val = scaled_data.skip(train_size).take(val_size)
    test = scaled_data.skip(train_size+val_size).take(test_size)
    # print(len(train), len(val), len(test))
    return train, val, test


def createModel():
    # Create the model
    model = Sequential()
    # Architecture:  16 filters, 3x3 kernel, 1 stride, relu activation, input shape 256x256x3
    model.add(Conv2D(16, (3, 3), 1, activation='relu', input_shape=(256, 256, 3)))
    model.add(MaxPooling2D())
    # Architecture:  32 filters, 3x3 kernel, 1 stride, relu activation
    model.add(Conv2D(32, (3, 3), 1, activation='relu'))
    model.add(MaxPooling2D())
    # Architecture:  64 filters, 3x3 kernel, 1 stride, relu activation
    model.add(Conv2D(16, (3, 3), 1, activation='relu'))
    model.add(MaxPooling2D())

    model.add(Flatten())
    # Architecture:  256 neurons, relu activation
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    # adam optimizer, binary crossentropy loss, accuracy metric
    model.compile('adam', loss=tf.losses.BinaryCrossentropy(),
                  metrics=['accuracy'])
    # model.summary()
    return model


def trainModel(model, train, val):
    # Train the model
    logdir = 'logs'
    tensorboard_callback = tf.keras.callbacks.TensorBoard(
        log_dir=logdir)  # Tensorboard callback
    hist = model.fit(train, epochs=20, validation_data=val,
                     callbacks=[tensorboard_callback])
    return hist


def plot(hist):
    # Plot the loss
    fig = plt.figure()
    plt.plot(hist.history['loss'], color='teal', label='loss')
    plt.plot(hist.history['val_loss'], color='orange', label='val_loss')
    fig.suptitle('Loss', fontsize=20)
    plt.legend(loc="upper left")
    plt.show()
    # Plot the accuracy
    fig = plt.figure()
    plt.plot(hist.history['accuracy'], color='teal', label='accuracy')
    plt.plot(hist.history['val_accuracy'],
             color='orange', label='val_accuracy')
    fig.suptitle('Accuracy', fontsize=20)
    plt.legend(loc="upper left")
    plt.show()


def evaluate(model, test):
    # Evaluate the model
    from tensorflow.keras.metrics import Precision, Recall, BinaryAccuracy
    pre = Precision()
    re = Recall()
    acc = BinaryAccuracy()

    for batch in test.as_numpy_iterator():
        X, y = batch
        yhat = model.predict(X)
        pre.update_state(y, yhat)
        re.update_state(y, yhat)
        acc.update_state(y, yhat)

    print(
        f"Precision: {pre.result().numpy()}, Recall: {re.result().numpy()}, Accuracy: {acc.result().numpy()}")


def saveModel(model):
    # Save the model
    model.save(os.path.join('models', 'testKP.h5'))
