from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import base64
import io
import yfinance
from datetime import date
from trend import select_calculator
from input import download_stock_codes, drop_down_options

app = Dash(__name__)

app.layout = html.Div([
    html.H4('ロウソク足'),
    html.Div(
        [
            html.Div(dcc.Dropdown(
                id='stock_name', options=drop_down_options,
                multi=False, placeholder='銘柄'
            ), style={"width": "50%", "margin-right": 10, "display": "inline-block"}),
            html.Div([
                dcc.Input(id="start-date", type="text", placeholder="yyyy/mm/dd"),
                "〜",
                dcc.Input(id="end-date", type="text", placeholder="yyyy/mm/dd")
            ], style={"width": "30%", "margin-right": 10, "display": "inline-block"}),
            html.Button('Go', id='submit-btn', n_clicks=0),
        ],
    ),
    dcc.Graph(id="graph"),
    html.Div([html.Button("銘柄一覧更新", id="btn_stock_code", n_clicks=0)]),
    html.P(id="hidden-div", style={"display":"none"}),
])

@app.callback(
    Output('graph', 'figure'),
    Input("submit-btn", "n_clicks"),
    State("stock_name", "value"),
    State("start-date", "value"), 
    State("end-date", "value")
)
def display_candlestick(n_clicks, code, start_date, end_date):

    fig = go.Figure()

    if n_clicks:
        start_date = start_date.split("/")
        start_date = date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
        end_date = end_date.split("/")
        end_date = date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
        df = yfinance.download(code, start_date, end_date)
        df.columns = ["始値", "高値", "安値", "終値", "調整後終値", "売買高"]
        df = df.reset_index()
        fig = go.Figure(go.Candlestick(
            x=df["Date"],
            open=df['始値'],
            high=df['高値'],
            low=df['安値'],
            close=df['終値'],
            name="ローソク足"
        ))
        fig.update_layout(xaxis_rangeslider_visible=False)

        fig = set_trend_method(df, fig)

    return fig


def set_trend_method(df, fig):
    for value, color in zip(
        [5, 20, 60], ["lightgoldenrodyellow", "lightcoral", "lightskyblue"]
    ):
        fig.add_trace(go.Scatter(
                x=df["Date"], y=select_calculator("simple")(df, value),
                name=f"{value}日単純移動平均線", marker={"color":color}
        ))

    fig.add_trace(go.Scatter(
            x=df["Date"], y=select_calculator("exponential")(df, 10),
            name="指数平滑移動平均線", marker={"color":"lightgray"}
    ))

    fig.add_trace(go.Scatter(
            x=df["Date"], y=select_calculator("regression")(df, 10),
            name="線形回帰値線", marker={"color":"lightpink"}
    ))

    def button_params(name):
        visible = [True]
        for data in fig["data"][1:]:
            if name in data["name"] or name=="全て":
                visible.append(True)
            else:
                visible.append(False)

        return {
            "label":name,
            "method":"update",
            "args":[{
                'visible': visible,
                'title': name,
                'showlegend': True
            }]
        }

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=[
                button_params("全て"),
                button_params("単純移動平均線"),
                button_params("指数平滑移動平均線"),
                button_params("線形回帰値線")
            ]
        )]
    )
    return fig

@app.callback(
    Output('hidden-div', 'children'),
    Input("btn_stock_code", "n_clicks")
)
def click_btn_stock_code(btn_stock_code):
    if btn_stock_code:
        download_stock_codes()
    return None
    

app.run_server(debug=True)