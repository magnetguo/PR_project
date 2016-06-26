import numpy as np
from wx.lib.pubsub import pub

#### func: calculate Euclidean distance
def euclDistance(vector1, vector2):
    return np.sqrt(sum(np.power(vector2 - vector1, 2)))

#### func: init centroids randomly
def initCentroids(dataSet, k):
    # deload vector to elements
    numSamples, dim = dataSet.shape
    centroids = np.zeros((k, dim))
    for i in range(k):
        # get uniform random number from 0 to numSamples
        index = int(np.random.uniform(0, numSamples))
        centroids[i, :] = dataSet[index, :]
    return centroids

def kmeans(dataSet, k, stop, pic):

    # k-means cluster
    numSamples = dataSet.shape[0]
    # first column stores which cluster this sample belongs to,
    # second column stores the error between this sample and its centroid
    clusterAssment = np.mat(np.zeros((numSamples, 2)))
    clusterChanged = True

    # step 1: init centroids
    centroids = initCentroids(dataSet, k)

    n = 0
    during = 0
    while clusterChanged:
        clusterChanged = False
        # for each sample
        for i in xrange(numSamples):
            minDist  = 100000.0
            minIndex = 0
            # for each centroid
            # step 2: find the centroid who is closest
            for j in range(k):
                distance = euclDistance(centroids[j, :], dataSet[i, :])
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
