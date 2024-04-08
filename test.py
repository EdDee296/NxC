from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.models import Sequential
import tensorflow as tf
import os
import cv2
import imghdr
from matplotlib import pyplot as plt
import numpy as np
from tensorflow.keras.models import load_model

new_model = load_model(os.path.join('models','testKP.h5'))
# Test the model
img = cv2.imread('1.jpeg')
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

resize = tf.image.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (256, 256))
plt.imshow(resize.numpy().astype(int))
plt.show()

yhat = new_model.predict(np.expand_dims(resize/255, 0))
print(yhat)
if yhat > 0.5: # 1 is puppy, 0 is kitten
    print(f'Predicted class is Puppy')
else:
    print(f'Predicted class is Kitten')
