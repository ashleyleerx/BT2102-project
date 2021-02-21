import pandas as pd

def stats_columns(filename, xlabel, ylabel):
    df = pd.read_csv(filename)

    xdata = df[xlabel]
    ydata = df[ylabel]

    xstats = xdata.describe()
    ystats = ydata.describe()
    
    return xstats, ystats

if __name__ == '__main__':
    print (stats_columns('tempRainYearly.csv','Temp', 'Rain' ))