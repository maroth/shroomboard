import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from PIL import Image
from random import randint
from datetime import datetime
import sqlite3
from time import sleep
from threading import Thread
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


@app.callback(Output("humidity-temperature-graph", "figure"), [Input("auto-refresh", "n_intervals")])
def update_graph(n_intervals):
    return create_figure()


def get_connection():
    return sqlite3.connect('shroomboard.db')


def read_sensor_data():
    delta = randint(-5, 5)
    humidity = last_humidity + delta
    humidity = max(humidity, 0)
    humidity = min(humidity, 100)
    now = datetime.now()
    temperature = 80
    return now, humidity, temperature


def create_table():
    cur = get_connection().cursor()
    cur.execute('''DROP TABLE IF EXISTS measurement''')
    cur.execute('''CREATE TABLE measurement
                   (timestamp datetime, humidity float, temperature float)''')


def write_data(timestamp, humidity, temperature):
    with get_connection() as connection:
        cur = connection.cursor()
        timestamp_formatted = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        statement = f"INSERT INTO measurement (timestamp, humidity, temperature) " \
                    f"VALUES ('{timestamp_formatted}', {humidity}, {temperature})"
        cur.execute(statement)
        cur.close()


def write_sensor_data_loop():
    while True:
        timestamp, humidity, temperature = read_sensor_data()
        write_data(timestamp, humidity, temperature)
        sleep(5)


def read_data():
    with get_connection() as connection:
        df = pd.read_sql_query("SELECT * FROM measurement", connection)
    return df


last_humidity = 40


def create_figure():
    df = read_data()
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
    app.run_server(debug=True, host='0.0.0.0')


if __name__ == '__main__':
    create_table()
    loop = Thread(target=write_sensor_data_loop)
    loop.start()
    host_dashboard()
