import shelve

import matplotlib.pyplot as plt
from keras.layers.core import Activation, Dense, Dropout
from keras.models import Sequential
from sklearn.cross_validation import train_test_split
from sklearn.manifold import (TSNE, Isomap, LocallyLinearEmbedding,
                              SpectralEmbedding)

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
    E = DATASET['energies']
    print('Datasets retrieved')
    dimred = TSNE(n_components=2)
    XX = dimred.fit_transform(X)
    sc = plt.scatter(XX[:, 0],
                     XX[:, 1],
                     c=E,
                     cmap="Spectral",
                     alpha=0.5,
                     edgecolors='none')
    plt.colorbar(sc)
    plt.show()


if __name__ == '__main__':
    main()
