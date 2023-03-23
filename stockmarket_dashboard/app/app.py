from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go

app = Dash(__name__)
app.title = "株価テクニカル分析ダッシュボード"

app.layout = html.Div([
    html.Div([
        html.P("AAAAAAAAAAA", id="stock-name", className="header-item"),
        html.P(120, id="stock-price", className="header-item" ),
        html.P("CCC", id="stock-volume", className="header-item"),
    ], className="header"),
    html.Div([
        html.H5("取得期間"),
        dcc.DatePickerRange(display_format="Y/M/D", id="period"),
        html.H5("株価範囲"),
        html.Div([
            dcc.Input(placeholder="株価下限値", type="number", min=0),
            " ~ ",
            dcc.Input(placeholder="株価上限値", type="number")
        ]),
        html.H5("出来高範囲"),
        html.Div([
            dcc.Input(placeholder="出来高下限値", type="number", min=0),
            " ~ ",
            dcc.Input(placeholder="出来高上限値", type="number")
        ]),
        html.H5("証券コード"),
        dcc.Input(placeholder="任意", style={"width":"100px"}),
        html.Div([
            html.Button("クエリを送信", id="query-submit", className="button-query-submit")
        ], style={"text-align":"center"})
    ], className="search-area"),
    html.Div([
        html.Div([
            html.H5("移動平均線"),
            dcc.Graph(id="candle-sma"),
            html.Div(["短期:",dcc.Input(id="sma-short", value=5, style={"width":"40px"})]),
            html.Div(["中期:",dcc.Input(id="sma-midium", value=20, style={"width":"40px"})]),
            html.Div(["長期:",dcc.Input(id="sma-long", value=60, style={"width":"40px"})]),
        ], style={"width":"33%"}),html.Div([
            html.H5("ボリンジャーバンド"),
            dcc.Graph(id="candle-bollinger"),
            html.Div(["標準偏差の計算範囲:",dcc.Input(id="bollinger-range", value=20, style={"width":"20px"})])
        ], style={"width":"33%"}),
        html.Div([
            html.H5("DMI"),
            dcc.Graph(id="candle-dmi"),
            html.Div(["DMIの計算範囲:",dcc.Input(id="dmi-range", value=10, style={"width":"20px"})])
        ], style={"width":"33%"}),
    ], className="technicals")
])

app.run_server(debug=True)