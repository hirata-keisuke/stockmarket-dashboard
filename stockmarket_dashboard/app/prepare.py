import os
import requests
import io
import re
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

def prepare_codes():
    """日本株と米国株のコードをCSVファイルに用意する
    """
    # DBへ接続
    conn = sqlite3.connect("stocks.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    # カーソルを作成
    cur = conn.cursor()
    cur.execute("DELETE FROM code_master")

    _code_path = os.path.join(os.path.dirname(__file__), os.pardir, "data", "codes.csv")
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
    for _, row in jpx.iterrows():
        cur.execute("INSERT INTO code_master VALUES (?, ?)", (row["コード"], row["銘柄名"]))
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
    for _, row in sbi.iterrows():
        cur.execute("INSERT INTO code_master VALUES (?, ?)", (row["コード"], row["銘柄名"]))
    
    conn.commit()
    conn.close()

def prepare_db():
    """DBテーブルを用意する
    """
    # DBへ接続
    conn = sqlite3.connect("stocks.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    # カーソルを作成
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS code_master
               (code text PRIMARY KEY, name text)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS stock_data
               (code text, date date, open_price real, high_price real, low_price real, close_price real, volume integer,
                PRIMARY KEY (code, date),
                FOREIGN KEY (code) REFERENCES code_master(code))""")
    conn.commit()
    conn.close()

if __name__ == "__main__":

    prepare_db()
    prepare_codes()