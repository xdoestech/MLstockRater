import pandas as pd
import os
import time
from datetime import datetime
from pickle import FALSE

from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")

import re

#data.nasdaq.com APIKEY:3UKWu_y1RsA6GCxUWTVC
path = "C:/Users/axyzh/OneDrive/Desktop/intraQuarter"

def Key_Stats(gather="Total Debt/Equity (mrq)"):
    statspath = path+"/_KeyStats"
    stock_list = [x[0] for x in os.walk(statspath)]#goes through the file and gets the path (os.walk returns tuple)(x[0] is dirpath
    #print(stock_list[1:40]) #normally too big to print
    df = pd.DataFrame(columns = ['Date',
                                 'Unix', 
                                 'Ticker',
                                 'DE Ratio',
                                 'Price',
                                 'stock_p_change',
                                 'NASDAQ',
                                 'nasdaq_p_change',
                                 'Difference']) 
    
     #data frame of nasdaq data from 2000-2015
    nasdaq_df = pd.read_csv("nasdaq_2000-2015.csv")
    
    #print(nasdaq_df)
    ticker_list = [] 
    
    for each_dir in stock_list[1:25]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split("\\")[1]
        ticker_list.append(ticker)
        #print(ticker)
        starting_stock_value = False 
        starting_nasdaq_value = False 
        
        
        if len(each_file) > 0:
            for file in each_file:
                date_stamp = datetime.strptime(file, "%Y%m%d%H%M%S.html")
                unix_time = time.mktime(date_stamp.timetuple())
                #print(date_stamp, unix_time)
                full_file_path = each_dir + '/' + file
                #print(full_file_path)
                source = open(full_file_path, 'r').read()
                #print(source)
                try:
                    #deal with the errors
                    try:
                        value = float(source.split(gather+':</td><td class="yfnc_tabledata1">')[-1][:10].split('</td>')[0])
                    except Exception as e:
                        value = float(source.split(gather+':</td>\n<td class="yfnc_tabledata1">')[-1][:10].split('</td>')[0])
                        print(str(e), ticker,file)
                        #time.sleep(1)
                    #value = float(source.replace('\n','').split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    #print(value)
                    try:
                        nasdaq_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        #print(nasdaq_date)
                        row = nasdaq_df[(nasdaq_df["Date"] == nasdaq_date)]
                        #print(row)
                        nasdaq_value = float(row["Adj Close"])
                        #print(nasdaq_value)
                    except: #if on a weekend subtract by 259200 (seconds in 3 days)
                        nasdaq_date = datetime.fromtimestamp(unix_time-259200).strftime('%Y-%m-%d')
                        row = nasdaq_df[(nasdaq_df["Date"] == nasdaq_date)]
                        nasdaq_value = float(row["Adj Close"])
                    # run block of code and catch warnings
                    ##APPEND IS DEPRECIATED NEED THIS TO GET RID OF WARNINGS
                    
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                    except Exception as e:
                        try:
                            print(str(e), ticker,file)
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,8}\.\d{1,8})',stock_price) #r from 1-8
                            stock_price = float(stock_price.group(1))
                            
                            print(stock_price)
                        except Exception as e:
                            print(str(e))
                            #time.sleep(15)
                        #print("stock_price:", stock_price, "ticker", ticker
                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    
                    if not starting_nasdaq_value:
                        starting_nasdaq_value = nasdaq_value
                    
                         
                    #stock_p_change = (stock_price - starting_stock_value)
                    stock_p_change = ((stock_price - starting_stock_value) / starting_stock_value) * 100
                    nasdaq_p_change= ((nasdaq_value - starting_nasdaq_value) / starting_nasdaq_value) * 100
                    
                    df = df.append({'Date': date_stamp,
                                    'Unix':unix_time,
                                    'Ticker':ticker,
                                    'DE Ratio':value,
                                    'Price':stock_price,
                                    'stock_p_change': stock_p_change,
                                    'NASDAQ':nasdaq_value,
                                    'nasdaq_p_change':nasdaq_p_change,
                                    'Difference':stock_p_change - nasdaq_p_change}, ignore_index = True) #change to CONCAT because append is depreciated concact is faster same supposedly
                except Exception as e:
                    pass
                #print(ticker+":", value)
                
    
    for each_ticker in ticker_list:
        try:
            plot_df = df[(df['Ticker'] == each_ticker)]
            plot_df = plot_df.set_index(['Date'])
            
            plot_df['Difference'].plot(label = each_ticker)
            plt.legend()
            
        except:
            pass
    plt.show()
    
    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)#file with all the data from sources

Key_Stats()

