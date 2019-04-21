import numpy as np
import pandas as pd
import os
import cv2
from collections import Counter
from numpy.random import shuffle

def balance(datafile_id):

    data = np.load('D:/data/v2/training_data_v2_{}.npy'.format(datafile_id))
    print('Load file {}...'.format(datafile_id))
    df = pd.DataFrame(data)
    print(Counter(df[1].apply(str)))
    shuffle(data)
    #df = pd.DataFrame(data)
    #print(Counter(df[1].apply(str)))

    w_s = []
    s_s = []
    a_s = []
    d_s = []
    wa_s = []
    wd_s = []
    sa_s = []
    sd_s = []
    nk_s = []

    w = [1,0,0,0,0,0,0,0,0]
    s = [0,1,0,0,0,0,0,0,0]
    a = [0,0,1,0,0,0,0,0,0]
    d = [0,0,0,1,0,0,0,0,0]
    wa = [0,0,0,0,1,0,0,0,0]
    wd = [0,0,0,0,0,1,0,0,0]
    sa = [0,0,0,0,0,0,1,0,0]
    sd = [0,0,0,0,0,0,0,1,0]
    nk = [0,0,0,0,0,0,0,0,1]



    for dd in data:
        img = dd[0]
        choice = dd[1]
        if choice == w:
            w_s.append([img, choice])
        elif choice == nk:
            nk_s.append([img, choice])
        elif choice == s:
            s_s.append([img, choice])
        elif choice == a:
            a_s.append([img, choice])
        elif choice == d:
            d_s.append([img, choice])
        elif choice == wa:
            wa_s.append([img, choice])
        elif choice == wd:
            wd_s.append([img, choice])
        elif choice == sa:
            sa_s.append([img, choice])
        elif choice == sd:
            sd_s.append([img, choice])

        else :
            print("no matches")


    #cut_length = len(s_s) + len(a_s) + len(d_s) + len(wa_s) + len(wd_s) + len(sa_s) + len(sd_s)
    w_s = w_s[:len(wa_s)][:len(wd_s)]
    nk_s = nk_s[:len(w_s)]
    finaldata = w_s + s_s + a_s + d_s + wa_s + wd_s + sa_s + sd_s + nk_s 

    print("After balancing...")
    df = pd.DataFrame(finaldata)
    print(Counter(df[1].apply(str)))
    print()

    np.save('D:/data/v2/training_data_balanced_{}.npy'.format(datafile_id),finaldata)

def balance_all(latest_id = 0):
    latest_data_id = latest_id
    file_name_template = 'D:/data/v2/training_data_v2_{}.npy'
    while os.path.isfile(file_name_template.format(latest_data_id)):
        latest_data_id+=1
    print('{} data files in total...'.format(latest_data_id))
    if(latest_data_id == 0): return
    for i in range(latest_data_id):
        balance(i)



def merge_balanced():
    latest_merged_id = 0
    merged_file_name_template = 'D:/data/v2/final_balanced_merged_{}.npy'
    while os.path.isfile(merged_file_name_template.format(latest_merged_id)):
        latest_merged_id+=1
    latest_data_id = 0
    file_name_template = 'D:/data/v2/training_data_balanced_{}.npy'
    while os.path.isfile(file_name_template.format(latest_data_id)):
        latest_data_id+=1
    merged_file_name = merged_file_name_template.format(latest_merged_id)
    print('{} balanced data files in total...'.format(latest_data_id))
    print('New merged file will be stored as {}'.format(merged_file_name))
    print('start merging...')
    final_merged_data = []
    for i in range(latest_data_id):
        print('load file {}'.format(i))
        subdata = list(np.load(file_name_template.format(i)))
        final_merged_data = final_merged_data + subdata
        if(len(final_merged_data)>1000):
            np.save(merged_file_name,final_merged_data)
            print('{} saved'.format(merged_file_name))
            latest_merged_id+=1
            merged_file_name = merged_file_name_template.format(latest_merged_id)
            final_merged_data=[]
    np.save(merged_file_name, final_merged_data)
    print('{} saved'.format(merged_file_name))

def main():
    balance_all()
    merge_balanced()

main()

