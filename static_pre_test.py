import numpy as np
import cv2
import time
#from googlenet import alexnet2
from alexnet import alexnet
import win32gui
import win32ui
import win32con
import win32api
from getkeys import key_check,keys2output
from keys_input import PressKey,ReleaseKey, W, A, S, D
from collections import deque, Counter
import random
import numpy as np


w = 1280
h = 800
LR = 1e-3
EPOCHS = 8
t_time = 0.09

WIDTH = 160
HEIGHT = 120
#MODEL_NAME = 'pre-bike-{}-{}-{}-epochs.model'.format(LR, 'alexnet2', EPOCHS)
MODEL_NAME = 'pygta5-car-fast-0.001-alexnetv2-10-epochs-300K-data.model'
model = alexnet(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

def main():
    data = np.load('D:/data/pretrained/training_data/training_data-18-balanced.npy')
#df= pd.DataFrame(data)
    id = 1
    while(True):
        img = data[id][0]
        #img = cv2.resize(img,(320,240))
        cv2.imshow('windows', img)
        prediction = model.predict([img.reshape(WIDTH,HEIGHT,1)])[0]
        print(data[id][1])
        print('predicition: {}'.format(prediction))
        print()
        id+=1
        cv2.waitKey()


main()   