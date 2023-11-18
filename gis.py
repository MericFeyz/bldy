
import rasterio
from rasterio.transform import from_origin
import numpy as np

import plotly.graph_objects as go

# Load the GeoTIFF data using rasterio
geotiff_path = f'C:/Users/yigit/Desktop/UNI/RCI/1.Semester/hackatum/bldy/data/test2.tif'
with rasterio.open(geotiff_path) as src:
    elevation = src.read(1) 
    
nrows,ncols=elevation.shape
x,y=np.meshgrid(np.arange(ncols),np.arange(nrows))


z = elevation
sh_0, sh_1 = z.shape
#x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                  width=500, height=500,
                  margin=dict(l=65, r=50, b=65, t=90))
fig.show()