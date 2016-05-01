import shelve

import matplotlib.pyplot as plt
from keras.layers.core import Activation, Dense, Dropout
from keras.models import Sequential
from sklearn.cross_validation import train_test_split

import createDataset

DATASET = shelve.open('DB.shlv')


def dienen(object):
    def __init__(self):
        pass

    def fit(X, Y):
        pass


def main():
    createDataset.createEntireDataset()
    X = DATASET['geometries']
    Y = DATASET['coeficients']

    input_size = X.shape[1]
    output_size = Y.shape[1]
    print 'input_size:', input_size
    print 'output_size:', output_size

    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        Y,
                                                        test_size=0.20,
                                                        random_state=42)

    print X_train, y_train

    model = Sequential()

    model.add(Dense(output_dim=300, input_dim=input_size,init='lecun_uniform', activation='relu'))
    model.add(Activation("relu"))
    model.add(Dropout(0.8))
    model.add(Dense(output_dim=600, input_dim=300))
    model.add(Activation("relu"))
    model.add(Dense(output_dim=output_size, input_dim=600))
    model.add(Activation("relu"))

    #model.add(Dense(output_dim=100,input_dim=input_size) )
    #model.add(Activation('relu'))
    #model.add(Dense(100, output_size))
    model.compile(loss='mean_squared_error', optimizer='rmsprop')

    model.fit(X_train, y_train, nb_epoch=100, batch_size=42)

    y_pred = model.predict(X_test)
    for o, p in zip(y_test, y_pred):
        print o
        print p
        print '\n'

    score = model.evaluate(X_test, y_test, batch_size=70)
    print 'Score:', score
    return score

def main_iterate_on_time(n=10,initial_ds_size=1000,batch_size=200):
    createDataset.createEntireDataset()
    X = DATASET['geometries']
    Y = DATASET['coeficients']

    input_size = X.shape[1]
    output_size = Y.shape[1]
    print 'input_size:', input_size
    print 'output_size:', output_size
    print 'X.shape', X.shape
    print 'Y.shape', Y.shape
    X_train, X_test, y_train, y_test = train_test_split(X,
                                                        Y,
                                                        test_size=0.20,
                                                        random_state=42)

    scores = []
    training_sizes = []
    for i in xrange(n):
        print 'STEP:', i
        X_train   = X[:initial_ds_size+i*batch_size]
        X_test = X[initial_ds_size+i*batch_size:initial_ds_size+i*batch_size+batch_size]
        y_train   = Y[:initial_ds_size+i*batch_size]
        y_test = Y[initial_ds_size+i*batch_size:initial_ds_size+i*batch_size+batch_size]

        print X_train, y_train
        print 'X_train.shape, y_train.shape:', X_train.shape, y_train.shape
        print 'X_test.shape, y_test.shape', X_test.shape, y_test.shape

        model = Sequential()

        model.add(Dense(output_dim=300, input_dim=input_size,init='lecun_uniform', activation='relu'))
        model.add(Activation("relu"))
        model.add(Dropout(0.8))
        model.add(Dense(output_dim=600, input_dim=300))
        model.add(Activation("relu"))
        model.add(Dense(output_dim=output_size, input_dim=600))
        model.add(Activation("softmax"))

        #model.add(Dense(output_dim=100,input_dim=input_size) )
        #model.add(Activation('relu'))
        #model.add(Dense(100, output_size))
        model.compile(loss='mean_squared_error', optimizer='rmsprop')

        model.fit(X_train, y_train, nb_epoch=50, batch_size=26)

        y_pred = model.predict(X_test)
        for o, p in zip(y_test, y_pred):
            print o
            print p
            print '\n'

        score = model.evaluate(X_test, y_test, batch_size=70)
        print 'Score:', score
        scores.append(score)
        training_sizes.append(str(initial_ds_size+i*batch_size))
    print 'Scores:', scores
    print 'training_sizes:', training_sizes
    plt.plot(scores)
    plt.show()
    return score

if __name__ == '__main__':
    main_iterate_on_time()
    #main()
