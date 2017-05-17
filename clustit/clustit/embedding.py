import numpy as np
import pandas
import os
import sys

import LargeVis
from clustit.utils import delete_temp_file

def get_column_names(outdim):
    names = ['filename']
    if outdim <= 3:
        names.append('x')
        names.append('y')
    if outdim == 3:
        names.append('z')
    if outdim > 3:
        names += [str(x) for x in range(outdim)]
    return names



def largevis(edgelist_filename, outdim=2, alpha=-1.0):
    """ Use LargeVis for embedding

        This function is Clustit's interface to the LargeVis model
        for embedding large-scale and high-dimensional data.

        :param edgelist_filename: The filename of the edgelist with the similarities or distances
        :type edgelist_filename: string

        :param outdim: The number of output dimensions, default is 2.
        :type outdim: int

        :returns: The resulting embedding of the input data
        :rtype: pandas.DataFrame
    """
    LargeVis.loadgraph(edgelist_filename)
    _run_largevis(outdim, alpha)

    #get output data from LargeVis
    temp_file = "/tmp/largevis_tempfile.txt"
    try:
        LargeVis.save(temp_file)
        names = get_column_names(outdim)
        data_frame = pandas.read_csv(temp_file, sep=" ", names=names, header=0)
    finally:
        #delete_temp_file(temp_file)
        pass

    return data_frame



def _run_largevis(outdim=-1, threads=-1, samples=-1, prop=-1, alpha=-1.0, trees=-1, neg=-1, neigh=-1, gamma=-1.0, perp=-1.0):
    """ Provide a nicer way to call LargeVis.run()

        This function provides defaults through optional parameters rather than command-line arguments.
        Like LargeVis.run() this function assumes LargeVis.loadfile() or LargeVis.loadgraph() have been called already.

        :param outdim: output dimensionality
        :type outdim: int
        :param threads: number of training threads
        :type threads: int
        :param samples: number of training mini-batches
        :type samples: int
        :param prop: number of propagations
        :type prop: int
        :param alpha: learning rate
        :type alpha: float
        :param trees: number of rp-trees
        :type trees: int
        :param neg: number of negative samples
        :type neg: int
        :param neigh: number of neighbors in the NN-graph
        :type neigh: int
        :param gamma: weight assigned to negative edges
        :type gamma: float
        :param perp: perplexity for the NN-grapn
        :type perp: float

    """
    LargeVis.run(np.int32(outdim), np.int32(threads), np.int32(samples), np.int32(prop),
            np.float32(alpha), np.int32(trees), np.int32(neg), np.int32(neigh), np.float32(gamma), np.float32(perp))

