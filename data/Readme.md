This folder contains datasets for image forensics.
The folders *canon, olympus, fuji, pentax* and *praktica* each contain a filelist (list of names of all images from the corresponding dataset) and 
an edgelist (list of pairwise PCE similarity scores of the images of the corresponding dataset).
The edgelist is used as an input to the [LargeVis](https://github.com/lferry007/LargeVis) application.  
The filelist is used to extract the image name and the source camera for benchmarking the clustering. 

The folder *embedded* contains the results of the embeddings of the image datasets in 3D, 2D or 8D, performed using LargeVis. In particular, *coordinates_files* contains the files that are direct output of LargeVis. *json* contains the version that can by uploaded by [DiVE](https://sherlock-clustering.github.io/Sherlock_DiVE/) via the button *choose file*.

The folder *combined* contains json files uploadible by [DiVE](https://sherlock-clustering.github.io/Sherlock_DiVE/). They present the embeddings of the image datasets, together with the cluster labels obtained after clustering. Please use the *coloring by property* section from the DiVE user interface to color by cluster labels. 




