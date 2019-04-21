import numpy as np
import cv2
import time
#from googlenet import alexnet2
from model import alexnet2, sterringNet, inception_v3
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

WIDTH = 320
HEIGHT = 200

MODEL_NAME = 'car-front-steering-regression-inceptionv3.model'
model = inception_v3()
#model = alexnet2(WIDTH, HEIGHT, LR, output=2)
model.load(MODEL_NAME)

def main():
    data = np.load('D:/data/v3/car/front/training_data_v3_7.npy')
#df= pd.DataFrame(data)
    id = 0
    while(True):
        if id < data.shape[0]:
            img = data[id][0]
            cv2.imshow('windows', img)
            prediction = model.predict([img.reshape(WIDTH,HEIGHT,3)])[0]
            print(id, data[id][1])
            #pred_val=(prediction[1]-prediction[0])/2.0
            pred_val = prediction[0]
            print('predicition: {}'.format(pred_val/10.0))
            print()
            id += 1
            cv2.waitKey()
        else:
            cv2.waitKey()

main()   
