import sqlite3
import pandas as pd

def query_stock(stock_code, start_period, end_period):
    """指定期間の株式情報をDBから取り出す

    Args:
        stock_code (str):証券コード
        start_period (date):YYYY-MM-DD形式の検索開始日
        end_date (date):YYYY-MM-DD形式の検索最終日

    Returns:
        pandas.DataFrame:インデックスが日付、列が始値・高値・安値・終値・出来高
    """

    conn = sqlite3.connect("stocks.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM code_master WHERE code = '{stock_code}'")
    name = cur.fetchone()[0]
    cur.execute(f"SELECT * FROM stock_data WHERE code = '{stock_code}' AND date>='{start_period}' AND date<='{end_period}'")

    indices, open_prices, close_prices, high_prices, low_prices, volumes = [], [], [], [], [], []
    for row in cur.fetchall():
        indices.append(row[1])
        open_prices.append(row[2])
        high_prices.append(row[3])
        low_prices.append(row[4])
        close_prices.append(row[5])
        volumes.append(row[6])
    st = pd.DataFrame(
        data={"Open":open_prices, "High":high_prices, "Low":low_prices, "Close":close_prices, "Volume":volumes},
        index=indices
    )
    st.name = name
    return None if len(st)==0 else st