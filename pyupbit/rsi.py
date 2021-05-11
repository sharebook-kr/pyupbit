import requests
import pandas as pd
import time
import sys
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

while True:
    
    def rsiindex(symbol, minutes = 10):
        url = "https://api.upbit.com/v1/candles/minutes/" + str(minutes)
    
        querystring = {"market":symbol,"count":"500"}
        response = requests.request("GET", url, params=querystring)
    
        try:
            data = response.json()
        except:
            print(f'Error : {symbol}')
            print("Unexpected error:", sys.exc_info()[0])
            return -1

        df = pd.DataFrame(data)
        df=df.reindex(index=df.index[::-1]).reset_index()
    
        df['close']=df["trade_price"]
        
        def rsi(ohlc: pd.DataFrame, period: int = 14):
            ohlc["close"] = ohlc["close"]
            delta = ohlc["close"].diff()
    
            up, down = delta.copy(), delta.copy()
            up[up < 0] = 0
            down[down > 0] = 0
    
            _gain = up.ewm(com=(period - 1), min_periods=period).mean()
            _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()
    
            RS = _gain / _loss
            return pd.Series(100 - (100 / (1 + RS)), name="RSI")
    
        rsi = rsi(df, 14).iloc[-1]
        #print(symbol)
        #print(f'Upbit {minutes} minute RSI: {rsi}')
        return rsi
       

    def check_rsi_3types(ticker):
        rsi_type = [1, 5, 10]
        rsi = []
        for i in rsi_type:
            rsi_vaule = rsiindex(ticker, i)
            if rsi_vaule >= 0:
                rsi.append(rsi_vaule)
            else:
                return
        
        if rsi[0] < 20 and rsi[1] < 20 and rsi[2] < 20:
            print(f'>>>>>')
            print(f'{ticker} RSI : 1min = {rsi[0]}, 5min =  { rsi[1]}, 10min = {rsi[2]}')
        
        del(rsi)
        time.sleep(0.01)

    for ticker in tickers:
        #rsiindex(ticker, 1)
        #print(f'{ticker} ')
        print('', end='.')

        check_rsi_3types(ticker)
    
    print(f'RSI checking')
    time.sleep(30)