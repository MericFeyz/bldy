import rasterio
from rasterio.transform import from_origin
import numpy as np
from mayavi import mlab

# Load the GeoTIFF data using rasterio
geotiff_path = f'C:/Users/yigit/Desktop/UNI/RCI/1.Semester/hackatum/bldy/data/test2.tif'
with rasterio.open(geotiff_path) as src:
    elevation = src.read(1)  # Assuming the elevation data is in the first band

    # Get the geotransform information to calculate coordinates
    #transform = src.transform
    #x_size = src.width
    #y_size = src.height

    # Create coordinate grids
    #x, y = np.meshgrid(np.linspace(transform[2], transform[2] + transform[0] * (x_size - 1), x_size),
                      #np.linspace(transform[5], transform[5] + transform[4] * (y_size - 1), y_size))


nrows,ncols=elevation.shape
x,y=np.meshgrid(np.arange(ncols),np.arange(nrows))
z=elevation
mesh=mlab.mesh(x,y,z)
# Create a Mayavi figure
#fig = mlab.figure()

# Create a surface plot of the topography
#surf = mlab.surf(x, y, elevation, colormap='terrain')

# Add contours to the surface plot
#contour = mlab.contour_surf(x, y, elevation, contours=10, colormap='terrain')

# Add a color bar to the figure
#mlab.colorbar(orientation='vertical')

# Show the plot
mlab.show()