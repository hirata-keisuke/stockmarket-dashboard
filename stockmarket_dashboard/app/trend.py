from sklearn.linear_model import LinearRegression

trend_calculators = {} # トレンド分析を計算する関数を格納する辞書

def trend_calculator(name):
    """トレンド分析を計算する関数を登録する

    デコレータとして使い、nameがキーで関数がバリューの辞書を作る

    Args:
        name (str): トレンド分析の名前

    Returns:
        function: 
    
    """

    def _trend_calculator(calc_fn):
        trend_calculators[name] = calc_fn
        return calc_fn
    
    return _trend_calculator

def select_calculator(name):
    """トレンド分析の手法を選択する

    Args:
        name (str): 手法の名前

    Returns:
        function: トレンド分析を計算する関数
    
    """
    return trend_calculators[name]

@trend_calculator("simple")
def calc_SMA(df, num):
    """単純移動平均線(Simple Moving Average)を計算する

    Args:
        df (pandas.DataFrame): 株価情報（日付、始値、終値、高値、安値、出来高）
        num (int): 移動平均を取る期間
    
    Returns:
        list: dfが持つ日付期間で単純移動平均を計算した値を格納したリスト
    
    """
    averages = []
    for i in range(len(df)):
        if i >= num-1:
            averages.append(df.loc[i-num+1:i,"終値"].sum()/num)
        else:
            averages.append(None)
    return averages

@trend_calculator("exponential")
def calc_EMA(df, num):
    """指数平滑移動平均線(Exponential Moving Average)を計算する

    Args:
        df (pandas.DataFrame): 株価情報（日付、始値、終値、高値、安値、出来高）
        num (int): 移動平均を取る期間
    
    Returns:
        list: dfが持つ日付期間で指数平滑移動平均を計算した値を格納したリスト
    
    """
    averages = []
    for i in range(len(df)):
        if i == num-1:
            averages.append(df.loc[i-num+1:i,"終値"].sum()/num)
        elif i > num-1:
            ema = averages[i-1]+2/(num+1)*(df.loc[i,"終値"]-averages[i-1])
            averages.append(ema)
        else:
            averages.append(None)

    return averages

@trend_calculator("regression")
def calc_LRI(df, num):
    """線形回帰値線(Linear Regression Indicator)を計算する

    その日からnum-1日前のデータで線形回帰を行い、その日の値を推論した値

    Args:
        df (pandas.DataFrame): 株価情報（日付、始値、終値、高値、安値、出来高）
        num (int): 線形回帰のデータを取る期間
    
    Returns:
        list: dfが持つ日付期間で線形回帰値を計算した値を格納したリスト
    
    """
    averages = []
    for i in range(len(df)):
        if i >= num-1:
            model = LinearRegression()
            X = [[j] for j in range(num)]
            y = df.loc[i-num+1:i,"終値"].to_list()
            model.fit(X,y)
            averages.append(model.predict([X[-1]])[0])
        else:
            averages.append(None)

    return averages
