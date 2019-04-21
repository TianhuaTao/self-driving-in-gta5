import numpy as np
from googlenet import inception_v3
from googlenet import alexnet2
from numpy.random import shuffle

WIDTH = 480
HEIGHT = 300
LR = 1e-2
EPOCHS = 8
LOAD_MODEL = False
FILE_ID_END = 7

MODEL_NAME = 'sam-car-{}-{}-{}-epochs.model'.format(LR, 'inception_v3', EPOCHS)
model = inception_v3(WIDTH, HEIGHT, 3, LR, output=9, model_name=MODEL_NAME)

# MODEL_NAME = 'sam-{}-{}-{}-epochs.model'.format(LR, 'alexnet2',EPOCHS)
# model = alexnet2(WIDTH,HEIGHT, LR,output=9)
# PRE_NAME = 'model_alexnet-2390'
if LOAD_MODEL:
    model.load(MODEL_NAME)
    print('We have loaded a previous model!!!!')


for e in range(EPOCHS):
    data_order = [i for i in range(0, FILE_ID_END + 1)]
    shuffle(data_order)
    for count, i in enumerate(data_order):

        # file_name = '/Volumes/LACIE SHARE/data/v2/final_balanced_merged_{}.npy'.format(i)

        file_name = 'D:/data/v2/final_balanced_merged_{}.npy'.format(i)
        train_data = np.load(file_name)
        shuffle(train_data)
        print('Training {}'.format(file_name))

        train = train_data[:-50]
        test = train_data[-50:]

        X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 3)
        Y = [i[1] for i in train]
        # Y =np.reshape(Y, (-1,1))

        test_x = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 3)
        test_y = [i[1] for i in test]
        # test_y =np.reshape(test_y, (-1,1))

        model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), batch_size=1,
                  show_metric=True, run_id=MODEL_NAME)
        model.save(MODEL_NAME)
        print('saving model...')
# tensorboard --logdir=foo:C:/Users/H/Desktop/ai-gaming/log
