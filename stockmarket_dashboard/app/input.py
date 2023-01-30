import pandas as pd
import yfinance
import requests
import io
import re
import os
import unicodedata

from datetime import datetime as dt
from bs4 import BeautifulSoup

if os.path.isfile("data/codes.csv"):
    df = pd.read_csv("data/codes.csv")
    df = df.sort_values("銘柄名")
    drop_down_options = [
        {"label":unicodedata.normalize("NFKC", row["銘柄名"]), "value":row["コード"]}
        for _, row in df.iterrows()
    ]
else:
    drop_down_options = [{"label":"", "value":""}]


def download_stock_codes():
    # 日本取引所より日本株
    response = requests.get(
        "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"
    )
    # 一度保存して
    with open("data/jpx.xlsx", "wb") as fp:
        fp.write(response.content)
    jpx = pd.read_excel("data/jpx.xlsx")
    jpx["コード"] = jpx["コード"].apply(lambda x: str(x)+".T")
    jpx.to_csv(
        "data/codes.csv",
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
        "data/codes.csv",
        columns=["コード", "銘柄名"],
        index=False, mode="a+"
    )