﻿""" module containing the implementations of clustering algorithms used in clustit """

import scipy.cluster.hierarchy as sch
#import hdbscan
import sklearn.cluster

import clustit.utils as utils
from clustit.output import OutputCollection


def hierarchical_clustering(similarities=None, method='complete', threshold=None, distance_cutoff=200):
    """ create a flat clustering based on hierarchical clustering methods and a threshold """
    if similarities is None:
        return None
    distance_matrix = utils.similarity_to_distance(similarities, distance_cutoff)
    linkage = sch.linkage(distance_matrix, method=method)
    threshold = threshold or 0.7*linkage[:, 2].max()
    labels = sch.fcluster(linkage, threshold, criterion='distance')
    return labels

def dbscan(similarities=None, threshold=None, distance_cutoff=200):
    """ cluster using DBSCAN algorithm """
    if similarities is None:
        return None
    distance_matrix = utils.similarity_to_distance(similarities, distance_cutoff)
    threshold = threshold or 2.8
    dbscan_clusterer = sklearn.cluster.DBSCAN(eps=threshold, min_samples=3, metric="precomputed", algorithm="brute")
    labels = dbscan_clusterer.fit_predict(distance_matrix)
    return labels

def hierarchical_dbscan(similarities=None, distance_cutoff=200):
    """ cluster using the Hierarchical DBSCAN algorithm """
    if similarities is None:
        return None
    distance_matrix = utils.similarity_to_distance(similarities, distance_cutoff)
    hdbscan_clusterer = hdbscan.HDBSCAN(metric="precomputed", min_samples=3)
    labels = hdbscan_clusterer.fit_predict(distance_matrix)
    return labels

def spectral(similarities=None, n_clusters=10):
    """ cluster using spectral clustering """
    if similarities is None:
        return None
    spectral_clusterer = sklearn.cluster.SpectralClustering(affinity="precomputed", n_clusters=n_clusters)
    labels = spectral_clusterer.fit_predict(similarities)
    return labels

def affinity(similarities=None):
    """ cluster using the affinity propagation algorithm """
    if similarities is None:
        return None
    affinity_clusterer = sklearn.cluster.AffinityPropagation(affinity="euclidean")
    labels = affinity_clusterer.fit_predict(similarities)
    return labels

def kmeans(embedded_space=None, n_clusters=10):
    """ cluster using the K-Means algorithm """
    if not isinstance(embedded_space, OutputCollection):
        return None
    kmeans_clusterer = sklearn.cluster.KMeans(n_clusters=n_clusters)
    labels = kmeans_clusterer.fit_predict(embedded_space.to_array())
    return labels

def meanshift(embedded_space=None):
    """ cluster using the mean shift algorithm """
    if not isinstance(embedded_space, OutputCollection):
        return None
    meanshift_clusterer = sklearn.cluster.MeanShift(cluster_all=False)
    labels = meanshift_clusterer.fit_predict(embedded_space.to_array())
    return labels
