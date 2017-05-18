Clustit - A simple tool for clustering data
===========================================

Clustit is a command-line tool for clustering data based on an edgelist or distance matrix.
Clustit should serve as an easy way of accessing the different clustering algorithms already implemented in Python.

For **paper reviewers**: please read the ipynbReadme.md file. 

Dependencies
------------
 * Python 2.7 or Python 3.5
 * Scipy
 * scikit-learn
 * hdbscan (https://github.com/scikit-learn-contrib/hdbscan)(not necessary)
 * Pandas
 * LargeVis (https://github.com/lferry007/LargeVis) (not necessary, can be used separately to generate embeddings)

Example usage
-------------
```
usage: clustit.py [-h] (-e edgelist | -m matrix) [-n names] [-c convert]
                  clustering_algorithm

specify either:
  -e edgelist, --edgelist edgelist
                        name of the edgelist file
  -m matrix, --matrix matrix
                        name of distance matrix file

positional arguments:
  clustering_algorithm  name of the clustering algorithm to use
                        choose from: hierarchical, dbscan, hdbscan, spectral, affinity

optional arguments:
  -h, --help            show this help message and exit
  -n names, --names names
                        filename storing a list of names for the items to be
                        clustered, in case distance matrix is used
  -c convert, --convert convert
                        convert similarity to distance with specified a cut-
                        off value

Example:
./clustit.py -m ../data/pentax/matrix-pentax-pce.dat --convert=200 hierarchical
./clustit.py -e ../data/pentax/edgelist-pentax-pce.txt --convert=200 dbscan
```

Contributing to clustit
-----------------------
Clustit follows the Google Python style guide, with Sphinxdoc docstrings for module public functions. If you want to
contribute to the project please fork it, create a branch including your addition, and create a pull request.

The tests use relative imports and can be run directly after making
changes to the code. To run all tests use `nosetests` in the main directory.

Before creating a pull request or committing changes, please ensure the following:
* You have written unit tests to test your additions
* All unit tests pass
* The code is compatible with both Python 2.7 and Python 3.5

Contributing authors so far:
* Anand Gavai
* Alessio Sclocco
* Arnold Kuzniar
* Rena Bakhshi
* Ben van Werkhoven

