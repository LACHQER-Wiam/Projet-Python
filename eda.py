import pandas as pd
import seaborn as sns

def correlation(df):
    corr = df.corr()
    corr.style.background_gradient(cmap='coolwarm')
    return corr

def scatterplot(data,x,y,var):
    sns.scatterplot(data=data, x=x, y=y, hue=var)

def histplot(data,x,bins=30,binwidth=3):
    sns.histplot(data=data, x=x, bins=bins, binwidth=binwidth)

