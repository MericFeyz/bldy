import rasterio
from rasterio.transform import from_origin
import numpy as np
from mayavi import mlab

# Load the GeoTIFF data using rasterio
geotiff_path = f'C:/Users/yigit/Desktop/UNI/RCI/1.Semester/hackatum/bldy/data/test2.tif'
with rasterio.open(geotiff_path) as src:
    elevation = src.read(1) 
    
nrows,ncols=elevation.shape
x,y=np.meshgrid(np.arange(ncols),np.arange(nrows))
z=elevation

z_test=z
z_test[z_test<=505]=505

mesh=mlab.mesh(x,y,z_test,colormap='terrain')
desired_elevation = 510

# Show the plot
mlab.show()
