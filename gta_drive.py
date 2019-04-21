import numpy as np
from PIL import ImageGrab
import cv2
import time
from getkeys import key_check,keys2output
from statistics import mean
from keys_input import PressKey,W,S,A,D
from get_training_data import training_data, file_name


th_low = 244
th_high = 309


def forward():
    PressKey(W)
    ReleaseKey(A)
    ReleaseKey(D)

def left():
    PressKey(A)
    ReleaseKey(W)
    ReleaseKey(D)
    ReleaseKey(A)

def right():
    PressKey(D)
    ReleaseKey(A)
    ReleaseKey(W)
    ReleaseKey(D)

def slide():
    ReleaseKey(W)
    ReleaseKey(A)
    ReleaseKey(D)


def screen_record():
    pass

        #if key == ord('w'):
        #    if th_low < th_high - 1: th_low+=1
        #if key == ord('s'):
        #    if th_low > 1: th_low-=1
        #if key == ord('e'):
        #    if th_high < 1024: th_high+=1
        #if key == ord('d'):
        #    if th_high > th_low + 1 : th_high-=1

def proc_image(image):
    global th_low
    global th_high
    original_image = image
    proc_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    proc_image = cv2.Canny(proc_image, threshold1=th_low, threshold2=th_high)

    vertices = np.array([[10,790],[10,500],[400,200],[880,200],[1270,500],[1270,790]],np.int32)
    proc_image = detect_region(proc_image, [vertices])
    blur_img = cv2.GaussianBlur(proc_image, (3,3),0)
    lines = cv2.HoughLinesP(blur_img, 1,np.pi / 180,180, 20,15)
    drawLines(proc_image, lines)
    return proc_image

def drawLines(img, lines):
    if lines is not None:
        for line in lines:
            coords = line[0]
            cv2.line(img,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],5)

def detect_region(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,vertices,255)
    masked = cv2.bitwise_and(img, mask)
    return masked

def main():
    for i in list(range(4))[0:0:-1]:
        print(i + 1)
        time.sleep(1)
        
    pause = False
    global th_low
    global th_high
    last_time = time.time()
    while True:
        if(not pause):
            key_pressed = key_check()
            output = keys2output(key_pressed)
            printscreen = np.array(ImageGrab.grab(bbox=(0,40,1280,840)))
            edge_screen = proc_image(printscreen) 
            time_used = time.time() - last_time
            print('fps: {}'.format(1 / time_used))
            #print('TH: {}-{}'.format(th_low,th_high))
            last_time = time.time()
            #cv2.imshow('window', cv2.cvtColor(printscreen,cv2.COLOR_BGR2RGB))
            cv2.imshow('edges', edge_screen)
            training_data.append([printscreen ,output])

        key = cv2.waitKey(10)
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
        if(key == ord('p')):
            pause = not pause

        if len(training_data)% 500 ==0:
            print(len(training_data))
            np.save(file_name, training_data)     

