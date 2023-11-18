import html


from flask import Flask, render_template
from flask_socketio import SocketIO
import rasterio
import numpy as np
from dash import Dash, html, dcc, Output, Input,State


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

    html.Div(id="dynamic-div", children="Dynamic!"),
    html.Div(id="dynamic-div-foto", children="Dynamic!"),

    dcc.Textarea(
            id='PLZ-field',
            style={'width': '20%', 'height': 70},
        ),

    html.Button('Enter your PLZ!', id='PLZ-button', n_clicks=0),
    html.Div(id='PLZ-out', style={'whiteSpace': 'pre-line'}),
],
style={"background-color": "black", "height": "100vh", "width": "100vw",
           "text-color": "white", "text-align": "center", "position": "absolute"}
)
    
@app_dash.callback(
    Output('dynamic-div', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_div_text(n):
    text=None
    if True is True:
        text="""It seems like your house will be flooded! No need to worry, we have prepared a checklist for your and your family's safety:<br>
            1. Create a flood plan/n
            First and foremost you need a simple but effective plan to follow when the flood happens./n
            Your plan should include an efficient route to the nearest emergency evacuation center
            while you gather all your valuables and supplies.
            All your household must agree on the plan, otherwise it doesn't mean anything!

            2. Prepare an emergency kit ASAP
            It should contain at the very least:
                + 3 days' worth food and drink supplies per person
                + First aid and medication kit
                + Flashlight and a radio with spare batteries (don't forget to put them in a waterproof bag!)
                + Warm clothing and blankets
                + Important documents, keys and some cash"""
    return text

@app_dash.callback(
    Output('PLZ-out', 'children'),
    Input('PLZ-button', 'n_clicks'),
    State('PLZ-field', 'value')
)
def update_output(n_clicks, value):
    if n_clicks > 0:
        return 'You have entered: \n{}'.format(value)

if __name__ == '__main__':
    app.run(debug=True)