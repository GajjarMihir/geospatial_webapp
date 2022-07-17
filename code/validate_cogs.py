import validate_cloud_optimized_geotiff
from pathlib import Path
from tqdm import tqdm

if __name__ == '__main__':
    imgs_dir = Path('../data/images/')
    tiff_imgs_paths = list(imgs_dir.rglob('*.tif'))
    cog_imgs_paths = [path for path in tiff_imgs_paths if "cog" in path.as_posix()]
    # for img_path in tqdm(cog_imgs_paths):
    #     validate_cloud_optimized_geotiff.validate(img_path.as_posix())
    # print(validate_cloud_optimized_geotiff.validate('/Volumes/Area51/Statcan/construction_starts/geospatial_webapp/data/images/train/5ae242fd0b093000130afd27.tif'))
    y = validate_cloud_optimized_geotiff.validate('/Volumes/Area51/Statcan/construction_starts/geospatial_webapp/data/images/train/cog_images/5ae242fd0b093000130afd27_cog.tif')
    x = validate_cloud_optimized_geotiff.validate('/Users/mihir/Downloads/30cm_vs_50cm_SaltLakeCity_WV3_ColorBalnce_Demos/SaltLake_WV3_30cm_ColorBalance.tif')
    print(len(x))
    print(x)
    print(x[0])
    print(len(y))
    print(y)
    print(y[0])