import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State

from callback.filter import filter_stocks, get_all_codes
from callback.query import query_stock
from callback.visualize import drow_technicals

app = Dash(__name__)
app.title = "株価テクニカル分析ダッシュボード"

app.layout = html.Div([
    html.Div([
        html.P(children="銘柄名", id="stock-name", className="header-item"),
        html.P(children="株価", id="stock-price", className="header-item" ),
        html.P(children="出来高", id="stock-volume", className="header-item")
    ], className="header"),
    dcc.ConfirmDialog(id="confirm-notfilled", message="未入力項目があります。"),
    html.Div([
        html.Div([
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
                    dcc.Input(placeholder="出来高上限値", type="number", id="stock-volume-upper-input")
                ]),
                html.Div([
                    html.Button("フィルタ", id="filter-button", className="submit-button", n_clicks=0),
                ], style={"text-align":"center"})
            ], className="filter-area"),
        html.Div([
            html.H5("取得期間"),
            dcc.DatePickerRange(display_format="Y/M/D", id="period-visualize", style={"margin-bottom":"5px"}),
            dcc.Dropdown(options=[], id="stock-code-dropdown", placeholder="証券コード", className="stock-code-dropdown"),
            html.Div([html.Div([
                html.H5("移動平均線"),
                html.Div(["短期:",dcc.Input(id="sma-short", value=5, type="number", style={"width":"40px"}, debounce=True)],style={"text-align":"center"}),
                html.Div(["中期:",dcc.Input(id="sma-medium", value=20, type="number", style={"width":"40px"}, debounce=True)],style={"text-align":"center"}),
                html.Div(["長期:",dcc.Input(id="sma-long", value=60, type="number", style={"width":"40px"}, debounce=True)],style={"text-align":"center"})
            ], style={"margin":"3px"}),html.Div([
                html.H5("ボリンジャーバンド"),
                html.Div(["σの範囲:",dcc.Input(id="bollinger-range", value=20, type="number", style={"width":"30px"}, debounce=True)],style={"text-align":"center"}),
                html.H5("DMI"),
                html.Div(["範囲:",dcc.Input(id="dmi-range", value=10, type="number", style={"width":"30px"}, debounce=True)], style={"text-align":"center"}),
            ], style={"margin":"3px"}),html.Div([
                html.Button("グラフ化", id="visualize-button", className="submit-button")
            ])], className="technicals-settings")
        ], className="visualize-area")
    ], className="setting-area"),
    html.Div([
        dcc.Graph(id="technicals"),
    ], className="technicals-graphs")
])

@app.callback(
    output=[Output("stock-code-dropdown", "options"), Output("confirm-notfilled", "displayed")],
    inputs=[Input("filter-button", "n_clicks")],
    state=[
        State("stock-price-lower-input", "value"), State("stock-price-upper-input", "value"),
        State("stock-volume-lower-input", "value"), State("stock-volume-upper-input", "value")
    ]
)
def filter_codes(n_clicks, lower_price, upper_price, lower_volume, upper_volume):

    if n_clicks == 0:
        return get_all_codes(), False
    start_date = 0
    end_date = 0
    # 値が入っていない箇所があれば戻す
    #if start_date is None or end_date is None or upper_price is None or upper_volume is None:
    #    return get_all_codes(), True
    lower_price = 0 if lower_price is None else lower_price
    lower_volume = 0 if lower_volume is None else lower_volume
    
    return filter_stocks(start_date, end_date, lower_price, upper_price, lower_volume, upper_volume), False


@app.callback(
    output=[
        Output("stock-name", "children"), Output("stock-price", "children"), 
        Output("stock-volume", "children"), Output("technicals", "figure")
    ],
    inputs=[
        Input("visualize-button", "n_clicks"),
        Input("sma-short", "value"), Input("sma-medium", "value"), Input("sma-long", "value"),
        Input("bollinger-range", "value"), Input("dmi-range", "value")
    ],
    state=[
        State("period-visualize", "start_date"), State("period-visualize", "end_date"),
        State("stock-code-dropdown", "value")
    ]
)
def visualize_technicals(
    n_clicks, sma_short, sma_medium, sma_long, n_sigma, n_dmi, start_date, end_date, code
):
    """選択された証券コード・期間でテクニカルを表示する
    """

    if start_date is None or end_date is None or code is None:
        return "銘柄名", "株価", "出来高", go.Figure()

    st = query_stock(code, start_date, end_date)

    if st is None:
        return "銘柄名", "株価", "出来高", go.Figure()

    included_dates = {d.strftime("%Y-%m-%d") for d in st.index}
    all_dates = {d.strftime("%Y-%m-%d") for d in pd.date_range(start=st.index[0], end=st.index[-1])}
    excluded_dates = all_dates - included_dates
    visualized_technicals = drow_technicals(
        st, excluded_dates, sma_short, sma_medium, sma_long, n_sigma, n_dmi
    )

    _recent = st.loc[st.index[-1]]
    unit = "￥" if code.endswith(".T") else "$"
    return st.name, unit+f'{_recent["Close"]:.1f}', f'{_recent["Volume"]:.0f}株', visualized_technicals

if __name__ == "__main__":
    app.run_server(debug=True)