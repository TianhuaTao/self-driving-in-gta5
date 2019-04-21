import os
import numpy as np
import time
import win32gui
import win32ui
import win32con
import win32api
from getkeys import key_check,keys2output
from PIL import ImageGrab
import cv2
latest_data_id = 0
file_name_template = 'D:/data/v2/training_data_v2_{}.npy'
training_data = []
print('Looking for previous data...')
while os.path.isfile(file_name_template.format(latest_data_id)):
    latest_data_id+=1
print('New data will be stored as {}'.format(file_name_template.format(latest_data_id)))

w = 1280
h = 800

def main():
    global training_data
    global latest_data_id

    for i in list(range(5)):
        print(5 - i)
        time.sleep(1)
        

    last_time = time.time()
    paused = False

    hwnd = win32gui.FindWindow(None, 'Grand Theft Auto V')
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    while True:      
        if not paused:
            key_pressed = key_check()
            output = keys2output(key_pressed)

            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(dcObj, w, h)
            cDC.SelectObject(bmp)
            cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)
            arr = bmp.GetBitmapBits(True)
            cap = np.fromstring(arr, dtype='uint8')
            cap.shape = (h, w, 4)
            cap = cap[..., :3]
            printscreen = cap

            #printscreen = np.array(ImageGrab.grab(bbox=(0,40,w,h+40)))
            #printscreen = cv2.cvtColor(printscreen,cv2.COLOR_BGR2GRAY)
            printscreen = cv2.resize(printscreen,(480,300))
            cv2.imshow('windows', printscreen)
            time_used = time.time() - last_time
            last_time = time.time()

            training_data.append([printscreen ,output])

            key = cv2.waitKey(10)
            if key == ord('q'):
                cv2.destroyAllWindows()
                break

            if len(training_data) % 500 == 0:
                filename = file_name_template.format(latest_data_id)
                print('{} is stored'.format(filename))
                np.save(filename, training_data)
                latest_data_id+=1
                training_data = []



    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(bmp.GetHandle())

main()