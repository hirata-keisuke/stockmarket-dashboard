import plotly.graph_objects as go
from plotly.subplots import make_subplots

from callback.technicals import calc_sma, calc_sigma, calc_dmi

def drow_candle_sma(st, excluded_dates, n_short, n_medium, n_long):
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
    candle_sma = make_subplots(
        rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_width=[0.2, 0.7]
    )
    candle_sma.add_trace(
        go.Candlestick(
            x=st.index, open=st["Open"], high=st["High"], low=st["Low"], 
            close=st["Close"], showlegend=False
        ), row=1, col=1
    )
    candle_sma.add_trace(
        go.Scatter(x=st.index, y=calc_sma(st, n_short), name=f"SMA{n_short}", mode="lines", showlegend=False),
        row=1, col=1
    )
    candle_sma.add_trace(
        go.Scatter(x=st.index, y=calc_sma(st, n_medium), name=f"SMA{n_medium}", mode="lines", showlegend=False),
        row=1, col=1
    )
    candle_sma.add_trace(
        go.Scatter(x=st.index, y=calc_sma(st, n_long), name=f"SMA{n_long}", mode="lines", showlegend=False),
        row=1, col=1
    )
    candle_sma.add_trace(
        go.Bar(x=st.index, y=st["Volume"], showlegend=False),
    row=2, col=1
    )
    candle_sma.update(layout_xaxis_rangeslider_visible=False)
    candle_sma.update_layout(margin=dict(l=5, r=5, t=10, b=10))
    candle_sma.update_xaxes(rangebreaks=[dict(values=excluded_dates)], tickformat="%Y/%m/%d")
    candle_sma.update_yaxes(separatethousands=True)

    return candle_sma

def draw_candle_bollinger(st, excluded_dates, n_sigma):
    """ローソク足とボリンジャーバンドを描画する
    Args:
        st (pandas.DataFrame):株式情報
        excluded_dates (list of str):市場が休みのため、グラフの表示から省略すべき日付のリスト
        n_sigma (int):株価の標準偏差を計算する期間
    
    Returns:
        Figureオブジェクト:plotlyで生成された、ローソク足とボリンジャーバンドのオブジェクト
    """
    candle_bollinger = go.Figure(go.Candlestick(
        x=st.index, open=st["Open"], high=st["High"], low=st["Low"], 
        close=st["Close"], showlegend=False
    ))
    sigma = calc_sigma(st, n_sigma)
    sma = calc_sma(st, n_sigma)
    candle_bollinger.add_trace(
        go.Scatter(x=st.index, y=sma, name=f"SMA{n_sigma}", mode="lines", showlegend=False)
    )
    candle_bollinger.add_trace(
        go.Scatter(x=st.index, y=sma+sigma, name="+1σ", line={"dash":"dot"}, showlegend=False)
    )
    candle_bollinger.add_trace(
        go.Scatter(x=st.index, y=sma-sigma, name="-1σ", line={"dash":"dot"}, showlegend=False)
    )
    candle_bollinger.add_trace(
        go.Scatter(x=st.index, y=sma+2*sigma, name="+2σ", line={"dash":"dot"}, showlegend=False)
    )
    candle_bollinger.add_trace(
        go.Scatter(x=st.index, y=sma-2*sigma, name="-2σ", line={"dash":"dot"}, showlegend=False)
    )

    candle_bollinger.update(layout_xaxis_rangeslider_visible=False)
    candle_bollinger.update_layout(margin=dict(l=5, r=5, t=10, b=10))
    candle_bollinger.update_xaxes(rangebreaks=[dict(values=excluded_dates)], tickformat="%Y/%m/%d")
    candle_bollinger.update_yaxes(separatethousands=True)

    return candle_bollinger

def draw_candle_dmi(st, excluded_dates, n_dmi):
    """ローソク足とボリンジャーバンドを描画する
    Args:
        st (pandas.DataFrame):株式情報
        excluded_dates (list of str):市場が休みのため、グラフの表示から省略すべき日付のリスト
        n_dmi (int):DMIを計算する期間
    
    Returns:
        Figureオブジェクト:plotlyで生成された、ローソク足とDMIのオブジェクト
    """
    candle_dmi = go.Figure(go.Candlestick(
        x=st.index, open=st["Open"], high=st["High"], low=st["Low"], 
        close=st["Close"], showlegend=False
    ))

    plus_di, minus_di, adx = calc_dmi(st, n_dmi)
    candle_dmi.add_trace(
        go.Scatter(x=st.index, y=plus_di, name="+DI", mode="lines", showlegend=False)
    )
    candle_dmi.add_trace(
        go.Scatter(x=st.index, y=minus_di, name="-DI", mode="lines", showlegend=False)
    )
    candle_dmi.add_trace(
        go.Scatter(x=st.index, y=adx, name="ADX", mode="lines", showlegend=False)
    )
    candle_dmi.update(layout_xaxis_rangeslider_visible=False)
    candle_dmi.update_layout(margin=dict(l=5, r=5, t=10, b=10))
    candle_dmi.update_xaxes(rangebreaks=[dict(values=excluded_dates)], tickformat="%Y/%m/%d")
    candle_dmi.update_yaxes(separatethousands=True)

    return candle_dmi