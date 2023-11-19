import html


from flask import Flask, render_template
from flask_socketio import SocketIO
import rasterio
import numpy as np
from dash import Dash, html, dcc, Output, Input,State
from gis import load, run
import sys

initial = True
load()
fig, is_alive, elevation_difference = run(0)
elevation_difference=0
app = Flask(__name__)
app_dash = Dash(__name__, server=app, url_base_pathname='/')

items1 = ["1. Create a flood plan:", "First and foremost you need a simple but effective plan to follow when the flood happens.",
         "Your plan should include an efficient route to the nearest emergency evacuation center while you gather all your valuables and supplies.",
         "All your household must agree on the plan, otherwise it doesn't mean anything!"]

items2 = ["2. Prepare an emergency kit ASAP:", "It should contain at the very least:",
          "3 days' worth food and drink supplies per person", "First aid and medication kit",
          "Flashlight and a radio with spare batteries (don't forget to put them in a waterproof bag!)",
          "Warm clothing and blankets",
          "Important documents, keys and some cash"]

items3=['With ever accelerating climate change floods have become increasingly dangerous.',
            'Although some terrible catastrophes like Arthal incident in 2021 happened, few people are aware and prepared for such events in Munich']

items4 = ['Good News, your location looks safe!',
          'It is important to raise awareness about dangers of floods!']

warning = html.Div(id='warning', children=[html.Div(
        "It seems like your house will be flooded! No need to worry, we have prepared a checklist for your and your family's safety:",
        style={"color": "white"}),
            html.Div(children=[html.H3(items1[0])] + [html.Div(item) for item in items1[1:]], style={"color": "white"}),
            html.Div(children=[html.H3(items2[0])] + [html.Div(items2[1])] + [
            html.Ul(children=[html.Li(item) for item in items2[2:]])], style={"color": "white"})], style={"display": "flex", "flex-direction": "column", "width": "50vw"})

zero_state = html.Div(id="zero_state", children=[html.H2(item) for item in items3], style={"color": "white", "width": "50vw"})
alive_state = html.Div(id="alive_state", children=[html.H2(item) for item in items4], style={"color": "white", "width": "50vw"})


prompt = html.Div(id='prompt',children=[zero_state])



#####


######
app_dash.layout = html.Div(children=[
    html.H1("How safe are you from flooding?", style={"color": "white", "display": "flex", "flex-direction": "column", "text-align": "center"}),

    # Plotly graph
    html.Div(children = [html.Div(id="graph_container", children=[dcc.Graph(id='3d-graph', figure=fig, style={"padding-right": "40px"}),
    dcc.Slider(0, 20, 5, value=0,id='slider', marks=None, tooltip={"placement": "bottom", "always_visible": True}),
    ],
    style={"display": "flex", "flex-direction": "column"}
    )] + [prompt], style={"display": "flex", "flex-direction": "row"}),

    dcc.Textarea(
            id='PLZ-field',
            style={'width': '20%', 'height': '20px'},
        ),

    html.Button('Check!', id='PLZ-button', n_clicks=0),
    html.Div(id='PLZ-out', style={'whiteSpace': 'pre-line', "color": "white"}),

],
style={"background-color": "black", "height": "100vh", "width": "100vw",
           "font-size": "1.75rem", "align-items": "center", "text-color": "white", "overflow": "hidden !important"}
)


    
@app_dash.callback(
    Output('dynamic-div', 'children'),
    Input('interval-component', 'n_intervals')
)



    
@app_dash.callback(
    Output('3d-graph', 'figure'),
    Input('slider', 'value'),
)
def update_map_slider(value):
    global is_alive,elevation_difference
    sys.setrecursionlimit(100000)
    fig,is_alive,elevation_difference=run(value)
    print(f'is_alive in run{is_alive}')
    return fig

@app_dash.callback(
    Output('prompt', 'children'),
    Input('PLZ-button', 'n_clicks'),
)
def update_text(placeholder):
    print(f'is_alive{is_alive}')
    print(f'elevation{elevation_difference}')
    global initial
    if initial:
        initial = False
        return zero_state
    if is_alive:
        return alive_state
    else:
        return warning
if __name__ == '__main__':
    app.run(debug=True)