import pandas as pd
import requests
import io
import re
import os
from bs4 import BeautifulSoup

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


def _prepare_codes():
    """日本株と米国株のコードをCSVファイルに用意する
    """
    code_path = os.path.isfile(os.path.join(__file__), os.pardir, "data", "codes.csv")
    if code_path:
        os.remove(code_path)

    # 日本取引所より日本株
    response = requests.get(
        "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    )
    # 一度保存して
    with open("_jpx.xlsx", "wb") as fp:
        fp.write(response.content)
    jpx = pd.read_excel("data/jpx.xlsx")
    jpx["コード"] = jpx["コード"].apply(lambda x: str(x)+".T")
    os.remove("_jpx.xlsx")
    jpx.to_csv(
        code_path,
        columns=["コード", "銘柄名"],
        index=False, mode="w"
    )

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
        code_path,
        columns=["コード", "銘柄名"],
        index=False, mode="a+"
    )