import numpy as np
from googlenet import inception_v3
from googlenet import alexnet2
from numpy.random import shuffle

WIDTH = 160
HEIGHT = 120
LR = 1e-3
EPOCHS = 8
LOAD_MODEL = True
FILE_ID_END = 22

MODEL_NAME = 'pre-bike-{}-{}-{}-epochs.model'.format(LR, 'alexnet2', EPOCHS)
model = alexnet2(WIDTH, HEIGHT, LR, output=3)

# MODEL_NAME = 'sam-{}-{}-{}-epochs.model'.format(LR, 'alexnet2',EPOCHS)
# model = alexnet2(WIDTH,HEIGHT, LR,output=9)
# PRE_NAME = 'model_alexnet-2390'
if LOAD_MODEL:
    model.load(MODEL_NAME)
    print('We have loaded a previous model!!!!')


for e in range(EPOCHS):
    data_order = [i for i in range(1, FILE_ID_END + 1)]
    shuffle(data_order)
    for count, i in enumerate(data_order):

        # file_name = '/Volumes/LACIE SHARE/data/v2/final_balanced_merged_{}.npy'.format(i)

        file_name = 'D:/data/pretrained/training_data/training_data-{}-balanced.npy'.format(i)
        train_data = np.load(file_name)
        shuffle(train_data)
        print('Training {}'.format(file_name))

        train = train_data[:-100]
        test = train_data[-100:]

        X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 1)
        Y = [i[1] for i in train]
        # Y =np.reshape(Y, (-1,1))

        test_x = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 1)
        test_y = [i[1] for i in test]
        # test_y =np.reshape(test_y, (-1,1))

        model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), batch_size=16,
                  show_metric=True, run_id=MODEL_NAME)
        model.save(MODEL_NAME)
        print('saving model...')
# tensorboard --logdir=foo:C:/Users/H/Desktop/ai-gaming/log
