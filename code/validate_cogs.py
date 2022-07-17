# Checks if the generated cog images are in a valid cog format.

import validate_cloud_optimized_geotiff
from pathlib import Path
from tqdm import tqdm

if __name__ == '__main__':
    
    imgs_dir = Path('../data/images/')
    tiff_imgs_paths = list(imgs_dir.rglob('*.tif'))
    cog_imgs_paths = [path for path in tiff_imgs_paths if "cog" in path.as_posix()]
    valid_cog_imgs_count = 0

    for img_path in tqdm(cog_imgs_paths):
        try:
            warnings, errors, details = validate_cloud_optimized_geotiff.validate(img_path.as_posix())
            if len(errors) == 0 and len(warnings) == 0:
                valid_cog_imgs_count += 1
            else:
                print(f'{img_path} is not in the cog format.')
        except validate_cloud_optimized_geotiff.ValidateCloudOptimizedGeoTIFFException as e:
            print('Unable to open the file or the file is not a Tiff.')
            continue

    print(f'In the cog_images dirs, {valid_cog_imgs_count}/{len(cog_imgs_paths)} images are in the cog format.')