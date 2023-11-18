import html


from flask import Flask, render_template
from flask_socketio import SocketIO
import rasterio
import numpy as np
from dash import Dash, html, dcc, Output, Input


app = Flask(__name__)
app_dash = Dash(__name__, server=app, url_base_pathname='/')

#####

geotiff_path = f'C:/Users/burak/OneDrive/Desktop/hackatum23/710_5287.tif'
with rasterio.open(geotiff_path) as src:
    elevation = src.read(1) 
    
nrows,ncols=elevation.shape
x,y=np.meshgrid(np.arange(ncols),np.arange(nrows))

######
app_dash.layout = html.Div(children=[
    html.H1("How safe are you from flooding?", style={"color": "white", "display": "flex", "flex-direction": "column"}),
    
    # Plotly graph

    html.Div(id="graph_container", children=[dcc.Graph(id='example-graph'),
    dcc.Slider(0, 10, 1, value=5, marks=None, tooltip={"placement": "bottom", "always_visible": True})], 
    style={"width": "50vw"}
    ),
], style={"background-color": "black", "height": "100vh", "width": "100vw",
           "text-color": "white", "text-align": "center", "position": "absolute"})

@app_dash.callback(
    Output('dynamic-div', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_div(n):
    return f'This div has been updated {n} times.'



if __name__ == '__main__':
    app.run(debug=True)