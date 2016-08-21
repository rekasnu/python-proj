from scipy.stats import pearsonr
import pandas as pd
import numpy as np
import Quandl as ql
import time
import datetime



import statsmodels.formula.api as smf
import statsmodels.api as sm

class Data(object):
    
    def getData(self,code):
        #data1 = ql.get("YAHOO/INDEX_GDAXI", trim_start="2001-12-31", trim_end="2016-03-26", rows=802)
        #data1.to_csv('dax.csv')

        data1 = ql.get(code, trim_start="2001-12-31", trim_end="2016-05-30", rows=802)
        code = code.replace('/', '-')
        data1.to_csv(code+'.csv')
        ###data1 = ql.get("WIKI/BAC", trim_start="2001-12-31", trim_end="2016-03-26", rows=802)
        ###data1.to_csv('WIKI-BAC.csv')


    def process_df(self,df,pr): 
        df['price'] = pr 
        df['MA20']=pd.stats.moments.rolling_mean(df['price'], 20)
        df['MA50']=pd.stats.moments.rolling_mean(df['price'], 50)
        df['MA100']=pd.stats.moments.rolling_mean(df['price'], 100)
        df['ABS']=abs(df['price']-df['MA20'])
        df['STDDEV']=pd.stats.moments.rolling_std(df['ABS'], 20)
        df['UPPER_BB']=df['MA20']+2*df['STDDEV']
        df['LOWER_BB']=df['MA20']-2*df['STDDEV']
        df['EWMA']= pd.ewma(df["price"], span=60)
        df.dropna(thresh=(len(df) - 3), axis=1)
        return df
    
    def calculatePolinomialCoef(self,opens,d,data1):
        c=1
        rez1 = 0
        while True:
            k = np.polyfit(d, opens, c)
            print 'coef c - ' ,c
            interpolatedX = np.linspace(min(d), max(d), len(d));
            interpolatedY = np.polyval(k, interpolatedX)
            rez = pearsonr(opens, interpolatedY)
            print 'xxx1=== ', rez[0], '  probabil === ', rez[1]
            if c==1:
            	rez1= rez[0]
            	coeffs = k
            	print 'c=1 ',coeffs
            	time.sleep(5)
            elif c==2:
                rez01 = rez[0]
                coeffs1 = k
                print 'c=2 ',coeffs1
            	time.sleep(5)
            elif rez01 <= rez[0] and data1.shape[0] < 500:
                coeffs = coeffs1
                print 'c = ',c,' and ',coeffs
                time.sleep(5)
                break
            elif rez01 <= rez[0] and rez1 <= rez[0] and data1.shape[0] > 500:  
            	coeffs = k
            	print 'c = ',c,' and ',coeffs
            	time.sleep(5)
                break
            else:
                rez1 = rez01
                rez01 = rez[0]
                coeffs1 = k
                print 'coeffs1 = ', coeffs1
            c+=1
        
        print 'calculate' ,coeffs
        interpolatedY = np.polyval(coeffs, d)
        k = np.polyfit(d, opens, 5)
        interpolatedY1 = np.polyval(k, interpolatedX);
        rez = pearsonr(opens, interpolatedY1)
        print 5,' disp ', rez[0]
        k = np.polyfit(d, opens, 6)
        interpolatedY2 = np.polyval(k, interpolatedX);
        rez = pearsonr(opens, interpolatedY2)
        print 6,' disp ', rez[0]
        k = np.polyfit(d, opens, 7)
        interpolatedY3 = np.polyval(k, interpolatedX);
        rez = pearsonr(opens, interpolatedY3)
        print 7,' disp ', rez[0]

        return coeffs

    def createNewDatesForPolinomialPred(self,d):
        d1 = list(d)
        d2 =[]
        for x in range(20):
            new_x = max(d1)+(d[1]-d[2])
            d1.append(new_x)
            d2.append(new_x)
            x+=1
        
        d1.sort(reverse=True)
        new_d=[datetime.datetime.fromtimestamp(a).strftime('%Y-%m-%d') for a in d1]
        new_d1 = pd.to_datetime(new_d)
        return new_d1

    def predictPriceFromDate(self,data1):
        
        data2 = data1.tail(600) 
        smresults = smf.ols('Open ~ Volume', data1).fit()
        df1 = pd.DataFrame()
        d2 = data1['Volume'].head(n=202).tolist()
        d3 = np.asarray(d2)
        df1['pred'] = smresults.predict(pd.DataFrame({'intercept':1, 'Volume': d3}))
        ndates = pd.to_datetime(data1['Date'].head(n=202))
        data1['pred'] = smresults.predict()
        return data1
    
    def hodericPrescotFilter(self,data1):
        price_cycle, price_trend = sm.tsa.filters.hpfilter(data1.Close)
        stock = pd.DataFrame(data1['Close'])
        stock['cycle'] = price_cycle
        stock['trend'] = price_trend
        
        data11 = data1.tail(n=50)
        return data11,price_cycle, price_trend, stock
        
    def getSignal(self, df1,price_trend,dates1):
        #print df1.tail(20)
        #print data1.tail(20)
        price_trend = price_trend.tail(600)
        #data1 = data1.tail(600)
        #print price_trend.iloc[-1::]
        
        trend = price_trend.tolist()
        ewma = df1['EWMA'].tolist()
        dates = dates1.tolist()
        print len(trend), len(ewma), len(dates)
        signal = []
        ndates = []
        newma = []
        trend1 = []
        for x in range(len(trend)-3):
            if ewma[x] <= trend[x] and ewma[x] >= trend[x+1]:
                signal.append('sell')
                ndates.append(dates[x])
                newma.append(ewma[x])
                trend1.append(trend[x])
            elif ewma[x] >= trend[x] and ewma[x] <= trend[x+1]:
                signal.append('buy')
                ndates.append(dates[x])
                newma.append(ewma[x])
                trend1.append(trend[x])
            else:
                signal.append('hold')
                ndates.append(dates[x])
                newma.append(ewma[x])
                trend1.append(trend[x])
        for a in range(len(signal)):
            if signal[a] != 'hold':
                print ndates[a],trend[a],ewma[a],signal[a]
        return ndates,trend1,newma,signal
        #signal.append('hold')
        #print signal
        #print data1['Close'].iloc[-1::]
        #result = pd.concat([df1, price_trend,data1], axis=1, join='inner')
        #result[result['EWMA']==result['price_trend']]
        #result['OK'] = np.where(result['price'] == result['Close'])
        #pd.get_dummies(df1['YEAR'])
        '''
        data1['action'] = pd.concat('hold', axis=1, join='inner')
        print df1
        for r in range(1,len(df1.index-1)):
            if df1['EWMA'].iloc[r] <= price_trend.iloc[r] and df1['EWMA'].iloc[r+1] >= price_trend.iloc[r]:
                #data1['action'] = pd.concat('hold', index=df1.index)
                data1['action'].iloc[r] = 'buy'
            elif df1['EWMA'].iloc[r] >= price_trend.iloc[r] and df1['EWMA'].iloc[r+1] <= price_trend.iloc[r]:
                data1['action'].iloc[r] = 'sell'
            else:
                data1['action'].iloc[r] = 'hold'
        #def que(x):
        #    if x['EWMA'].iloc[-1::] <= x['Close'] and x['EWMA'].iloc[1::] >= x['Close']:
        #        x['']
        #        return x['one']
        #    else:
        #        ''
        #result['que'] = result.apply(que, axis=1)
        for p in data1['action']:
            print p
        df[data1['action'] == 'buy']
        print df
        print result.iloc[-1::]
        '''