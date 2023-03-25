import plotly.graph_objects as go
from plotly.subplots import make_subplots

from callback.technicals import calc_sma, calc_sigma, calc_dmi

def drow_technicals(st, excluded_dates, n_short, n_medium, n_long, n_sigma, n_dmi):
    """ローソク足と単純移動平均線を描画する

    Args:
        st (pandas.DataFrame):株式情報
        excluded_dates (list of str):市場が休みのため、グラフの表示から省略すべき日付のリスト
        n_short (int):日足の短期移動平均線
        n_medium (int):日足の中期移動平均線
        n_long (int):日足の長期移動平均線
    
    Returns:
        Figureオブジェクト:plotlyで生成された、ローソク足と単純移動平均線のオブジェクト
    """
    technicals = make_subplots(
        rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05,
        row_heights=[0.7, 0.5, 0.3, 0.3]
    )
    technicals.add_trace(
        go.Candlestick(
            x=st.index, open=st["Open"], high=st["High"], low=st["Low"], 
            close=st["Close"], showlegend=False
        ), row=1, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=calc_sma(st, n_short), name=f"SMA{n_short}", mode="lines", showlegend=False),
        row=1, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=calc_sma(st, n_medium), name=f"SMA{n_medium}", mode="lines", showlegend=False),
        row=1, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=calc_sma(st, n_long), name=f"SMA{n_long}", mode="lines", showlegend=False),
        row=1, col=1
    )

    technicals.add_trace(
        go.Scatter(x=st.index, y=st["Close"], showlegend=False, name="株価", mode="lines"),
        row=2, col=1
    )
    sigma = calc_sigma(st, n_sigma)
    sma = calc_sma(st, n_sigma)
    technicals.add_trace(
        go.Scatter(x=st.index, y=sma, name=f"SMA{n_sigma}", mode="lines", showlegend=False),
        row=2, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=sma+sigma, name="+1σ", line={"dash":"dot"}, showlegend=False),
        row=2, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=sma-sigma, name="-1σ", line={"dash":"dot"}, showlegend=False),
        row=2, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=sma+2*sigma, name="+2σ", line={"dash":"dot"}, showlegend=False),
        row=2, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=sma-2*sigma, name="-2σ", line={"dash":"dot"}, showlegend=False),
        row=2, col=1
    )

    plus_di, minus_di, adx = calc_dmi(st, n_dmi)
    technicals.add_trace(
        go.Scatter(x=st.index, y=plus_di, name="+DI", mode="lines", showlegend=False),
        row=3, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=minus_di, name="-DI", mode="lines", showlegend=False),
        row=3, col=1
    )
    technicals.add_trace(
        go.Scatter(x=st.index, y=adx, name="ADX", mode="lines", showlegend=False),
        row=3, col=1
    )

    technicals.add_trace(
        go.Bar(x=st.index, y=st["Volume"], showlegend=False, name="出来高"),
        row=4, col=1
    )

    technicals.update(layout_xaxis_rangeslider_visible=False)
    technicals.update_layout(margin=dict(l=0, r=0, t=10, b=0))
    technicals.update_xaxes(rangebreaks=[dict(values=list(excluded_dates))], tickformat="%Y/%m/%d")
    technicals.update_yaxes(separatethousands=True)

    return technicals