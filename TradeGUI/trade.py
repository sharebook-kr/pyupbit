import pyupbit
import requests
import time
from tkinter import *

from pyupbit.quotation_api import get_ohlcv

global coinSelect
global k_value
global date_loop
global s_count
global minute_day
global url

access_key = ""
secret_key = ""

global upbit
upbit = pyupbit.Upbit(access_key, secret_key) #일종의 거래계좌이다

global coin_data
coin_data = []
global coin_list
coin_list = ['BTC']
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

    
    
def show():
    
    global coin_list
    global coin_data
    global coinSelect
    global k_value
    global date_loop
    global s_count
    global minute_day
    minute_day = "day"
    s_count = 150
    
    win = Tk()
    win.geometry("1200x700")
    win.title("show")
    win.option_add("*Font", "맑은고딕 12")
 
    date_loop_label = Label(win, text = "DateLoop")
    date_loop_label.place(x = 10, y = 508)
    date_loop_listbox =Listbox(win, selectmode='extended', height=0)
    date_loop_listbox.place(x = 10, y = 530)
    date_loop_listbox.insert(0, "1분봉")
    date_loop_listbox.insert(1, "3분봉")
    date_loop_listbox.insert(2, "5분봉")
    date_loop_listbox.insert(3, "10분봉")
    date_loop_listbox.insert(4, "30분봉")
    date_loop_listbox.insert(5, "60분봉")
    date_loop_listbox.insert(6, "240분봉")
    date_loop_listbox.insert(7, "1일봉")
    
    coinEntry = Entry(win)
    coinEntry.place(x = 310, y = 508)
    coinLabel = Label(win, text = "종목")
    coinLabel.place(x = 210, y = 508)

    kEntry = Entry(win)
    kEntry.place(x = 310, y = 558)
    kLabel = Label(win, text = "k값(0 ~ 1)")
    kLabel.place(x = 210, y = 558)

    loopEntry = Entry(win)
    loopEntry.place(x = 310, y = 608)
    loopLabel = Label(win, text = "횟수\n(최대 150)")
    loopLabel.place(x = 210, y = 608)

    resultFrame = Frame(win, width= 600, height= 150, relief="solid", bd = 2)
    resultFrame.place(x = 530, y = 508)

    resultLabel = Label(resultFrame, text = "")
    resultLabel.place(x = 10, y = 40)
    
    profitLabel = Label(resultFrame, text = "")
    profitLabel.place(x = 200, y = 40)



    def Update():
      resultLabel.config(text = "종목 : " + coinSelect + "\n" + "K : " + k_value + "\n" + "횟수 : " + s_count + "\n" + "봉 : " + date_loop, justify=LEFT)
      drawResult()

    def getResult():
      global coinSelect
      global k_value
      global date_loop
      global s_count
      global minute_day
      
      coinSelect = coinEntry.get()
      k_value = kEntry.get()
      s_count = loopEntry.get()
      if date_loop_listbox.curselection()[0] == 0:
        date_loop = "1분봉"
        minute_day = "minute1"
      elif date_loop_listbox.curselection()[0] == 1:
        date_loop = "3분봉"
        minute_day = "minute3"
      elif date_loop_listbox.curselection()[0] == 2:
        date_loop = "5분봉"
        minute_day = "minute5"
      elif date_loop_listbox.curselection()[0] == 3:
        date_loop = "10분봉"
        minute_day = "minute10"
      elif date_loop_listbox.curselection()[0] == 4:
        date_loop = "30분봉"
        minute_day = "minute30"
      elif date_loop_listbox.curselection()[0] == 5:
        date_loop = "60분봉"
        minute_day = "minute60"
      elif date_loop_listbox.curselection()[0] == 6:
        date_loop = "240분봉"
        minute_day = "minute240"
      elif date_loop_listbox.curselection()[0] == 7:
        date_loop = "1일봉"
        minute_day = "day"
    
      Update()

    resultButton = Button(resultFrame, text = "매매 결과 출력", command=getResult)
    resultButton.place(x = 10, y = 10)
    
    def drawResult():
        
        s_count_int = int(s_count)
        tw = 1192 - 100 - s_count_int
        th = 500
        tics = Canvas(win, relief="solid", bd = 2, width = tw + 100 + s_count_int, height = th)
        tics.place(x = 0, y = 0)

        ohlcv = get_ohlcv(coinSelect, interval=minute_day, count=s_count_int)
        mx_high = max(ohlcv["high"])
        mn_low = min(ohlcv["low"])
        xn_height = 400 / (mx_high - mn_low)

        for i in range(s_count_int):
            if ohlcv["open"][i] > ohlcv["close"][i]:
                tics.create_rectangle(i + 50 + (i * tw/s_count_int), 50 + (mx_high - ohlcv["open"][i]) * xn_height , i + 50 + ((i + 1) * tw/s_count_int), 50 + (mx_high - ohlcv["close"][i]) * xn_height, fill = "blue", outline= "blue")
                tics.create_rectangle(i + 50 + (i * tw/s_count_int + tw/2/s_count_int), 50 + (mx_high - ohlcv["high"][i]) * xn_height, i + 50 + (i * tw/s_count_int + tw/2/s_count_int), 50 + (mx_high - ohlcv["low"][i]) * xn_height, fill = "blue", outline= "blue")
            else : 
                tics.create_rectangle(i + 50 + (i * tw/s_count_int), 50 + (mx_high - ohlcv["open"][i]) * xn_height , i + 50 + ((i + 1) * tw/s_count_int), 50 + (mx_high - ohlcv["close"][i]) * xn_height, fill = "red", outline= "red")
                tics.create_rectangle(i + 50 + (i * tw/s_count_int + tw/2/s_count_int), 50 + (mx_high - ohlcv["high"][i]) * xn_height, i + 50 + (i * tw/s_count_int + tw/2/s_count_int), 50 + (mx_high - ohlcv["low"][i]) * xn_height, fill = "red", outline= "red")

        _time_gap = ''
        print("계산중... 대략 10분 정도 소요됩니다")

        _loop = s_count_int
        noise_account = 21
        #file = ''
        #for coin in coin_list:
        #    file+= coin+', '
        #file+='.txt'
        #fw = open(file, "wt")

        global url
        #url = "https://api.upbit.com/v1/candles/days/"
        loop = _loop
        if(date_loop == "1분봉"):
            url = "https://api.upbit.com/v1/candles/minutes/1"
            _time_gap = '1분'
        if(date_loop == "3분봉"):
            url = "https://api.upbit.com/v1/candles/minutes/3"
            _time_gap = '3분'
        if(date_loop == "5분봉"):
            url = "https://api.upbit.com/v1/candles/minutes/5"
            _time_gap = '5분'
        if(date_loop == "10분봉"):
            url = "https://api.upbit.com/v1/candles/minutes/10"
            _time_gap = '10분'
        if(date_loop == "30분봉"):
            url = "https://api.upbit.com/v1/candles/minutes/30"
            _time_gap = '30분'
        if(date_loop == "60분봉"):
            url = "https://api.upbit.com/v1/candles/minutes/60"
            _time_gap = '60분'
        if(date_loop == "240분봉"):
            url = "https://api.upbit.com/v1/candles/minutes/240"
            _time_gap = '240분'
        if(date_loop == "1일봉"):
            url = "https://api.upbit.com/v1/candles/days/"
            _time_gap = '1일'
    
        amount = 100
        amount_sum = 100
        #data loop
        while(loop>0):
            score_sum = 0

            #coin_list 데이터 입력
            for coin in coin_data:
                querystring = {"market": coinSelect,"count":"200"}
                response = requests.request("GET", url, params=querystring)
                j_res = response.json()
                time.sleep(0.08)##############################################
             
                #range & stand_price 설정
                k_value_int = float(k_value)
                
                _range = j_res[loop+1]['high_price'] - j_res[loop+1]['low_price']
                _range = float(_range) * k_value_int
                stand_price = j_res[loop]['opening_price'] + _range
                coin['stand_price'] = stand_price
                
            for coin in coin_data:
                #계산로직
                if(coin['stand_price'] <j_res[loop]['high_price']):
                    _gap = j_res[loop]['trade_price'] * 0.9995 - coin['stand_price'] * 1.0005
                    tics.create_oval(s_count_int - loop + 50 + ((s_count_int - loop - 1) * tw/s_count_int), 50 + (mx_high - coin['stand_price']) * xn_height + 1, s_count_int - loop + 50 + ((s_count_int - loop) * tw/s_count_int), 50 + (mx_high - coin['stand_price']) * xn_height - 1, fill = "black")
                    _gap_per = _gap / j_res[loop]['trade_price']
                    amount_sum += _gap_per
            loop-=1
        profitLabel.config(text = "이익 실현율 :\n" + str(amount_sum) + "%", justify=LEFT)
        
        
        #파일입출력
        #fw.write("{0:}봉 이익 실현율: {1:.3f}%".format(_time_gap, amount_sum))
        #fw.write('\n')
        #fw.close()
        
        
        
    
    
    win.mainloop()
    

show()
#datacheck()
