import requests
import io
import re
import os
import yfinance
import pandas as pd
from bs4 import BeautifulSoup

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
        st.code = code
    except:
        st = None
    return st

def save_stock(st):
    """株式情報を保存する

    args:
        st (pandas.DataFrame):株式情報
    """
    _save_path = os.path.join(os.path.dirname(__file__), os.pardir, "data")
    _start = st.index[0].strftime("%Y%m%d")
    _end = st.index[-1].strftime("%Y%m%d")
    st.to_csv(
        os.path.join(_save_path, _start+"_"+_end+"_"+st.code+".csv"),
        encoding="utf8"
    )

def _prepare_codes():
    """日本株と米国株のコードをCSVファイルに用意する
    """
    _code_path = os.path.join(os.path.dirname(__file__), os.pardir, "data", "codes.csv")
    print(_code_path)
    if os.path.isfile(_code_path):
        os.remove(_code_path)

    # 日本取引所より日本株
    response = requests.get(
        "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    )
    # 一度保存して
    with open("_jpx.xlsx", "wb") as fp:
        fp.write(response.content)
    jpx = pd.read_excel("_jpx.xlsx")
    jpx["コード"] = jpx["コード"].apply(lambda x: str(x)+".T")
    jpx.to_csv(
        _code_path,
        columns=["コード", "銘柄名"],
        index=False, mode="w"
    )
    os.remove("_jpx.xlsx")

    # SBI証券より米国株
    response = requests.get(
        "https://search.sbisec.co.jp/v2/popwin/info/stock/pop6040_usequity_list.html",
    )
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, "html.parser")
    tbl = soup.find_all('table')
    with io.StringIO(re.sub(r"<br/>.+?(?=</td>)", "", str(tbl[4]))) as fp:
        sbi = pd.read_html(fp)[0]
        sbi.columns = ["コード", "銘柄名", "事業内容", "市場"]
    sbi.to_csv(
        _code_path,
        columns=["コード", "銘柄名"],
        index=False, mode="a+"
    )