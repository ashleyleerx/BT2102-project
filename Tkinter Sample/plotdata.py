import pandas as pd
from  matplotlib import pyplot as plt
import matplotlib
import seaborn as sns

def regression_plot(filename, xlabel, ylabel):
    # create the dataframe using the csv file upload
    df = pd.read_csv(filename)
    # Temp, Year and Rain(fall)
    # How we set width, height using matplotlib settings
    sns.set(rc={'figure.figsize':(12,6)})
    sns.regplot(x=xlabel, y=ylabel, data=df)
    # regression line shows a possible positive correlation - as temp increases so does rainfall.
    plt.show() 
    
    return

if __name__ == '__main__':
    regression_plot('tempRainYearly.csv','Temp', 'Rain' )