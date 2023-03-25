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

    try:
        save_path = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir, "data")
        filename = start.replace("-", "")+"_"+end.replace("-", "")+"_"+code+".csv"
        save_filepath = os.path.join(save_path, filename)
        if os.path.isfile(save_filepath):
            st = pd.read_csv(save_filepath, index_col=0)
            st.index = pd.to_datetime(st.index)
        else:
            st = yfinance.download(code, start=start, end=end)
            st.index = st.index.tz_convert("Asia/Tokyo")
            st.to_csv(save_filepath, encoding="utf-8")
        with open(os.path.join(save_path, "codes.csv"), "r") as f:
            for line in f.readlines():
                line = line.split(",")
                if line[0] == code:
                    st.code = line[0]
                    st.name = line[1]
                    break
        return st
    except:
        return None

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