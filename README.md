# pyupbit
Python Wrapper for Upbit API

## Installation
```sh
pip install pyupbit
```

## Import
```python
import pyupbit
```

## Quotation API
####  암호화폐 목록
업비트가 지원하는 암호화폐 목록을 얻어온다.
```python
print(pyupbit.get_tickers())
```

####  암호화폐 목록 (KRW/BTC/ETH/USDT)
업비트가 지원하는 암호화폐 목록 중 특정 Fiat로 매매가 가능한 목록만 얻어온다.
```python
print(pyupbit.get_tickers(fiat="KRW"))
print(pyupbit.get_tickers(fiat="BTC"))
print(pyupbit.get_tickers(fiat="ETH"))
print(pyupbit.get_tickers(fiat="USDT"))
```


#### 최근 체결가격
특정 암호화폐에 대한 현재가를 얻어온다. 
```python
print(get_current_price("KRW-BTC"))
```

#### 차트 데이터
```python
print(get_ohlcv("KRW-BTC"))                             # 기본 일봉 데이터
print(get_ohlcv("KRW-BTC", interval="minute"))          # 분봉 데이터
print(get_ohlcv("KRW-BTC", interval="week"))            # 주봉 데이터 
```

#### 매수/매도 호가
```python
print(get_orderbook(tickers="KRW-BTC")
print(get_orderbook(tickers=["KRW-BTC", "KRW-XRP"]))
```  


## Exchange API
#### 로그인
Access Key와 Sercret Key를 사용해서 로그인한다. 
```python
access = "73kVqowGQOGEjdR31221j31j2ifekjkgjekgjekg"          # 본인 값으로 변경
secret = "egjekgj3iekeEEkej3i3j3iejjwiEejiejeEeijg"          # 본인 값으로 변경
upbit = Upbit(access, secret)
```

#### 잔고 조회
```python
print(upbit.get_balances())
```

#### 매수/매도 주문
리플을 507원에 20개 매수한다. 
리플을 500원에 20개 매도한다. 
```python
# 매도
print(upbit.sell_limit_order("KRW-XRP", 507, 20))

# 매수
print(upbit.buy_limit_order("KRW-XRP", 500, 20))
```

#### 매수/매도 주문 취소
주문 함수의 리턴 값 중 uuid 값을 사용해서 주문을 취소할 수 있다. 
```python
print(upbit.cancel_order('e57a3bc0-0b0b-4540-96f2-f35f19c51e8d'))
```

