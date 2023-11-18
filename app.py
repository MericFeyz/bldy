import html


from flask import Flask, render_template
from flask_socketio import SocketIO
import rasterio
import numpy as np
from dash import Dash, html, dcc, Output, Input,State
from gis import load, run

load()
fig = run(15)

app = Flask(__name__)
app_dash = Dash(__name__, server=app, url_base_pathname='/')

#####


######
app_dash.layout = html.Div(children=[
    html.H1("How safe are you from flooding?", style={"color": "white", "display": "flex", "flex-direction": "column"}),
    html.H2("H2 efenimm?"),


    # Plotly graph

    html.Div(id="graph_container", children=[dcc.Graph(id='example-graph', figure=fig),
    dcc.Slider(0, 10, 1, value=5, marks=None, tooltip={"placement": "bottom", "always_visible": True}),
    html.Div(id="dynamic-div", children="Dynamic!", style={"color": "white"})], 
    style={"height": "70%", "display": "flex", "flex-direction": "row"}
    ),

    html.Div(id="dynamic-div-foto", children="Dynamic!"),

    dcc.Textarea(
            id='PLZ-field',
            style={'width': '20%', 'height': 70},
        ),

    html.Button('Enter your PLZ!', id='PLZ-button', n_clicks=0),
    html.Div(id='PLZ-out', style={'whiteSpace': 'pre-line', "color": "white"}),

    dcc.Interval(id='interval-component', interval=2 * 1000, n_intervals=0),
],
style={"background-color": "black", "height": "100vh", "width": "100vw",
           "text-color": "white", "text-align": "center", "position": "absolute", "overflow": "hidden !important"}
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