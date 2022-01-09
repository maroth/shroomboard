import dash
from dash import dcc
from dash import html
import plotly.express as px
from PIL import Image
from dash.dependencies import Input, Output

import database

app = dash.Dash(__name__)


def create_figure():
    df = database.read_data()
    fig = px.line(df, x="timestamp", y="humidity")
    fig.update_layout(yaxis_range=[0, 100])

    fig.add_hrect(
        y0=80, y1=90,
        fillcolor="PaleGreen", opacity=0.5,
        layer="below", line_width=0,
    )

    shroom_pic = Image.open("grey_oyster.jpg")

    fig.add_layout_image(
        dict(
            source=shroom_pic,
            xref="paper",
            yref="paper",
            x=0,
            y=1,
            sizex=1,
            sizey=1,
            sizing="fill",
            opacity=0.5,
            layer="below")
    )

    return fig


def host_dashboard():
    fig = create_figure()
    app.layout = html.Div(children=[
        html.H1(children='Behold our fabulous mushroom farm!'),

        html.Div(children='''
            Mushrooms are tasty and also look nice.
        '''),

        dcc.Graph(
            id='humidity-temperature-graph',
            figure=fig
        ),

        dcc.Interval(id="auto-refresh", interval=60*1000)
    ])
    app.run_server(debug=False, host='0.0.0.0')


@app.callback(Output("humidity-temperature-graph", "figure"), [Input("auto-refresh", "n_intervals")])
def update_graph(n_intervals):
    return create_figure()


