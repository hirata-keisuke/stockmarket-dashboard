def stock_filter(st, price_upper, price_lower, volume_upper, volume_lower):
    """株価や出来高が指定範囲内かを調べる

    args:
        st (pandas.DataFrame):株式情報
        price_upper (float):株価の上限
        price_lower (float):株価の下限
        volume_upper (float):出来高の上限
        volume_lower (float):出来高の下限
    
    returns:
        pandas.DataFrame or None
    """
    _mean = st.mean()
    if _mean["Close"] < price_lower or price_upper < _mean["Close"]:
        return None
    if _mean["Volume"] < volume_lower or volume_upper < _mean["Volume"]:
        return None
    return st