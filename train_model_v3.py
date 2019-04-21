
import numpy as np
from model import alexnet2, sterringNet,inception_v3
from numpy.random import shuffle

WIDTH = 320
HEIGHT = 200
LR = 1e-3
EPOCHS = 16
LOAD_MODEL = True
FILE_ID_END = 1
FILE_ID_START = 0
MODEL_NAME = 'car-front-steering-regression-inceptionv3.model'
model = inception_v3()
#model = alexnet2(WIDTH, HEIGHT, LR, output=2)

# MODEL_NAME = 'sam-{}-{}-{}-epochs.model'.format(LR, 'alexnet2',EPOCHS)
# model = alexnet2(WIDTH,HEIGHT, LR,output=9)
# PRE_NAME = 'model_alexnet-2390'
if LOAD_MODEL:
    model.load(MODEL_NAME)
    print('We have loaded a previous model!!!!')


def prepare_data(train_data):
    train = train_data[:-100]
    test = train_data[-100:]

    X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 3)
    Y = [i[1] for i in train]
    #steering
    Y = [[0.5 - i[0],i[0] + 0.5] for i in Y]
    # Y =np.reshape(Y, (-1,1))

    test_x = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 3)
    test_y = [i[1] for i in test]
    test_y = [[0.5 - i[0],i[0] + 0.5] for i in test_y]
    # test_y =np.reshape(test_y, (-1,1))

    return X,Y, test_x, test_y

def prepare_data_1d(train_data):
    train = train_data[:-100]
    test = train_data[-100:]

    X = np.array([i[0] for i in train]).reshape(-1, WIDTH, HEIGHT, 3)
    Y = [i[1] for i in train]
    #steering only
    Y = [[i[0]*10] for i in Y]


    test_x = np.array([i[0] for i in test]).reshape(-1, WIDTH, HEIGHT, 3)
    test_y = [i[1] for i in test]
    test_y = [[i[0]*10] for i in test_y]


    return X,Y, test_x, test_y

for e in range(EPOCHS):
    data_order = [i for i in range(FILE_ID_START, FILE_ID_END + 1)]
    shuffle(data_order)
    for count, i in enumerate(data_order):

        # file_name = '/Volumes/LACIE
        # SHARE/data/v2/final_balanced_merged_{}.npy'.format(i)

        file_name = 'D:/data/v3/car/front/final_balanced_merged_{}.npy'.format(i)
        train_data = np.load(file_name)
        #shuffle(train_data)
        print('Training {}'.format(file_name))

        X,Y, test_x, test_y = prepare_data_1d(train_data)

        model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}), batch_size=32,
                  show_metric=True, run_id=MODEL_NAME)
        model.save(MODEL_NAME)
        print('saving model...')
# tensorboard --logdir=foo:C:/Users/H/Desktop/ai-gaming/log --host=127.0.0.1
