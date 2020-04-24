
import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go

import pandas as pd
from datetime import datetime
import numpy as np

# Initialization
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#%% Load data
df = pd.read_csv('data/stock_prices.csv')
df['shortened_date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')
# df.head()

# Plot stock movements for 2016
year = 2016
# Get available stocks
unique_stocks = np.unique(df['symbol'].values)              

available_years = np.unique(df['shortened_date'].dt.year.values)
app.layout = html.Div([
    html.Div([
        html.Div([
                html.Div(
                [
                    html.P("""Compare:""",
                            style={'margin-right': '2em'})
                ],style={'width': '200'}),
                dcc.Dropdown(
                    id='stock1',
                    options=[{'label': i, 'value': i} for i in unique_stocks],
                    value=unique_stocks[0],
                    style={'width': '40%', 'display': 'inline-block'}
                ),
                html.Div(
                [
                    html.P("""To:""",
                            style={'margin-right': '2em'})
                ],style={'width': '200'}),                
                dcc.Dropdown(
                    id='stock2',
                    options=[{'label': i, 'value': i} for i in unique_stocks],
                    value=unique_stocks[1],
                    style={'width': '40%', 'display': 'inline-block'}
                    # ,
                    # labelStyle={'display': 'inline-block'}
                )
        ],
        style={'display': 'flex'}),
        html.Div([
        html.Div(
                [
                    html.P("""Year:""",
                            style={'margin-right': '4em'})
                ],style={'width': '300'}),
        dcc.Dropdown(
            id='year',
            options=[{'label': i, 'value': i} for i in available_years],
            value=available_years[0],
            style={'width': '40%', 'display': 'inline-block'}),
        html.Div(
                [
                    html.P("""Figure to Show:""",
                            style={'margin-right': '4em'})
                ],style={'width': '300'}),            
        dcc.RadioItems(
            id='plot-type',
            options=[{'label': i, 'value': i} for i in ['open-close', 'volume']],
            value='open-close',
            labelStyle={'display':'inline-block', 'width':'100%'}
        )
        ],
        style={'display': 'flex'})
    ]),
    
    dcc.Graph(id='graph')

])
@app.callback(Output('graph', 'figure'), 
                [Input('stock1', 'value'),
                 Input('stock2', 'value'),
                 Input('year','value'),
                 Input('plot-type', 'value')])
def update_graph(stock_name1, stock_name2, year, plot_type):
    data1 = df.loc[(df['symbol'] == stock_name1) & (df['shortened_date'].dt.year == year),:]
    data2 = df.loc[(df['symbol'] == stock_name2) & (df['shortened_date'].dt.year == year),:]
    mean1 = data1[['high','low']].mean(axis=1)
    mean2 = data2[['high','low']].mean(axis=1)
    fig = go.Figure()

    if plot_type == 'open-close':
        fig.add_trace(
            go.Candlestick(x=data1['shortened_date'],
                        open=data1.open,
                        high=data1.high,
                        low=data1.low,
                        close=data1.close,
                        showlegend=False)
                        )

        fig.add_trace(
            go.Candlestick(x=data2['shortened_date'],
                        open=data2.open,
                        high=data2.high,
                        low=data2.low,
                        close=data2.close,
                        showlegend=False)
                        )
        fig.add_trace(
            go.Scatter(x=data2['shortened_date'],
                        y=mean1,
                        name='Mean price of\n' + stock_name1,
                        line_color='blue')
                        )
        fig.add_trace(
            go.Scatter(x=data2['shortened_date'],
                        y=mean2,
                        name='Mean price of\n ' + stock_name2)
                        )
    else: 
        fig.add_trace(
            go.Scatter(x=data1['shortened_date'],
                        y=data1['volume'],
                        name='Volume of\n' + stock_name1,
                        line_color='blue')
                        )
        fig.add_trace(
            go.Scatter(x=data2['shortened_date'],
                        y=data2['volume'],
                        name='Volume of\n ' + stock_name2)
                        )                                      
    fig.update_layout(
        title='Candlestick Plot' if plot_type == 'open-close' else 'Volume Plot',
        yaxis_title='Stock Price',
        autosize=True,
        width=1500,
        height=1000,
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        paper_bgcolor="LightSteelBlue",
    )
    return fig
if __name__ == '__main__':
    app.run_server(debug=True)
