# Script to convert .geojson to .shp

# Imports
import geopandas as gpd
import argparse
from pathlib import Path

if __name__ == '__main__':
    # Create an argument parser
    parser = argparse.ArgumentParser(description='Convert geojson to shapefile.')

    # Add arguments
    parser.add_argument('path_to_input_geojson_files_dir', type=str, help='Path to the input geojson files.')
    parser.add_argument('path_to_output_shapefiles_dir', type=str, help='Path to the output shapefile directory.')
    
    # Parse the arguments
    args = parser.parse_args()

    # Get the input and output paths
    input_geojson_files_dir = Path(args.path_to_input_geojson_files_dir)
    output_shapefiles_dir = Path(args.path_to_output_shapefiles_dir)

    # Create the output directory if it does not exist already.
    output_shapefiles_dir.mkdir(parents=False, exist_ok=True)

    # Get the geojson files
    geojson_files = input_geojson_files_dir.rglob('*.geojson')

    # Iterating over the geojson files and converting them to shapefiles.
    for geojson_file in geojson_files:
        geojson_file_name = geojson_file.name.rsplit('.', 1)[0]
        output_shapefile_path = output_shapefiles_dir / (geojson_file_name + '.shp')
        print(f'Converting {geojson_file} to {output_shapefile_path}')
        gdf = gpd.read_file(geojson_file)
        gdf.to_file(output_shapefile_path, driver='ESRI Shapefile')
        print(f'Done converting {geojson_file} to {output_shapefile_path}')
        print('-' * 50)