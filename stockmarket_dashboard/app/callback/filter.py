import sqlite3

def filter_stocks(start_date, end_date, price_upper, price_lower, volume_upper, volume_lower):
    """株価や出来高が指定範囲内かを調べる

    条件に合ったコードだけをドロップダウン用のリストに残す

    args:
        start_date (str):株価を取る範囲（始）
        end_date (str):株価を取る範囲（終）
        price_upper (float):株価の上限
        price_lower (float):株価の下限
        volume_upper (float):出来高の上限
        volume_lower (float):出来高の下限
    
    returns:
        list:条件に合う銘柄の{label:銘柄名,value:証券コード}のリスト
    """
    conn = sqlite3.connect("stocks.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()

    cur.execute("SELECT * FROM code_master")
    codes, names = [], []
    dropdown_list = []
    for row in cur.fetchall():
        codes.append(row[0])
        names.append(row[1])

    # 各コードを指定された期間で取得する
    for code, name in zip(codes, names):
        cur.execute(f"""SELECT code FROM stock_data 
        WHERE date >= '{start_date}' AND date <= '{end_date}' 
        group by code having avg(volume) >= {volume_lower} AND avg(volume) <= {volume_upper} 
        AND avg(close_price) >= {price_lower} AND avg(close_price) <= {price_upper}""")

        if len(cur.fetchall()) != 0:
            dropdown_list.append(
                {"label":name, "value":code}
            )
    
    return dropdown_list

def get_all_codes():
    conn = sqlite3.connect("stocks.db", detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    cur = conn.cursor()

    cur.execute("SELECT * FROM code_master")
    dropdown_list = []
    for row in cur.fetchall():
        dropdown_list.append(
            {"label":row[1], "value":row[0]}
        )
    return dropdown_list