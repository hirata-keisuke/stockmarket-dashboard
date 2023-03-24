import pandas as pd
import numpy as np

def calc_sma(st, n):
    """単純移動平均線を計算する
    
    Args:
        st (pandas.DataFrame):株式情報
        n (int):平均を取る期間
    
    Returns:
        ndarray:単純移動平均値
    
    """

    return st["Close"].rolling(window=n).mean()

def calc_sigma(st, n):
    """n日間の株価の標準偏差を計算する
    
    Args:
        st (pandas.DataFrame):株式情報
        n (int):標準偏差を計算する期間
        
    Returns:
        ndarray:株価の標準偏差
        
    """

    return st["Close"].rolling(window=n).std().to_numpy()

def calc_dmi(st, n):
    """DMIを計算する
    
    Args:
        st (pandas.DataFrame):株式情報
        n (int):DMIを計算する期間

    Returns:
        ndarray:+DIの配列
        ndarray:-DIの配列
        ndarray:ADXの配列
    """

    # DMIを計算するために必要なデータを準備する
    _high = st["High"]
    _low = st["Low"]
    _close = st["Close"]

    # True Range（TR）を計算する
    _tr1 = _high - _low # 当日高値-当日安値
    _tr2 = abs(_high - _close.shift()) # 当日高値-前日終値
    _tr3 = abs(_low - _close.shift()) # 当日安値-前日終値
    _tr = pd.concat([_tr1, _tr2, _tr3], axis=1).max(axis=1)

    # Directional Movement（DM）を計算する
    _up_move = _high - _high.shift()
    _down_move = _low.shift() - _low
    _plus_dm = pd.Series(0, index=st.index)
    _minus_dm = pd.Series(0, index=st.index)

    # 上昇する力があり下降する力より強い日は上昇する力を採用する
    _plus_dm[(_up_move > _down_move) & (_up_move > 0)] = _up_move[(_up_move > _down_move) & (_up_move > 0)]
    # 下降する力があり上昇する力より強い日は下降する力を採用する
    _minus_dm[(_down_move > _up_move) & (_down_move > 0)] = _down_move[(_down_move > _up_move) & (_down_move > 0)]

    # Plus Directional Indicator（+DI）とMinus Directional Indicator（-DI）を計算する
    _plus_di = 100 * _plus_dm.rolling(window=n).sum() / _tr.rolling(window=n).sum()
    _minus_di = 100 * _minus_dm.rolling(window=n).sum() / _tr.rolling(window=n).sum()
    
    # Directional Index（DX）とAverage Directional Index（ADX）を計算する
    _dx = 100 * (abs(_plus_di - _minus_di) / (_plus_di + _minus_di))
    _adx = _dx.rolling(window=n).mean()

    return _plus_di, _minus_di, _adx