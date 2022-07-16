from osgeo import gdal
from pathlib import Path
from tqdm import tqdm

def convert_tiff_to_cog(in_img_path, out_img_path):
    _ = gdal.Translate(
        srcDS=in_img_path,
        destName=out_img_path,
        options="-of COG -co COMPRESS=LZW -co NUM_THREADS=ALL_CPUS -co BIGTIFF=IF_SAFER"
    )

if __name__=='__main__':

    tiff_imgs_dir = Path('../data/images/')
    tiff_imgs_paths = list(tiff_imgs_dir.rglob('*.tif'))

    Path('../data/images/train/cog_images/').mkdir(parents=False, exist_ok=True)
    Path('../data/images/val/cog_images/').mkdir(parents=False, exist_ok=True)
    Path('../data/images/test/cog_images/').mkdir(parents=False, exist_ok=True)

    for path in tqdm(tiff_imgs_paths):
        file_name = path.as_posix().rsplit('/', 1)[1]
        cog_file_name = 'cog_images/' + file_name.replace('.tif', '_cog.tif')
        cog_file_path = Path(path.as_posix().replace(file_name, cog_file_name))
        convert_tiff_to_cog(path.as_posix(), cog_file_path.as_posix())