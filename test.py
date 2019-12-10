import dash
import json
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import math
import numpy as np
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})
app.config.suppress_callback_exceptions = True
df = pd.read_csv('https://raw.githubusercontent.com/hunterjimenezsbu/DataViz/master/listings.csv')


app.layout = html.Div(
    [html.Div([html.H1("Airbnb Stats")], style={'textAlign': "center", 'padding': 10}),
     html.Div([
         dcc.RadioItems(id="Housingtype", value=str(1), labelStyle={'display': 'inline-block', 'padding': 10},
                        options=[{'label': "Entire home/apt", 'value': "Entire home/apt"}, {'label': "Private room", 'value': "Private room"}], )], style={'textAlign': "center", }),
     html.Div([html.Div([dcc.Graph(id="scatter-graph", hoverData={'points': [{'customdata': '30'}]})], ), ], style={"height": 600, "width": 1600}),
     html.Div([html.Div([dcc.Graph(id="hist-graph", clear_on_unhover=True, )], ), ], style={"height": 600, "width": 1600}),
     html.Div([html.Div([dcc.Graph(id="hist-money", clear_on_unhover=True, )], ), ], style={"height": 600, "width": 1600}),
     html.Div([html.Div([dcc.Graph(id="scatter-money", hoverData={'points': [{'customdata': '30'}]})], ), ], style={"height": 600, "width": 1600}),
     ], style={"height": 1600, "width": 1600})


@app.callback(
    dash.dependencies.Output("scatter-graph", "figure"),
    [dash.dependencies.Input("Housingtype", "value"), dash.dependencies.Input("hist-graph", "clickData")])
def update_scatter(selected, clickdata):
    dff = df[df["room_type"] == selected]
    trace = []
    for neighbourhood_group in df.neighbourhood_group.unique():
        trace.append(go.Scatter(x=dff[dff["neighbourhood_group"] == neighbourhood_group]["latitude"], y=dff[dff["neighbourhood_group"] == neighbourhood_group]["longitude"], mode="markers",
                                name=neighbourhood_group.title(), customdata=df[df['neighbourhood_group'] == neighbourhood_group]['neighbourhood'], text=df[df['neighbourhood_group'] == neighbourhood_group]['neighbourhood'],
                                marker={"size": 10, "line": {"color": "#25232C", "width": .5}}))

    layout = go.Layout(title=f"Laititude VS. Longitude", colorway=['#1db954', '#8080ff', '#eeb932', '#ff00ff', '#7d0d2b'], hovermode='closest',
                       xaxis={"title": "Latitude", "range": [40.4, 41], "showgrid": False, },
                       yaxis={"title": "Longitude", "range": [-73.6, -74.4],
                              "showgrid": False, },)
    figure1 = {"data": trace, "layout": layout}
    if clickdata is not None:
        age = clickdata["points"][0]['customdata']
        size1 = []
        size2 = []
        size3 = []
        size4 = []
        size5 = []
        for i in dff[dff["neighbourhood_group"] == "Manhattan"]["latitude"]:
            if "Manhattan" in age:
                size1.append(25)
                color.append("#000000")
            else:
                size1.append(0)
        for i in dff[dff["neighbourhood_group"] == "Brooklyn"]["latitude"]:
            if "Brooklyn" in age:
                size2.append(10)

            else:
                size2.append(0)
        for i in dff[dff["neighbourhood_group"] == "Bronx"]["latitude"]:
            if "Bronx" in age:
                size3.append(10)
            else:
                size3.append(0)
        for i in dff[dff["neighbourhood_group"] == "Queens"]["latitude"]:
            if "Queens" in age:
                size4.append(10)
            else:
                size4.append(0)
        for i in dff[dff["neighbourhood_group"] == "Staten Island"]["latitude"]:
            if "Staten Island" in age:
                size5.append(10)
            else:
                size5.append(0)

        figure1["data"][0].update(go.Scatter(marker={"size": size1, "opacity": 1}))
        figure1["data"][1].update(go.Scatter(marker={"size": size2, "opacity": 1}))
        figure1["data"][2].update(go.Scatter(marker={"size": size3, "opacity": 1}))
        figure1["data"][3].update(go.Scatter(marker={"size": size4, "opacity": 1}))
        figure1["data"][4].update(go.Scatter(marker={"size": size5, "opacity": 1}))

    return figure1

@app.callback(
    dash.dependencies.Output("hist-graph", "figure"),
    [dash.dependencies.Input("Housingtype", "value"), dash.dependencies.Input('scatter-graph', 'clickData'), ])
def update_graph(selected, clickdata):
    dff = df[df["room_type"] == selected]
    trace = go.Histogram(x=dff["neighbourhood"], opacity=0.8, marker={"line": {"color": "#0000ff", "width": 5.0}},
                          customdata=dff["neighbourhood_group"], )
    layout = go.Layout(title=f"Count vs Neighbourhood", xaxis={"title": "Neibhbourhood", "showgrid": False},
                       yaxis={"title": "Count", "showgrid": False}, )
    figure2 = {"data": [trace], "layout": layout}

    def create_bins(lower_bound, width, quantity):
        bins = []
        for low in range(lower_bound,
                         lower_bound + quantity * width + 1, width):
            bins.append((low, low + width))
        return bins
    t =0
    for i in df.neighbourhood.unique():
        t = t + 1
    bins = create_bins(lower_bound=0, width=10, quantity=t)

    def find_bin(value, bins):
        k=0

        for i in dff.neighbourhood.unique():
            if i in value:
                return k
            k = k + 1
        return -1

    if clickdata is not None:
        age = clickdata["points"][0]['customdata']
        # return json.dumps(age, indent=2)
        color = []
        for i in range(0, len(bins)):
            if bins[i] == bins[find_bin(age, bins)]:
                color.append("#ff0000")
            else:
                color.append("#0000ff")

        # noinspection PyTypeChecker
        figure2["data"][0].update(go.Histogram(marker={"color": color}))
    return figure2
@app.callback(
    dash.dependencies.Output("hist-money", "figure"),
    [dash.dependencies.Input("Housingtype", "value"), dash.dependencies.Input('scatter-graph', 'clickData'), ])
def update_graph_money(selected, clickdata):
    dff = df[df["room_type"] == selected]
    trace = go.Histogram(x=dff["price"], opacity=0.7, marker={"line": {"color": "#0000ff", "width": 5.0}},
                          customdata=dff["neighbourhood_group"], )
    layout = go.Layout(title=f"Count vs Price", xaxis={"title": "Price", "showgrid": False},
                       yaxis={"title": "Count", "showgrid": False}, )
    figure2 = {"data": [trace], "layout": layout}

    def create_bins(lower_bound, width, quantity):
        bins = []
        for low in range(lower_bound,
                         lower_bound + quantity * width + 1, width):
            bins.append((low, low + width))
        return bins
    t =0
    for i in df.neighbourhood.unique():

        t = t + 1


    bins = create_bins(lower_bound=0, width=10, quantity=20)

    def find_bin(value, bins):
        for i in df.neighbourhood_group.unique():
            if i in value:
                return i
        return -1

    if clickdata is not None:
        age = clickdata["points"][0]['customdata']
        color = []
        for i in range(0, len(bins)):
            if bins[i] == bins[find_bin(age, bins)]:
                color.append("#dd1c77")
            else:
                color.append("#fa9fb5")

        # noinspection PyTypeChecker
        figure2["data"][0].update(go.Histogram(marker={"color": color}))
    return figure2
@app.callback(
    dash.dependencies.Output("scatter-money", "figure"),
    [dash.dependencies.Input("Housingtype", "value"), dash.dependencies.Input("hist-graph", "clickData")])
def update_scatter(selected, clickdata):
    dff = df[df["room_type"] == selected]
    trace = []
    for neighbourhood_group in df.neighbourhood_group.unique():
        trace.append(go.Scatter(x=dff[dff["neighbourhood_group"] == neighbourhood_group]["price"], y=dff[dff["neighbourhood_group"] == neighbourhood_group]["calculated_host_listings_count"], mode="markers",
                                name=neighbourhood_group.title(), customdata=df[df['neighbourhood_group'] == neighbourhood_group]['neighbourhood'], text=df[df['neighbourhood_group'] == neighbourhood_group]['price'],
                                marker={"size": 10, "line": {"color": "#25232C", "width": .5}}))

    layout = go.Layout(title=f"Price VS Airbnb #", colorway=['#1db954', '#8080ff', '#eeb932', '#ff00ff', '#7d0d2b'], hovermode='closest',
                       xaxis={"title": "Price", "range": [75, 200], "showgrid": False, },
                       yaxis={"title": "Airbnb #", "range": [-1, 25],
                              "showgrid": False, },)
    figure1 = {"data": trace, "layout": layout}
    if clickdata is not None:
        age = clickdata["points"][0]['customdata']
        size1 = []
        color = []
        for i in dff[dff["neighbourhood_group"] == "Manhattan"]["latitude"]:
            if "Manhattan" in age:
                size1.append(25)
                color.append("#000000")
            else:
                size1.append(0)
        size2 = []
        size3 = []
        size4 = []
        size5 = []
        for i in dff[dff["neighbourhood_group"] == "Brooklyn"]["latitude"]:
            if "Brooklyn" in age:
                size2.append(10)

            else:
                size2.append(0)
        for i in dff[dff["neighbourhood_group"] == "Bronx"]["latitude"]:
            if "Bronx" in age:
                size3.append(10)
            else:
                size3.append(0)
        for i in dff[dff["neighbourhood_group"] == "Queens"]["latitude"]:
            if "Queens" in age:
                size4.append(10)
            else:
                size4.append(0)
        for i in dff[dff["neighbourhood_group"] == "Staten Island"]["latitude"]:
            if "Staten Island" in age:
                size5.append(10)
            else:
                size5.append(0)
        # noinspection PyTypeChecker
        figure1["data"][0].update(go.Scatter(marker={"size": size1, "opacity": 1}))
        # noinspection PyTypeChecker
        figure1["data"][1].update(go.Scatter(marker={"size": size2, "opacity": 1}))
        figure1["data"][2].update(go.Scatter(marker={"size": size3, "opacity": 1}))
        figure1["data"][3].update(go.Scatter(marker={"size": size4, "opacity": 1}))
        figure1["data"][4].update(go.Scatter(marker={"size": size5, "opacity": 1}))

    return figure1



if __name__ == '__main__':
    app.run_server(debug=True)