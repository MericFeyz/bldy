import copy
import sys

import rasterio
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
from shapely.geometry import Point


TRANSFORM_MATRIX = None
OVERFLOW = 15


def get_coordinates(x, y):
    return TRANSFORM_MATRIX * (x, y)


def get_first_river_height(xyz_matrix, river_coordinates):
    for (x, y), value in np.ndenumerate(xyz_matrix):
        for river_coordinate in river_coordinates:
            map_coordinates = get_coordinates(x, y)
            point = Point(map_coordinates)

            if river_coordinate.contains(point):
                return x, y, value


def add_overflow(xyz_matrix, ref_point, overflow):
    ref_x = ref_point[0]
    ref_y = ref_point[1]
    ref_z = ref_point[2]

    if xyz_matrix[ref_x, ref_y] < 0:
        return

    if xyz_matrix[ref_x, ref_y] <= ref_z + overflow:
        try:
            for i in range(-3, 4):
                for j in range(-4, 5):
                    xyz_matrix[ref_x + i, ref_y + j] = -1 * (ref_z + overflow)
        except:
            return
    else:
        return

    window_size = 7
    if (
        0 <= ref_x + window_size < 1000
        and ref_z + overflow >= xyz_matrix[ref_x + window_size, ref_y] > 0
    ):
        add_overflow(
            xyz_matrix,
            (ref_x + window_size, ref_y, ref_z),
            overflow,
        )
    if (
        0 <= ref_x - window_size < 1000
        and ref_z + overflow >= xyz_matrix[ref_x - window_size, ref_y] > 0
    ):
        add_overflow(
            xyz_matrix,
            (ref_x - window_size, ref_y, ref_z),
            overflow,
        )
    if (
        0 <= ref_y + window_size < 1000
        and ref_z + overflow >= xyz_matrix[ref_x, ref_y + window_size] > 0
    ):
        add_overflow(
            xyz_matrix,
            (ref_x, ref_y + window_size, ref_z),
            overflow,
        )
    if (
        0 <= ref_y - window_size < 1000
        and ref_z + overflow >= xyz_matrix[ref_x, ref_y - window_size] > 0
    ):
        add_overflow(
            xyz_matrix,
            (ref_x, ref_y - window_size, ref_z),
            overflow,
        )


def main():
    global TRANSFORM_MATRIX
    sys.setrecursionlimit(100000)

    print("Loading the map data...")
    geotif_path = f"./data/test2.tif"
    tif_file = rasterio.open(geotif_path)

    elevation_matrix = tif_file.read(1)
    elevation_matrix_flood = copy.deepcopy(elevation_matrix)
    tif_file.close()

    # Used for getting the real life coordinates from x, y
    # see get_coordinates()
    TRANSFORM_MATRIX = tif_file.transform

    print("Loading the shape data...")
    sf = gpd.read_file("./data/shape_files/tn_09162")
    isar_coordinates = sf[sf.name == "Isar"]["geometry"]

    print("Detecting river altitude...")
    river_ref_point = get_first_river_height(elevation_matrix_flood, isar_coordinates)

    print("Simulating flow...")
    add_overflow(elevation_matrix_flood, river_ref_point, OVERFLOW)

    for (x, y), value in np.ndenumerate(elevation_matrix_flood):
        if elevation_matrix_flood[x, y] < 0:
            elevation_matrix_flood[x, y] = -1 * elevation_matrix_flood[x, y]

    print("Generating figure...")
    nrows, ncols = elevation_matrix.shape
    x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))

    z = elevation_matrix_flood
    # sh_0, sh_1 = z.shape
    # x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(
        title="Mt Bruno Elevation",
        autosize=False,
        width=500,
        height=500,
        margin=dict(l=65, r=50, b=65, t=90),
    )
    fig.show()


if __name__ == "__main__":
    main()
