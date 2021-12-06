import pyupbit
import requests
import time
from tkinter import *

from pyupbit.quotation_api import get_ohlcv

access_key = ""
secret_key = ""

global upbit
upbit = pyupbit.Upbit(access_key, secret_key) #일종의 거래계좌이다

global coin_data
coin_data = []
global coin_list
coin_list = ['STEEM']
for coin in coin_list:
    coin_data.append({'market_data':coin, 'trade_amount':0, 'noise':0, 'stand_price':0, 'score':0, 'isBuy':True, 'isSell':False})

global time_gap
global trade_amount

def start():
    global coin_list
    print("-----------------------------")
    print("  코인 자동 매매 프로그램  ")
    print("-----------------------------")
    print("\n현재 감시대상: ")
    print(coin_list)

    global time_gap
    time_gap = input("원하는 (시간)봉 입력(100입력시 일봉): ")

    global trade_amount
    trade_amount = int(input("매매 금액 입력: "))
    
    trade_loop()


def trade_loop():
    global coin_data
    global time_gap
    global trade_amount

    #response 설정
    if(time_gap == '100'):
        url = "https://api.upbit.com/v1/candles/days/"
    else:
        url = "https://api.upbit.com/v1/candles/minutes/" + time_gap
        
    score_sum = 0
    #coin_list 데이터 입력
    for coin in coin_data:
        querystring = {"market": "KRW-"+coin['market_data'],"count":"60"}
        response = requests.request("GET", url, params=querystring)
        j_res = response.json()
        #print(j_res)

        #noise설정
        noise_account = 21 # noise 20개 기준
        k=0
        _divide = 0
        for _term in range(1, noise_account):
            if(j_res[_term]['high_price'] - j_res[_term]['low_price'] != 0):
                k += (1 - abs((j_res[_term]['opening_price'] - j_res[_term]['trade_price'])/(j_res[_term]['high_price'] - j_res[_term]['low_price'])))
                _divide+=1
            else:
                pass
        k/=_divide
        coin['noise'] = k

        #score 설정, 18-18평균선
        avr_score = 0
        for price_20 in range(3, 21):
            avr_price = 0
            divide_count = 0
            for date_count in range(1, 19):
                avr_price += j_res[price_20 + date_count]['trade_price']
                divide_count += 1
            avr_price /= divide_count
            if(avr_price<j_res[price_20]['trade_price']):
                avr_score += 1/18
        if(avr_score >= 1):
            avr_score = 1
        coin['score'] = avr_score
        score_sum += coin['score']
        if(coin['score'] == 0):
            coin['isBuy'] = False
        else:
            coin['isBuy'] = True

        #range & stand_price 설정
        _range = j_res[1]['high_price'] - j_res[1]['low_price']
        _range = float(_range) * coin['noise']
        stand_price = j_res[0]['opening_price'] + _range
        coin['stand_price'] =  stand_price

    for coin in coin_data:
        if(score_sum != 0):
            coin['trade_amount'] = int(trade_amount * coin['score'] *coin['score'] / score_sum)
        print(coin)
    #print(coin_data)
    
    #시간 계산 로직
    stand_time = j_res[0]['candle_date_time_kst']
    print("현재 기준 시간: {0:}".format(stand_time))
    cur_time = j_res[0]['candle_date_time_kst']
    while(stand_time == cur_time):
        for coin in coin_data:
            if(coin['isBuy']==True):
                buycall(coin['market_data'], coin['trade_amount'], coin['stand_price'])
        #현재 시각 초기화 로직                
        response = requests.request("GET", url, params=querystring)
        j_res = response.json()
        cur_time = j_res[0]['candle_date_time_kst']
        time.sleep(1)
                
    for coin in coin_data:
        if(coin['isSell']==True):
            sellcall(coin['market_data'])

    trade_loop()
                
            
def buycall(market_data, trade_amount, stand_price):
    global upbit
    global coin_data
    market_data = "KRW-"+market_data

    cur_price = pyupbit.get_current_price(market_data)
    '''for coin in coin_data:
        print(coin['isBuy'])'''

    if(stand_price < cur_price):
        print("\n{0:} 매수 기준가 도달!!" .format(market_data))
        upbit.buy_market_order(market_data, trade_amount)

        for coin in coin_data:
            if(market_data == "KRW-"+coin['market_data']):
                coin['isBuy'] = False
                coin['isSell'] = True
            print(coin)
    
def sellcall(market_data):
    global coin_data
    global upbit
    market_data = "KRW-"+market_data
    upbit.sell_market_order(market_data, upbit.get_balance(ticker=market_data))
    print("\n{0:} 매도 완료" .format(market_data))

    for coin in coin_data:
        if(market_data == "KRW-"+coin['market_data']):
            coin['isBuy'] = True
            coin['isSell'] = False

    

def datacheck():
    global coin_list
    global coin_data
    
    _time_gap = ''
    print("계산중... 대략 10분 정도 소요됩니다")
    
    _loop = 150
    noise_account = 21
    file = ''
    for coin in coin_list:
        file+= coin+', '
    file+='.txt'
    fw = open(file, "wt")

    #for date_loop in range(0, 8):
    date_loop = 0
    loop = _loop
    if(date_loop == 0):
        url = "https://api.upbit.com/v1/candles/minutes/1"
        _time_gap = '1분'
    if(date_loop == 1):
        url = "https://api.upbit.com/v1/candles/minutes/3"
        _time_gap = '3분'
    if(date_loop == 2):
        url = "https://api.upbit.com/v1/candles/minutes/5"
        _time_gap = '5분'
    if(date_loop == 3):
        url = "https://api.upbit.com/v1/candles/minutes/10"
        _time_gap = '10분'
    if(date_loop == 4):
        url = "https://api.upbit.com/v1/candles/minutes/30"
        _time_gap = '30분'
    if(date_loop == 5):
        url = "https://api.upbit.com/v1/candles/minutes/60"
        _time_gap = '60분'
    if(date_loop == 6):
        url = "https://api.upbit.com/v1/candles/minutes/240"
        _time_gap = '240분'
    if(date_loop == 7):
        url = "https://api.upbit.com/v1/candles/days/"
        _time_gap = '1일'
   
    amount = 100
    amount_sum = 100
    #data loop
    while(loop>0):
        score_sum = 0
        
        #coin_list 데이터 입력
        for coin in coin_data:
            querystring = {"market": "KRW-"+coin['market_data'],"count":"200"}
            response = requests.request("GET", url, params=querystring)
            j_res = response.json()
            time.sleep(0.05)##############################################
            #nosie 설정
            k = 0
            _divide = 0
            for _term in range(1, noise_account):
                if((j_res[loop+ _term]['high_price'] - j_res[loop+ _term]['low_price']) !=0 ):
                    k += 1 - abs((j_res[loop+ _term]['opening_price'] - j_res[loop+ _term]['trade_price'])/(j_res[loop+ _term]['high_price'] - j_res[loop+ _term]['low_price']))
                    _divide += 1
                else:
                    pass
            k/=_divide
            coin['noise'] = k
            #score 설정
            avr_score = 0
            for price_20 in range(3, 21):
                avr_price = 0
                divide_count = 0
                for date_count in range(1, 19):
                    avr_price += j_res[loop+price_20 + date_count]['trade_price']
                    divide_count += 1
                avr_price/=divide_count
                if(avr_price<j_res[loop+price_20]['trade_price']):
                    avr_score += 1/18
            if(avr_score >= 1):
                avr_score = 1
            coin['score'] = avr_score
            score_sum += coin['score']
            #range & stand_price 설정
            _range = j_res[loop+1]['high_price'] - j_res[loop+1]['low_price']
            _range = float(_range) * coin['noise']
            stand_price = j_res[loop]['opening_price'] + _range
            coin['stand_price'] = stand_price
        for coin in coin_data:
            if(score_sum != 0):
                coin['trade_amount'] = int(amount * coin['score'] / score_sum)
            else:
                coin['trade_amount'] = 0
            #계산로직
            if(coin['stand_price'] <j_res[loop]['high_price']):
                _gap = j_res[loop]['trade_price'] * 0.9995 - coin['stand_price'] * 1.0005
                _gap_per = _gap / j_res[loop]['trade_price'] * coin['trade_amount']
                amount_sum += _gap_per * coin['score']
        loop-=1
    #print("{0:}봉 이익 실현율: {1:.3f}%".format(_time_gap, amount_sum))
    #파일입출력
    fw.write("{0:}봉 이익 실현율: {1:.3f}%".format(_time_gap, amount_sum))
    fw.write('\n')
    fw.close()




















    
def show():
    s_count = 150
    
    ohlcv = get_ohlcv("KRW-STEEM", interval="day", count=s_count)
    mx_high = max(ohlcv["high"])
    mn_low = min(ohlcv["low"])
    xn_height = 400 / (mx_high - mn_low)
      
    win = Tk()
    win.geometry("1200x600")
    win.title("show")
    win.option_add("*Font", "맑은고딕 12")
    btn = Button(win, text = "매매 결과 출력")
    btn.place(x = 0, y = 508)
    tw = 1192 - 100 - s_count
    th = 500
    tics = Canvas(win, relief="solid", bd = 2, width = tw + 100 + s_count, height = th)
    tics.place(x = 0, y = 0)
    
    for i in range(s_count):
        if ohlcv["open"][i] > ohlcv["close"][i]:
            tics.create_rectangle(i + 50 + (i * tw/s_count), 50 + (mx_high - ohlcv["open"][i]) * xn_height , i + 50 + ((i + 1) * tw/s_count), 50 + (mx_high - ohlcv["close"][i]) * xn_height, fill = "blue", outline= "blue")
            tics.create_rectangle(i + 50 + (i * tw/s_count + tw/2/s_count), 50 + (mx_high - ohlcv["high"][i]) * xn_height, i + 50 + (i * tw/s_count + tw/2/s_count), 50 + (mx_high - ohlcv["low"][i]) * xn_height, fill = "blue", outline= "blue")
        else : 
            tics.create_rectangle(i + 50 + (i * tw/s_count), 50 + (mx_high - ohlcv["open"][i]) * xn_height , i + 50 + ((i + 1) * tw/s_count), 50 + (mx_high - ohlcv["close"][i]) * xn_height, fill = "red", outline= "red")
            tics.create_rectangle(i + 50 + (i * tw/s_count + tw/2/s_count), 50 + (mx_high - ohlcv["high"][i]) * xn_height, i + 50 + (i * tw/s_count + tw/2/s_count), 50 + (mx_high - ohlcv["low"][i]) * xn_height, fill = "red", outline= "red")
        #k = tics.create_rectangle(50 + (i * 600/s_count), 1000 - ohlcv["open"][i], 50 + ((i + 1) * 600/s_count), 1000 - (ohlcv["close"][i]))
        
    
    global coin_list
    global coin_data
    
    _time_gap = ''
    print("계산중... 대략 10분 정도 소요됩니다")
    
    _loop = 150
    noise_account = 21
    #file = ''
    #for coin in coin_list:
    #    file+= coin+', '
    #file+='.txt'
    #fw = open(file, "wt")

    #for date_loop in range(0, 8):
    date_loop = 7
    loop = _loop
    if(date_loop == 0):
        url = "https://api.upbit.com/v1/candles/minutes/1"
        _time_gap = '1분'
    if(date_loop == 1):
        url = "https://api.upbit.com/v1/candles/minutes/3"
        _time_gap = '3분'
    if(date_loop == 2):
        url = "https://api.upbit.com/v1/candles/minutes/5"
        _time_gap = '5분'
    if(date_loop == 3):
        url = "https://api.upbit.com/v1/candles/minutes/10"
        _time_gap = '10분'
    if(date_loop == 4):
        url = "https://api.upbit.com/v1/candles/minutes/30"
        _time_gap = '30분'
    if(date_loop == 5):
        url = "https://api.upbit.com/v1/candles/minutes/60"
        _time_gap = '60분'
    if(date_loop == 6):
        url = "https://api.upbit.com/v1/candles/minutes/240"
        _time_gap = '240분'
    if(date_loop == 7):
        url = "https://api.upbit.com/v1/candles/days/"
        _time_gap = '1일'
   
    amount = 100
    amount_sum = 100
    #data loop
    while(loop>0):
        score_sum = 0
        
        #coin_list 데이터 입력
        for coin in coin_data:
            querystring = {"market": "KRW-"+coin['market_data'],"count":"200"}
            response = requests.request("GET", url, params=querystring)
            j_res = response.json()
            time.sleep(0.08)##############################################
            #nosie 설정
            k = 0
            _divide = 0
            for _term in range(1, noise_account):
                if((j_res[loop+ _term]['high_price'] - j_res[loop+ _term]['low_price']) !=0 ):
                    k += 1 - abs((j_res[loop+ _term]['opening_price'] - j_res[loop+ _term]['trade_price'])/(j_res[loop+ _term]['high_price'] - j_res[loop+ _term]['low_price']))
                    _divide += 1
                else:
                    pass
            k/=_divide
            coin['noise'] = k
            #score 설정
            avr_score = 0
            for price_20 in range(3, 21):
                avr_price = 0
                divide_count = 0
                for date_count in range(1, 19):
                    avr_price += j_res[loop+price_20 + date_count]['trade_price']
                    divide_count += 1
                avr_price/=divide_count
                if(avr_price<j_res[loop+price_20]['trade_price']):
                    avr_score += 1/18
            if(avr_score >= 1):
                avr_score = 1
            coin['score'] = avr_score
            score_sum += coin['score']
            #range & stand_price 설정
            _range = j_res[loop+1]['high_price'] - j_res[loop+1]['low_price']
            _range = float(_range) * coin['noise']
            stand_price = j_res[loop]['opening_price'] + _range
            coin['stand_price'] = stand_price
        for coin in coin_data:
            if(score_sum != 0):
                coin['trade_amount'] = int(amount * coin['score'] / score_sum)
            else:
                coin['trade_amount'] = 0
            #계산로직
            if(coin['stand_price'] <j_res[loop]['high_price']):
                _gap = j_res[loop]['trade_price'] * 0.9995 - coin['stand_price'] * 1.0005
                tics.create_oval(150 - loop + 50 + ((150 - loop - 1) * tw/s_count), 50 + (mx_high - coin['stand_price']) * xn_height + 1, 150 - loop + 50 + ((150 - loop) * tw/s_count), 50 + (mx_high - coin['stand_price']) * xn_height - 1, fill = "black")
                _gap_per = _gap / j_res[loop]['trade_price'] * coin['trade_amount']
                amount_sum += _gap_per * coin['score']
        loop-=1
    #print("{0:}봉 이익 실현율: {1:.3f}%".format(_time_gap, amount_sum))
    #파일입출력
    #fw.write("{0:}봉 이익 실현율: {1:.3f}%".format(_time_gap, amount_sum))
    #fw.write('\n')
    #fw.close()
    
    
    win.mainloop()
    

show()
#datacheck()
