from logging import warning
from osgeo import gdal
from pathlib import Path
from tqdm import tqdm
import validate_cloud_optimized_geotiff

def convert_tiff_to_cog(in_img_path, out_img_path):
    _ = gdal.Translate(
        srcDS=in_img_path,
        destName=out_img_path,
        options="-of COG -co COMPRESS=LZW -co NUM_THREADS=ALL_CPUS -co BIGTIFF=IF_SAFER"
    )

if __name__=='__main__':

    imgs_dir = Path('../data/images/')
    tiff_imgs_paths = list(imgs_dir.rglob('*.tif'))

    cog_format_img_count = 0
    
    for img_path in tqdm(tiff_imgs_paths):
        try:
            # Checking if the img is already a cog.
            warnings, errors, details = validate_cloud_optimized_geotiff.validate(img_path.as_posix())
            if len(warnings) == 0 and len(errors) == 0:
                # is a valid cog. Being strict here, can remove the warnings condition - yet to test.
                cog_format_img_count += 1
                print(f'The image {img_path} is already in the cog format.')
            else:
                file_name = img_path.as_posix().rsplit('/', 1)[1]
                cog_file_name = 'cog_images/' + file_name.replace('.tif', '_cog.tif')
                cog_file_path = Path(img_path.as_posix().replace(file_name, cog_file_name))
                cog_dir = cog_file_path.as_posix().rsplit('/', 1)[0]
                Path(cog_dir).mkdir(parents=False, exist_ok=True)
                convert_tiff_to_cog(img_path.as_posix(), cog_file_path.as_posix())
        except validate_cloud_optimized_geotiff.ValidateCloudOptimizedGeoTIFFException as e:
            print('Unable to open the file or the file is not a Tiff.')
    
    print(f'Converted {len(tiff_imgs_paths)-cog_format_img_count} image(s) to cog format. {cog_format_img_count}/{len(tiff_imgs_paths)} images were already in the cog format.')