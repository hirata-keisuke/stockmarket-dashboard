from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
import base64
import io
from trend import select_calculator

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

@app.callback(Output('graph', 'figure'),
              Input('upload-data', 'contents')
)
def display_candlestick(content):

    fig = go.Figure()
    if content:
        _, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')),
            parse_dates=True, usecols=[0,1,2,3,4,6]
        )
        fig = go.Figure(go.Candlestick(
            x=df['Date'],
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
    for value, color in zip([5, 20, 60], ["lightgoldenrodyellow", "lightcoral", "lightskyblue"]):
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
    

app.run_server(debug=True)