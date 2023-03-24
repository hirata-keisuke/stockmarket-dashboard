import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State

from callback.download import download_stock
from callback.visualize import drow_candle_sma, draw_candle_bollinger, draw_candle_dmi

def set_codes():
    """ドロップダウンにコードを表示する
    """
    codes = pd.read_csv("../data/codes.csv")
    return [
        {"label":code["銘柄名"], "value":code["コード"]} for _, code in codes.iterrows()
    ]

app = Dash(__name__)
app.title = "株価テクニカル分析ダッシュボード"

app.layout = html.Div([
    html.Div([
        html.P(children="銘柄名", id="stock-name", className="header-item"),
        html.P(children="株価", id="stock-price", className="header-item" ),
        html.P(children="出来高", id="stock-volume", className="header-item"),
    ], className="header"),
    html.Div([
        html.H5("取得期間"),
        dcc.DatePickerRange(display_format="Y/M/D", id="period"),
        html.H5("株価範囲"),
        html.Div([
            dcc.Input(placeholder="株価下限値", type="number", min=0, id="stock-price-lower-input"),
            " ~ ",
            dcc.Input(placeholder="株価上限値", type="number", id="stock-price-upper-input")
        ]),
        html.H5("出来高範囲"),
        html.Div([
            dcc.Input(placeholder="出来高下限値", type="number", min=0, id="stock-volume-lower-input"),
            " ~ ",
            dcc.Input(placeholder="出来高上限値", type="number", id="stock-volume-upper-inpur")
        ]),
        html.H5("証券コード"),
        dcc.Dropdown(options=set_codes(), id="stock-code-dropdown", className="stock-code-dropdown"),
        html.Div([
            html.Button("クエリを送信", id="query-submit-button", className="query-submit-button", n_clicks=0)
        ], style={"text-align":"center"})
    ], className="search-area"),
    html.Div([
        html.Div([
            html.H5("移動平均線"),
            dcc.Graph(id="candle-sma"),
            html.Div(["短期:",
                      dcc.Input(id="sma-short", value=5, type="number", style={"width":"40px"}, debounce=True)],
                      style={"text-align":"center"}),
            html.Div(["中期:",
                      dcc.Input(id="sma-medium", value=20, type="number", style={"width":"40px"}, debounce=True)],
                      style={"text-align":"center"}),
            html.Div(["長期:",
                      dcc.Input(id="sma-long", value=60, type="number", style={"width":"40px"}, debounce=True)],
                      style={"text-align":"center"}),
        ], style={"width":"33%"}),html.Div([
            html.H5("ボリンジャーバンド"),
            dcc.Graph(id="candle-bollinger"),
            html.Div(["標準偏差の計算範囲:",
                      dcc.Input(id="bollinger-range", value=20, type="number", style={"width":"30px"}, debounce=True)],
                      style={"text-align":"center"})
        ], style={"width":"33%"}),
        html.Div([
            html.H5("DMI"),
            dcc.Graph(id="candle-dmi"),
            html.Div(["DMIの計算範囲:",
                      dcc.Input(id="dmi-range", value=10, type="number", style={"width":"30px"}, debounce=True)],
                      style={"text-align":"center"}
                      )
        ], style={"width":"33%"}),
    ], className="technicals")
])

@app.callback(
    output=[
        Output("stock-name", "children"), Output("stock-price", "children"), 
        Output("stock-volume", "children"),
        Output("candle-sma", "figure"), Output("candle-bollinger", "figure"),
        Output("candle-dmi", "figure"),
    ],
    inputs=[
        Input("query-submit-button", "n_clicks"),
        Input("sma-short", "value"), Input("sma-medium", "value"), Input("sma-long", "value"),
        Input("bollinger-range", "value"), Input("dmi-range", "value")
    ],
    state=[
        State("period", "start_date"), State("period", "end_date"),
        State("stock-code-dropdown", "value")
    ]
)
def visualize_technicals(
    query_submit, sma_short, sma_medium, sma_long, n_sigma, n_dmi, start_date, end_date, code
):
    """選択された証券コード・期間でテクニカルを表示する
    """

    if start_date is None or end_date is None or code is None:
        return "銘柄名", "株価", "出来高", go.Figure(), go.Figure(), go.Figure()

    st = download_stock(code, start_date, end_date)

    if st is None:
        return None, None, None, go.Figure(), go.Figure(), go.Figure()

    excluded_dates = [
        d.strftime("%Y-%m-%d") 
        for d in pd.date_range(start=st.index[0], end=st.index[-1]) 
        if d not in st.index
    ]
    candle_sma = drow_candle_sma(st, excluded_dates, sma_short, sma_medium, sma_long)
    
    candle_bollinger = draw_candle_bollinger(st, excluded_dates, n_sigma)

    candle_dmi = draw_candle_dmi(st, excluded_dates, n_dmi)

    _recent = st.loc[st.index[-1]]
    return st.name, f'{_recent["Close"]:.1f}円', f'{_recent["Volume"]:.0f}株', candle_sma, candle_bollinger, candle_dmi

if __name__ == "__main__":
    app.run_server(debug=True)
