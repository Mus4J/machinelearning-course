import numpy as np
import scipy as sp
import sklearn as sklearn
import sklearn.datasets
import matplotlib.pyplot as plt
from time import time
import sys
import getopt
import ast

# Minimal learning machine training


def mlm_train(X, R, Y, T):
    D_x = sp.spatial.distance.cdist(X, R)
    Delta_y = sp.spatial.distance.cdist(Y, T)
    B = np.matmul(np.matmul(np.linalg.pinv(
        np.matmul(np.transpose(D_x), D_x)), np.transpose(D_x)), Delta_y)
    #B = np.linalg.pinv(D_x, Delta_y)
    return B

# Minimal learning machine testing


def mlm_test(x_test, R, T, B):

    from scipy.optimize import least_squares

    def J_fun(y, delta_yT, T):
        return np.sum((np.multiply(np.transpose(y-T), (y-T))-delta_yT**2)**2)

    y = np.zeros((x_test.shape[0]))
    a = np.zeros((x_test.shape[0]))
    for i in range(x_test.shape[0]):

        d_xR = sp.spatial.distance.cdist(
            x_test[i, :].reshape(1, x_test.shape[1]), R)
        delta_yT = np.matmul(d_xR, B)
        y_hat = least_squares(J_fun, 0, method='lm', args=(delta_yT, T))

        y[i] = y_hat.x[:]
        a[i] = np.sqrt(np.sum(delta_yT**2))

    return y, a


def mlm_majority_voting(x_test, R, T, B, k, metriX):
    y = np.zeros((x_test.shape[0]))
    a = np.zeros((x_test.shape[0]))

    d_xR = sp.spatial.distance.cdist(x_test, R, metric=metriX)
    delta_yT = np.matmul(d_xR, B)

    from scipy.stats import mode
    k_shortest_id = np.argsort(delta_yT)[:, 0:k]
    y = mode(T[k_shortest_id, :], axis=1)[0][:, 0]

    return y


def process_data(inputfile):
    file = open(inputfile, 'r')
    # with open(inputfile, 'r') as inputFile:
    contents = file.read()
    dictionary = ast.literal_eval(contents)

    file.close()

    return dictionary


def execute(inputfile):
    dataset = process_data(inputfile)

    test_set_size = 30

    X = dataset.keys()
    Y = [[]]
    N_data = [[]]
    for x, data in enumerate(dataset):
        list = []
        list2 = []
        for i, single in enumerate(dataset.get(data)):
            list.append(single['average'])
            list2.append(single['time_points'])
            list2.append(single['ip'])
            list2.append(single['size'])
            list2.append(single['method'])
            list2.append(single['logIn'])
        Y.append(list)
        N_data.append(list2)

    list = []
    list2 = []

    for x, data_list in enumerate(Y):
        if(len(data_list) == 1):
            list.append(data_list)

    list = np.array(list)

    for x, data_list in enumerate(N_data):
        if(len(data_list) == 5):
            list2.append(data_list)

    list2 = np.array(list2)

    # print(list2)

    #X, Y = sklearn.datasets.make_moons()
    #X, Y = sklearn.datasets.make_swiss_roll()

    ids = np.arange(0, list.shape[0])
    np.random.shuffle(ids)

    ids2 = np.arange(0, list2.shape[0])
    np.random.shuffle(ids2)

    x_test = list[ids[0:test_set_size], :].reshape(
        test_set_size, list.shape[1])
    y_test = list[ids[0:test_set_size]]

    x_test2 = list2[ids2[0:test_set_size], :].reshape(
        test_set_size, list2.shape[1])
    y_test2 = list2[ids2[0:test_set_size]]

    X = list[ids[test_set_size::], :]
    Y = list[ids[test_set_size::]].reshape(-1, 1)
    R = list[::1, :]
    T = list[::1].reshape(list[::1].shape[0], 1)

    X2 = list2
    Y2 = list2
    R2 = list2[::5, :]
    T2 = list2

    B = mlm_train(X, R, Y, T)
    B2 = mlm_train(X2, R2, Y2, T2)

    y = mlm_majority_voting(x_test, R, T, B, k=1, metriX='euclidean')

    y2 = mlm_majority_voting(x_test2, R2, T2, B2, k=1, metriX='euclidean')

    y2 = np.squeeze(y2)

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 4, 1)
    plt.scatter(y, y_test, c=np.round(y))
    plt.scatter(y, y_test, c=np.round(y))
    plt.xlabel('Luokittelutulos')
    plt.ylabel('Taustatotuus')
    plt.title('Luokittelun tulokset ristiintaulukoitu')

    plt.subplot(1, 4, 2)
    plt.scatter(X[:, :], X[:, :], marker='*', c=Y.squeeze(), alpha=0.5)
    plt.scatter(x_test[:, :], x_test[:, :], c=np.round(y))

    plt.subplot(1, 4, 3)
    plt.scatter(y2, y_test2, c=np.round(y2))
    plt.scatter(y2, y_test2, c=np.round(y2))
    plt.xlabel('Luokittelutulos')
    plt.ylabel('Taustatotuus')
    plt.title('Luokittelun tulokset ristiintaulukoitu')

    plt.subplot(1, 4, 4)
    plt.scatter(X2[:, :], X2[:, :], marker='*', c=Y2.squeeze(), alpha=0.5)
    plt.colorbar()
    plt.scatter(x_test2[:, :], x_test2[:, :], c=np.round(y2))
    plt.colorbar()

    plt.show()

    # spotAnomaly(dataset)


def reverseKNN(X, k):

    from sklearn.neighbors import NearestNeighbors as KNN
    knn = KNN(k)
    knn.fit(X)
    kNN_dist = knn.kneighbors()[0]
    kNN_id = knn.kneighbors()[1]
    reverse_knn = np.zeros((X.shape[0]))
    for i in range(X.shape[0]):
        reverse_knn[i] = np.size(np.where(kNN_id == i))
    return reverse_knn

# Spotting anomaly method


def spotAnomaly(dataset):
    test_set_size = 30

    X = dataset.keys()
    Y = [[]]
    for x, data in enumerate(dataset):
        list = []
        for i, single in enumerate(dataset.get(data)):
            list.append(single['average'])
        Y.append(list)

    # Y = np.sum((X-np.mean(X,axis=0))**2,axis=1)**(1/2)

    # ABOD
    # bod, Y, D = abod(X)

    # Reverse KNN
    Y = reverseKNN(X, 6)

    Y[np.where(np.isnan(Y))] = 0
    Y = Y/30

    ids = np.arange(0, X.shape[0])
    np.random.shuffle(ids)

    x_test = X[ids[0:test_set_size], :].reshape(test_set_size, X.shape[1])
    y_test = Y[ids[0:test_set_size]]

    X = X[ids[test_set_size::], :]
    Y = Y[ids[test_set_size::]].reshape(X.shape[0], 1)
    R = X[::5, :]
    T = Y[::5].reshape(Y[::5].shape[0], 1)
    # Y[:,:] = 0
    # T[:,:] = 0
    # x_test = np.concatenate((x_test,np.array([8,4,4,5]).reshape(1,4)),axis=0)
    x_test = np.concatenate((x_test, np.mean(X, axis=0).reshape(
        1, 4)+np.array([4, 2, 2, 2]).reshape(1, 4)), axis=0)

    start = time()
    B = mlm_train(X, R, Y, T)
    y, a = mlm_test(x_test, R, T, B)
    stop = time()
    print(stop-start)

    plt.figure()
    plt.bar(np.arange(0, test_set_size+1), y)
    plt.show()

# Entry method


def main(argv):
    inputfile = ''

    try:
        opts, args = getopt.getopt(
            argv, "h:i:", ["help=", "ifile="])
    except getopt.GetoptError:
        print('Message: Error')
        print()
        print('     -i  | --ifile       Name of file used')
        print()
        print('Example line: MachineLearning.py -o <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--ifile"):
            inputfile = arg
    if(inputfile != ''):
        execute(inputfile)
    else:
        print('Message: Argument missing.')
        print()
        print('     -i  | --ifile       Name of file used')
        print()
        print('Example line: MachineLearning.py -o <inputfile>')
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
