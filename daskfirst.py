import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from data import *
import dash  # (version 1.12.0) pip install dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

dff = JSONtoDataframe('Stock List.json')

companies = dff['symbol'].unique()

app.layout = html.Div([

    html.H1("Visualizing Stock Market Data", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_graph",
                 options=[
                     {"label": "OHLC", "value": 1},
                     {"label": "CandleStick", "value": 2},
                     {"label": "ColoredBar", "value": 3},
                     {"label": "VertexLine", "value": 4}],
                 multi=False,
                 value=1,
                 style={'width': "40%"}
                 ),
    dcc.Dropdown( id = 'slct_comp',
                    options = [{'value':i,'label':i} for i in companies],
                    value ='AAPL',
                    style={'width': "40%"}),
    html.Br(),
    html.Div(id='output_container', children=[]),
    dcc.Graph(id='graph_type', figure={})

])


@app.callback(
    [Output(component_id='graph_type', component_property='figure'),
    Output(component_id='output_container', component_property='children')],
    [Input(component_id='slct_graph', component_property='value'),
    Input(component_id='slct_comp', component_property='value')]
)
def update_graph(option_slctd,option_comp):
    print(option_slctd)
    print(type(option_slctd))
    container = "The stock chosen is {} and the type of graph is {}".format(option_comp,option_slctd)
    df = dff[dff['symbol']==option_comp]

    if option_slctd == 1:
        fig = go.Figure(data=go.Ohlc(x=df['date'],
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close']))
    elif option_slctd == 2:
        fig = go.Figure(data=[go.Candlestick(x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])
    elif option_slctd == 3:
        fig = px.bar(df, x=df["date"], y=[df['open'],df['high'],df['low'],df['close']])

    elif option_slctd == 4:
        fig = px.line(df, x=df["date"], y=[df['open'],df['high'],df['low'],df['close']])

    return fig, container


if __name__ == '__main__':
    app.run_server(debug=True)
