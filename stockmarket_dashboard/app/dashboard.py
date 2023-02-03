from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import os
import glob
import yfinance
from datetime import date
from trend_direction import trend_direction
from trend_strength import trend_strength
from input import download_stock_codes, drop_down_options

app = Dash(__name__)

app.layout = html.Div([
    html.H1("テクニカル分析ツール"),
    html.Div([
        html.H3("銘柄選択"),
        html.Div(dcc.Dropdown(
            id='stock_name', options=drop_down_options,
            multi=False, placeholder='銘柄'
        ), style={"width": "50%", "margin-right": 10}),
        html.H3("期間指定"),
        html.Div([
            dcc.Input(
                id="start-date", type="text", placeholder="yyyy/mm/dd",
                style={"font-size": "100%", "margin-right": "10px"}
            ),
            "〜",
            dcc.Input(
                id="end-date", type="text", placeholder="yyyy/mm/dd",
                style={"font-size": "100%", "margin": "10px"}
            ),
            html.Button('計算する', id='submit-btn', n_clicks=0, style={"font-size": "100%"})
        ], style={"display": "inline-block", }),
    ]),
    dcc.Tabs([
        dcc.Tab(label="トレンド方向", children=[
            dcc.Graph(id="trend-direction"),
        ]),
        dcc.Tab(label="トレンド強度", children=[
            dcc.Graph(id="trend-strength")
        ])
    ]),
    html.Div([html.Button("銘柄一覧更新", id="btn_stock_code", n_clicks=0)]),
    html.P(id="hidden-div", style={"display":"none"}),
])

@app.callback(
    Output("trend-direction", "figure"),
    Output("trend-strength", "figure"),
    Input("submit-btn", "n_clicks"),
    State("stock_name", "value"),
    State("start-date", "value"), 
    State("end-date", "value")
)
def technical_analysis(n_clicks, code, start_date, end_date):

    direction = go.Figure()
    strength = go.Figure()

    if n_clicks:
        start_date = start_date.split("/")
        start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date = end_date.split("/")
        end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        filepath = "downloaded"+code+start_date.strftime("%Y%m%d")+end_date.strftime("%Y%m%d")+".csv"

        if os.path.isfile(filepath):
            df = pd.read_csv(filepath, encoding="utf-8")
        else:
            for f in glob.glob("downloaded*.csv"):
                os.remove(f)
            df = yfinance.download(code, start_date, end_date)
            df.columns = ["始値", "高値", "安値", "終値", "調整後終値", "売買高"]
            df = df.reset_index()
            df.to_csv(filepath, index=False, encoding="utf-8")

        direction = go.Figure(go.Candlestick(
            x=df["Date"],
            open=df['始値'],
            high=df['高値'],
            low=df['安値'],
            close=df['終値'],
            name="ローソク足"
        ))
        direction.update_layout(xaxis_rangeslider_visible=False)
        direction = trend_direction(df, direction)

        strength = trend_strength(df, strength)

    return direction, strength

@app.callback(
    Output('hidden-div', 'children'),
    Input("btn_stock_code", "n_clicks")
)
def click_btn_stock_code(btn_stock_code):
    if btn_stock_code:
        download_stock_codes()
    return None
    

app.run_server(debug=True)