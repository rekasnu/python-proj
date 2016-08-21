
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import pandas as pd
from matplotlib.finance import  candlestick_ohlc




class View(object):
    
    def candlestickChart(self,data11):
        asdate = pd.to_datetime(data11['Date']).tolist()
        ddates = mdates.date2num(asdate)
        #print ddates
        DOCHLV = zip(ddates , data11.Open, data11.High, data11.Low,data11.Close, data11.Volume)
        
        fig, ax1 = plt.subplots()
        candlestick_ohlc(ax1, DOCHLV, colorup='g', colordown='r', width=0.6 ,alpha = 1.0)
        
        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(45)

        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
        ax1.grid(True)
        mng = plt.get_current_fig_manager()
        
        mng.resize(1000,700)  
        
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Bank of America Stock Price')
        #_FIG_SIZE = (20, 10)
        #stock.plot(figsize=_FIG_SIZE, title='Bank of America Stock Price')
        #plt.legend()
        plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
        #fig.autofmt_xdate()
        plt.show()

    def simpleChart(self,dates,opens):
        
        years = YearLocator()   # every year
        months = MonthLocator()  # every month
        yearsFmt = DateFormatter('%m-%Y')
        monthFmt = DateFormatter('%m-%Y')
        fig, ax = plt.subplots()
        plt.plot_date(dates, opens, '-',label="Bank of America oclose price")
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        
        # format the coords message box
        def price(x):
            return '$%1.2f' % x
        ax.fmt_xdata = DateFormatter('%Y-%m-%d')
        ax.fmt_ydata = price
        ax.grid(True)
        
        fig.autofmt_xdate()
        legend = ax.legend(loc=8, shadow=True)
        # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        
        # Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('small')
        
        for label in legend.get_lines():
            label.set_linewidth(1.0)  # the legend line width
        mng = plt.get_current_fig_manager()
        mng.resize(1000,700)
        fig.savefig('rezult.png', dpi=100)
        plt.show()


    def movingaveragesChart(self,dates,df,price_trend,ndates,trend1,signal):
        
        years = YearLocator()   # every year
        months = MonthLocator()  # every month
        yearsFmt = DateFormatter('%m-%Y')
        monthFmt = DateFormatter('%m-%Y')
        fig, ax = plt.subplots()
        #ax.plot_date(new_d1, interpolatedY4, '-',label="polinomeal prediction")
        #plt.plot_date(dates, opens, '-',label="Bank of America oclose price")
        #plt.plot_date(dates, data1['pred'], '-',label="Bank of America pred price")
        #plt.plot_date(ndates, df1['pred'], '-',label="Bank pred price")
        
        #plt.plot_date(new_d1, results, '-', label="aaaaaaaaaaaaaaaaa")
        ##plt.plot_date(dates, interpolatedY, '-')
        
        #sp= sp[-200:]
        #dates = dates[-200:]
        ##plt.plot_date(dates, sp['ave'], '-')
        ##plt.plot_date(dates, sp['upper'], '-')
        ##plt.plot_date(dates, sp['lower'], '-')
        #dates100 = dates.tolist()
        #dates = dates100[-600:]
        
        ma20 = df['MA20'].tolist()
        #ma20 = ma20[:600]
        ma50 = df['MA50'].tolist()
        #ma50 = ma50[:600]
        ma100 = df['MA100'].tolist()
        #ma100 = ma100[:600]
        ewma = df['EWMA'].tolist()
        #ewma = ewma[:600]
        #ma20.reverse()
        upper_bb = df['UPPER_BB'].tolist()
        #upper_bb.reverse()
        lower_bb = df['LOWER_BB'].tolist()
        max_size = len(lower_bb)
        dates = dates[:max_size]
        #lower_bb.reverse()
        plt.plot_date(dates, ewma, '-',label="Weighted moving average")
        plt.plot_date(dates, ma20, '-',label="20 day moving average")
        plt.plot_date(dates, ma50, '-',label="50 day moving average")
        plt.plot_date(dates, ma100, '-',label="100 day moving average")
        #=plt.plot_date(dates, upper_bb, '-')
        #=plt.plot_date(dates, lower_bb, '-')
        #plt.plot_date(dates, price_cycle, '-', label="noise")
        #price_trend = price_trend[:600]
        plt.plot_date(dates, price_trend.tail(600), '-',label="Bank of America Stock Price(trend)")
        # format the ticks
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        #ax.autoscale_view()
        #print dates
        
        # format the coords message box
        def price(x):
            return '$%1.2f' % x
        ax.fmt_xdata = DateFormatter('%Y-%m-%d')
        ax.fmt_ydata = price
        ax.grid(True)
        
        fig.autofmt_xdate()
        legend = ax.legend(loc=8, shadow=True)
        # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        # add arrows to the chart
        for xl in range(len(signal)):
            if signal[xl] == 'sell':
                ax.annotate('sell', xy=(ndates[xl], trend1[xl]), xytext=(ndates[xl], trend1[xl]+0.5),
                    arrowprops=dict(facecolor='red', shrink=0.05),
                    )
            if signal[xl] == 'buy':
                ax.annotate('buy', xy=(ndates[xl], trend1[xl]), xytext=(ndates[xl], trend1[xl]-0.5),
                    arrowprops=dict(facecolor='green', shrink=0.05),
                    )
        # Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('small')
        
        for label in legend.get_lines():
            label.set_linewidth(1.0)  # the legend line width
        mng = plt.get_current_fig_manager()
        mng.resize(1000,700)
        fig.savefig('rezult.png', dpi=100)
        plt.show()

    def trendANDnoizeSplit(self,stock):
        #plt.style.use('fivethirtyeight')
        _FIG_SIZE = (20, 10)
        stock.plot(figsize=_FIG_SIZE, title='Stock Price of Cycle and Trend')
        plt.show()

    def plotTrendAndNoise(self,dates,price_trend,price_cycle,opens):
    	years = YearLocator()   # every year
        months = MonthLocator()  # every month
        yearsFmt = DateFormatter('%m-%Y')
        monthFmt = DateFormatter('%m-%Y')
        fig, ax = plt.subplots()
        plt.plot_date(dates, opens, '-',label="Bank of America oclose price")
        plt.plot_date(dates, price_cycle, '-', label="noise")
        plt.plot_date(dates, price_trend, '-',label="Bank of America Stock Price(trend)")
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)
        
        # format the coords message box
        def price(x):
            return '$%1.2f' % x
        ax.fmt_xdata = DateFormatter('%Y-%m-%d')
        ax.fmt_ydata = price
        ax.grid(True)
        
        fig.autofmt_xdate()
        legend = ax.legend(loc=8, shadow=True)
        # The frame is matplotlib.patches.Rectangle instance surrounding the legend.
        frame = legend.get_frame()
        frame.set_facecolor('0.90')
        
        # Set the fontsize
        for label in legend.get_texts():
            label.set_fontsize('small')
        
        for label in legend.get_lines():
            label.set_linewidth(1.0)  # the legend line width
        mng = plt.get_current_fig_manager()
        mng.resize(1000,700)
        fig.savefig('rezult.png', dpi=100)
        plt.show()
