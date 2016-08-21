

import matplotlib.ticker as mticker

import datetime
import time
import pandas as pd
import numpy as np



#from sklearn import linear_model 
from manipulate_data import Data
from view import View


data = Data()

## get data from web
#data.getData("WIKI-BAC")

## get from csv
data1 = pd.read_csv('WIKI-BAC.csv',nrows = 802)
data100 = pd.read_csv('WIKI-BAC.csv',nrows = 802)


dates = pd.to_datetime(data1['Date'])
dates15 = pd.to_datetime(data100['Date'])
opens = data1['Close'].tail(600)

d=[]
for i in data1['Date'].tail(600):
    d.append(time.mktime(datetime.datetime.strptime(i, "%Y-%m-%d").timetuple()))

coeffs = data.calculatePolinomialCoef(opens,d,data1)

d1 = list(d)

new_d1 = data.createNewDatesForPolinomialPred(d)


interpolatedY4 = np.polyval(coeffs, d1);

dates = pd.to_datetime(data1['Date'])

opens = data1['Close']
df= pd.DataFrame()


dn=[]
for i in data1['Date']:
    dn.append(time.mktime(datetime.datetime.strptime(i, "%Y-%m-%d").timetuple()))
dn = np.asarray(dn)
dn= dn.reshape(len(dn),1)

df = data.process_df(df,opens) 

data10 = data.predictPriceFromDate(data1)

data11, price_cycle, price_trend, stock = data.hodericPrescotFilter(data1)

dates1 = pd.to_datetime(data1['Date'].tail(600))

df1 = df.tail(600)

ndates,trend1,newma,signal = data.getSignal(df1,price_trend,dates1)

######### Charts ########################

view = View()
view.candlestickChart(data11)

view.simpleChart(dates15,opens)
#view.trendANDnoizeSplit(stock)
view.plotTrendAndNoise(dates,price_trend,price_cycle,opens)
view.movingaveragesChart(dates1,df1,price_trend,ndates,trend1,signal)


