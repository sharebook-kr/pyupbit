import requests
import pandas as pd
import time
import webbrowser
import pyupbit

ticker_list = pyupbit.get_tickers()
#tickers = ['KRW-BTC', 'KRW-ETH']

tickers = list()
for ticker in ticker_list:
    #print(f'{ticker[0:3]}')
    if ticker.startswith('KRW'):
        #print('yes')
        tickers.append(ticker)

print(tickers)
