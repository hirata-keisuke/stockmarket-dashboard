def short_SMA(df, num):
    averages = []
    for i in range(len(df)):
        if i >= 4:
            averages.append(df.loc[i-4:i,"終値"].sum()/5)
        else:
            averages.append(None)
    return averages

def middle_SMA(df):
    averages = []
    for i in range(len(df)):
        if i >= 19:
            averages.append(df.loc[i-19:i,"終値"].sum()/20)
        else:
            averages.append(None)
    return averages

def long_SMA(df):
    averages = []
    for i in range(len(df)):
        if i >= 59:
            averages.append(df.loc[i-19:i,"終値"].sum()/60)
        else:
            averages.append(None)
    return averages

def calc_SMA(df, num):
    averages = []
    for i in range(len(df)):
        if i >= num-1:
            averages.append(df.loc[i-num-1:i,"終値"].sum()/num)
        else:
            averages.append(None)
    return averages
