# cython: infer_types=True
# cython: boundscheck=False
# cython: wraparound=False

import numpy as np
cimport numpy as np
from libc.math cimport sqrt
from wx.lib.pubsub import pub

#### func: calculate Euclidean distance
cdef euclDistance(vector1, vector2):
    return np.sqrt(sum(np.power(vector2 - vector1, 2)))

#### func: init centroids randomly
cdef initCentroids(np.ndarray[np.int64_t, ndim=2] dataSet, int k):
    # deload vector to elements
    cdef int numSamples = dataSet.shape[0]

    a = np.zeros((k, 3))
    a.dtype = "int64"
    cdef np.ndarray[np.int64_t, ndim=2] centroids = a

    cdef int index

    for i in range(k):
    # get uniform random number from 0 to numSamples
        index = int(np.random.uniform(0, numSamples))
        centroids[i, :] = dataSet[index, :]
    return centroids

def kmeans(np.ndarray[np.int64_t, ndim=2] dataSet, int k, int stop, pic):
    # k-means cluster
    cdef int numSamples = dataSet.shape[0]
    cdef int dims = dataSet.shape[1]
    # first column stores which cluster this sample belongs to,
    # second column stores the error between this sample and its centroid
    cdef np.ndarray[np.float64_t, ndim=2] clusterAssment = np.mat(np.zeros((numSamples, 2)))
    clusterChanged = True

    # step 1: init centroids
    cdef np.ndarray[np.int64_t, ndim=2] centroids = initCentroids(dataSet, k)

    cdef int n = 0
    cdef float minDist
    cdef int minIndex

    cdef float distance

    cdef np.ndarray[np.int64_t, ndim=2] pointsInCluster
    cdef np.ndarray[np.float64_t, ndim=1] centroid_new

    while clusterChanged:
        clusterChanged = False
        # for each sample
        for i in xrange(numSamples):
            minDist  = 100000.0
            minIndex = 0
            # for each centroid
            # step 2: find the centroid who is closest
            for j in range(k):
                distance = 0.0
                for h in range(dims):
                    distance = distance + (centroids[j, h] - dataSet[i, h]) * (centroids[j, h] - dataSet[i, h])
                distance = sqrt(distance)
                if distance < minDist:
                    minDist  = distance
                    minIndex = j

            # step 3: update its cluster
            if clusterAssment[i, 0] != minIndex:
                clusterAssment[i, :] = minIndex, minDist**2

        # step 4: update centroids
        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(clusterAssment[:, 0].A == j)[0]]
            centroid_new = np.mean(pointsInCluster, axis = 0)
            print euclDistance(centroids[j, :], centroid_new)
            if euclDistance(centroids[j, :], centroid_new) > stop:
                clusterChanged = True
                centroids[j, :] = centroid_new
        if pic == 0:
            # send messages to redraw the diagram
            pub.sendMessage("Centriods CHANGED", data=41, extra1 = clusterAssment, extra2 = centroids)

        n = n + 1
        print n

    print 'Congratulations, cluster complete!'
    return centroids, clusterAssment.A, n