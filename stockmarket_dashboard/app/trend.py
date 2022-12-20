from sklearn.linear_model import LinearRegression

def calc_SMA(df, num):
    averages = []
    for i in range(len(df)):
        if i >= num-1:
            averages.append(df.loc[i-num+1:i,"終値"].sum()/num)
        else:
            averages.append(None)
    return averages

def calc_EMA(df, num):

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

def calc_LRI(df, num):

    averages = []
    for i in range(len(df)):
        if i >= num-1:
            model = LinearRegression()
            X = [[i] for i in range(num)]
            y = df.loc[i-num+1:i,"終値"].to_list()
            model.fit(X,y)
            averages.append(model.predict([X[-1]])[0])
        else:
            averages.append(None)

    return averages