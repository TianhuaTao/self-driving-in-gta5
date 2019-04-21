import os

file_name_template = 'D:\\data\\v3\\car\\front\\training_data_v3_{}.npy'
for i in range(12):
    oldname = file_name_template.format(i)
    newname = file_name_template.format(i+55)
    os.rename(oldname, newname)
