This folder contains datasets for image forensics. The same datasets are available in https://figshare.com/articles/data_zip/5016965 . 
The edgelists (pairwise PCE similarity scores), due to their size, are available only separatately  at [PCE similarities](https://figshare.com/articles/PCE_similarities_dresden_zip/5017058) .

The edgelist is used as an input to the [LargeVis](https://github.com/lferry007/LargeVis) application.  
The filelists from  [PCE similarities](https://figshare.com/articles/PCE_similarities_dresden_zip/5017058) are used to extract the image name and the source camera for benchmarking the clustering. 

The folder *embedded* contains the results of the embeddings of the image datasets in 3D, 2D or 8D, performed using LargeVis. In particular, *coordinates_files* contains the files that are direct output of LargeVis. *json* contains the version that can by uploaded by [DiVE](https://sherlock-clustering.github.io/Sherlock_DiVE/) via the button *choose file*.

The folder *combined* contains json files uploadible by [DiVE](https://sherlock-clustering.github.io/Sherlock_DiVE/). They present the embeddings of the image datasets, together with the cluster labels obtained after clustering. Please use the *coloring by property* section from the DiVE user interface to color by cluster labels. 




