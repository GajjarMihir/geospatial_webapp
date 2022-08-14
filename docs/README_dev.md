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

- Installed and set up Geoserver

- I need to add alpha band in order to make the black edges disappear. I tried to make the black color transparent using Geoserver but the edges were not smooth unless the "Overview Policy" was set to "IGNORE" but with this option rendering of the image tiles in the web app was very slow. After adding the alpha channel/band the edges were very smooth and the "Overview Policy" was set to "QUALITY". So next, I will add a python script in the pipeline to add alpha channel to all the .tif images which are to be served in order to blend them nicely with the base map.

Adding no data value to .tif images

- I also tried to add no data value to the .tif images by using the following commands:

1. ~{path_to}/anaconda3/envs/geospatial_webapp/bin/gdal_edit.py -a_nodata 255 gedit_test/gedit_test.tif
2.  gdal_translate -a_nodata 255 input_image.tif output_image.tif

But the (black) boundaries of the .tif images were not smooth with these.tif images and hence I will go ahead with adding the alpha band to the .tif images.

Now, we have added the .tif image data on top of the base map in the leaflet webapp. The next step would be to add the polygons on top of the .tif image data.

**Adding polygons on top of .tif image data in the webapp**
- Tried using the L.geoJSON option but need to manually add the .geojson data in the file as text - this does not look like an elegant option
- Also tried the leaflet ajax plugin but it did not work - got two errors and one of them said that it was having issues accessing the .geojson file on disk because of permission issues. I thought serving with wms might be a better option and hence the next step.
- Now, I am serving the .geojson files after converting them to .shp file via Geoserver to the leaflet webapp. The only step that I have to add is a script to convert the .geojson files to .shp files in order to serve this data with Geoserver. There's a plugin for geojson files in geoserver but they say it's not supported anymore and there are issues with it so going ahead with the .shp files option should be more stable and it's a standard format so there should not be any issues.
- Will create a script to convert .geojson files to .shp files using geopandas.
- After creating this script, I used Geoserver to serve all these .shpfiles and was able to load the polygons in the web app.

**Adding control to make the polygons transparent**





