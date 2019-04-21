import numpy as np
import cv2
import time
from googlenet import alexnet2
#from alexnet import alexnet
import win32gui
import win32ui
import win32con
import win32api
from getkeys import key_check,keys2output
from keys_input import PressKey,ReleaseKey, W, A, S, D
from collections import deque, Counter
import random
import numpy as np


w = 800
h = 600
LR = 1e-3
EPOCHS = 8
t_time = 0.05
def straight():
    if random.randrange(10) == 1:
        PressKey(W)
        #time.sleep(0.2)
        #ReleaseKey(W)
        ReleaseKey(A)
        ReleaseKey(D)

def left():
    PressKey(W)
    PressKey(A)
    #ReleaseKey(W)
    ReleaseKey(D)
    #ReleaseKey(A)
    time.sleep(t_time)
    ReleaseKey(A)
    ReleaseKey(W)

def right():
    PressKey(W)
    PressKey(D)
    ReleaseKey(A)
    #ReleaseKey(W)
    #ReleaseKey(D)
    time.sleep(t_time)
    ReleaseKey(D)
    ReleaseKey(W)

WIDTH = 160
HEIGHT = 120
#MODEL_NAME = 'pygta5-car-fast-0.001-alexnetv2-10-epochs-300K-data.model'
MODEL_NAME = 'pre-bike-{}-{}-{}-epochs.model'.format(LR, 'alexnet2', EPOCHS)
model = alexnet2(WIDTH, HEIGHT, LR, output=3)
model.load(MODEL_NAME)

def main():
    last_time = time.time()
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    mode_choice = 0

    hwnd = win32gui.FindWindow(None, 'Grand Theft Auto V')
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()

    while(True):
        if not paused:
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(dcObj, w, h)
            cDC.SelectObject(bmp)
            cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
            arr = bmp.GetBitmapBits(True)
            cap = np.fromstring(arr, dtype='uint8')
            cap.shape = (h, w, 4)
            cap = cap[..., :3]
            screen = cap
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            screen = cv2.resize(screen,(160,120))
            cv2.imshow('windows', screen)
            cv2.waitKey(1)
            last_time = time.time()


            prediction = model.predict([screen.reshape(WIDTH,HEIGHT,1)])[0]


            turn_thresh = 0.75
            fwd_thresh = 0.70

            print(prediction)
            if prediction[1] > fwd_thresh:
                straight()
                print("straight")
            elif prediction[0] > turn_thresh:
                left()
                print("left")
            elif prediction[2] > turn_thresh:
                right()
                print("right")
            else:
                straight()
                print("straight")



            
        keys = key_check()

        # p pauses game and can get annoying.
        if 'T' in keys:
            if paused:
                paused = False
                time.sleep(1)
            else:
                paused = True
                time.sleep(1)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(bmp.GetHandle())

main()   