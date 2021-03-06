Workflow README:

**Possible options**

There are two possible options/workflows:

1. Terracotta (tile server) only supports serving .tif images in COG format having a **single band**. Because of this reason, the first option is to store different bands in different .tif images. Something like image_1_b1.tif, image_1_b2.tif, image_1_b3.tif, image_2_b1.tif, image_2_b2.tif, etc. We can create .vrt files in which the corresponding .tif images for different bands can be stacked together. These .vrt files can then be used further in the machine learning pipeline.

Pros:
* The file size of the .tif images remain manageable compared to having multiple bands in a single .tif image.

Cons:
* There can be many files to manage as the project scales.
* It is time consuming to load .tif images for all the different bands for visualization for e.g. QGIS.
* Can use .vrt for having a virtual file that contains the combined .tif image for all the different bands but need to check if this can fit-in in the machine learning pipeline, for e.g. loading the file using gdal or rasterio in python.

2. The second option is to store a single .tif image having multiple bands

Pros:
* Less files to manage.
* Easy to visualize.
* Do not need to create .vrt. Easy to load/integrate in the machine learning pipeline(s).

Cons:
* The file size can become huge having multiple bands in a single .tif image and also when converting to COG format.
* GeoServer can only serve COG with 3 bands or having a single band. So if we can serve multiple bands with Terracotta/Option 1 then it **might** be better.

**Approach chosen**
I am going forward with option 2 because it should be easier to manage the image data files organized this way compared to option 1. Also, I hope that I can still implement the funcationality of having a filter in the webapp to select a particular band from a .tif image - not sure if this would be possible but hope it is.

The next step is to install and setup Geoserver and make it work with COG's.




