# Converts the tiff images in to valid cog formatted images. When converting, the script checks whether the input image
# is already in a valid cog format.

from logging import warning
from osgeo import gdal
from pathlib import Path
from tqdm import tqdm
import validate_cloud_optimized_geotiff
import os

def convert_tiff_to_cog(in_img_path, out_img_path):
    _ = gdal.Translate(
        srcDS=in_img_path,
        destName=out_img_path,
        options="-of COG -co COMPRESS=LZW -co NUM_THREADS=ALL_CPUS -co BIGTIFF=IF_SAFER"
    )

def add_alpha_channel_to_tiff(in_img_path, out_img_path):
    # equivalent to: gdalwarp -of Gtiff -dstalpha -multi -wo NUM_THREADS=16 in_img_path out_img_path
    _ = gdal.Warp(
        srcDSOrSrcDSTab=in_img_path,
        destNameOrDestDS=out_img_path,
        options='-of Gtiff -dstalpha -multi -wo NUM_THREADS=8'
    )

if __name__=='__main__':

    imgs_dir = Path('../data/images/')
    tiff_imgs_paths = list(imgs_dir.rglob('*.tif'))

    add_alpha_channel = True

    cog_format_img_count = 0
    
    for img_path in tqdm(tiff_imgs_paths):
        
        # Convert to cog format if not already in cog format.
        file_name = img_path.as_posix().rsplit('/', 1)[1]
        cog_file_name = 'cog_images/' + file_name.replace('.tif', '_cog.tif')
        cog_file_path = Path(img_path.as_posix().replace(file_name, cog_file_name))

        cog_dir = cog_file_path.as_posix().rsplit('/', 1)[0]
        Path(cog_dir).mkdir(parents=False, exist_ok=True)

        try:
            # Checking if the img is already a cog.
            warnings, errors, details = validate_cloud_optimized_geotiff.validate(img_path.as_posix())
    
            if len(errors) == 0 and len(warnings) == 0:
                # is a valid cog. Being strict here, can remove the warnings condition - yet to test.
                cog_format_img_count += 1
                print(f'The image {img_path} is already in the cog format.')

                # Creating a symlink to the original file in the 'cog_images' directory.
                sym_link_path = '../' + img_path.as_posix().rsplit('/', 1)[1]
                cog_file_path.symlink_to(sym_link_path)

            else:
                convert_tiff_to_cog(img_path.as_posix(), cog_file_path.as_posix())
        
        except validate_cloud_optimized_geotiff.ValidateCloudOptimizedGeoTIFFException as e:
            print('Unable to open the file or the file is not a Tiff.')
            continue

        # Add alpha channel to the cog image if add_alpha_channel is set to True.
        if add_alpha_channel:
            print(f'Adding alpha channel to the cog image: {cog_file_path}')
            file_name = img_path.as_posix().rsplit('/', 1)[1]
            cog_alpha_file_name = 'cog_images_with_alpha_band/' + file_name.replace('.tif', '_cog_with_alpha.tif')
            cog_alpha_file_path = Path(img_path.as_posix().replace(file_name, cog_alpha_file_name))

            cog_with_alpha_dir = cog_alpha_file_path.as_posix().rsplit('/', 1)[0]
            Path(cog_with_alpha_dir).mkdir(parents=False, exist_ok=True)

            # Adding the alpha channel.
            add_alpha_channel_to_tiff(cog_file_path.as_posix(), cog_alpha_file_path.as_posix())

    print(f'Converted {len(tiff_imgs_paths)-cog_format_img_count} image(s) to cog format. {cog_format_img_count}/{len(tiff_imgs_paths)} images were already in the cog format.')