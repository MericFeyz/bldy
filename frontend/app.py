import html


from flask import Flask, render_template
from flask_socketio import SocketIO
import rasterio
import numpy as np
from dash import Dash, html, dcc, Output, Input


app = Flask(__name__)
app_dash = Dash(__name__, server=app, url_base_pathname='/')

#####

geotiff_path = f'C:/Users/yigit/Desktop/UNI/RCI/1.Semester/hackatum/bldy/data/test2.tif'
with rasterio.open(geotiff_path) as src:
    elevation = src.read(1) 
    
nrows,ncols=elevation.shape
x,y=np.meshgrid(np.arange(ncols),np.arange(nrows))

######
app_dash.layout = html.Div(children=[
    html.H1("How safe are you from flooding?"),
    
    # Plotly graph
    dcc.Graph(
        id='example-graph'
    ),
    
    # Changing div
    html.Div(id='dynamic-div', children='This div will change dynamically.'),
    
    dcc.Slider(0, 10, 1, value=5, marks=None,
    tooltip={"placement": "bottom", "always_visible": True}),
    
    #Callback to update the changing div
    """dcc.Interval(
        id='interval-component',
        interval=2 * 1000,  # in milliseconds
        n_intervals=0
    )"""
])

@app_dash.callback(
    Output('dynamic-div', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_div(n):
    return f'This div has been updated {n} times.'



if __name__ == '__main__':
    app.run(debug=True)