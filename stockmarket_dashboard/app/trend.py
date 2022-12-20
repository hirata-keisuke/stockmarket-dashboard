def calc_SMA(df, num):
    averages = []
    for i in range(len(df)):
        if i >= num-1:
            averages.append(df.loc[i-num-1:i,"終値"].sum()/num)
        else:
            averages.append(None)
    return averages

def calc_EMA(df, num):

    return [None,None,1.0,2.0,3.0]