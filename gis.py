import copy
import sys

import rasterio
import numpy as np
import plotly.graph_objects as go
import geopandas as gpd
from shapely.geometry import Point
import time

TRANSFORM_MATRIX = None
ELEVATION_MATRIX = None
ISAR_COORD = None

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
                for j in range(-3, 4):
                    xyz_matrix[ref_x + i, ref_y + j] = -1 * (ref_z + overflow)
        except Exception as e:
            print(e)
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


def load():
    global TRANSFORM_MATRIX
    global ELEVATION_MATRIX
    global ISAR_COORD

    print("Loading the map data...")
    geotif_path = f"./data/test2.tif"
    tif_file = rasterio.open(geotif_path)

    ELEVATION_MATRIX = tif_file.read(1)
    tif_file.close()

    # Used for getting the real life coordinates from x, y
    # see get_coordinates()
    TRANSFORM_MATRIX = tif_file.transform

    print("Loading the shape data...")
    sf = gpd.read_file("./data/shape_files/tn_09162")
    ISAR_COORD = sf[sf.name == "Isar"]["geometry"]

def run(overflow :int):
    sys.setrecursionlimit(100000)
    elevation_matrix_flood = copy.deepcopy(ELEVATION_MATRIX)
    print("Detecting river altitude...")
    river_ref_point = get_first_river_height(elevation_matrix_flood, ISAR_COORD)

    print("Simulating flow...")
    add_overflow(elevation_matrix_flood, river_ref_point, overflow)

    for (x, y), value in np.ndenumerate(elevation_matrix_flood):
        if elevation_matrix_flood[x, y] < 0:
            elevation_matrix_flood[x, y] = -1 * elevation_matrix_flood[x, y]

    print("Generating figure...")
    nrows, ncols = ELEVATION_MATRIX.shape
    x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))

    z = elevation_matrix_flood
    # sh_0, sh_1 = z.shape
    # x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title='Isar Flood Map', autosize=False,
                scene = dict(
                    xaxis = dict(showbackground=False, showticklabels=False, ),
                    yaxis = dict(showbackground=False, showticklabels=False, ),
                    zaxis = dict(nticks=5, range=[200,800], showbackground=False,showticklabels=False,),
                    xaxis_title='',
                    yaxis_title='',
                    zaxis_title='',),
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig


# if __name__ == "__main__":
#     sys.setrecursionlimit(100000)
#     load()
#     fig1=run(15)
#     print("Its over")
#     sys.setrecursionlimit(100000)
#     fig2=run(20)
#     sys.setrecursionlimit(100000)
#     fig3=run(25)
#     fig1.show()
#     fig2.show()
#     fig3.show()
