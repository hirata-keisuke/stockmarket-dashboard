def query_stocks(start_period, end_period, prices, volumes):
    """株式情報をダウンロードしてフィルタにかける

    Args:
        start_period (str):YYYY-MM-DD形式の検索開始日
        end_date (str):YYYY-MM-DD形式の検索最終日
        price_lower (float):検索の株価下限値
        price_upper (float):検索の株価上限値
        volume_lower (float):検索の出来高下限値
        volume_upper (float):検索の出来高上限値
    """