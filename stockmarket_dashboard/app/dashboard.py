from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
import base64
import io
from sma import calc_SMA

app = Dash(__name__)

app.layout = html.Div([
    html.H4('ロウソク足'),
    html.H6("株価情報CSVファイル: "),
    dcc.Upload(
        id='upload-data', 
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select File', style={"font-weight":"bold"})
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        }
    ),
    dcc.Graph(id="graph"),
])

@app.callback(
    Output("graph", "figure"), 
    Input("upload-data", "contents"),
)
def display_candlestick(contents):
    fig = None
    if contents is not None:
        _, content_string = contents.split(',')

        decoded = base64.b64decode(content_string)
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')),
            parse_dates=True, usecols=[0,1,2,3,4,6]
        )
        candlestick = go.Figure(go.Candlestick(
            x=df['Date'],
            open=df['始値'],
            high=df['高値'],
            low=df['安値'],
            close=df['終値'],
            name="ローソク足"
        ))
        fig = go.Figure(candlestick)

        for value in [5, 20, 60]:
            df["calc_sma"] = calc_SMA(df, value)
            line = go.Scatter(
                x=df["Date"], y=df["calc_sma"],
                name=f"{value}日移動平均線",
                mode="lines",
                marker=dict(color="#a0a0a0")
            )
            fig.add_traces(line)

    return fig

app.run_server(debug=True)