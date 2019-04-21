import numpy as np
import pandas as pd
import os
import cv2
from random import shuffle
from collections import Counter


#data = np.load('D:/data/v2/training_data_v2_64.npy')
data = np.load('D:\\data\\v3\car\\front\\final_balanced_merged_1.npy')
#data = np.load('/Volumes/LACIE SHARE/data/v3/car/far/final_balanced_merged_2.npy')
#df= pd.DataFrame(data)
id = 0
while(True):
    if id < data.shape[0]:
        img = data[id][0]
        img = cv2.resize(img, (640, 400))
        cv2.imshow('windows', img)
        print(id, data[id][1])
        id += 1
        cv2.waitKey()
    else:
        cv2.waitKey()

# print(Counter(df[1].apply(str)))
# shuffle(list(data))
#df= pd.DataFrame(data)
# print(Counter(df[1].apply(str)))
