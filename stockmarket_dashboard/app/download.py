import yfinance

def download_stock(code, start, end):
    """株価と出来高をダウンロードする

    args:
        code (str):証券コード
        start (str):開始日付
        end (str):終了日付

    returns:
        pandas.DataFrame or None
    """

    st = None
    try:
        st = yfinance(code, start=start, end=end)
    except:
        st = None
    return st