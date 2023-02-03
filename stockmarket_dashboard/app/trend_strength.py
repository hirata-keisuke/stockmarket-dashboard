import math
import pandas as pd
from trend_direction import calc_SMA
import plotly.graph_objects as go

strength_calculators = {} # トレンド強度を計算する関数を格納する辞書

def strength_calculator(name):
    """トレンド強度を計算する関数を登録する

    デコレータとして使い、nameがキーで関数がバリューの辞書を作る

    Args:
        name (str): トレンド強度分析の名前

    Returns:
        function: 
    
    """

    def _strength_calculator(calc_fn):
        strength_calculators[name] = calc_fn
        return calc_fn
    
    return _strength_calculator

def select_calculator(name):
    """トレンド強度分析の手法を選択する

    Args:
        name (str): 手法の名前

    Returns:
        function: トレンド強度分析を計算する関数
    
    """
    return strength_calculators[name]

@strength_calculator("RWI")
def random_walk_index(df, num):
    """ランダムウォーク指数を計算する

    Args:
        df (pandas.DataFrame): 株価情報（日付、始値、終値、高値、安値、出来高）
        num (int): 日中差の平均を取る期間

    Returns:
        list: dfが持つ日付期間でランダムウォーク指数を計算した値を格納したリスト
    """

    RWIH = []
    RWIL = []
    df["日中差"] = df["高値"] - df["安値"]
    for i in range(len(df)):
        if i >= num-1:
            avg = df.loc[i-(num-1):i,"日中差"].sum()*math.sqrt(num)
            RWIH.append((df.loc[i,"高値"]-df.loc[i-(num-1):i,"安値"].min())/avg)
            RWIL.append((df.loc[i-(num-1):i,"高値"].max()-df.loc[i,"安値"])/avg)
        else:
            RWIH.append(None)
            RWIL.append(None)
    return RWIH, RWIL

@strength_calculator("TII")
def trend_intensity_index(df, num, m):
    """トレンドインテンシティ指数を計算する

    Args:
        df (pandas.DataFrame): 株価情報（日付、始値、終値、高値、安値、出来高）
        num (int): TIIを計算する際に遡る日数
        m (int): 移動平均を取る期間

    Returns:
        list: dfが持つ日付期間でトレンドインテンシティ指数を計算した値を格納したリスト
    """

    TTI = []
    df["SMA"] = calc_SMA(df, m)
    df = df.fillna(0)
    df["D"] = df["終値"] - df["SMA"]
    for i in range(len(df)):
        if i >= num-1:
            _df = df.loc[i-(num-1):i]
            SDp = _df[_df["D"]>0]["D"].sum()
            SDm = -1 * _df[_df["D"]<0]["D"].sum()
            TTI.append(SDp/(SDp+SDm))
        else:
            TTI.append(None)
    return TTI

@strength_calculator("PTI")
def price_trend_index(df, num):
    """価格トレンド指数を計算する

    Args:
        df (pandas.DataFrame): 株価情報（日付、始値、終値、高値、安値、出来高）
        num (int): 相関係数を計算する期間の日数

    Returns:
        list: dfが持つ日付期間で価格トレンド指数を計算した値を格納したリスト
    """

    PTI = []
    for i in range(len(df)):
        if i >= num-1:
            _df = df.loc[i-(num-1):i,"終値"]
            PTI.append(_df.corr(_df.index.to_series()))
        else:
            PTI.append(None)
    return PTI

def trend_strength(df, fig):
    """トレンドの方向を示すグラフとロウソク足を描画する
    
    """

    for rwi, name, color in zip(
        select_calculator("RWI")(df, 15),
        ["RWI-H", "RWI-L"],
        ["lightblue", "lightyellow"]
    ):
        fig.add_trace(go.Scatter(
                x=df["Date"], y=rwi,
                name=name, marker={"color":color}
        ))

    fig.add_trace(go.Scatter(
            x=df["Date"], y=select_calculator("TII")(df, 10, 15),
            name="TII(10,15)", marker={"color":"lightgray"}
    ))

    fig.add_trace(go.Scatter(
            x=df["Date"], y=select_calculator("PTI")(df, 10),
            name="PTI(20)", marker={"color":"lightpink"}
    ))

    def button_params(name):
        visible = []
        for data in fig["data"]:
            if name in data["name"] or name=="全て":
                visible.append(True)
            else:
                visible.append(False)

        return {
            "label":name,
            "method":"update",
            "args":[{
                'visible': visible,
                'title': name,
                'showlegend': True
            }]
        }

    fig.update_layout(
        updatemenus=[go.layout.Updatemenu(
            active=0,
            buttons=[
                button_params("全て"),
                button_params("RWI"),
                button_params("TII"),
                button_params("PTI")
            ]
        )]
    )
    return fig