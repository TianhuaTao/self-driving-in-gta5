import numpy as np
import pandas as pd
import os
import cv2
from collections import Counter
from numpy.random import shuffle

DIR = 'D:/data/v3/car/front/'

def balance(datafile_id):

    data = np.load(DIR + 'training_data_v3_{}.npy'.format(datafile_id))
    print('Load file {}...'.format(datafile_id))
    shuffle(data)

    leftrights = []
    no_leftrights = []

    for dd in data:
        img = dd[0]
        choice = dd[1]
        if(choice[0] == 0.0):
            no_leftrights.append(dd)
        else:
            leftrights.append(dd)
    
    no_leftrights = no_leftrights[:len(leftrights)]
    leftrights = leftrights[:len(no_leftrights)]

    final_data = no_leftrights + leftrights
    shuffle(final_data)
    np.save(DIR + 'training_data_balanced_v3_{}.npy'.format(datafile_id),final_data)

def balance_all(latest_id=0):
    latest_data_id = latest_id
    file_name_template = DIR + 'training_data_v3_{}.npy'
    while os.path.isfile(file_name_template.format(latest_data_id)):
        latest_data_id+=1
    print('{} data files in total...'.format(latest_data_id))
    if(latest_data_id == 0): return
    for i in range(15, 24):
        balance(i)



def merge_balanced():
    latest_merged_id = 0
    merged_file_name_template = DIR + 'final_balanced_merged_{}.npy'
    while os.path.isfile(merged_file_name_template.format(latest_merged_id)):
        latest_merged_id+=1
    latest_data_id = 0
    file_name_template = DIR + 'training_data_balanced_v3_{}.npy'
    while os.path.isfile(file_name_template.format(latest_data_id)):
        latest_data_id+=1
    merged_file_name = merged_file_name_template.format(latest_merged_id)
    print('{} balanced data files in total...'.format(latest_data_id))
    print('New merged file will be stored as {}'.format(merged_file_name))
    print('start merging...')
    final_merged_data = []
    for i in range(13,24):
        print('load file {}'.format(i))
        subdata = list(np.load(file_name_template.format(i)))
        final_merged_data = final_merged_data + subdata
        if(len(final_merged_data) > 5000):
            shuffle(final_merged_data)
            np.save(merged_file_name,final_merged_data)
            print('{} saved'.format(merged_file_name))
            latest_merged_id+=1
            merged_file_name = merged_file_name_template.format(latest_merged_id)
            final_merged_data = []
    shuffle(final_merged_data)
    np.save(merged_file_name, final_merged_data)
    print('{} saved'.format(merged_file_name))

def main():
    #balance_all()
    merge_balanced()

if __name__ == '__main__':
    main()
