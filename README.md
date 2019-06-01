# pyupbit
Python Wrapper for Upbit API

## Installation
파이썬 개발 환경으로 최신 버전의 Anaconda를 설치하세요. (Python3 버전용) 

```sh
pip install pyupbit
```

## Import
```python
import pyupbit
```

## Quotation API
####  암호화폐 목록
업비트가 지원하는 모든 암호화폐 목록을 얻어온다.
```python
print(pyupbit.get_tickers())
```

리턴값은 다음과 같다. 
```
['KRW-BTC', 'KRW-DASH', 'KRW-ETH', 'BTC-NEO', 'BTC-ETH', 'BTC-LTC', 'BTC-STRAT', 'BTC-XRP', 'BTC-ETC', 'BTC-OMG', 'BTC-CVC', 'BTC-DGB', 'BTC-PAY', 'BTC-SC', 'BTC-SNT', 'BTC-DASH', 'BTC-XVG', 'BTC-WAVES', 'BTC-NMR', 'BTC-SYNX', 'BTC-PIVX', 'BTC-GBYTE', 'BTC-XEM', 'BTC-ZEC', 'BTC-XMR', 'BTC-LBC', 'BTC-QTUM', 'BTC-GNT', 'BTC-NXT', 'BTC-BAT', 'BTC-XEL', 'BTC-EDG', 'BTC-LSK', 'BTC-RDD', 'BTC-DCT', 'BTC-STEEM', 'BTC-GAME', 'BTC-FCT', 'BTC-PTOY', 'BTC-DCR', 'BTC-DOGE', 'BTC-BNT', 'BTC-XLM', 'BTC-PART', 'BTC-MCO', 'BTC-UBQ', 'BTC-ARDR', 'BTC-KMD', 'BTC-ARK', 'BTC-ADX', 'BTC-SYS', 'BTC-ANT', 'BTC-MUE', 'BTC-XDN', 'BTC-STORJ', 'BTC-QRL', 'BTC-NXS', 'BTC-GRS', 'BTC-VTC', 'BTC-CLOAK', 'BTC-SIB', 'BTC-REP', 'BTC-VIA', 'BTC-WINGS', 'BTC-CFI', 'BTC-UNB', 'BTC-NBT', 'BTC-SWT', 'BTC-SLS', 'BTC-MONA', 'BTC-AMP', 'BTC-HMQ', 'BTC-TX', 'BTC-RLC', 'BTC-BLOCK', 'BTC-DYN', 'BTC-GUP', 'BTC-MEME', 'BTC-OK', 'BTC-XZC', 'BTC-ADT', 'BTC-FTC', 'BTC-ION', 'BTC-BSD', 'BTC-GNO', 'BTC-EMC2', 'BTC-EXCL', 'BTC-SPHR', 'BTC-EXP', 'BTC-BITB', 'BTC-BAY', 'BTC-VRC', 'BTC-BURST', 'BTC-SHIFT', 'BTC-BLK', 'BTC-ZEN', 'BTC-KORE', 'BTC-RADS', 'ETH-NEO', 'ETH-LTC', 'ETH-STRAT', 'ETH-XRP', 'ETH-ETC', 'ETH-OMG', 'ETH-CVC', 'ETH-DGB', 'ETH-PAY', 'ETH-SC', 'ETH-SNT', 'ETH-DASH', 'ETH-WAVES', 'ETH-XEM', 'ETH-ZEC', 'ETH-XMR', 'ETH-QTUM', 'ETH-GNT', 'ETH-BAT', 'ETH-FCT', 'ETH-BNT', 'ETH-XLM', 'ETH-MCO', 'ETH-ADX', 'ETH-ANT', 'ETH-REP', 'ETH-CFI', 'ETH-RLC', 'ETH-GUP', 'ETH-ADT', 'ETH-GNO', 'USDT-BTC', 'USDT-NEO', 'USDT-ETH', 'USDT-LTC', 'USDT-XRP', 'USDT-ETC', 'USDT-DASH', 'USDT-ZEC', 'USDT-XMR', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-STRAT', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-PIVX', 'KRW-XEM', 'KRW-ZEC', 'KRW-XMR', 'KRW-QTUM', 'KRW-GNT', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-VTC', 'KRW-REP', 'KRW-EMC2', 'BTC-IOP', 'BTC-NAV', 'KRW-ADA', 'BTC-ADA', 'BTC-MANA', 'ETH-MANA', 'USDT-OMG', 'BTC-SALT', 'ETH-SALT', 'KRW-SBD', 'BTC-SBD', 'KRW-TIX', 'BTC-TIX', 'ETH-TIX', 'BTC-RCN', 'ETH-RCN', 'BTC-VIB', 'ETH-VIB', 'KRW-POWR', 'BTC-POWR', 'ETH-POWR', 'KRW-MER', 'BTC-MER', 'BTC-BTG', 'ETH-BTG', 'KRW-BTG', 'USDT-XVG', 'USDT-ADA', 'USDT-BTG', 'USDT-NXT', 'BTC-ENG', 'BTC-UKG', 'BTC-DNT', 'BTC-IGNIS', 'BTC-SRN', 'ETH-SRN', 'BTC-WAX', 'ETH-WAX', 'BTC-ZRX', 'ETH-ZRX', 'ETH-VEE', 'BTC-VEE', 'BTC-BCPT', 'ETH-BCPT', 'BTC-TRX', 'ETH-TRX', 'BTC-TUSD', 'BTC-LRC', 'ETH-LRC', 'BTC-RVR', 'ETH-TUSD', 'BTC-UP', 'ETH-UP', 'KRW-ICX', 'KRW-EOS', 'KRW-STORM', 'ETH-ADA', 'ETH-ENG', 'ETH-UKG', 'BTC-DMT', 'ETH-DMT', 'USDT-TUSD', 'BTC-LUN', 'ETH-LUN', 'KRW-TRX', 'BTC-POLY', 'ETH-POLY', 'BTC-EMC', 'KRW-MCO', 'BTC-PRO', 'ETH-PRO', 'USDT-SC', 'USDT-TRX', 'KRW-SC', 'KRW-GTO', 'KRW-IGNIS', 'KRW-ONT', 'KRW-DCR', 'KRW-ZIL', 'BTC-BLT', 'ETH-BLT', 'BTC-STORM', 'ETH-STORM', 'BTC-AID', 'ETH-AID', 'BTC-NGC', 'ETH-NGC', 'BTC-GTO', 'ETH-GTO', 'USDT-DCR', 'BTC-OCN', 'ETH-OCN', 'KRW-POLY', 'KRW-ZRX', 'BTC-TUBE', 'KRW-SRN', 'KRW-LOOM', 'BTC-CMCT', 'BTC-BCH', 'ETH-BCH', 'USDT-BCH', 'KRW-BCH', 'BTC-BKX', 'BTC-MFT', 'BTC-LOOM']
```

업비트가 지원하는 암호화폐 목록 중 특정 Fiat로 매매가 가능한 목록만 얻어올 수도 있다. 
```python
print(pyupbit.get_tickers(fiat="KRW"))
print(pyupbit.get_tickers(fiat="BTC"))
print(pyupbit.get_tickers(fiat="ETH"))
print(pyupbit.get_tickers(fiat="USDT"))
```

fiat="KRW"의 리턴값은 다음과 같다. 
```
['KRW-BTC', 'KRW-DASH', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', 'KRW-STRAT', 'KRW-XRP', 'KRW-ETC', 'KRW-OMG', 'KRW-SNT', 'KRW-WAVES', 'KRW-PIVX', 'KRW-XEM', 'KRW-ZEC', 'KRW-XMR', 'KRW-QTUM', 'KRW-GNT', 'KRW-LSK', 'KRW-STEEM', 'KRW-XLM', 'KRW-ARDR', 'KRW-KMD', 'KRW-ARK', 'KRW-STORJ', 'KRW-GRS', 'KRW-VTC', 'KRW-REP', 'KRW-EMC2', 'KRW-ADA', 'KRW-SBD', 'KRW-TIX', 'KRW-POWR', 'KRW-MER', 'KRW-BTG', 'KRW-ICX', 'KRW-EOS', 'KRW-STORM', 'KRW-TRX', 'KRW-MCO', 'KRW-SC', 'KRW-GTO', 'KRW-IGNIS', 'KRW-ONT', 'KRW-DCR', 'KRW-ZIL', 'KRW-POLY', 'KRW-ZRX', 'KRW-SRN', 'KRW-LOOM', 'KRW-BCH']
```


#### 최근 체결가격
특정 암호화폐에 대한 현재가를 얻어온다. 
```python
print(pyupbit.get_current_price("KRW-BTC"))
```

리턴값은 다음과 같다. 
```
8392000.0
```

리스트를 통해 여러 종목에 대해 한 번에 조회할 수 있다. 
```python
print(pyupbit.get_current_price(["KRW-BTC", "KRW-XRP"]))
```

여러 종목에 대해 동시 조회한 경우 딕셔너리 객체로 리턴한다. 

```
{'KRW-BTC': 8300000.0, 'KRW-XRP': 511.0}
```


#### 차트 데이터
```python
print(pyupbit.get_ohlcv("KRW-BTC", interval="day", count=5))    # 일봉 데이터 (5일)
print(pyupbit.get_ohlcv("KRW-BTC", interval="minute1"))         # 분봉 데이터
print(pyupbit.get_ohlcv("KRW-BTC", interval="week"))            # 주봉 데이터 
```

리턴값은 Pandas DataFrame 객체이다. 
```
                          open       high     ...           close       volume
2018-07-16 09:00:00  7179000.0  7468000.0     ...       7454000.0  6215.793339
2018-07-17 09:00:00  7454000.0  8140000.0     ...       8080000.0  8866.816695
2018-07-18 09:00:00  8080000.0  8450000.0     ...       8302000.0  9226.449696
2018-07-19 09:00:00  8292000.0  8512000.0     ...       8443000.0  6091.929945
2018-07-20 09:00:00  8443000.0  8671000.0     ...       8389000.0  6985.379832
```

#### 매수/매도 호가
```python
print(pyupbit.get_orderbook(tickers="KRW-BTC")
print(pyupbit.get_orderbook(tickers=["KRW-BTC", "KRW-XRP"]))
```  

리턴값은 다음과 같다. 
```
[{'market': 'KRW-BTC', 'timestamp': 1532118943687, 'total_ask_size': 17.08116346, 'total_bid_size': 3.07150192, 'orderbook_units': [{'ask_price': 8390000.0, 'bid_price': 8389000.0, 'ask_size': 3.16057415, 'bid_size': 0.5515136}, {'ask_price': 8392000.0, 'bid_price': 8387000.0, 'ask_size': 0.71247596, 'bid_size': 0.95157819}, {'ask_price': 8393000.0, 'bid_price': 8386000.0, 'ask_size': 3.70536818, 'bid_size': 0.15824907}, {'ask_price': 8398000.0, 'bid_price': 8385000.0, 'ask_size': 0.00481809, 'bid_size': 0.00119147}, {'ask_price': 8399000.0, 'bid_price': 8383000.0, 'ask_size': 1.1228337, 'bid_size': 0.05}, {'ask_price': 8400000.0, 'bid_price': 8380000.0, 'ask_size': 0.48354827, 'bid_size': 0.00613734}, {'ask_price': 8401000.0, 'bid_price': 8375000.0, 'ask_size': 0.00433629, 'bid_size': 0.05}, {'ask_price': 8402000.0, 'bid_price': 8374000.0, 'ask_size': 2.7434153, 'bid_size': 0.32104953}, {'ask_price': 8420000.0, 'bid_price': 8373000.0, 'ask_size': 0.0028, 'bid_size': 0.5010063}, {'ask_price': 8428000.0, 'bid_price': 8370000.0, 'ask_size': 5.14099352, 'bid_size': 0.48077642}]}]
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

튜플 객체를 리턴하는데 0번에는 잔고 데이터 (파이썬 리스트)가 1번에는 호출 제한 데이터 (파이썬 딕셔너리)가 있다. 
```
([{'currency': 'KRW', 'balance': '10134.93', 'locked': '0.0', 'avg_krw_buy_price': '0', 'modified': False}, {'currency': 'XRP', 'balance': '20.0', 'locked': '0.0', 'avg_krw_buy_price': '508.66', 'modified': False}], {'group': 'default', 'min': 1799, 'sec': 29})
```

#### 원화/코인 잔고 조회
특정 코인이나 원화의 잔고만 조회한다. 
```python
print(upbit.get_balance(ticker="KRW"))
print(upbit.get_balance(ticker="KRW-BTC"))
print(upbit.get_balance(ticker="KRW-XRP"))
```

#### 지정가 매수/매도 주문
리플을 507원에 20개 매수한다. 
리플을 500원에 20개 매도한다. 

```python
# 매도
print(upbit.sell_limit_order("KRW-XRP", 507, 20))
```

튜플 객체를 리턴하는데 0번에는 주문 정보 (파이썬 딕셔너리)가 1번에는 호출 제한 데이터 (파이썬 딕셔너리)가 있다.

```
({'uuid': '1ab8ac28-e880-4a04-b868-a82d755b0945', 'side': 'ask', 'ord_type': 'limit', 'price': '1000.0', 'avg_price': '0.0', 'state': 'wait', 'market': 'KRW-XRP', 'created_at': '2018-07-21T05:38:48+09:00', 'volume': '20.0', 'remaining_volume': '20.0', 'reserved_fee': '0.0', 'remaining_fee': '0.0', 'paid_fee': '0.0', 'locked': '20.0', 'executed_volume': '0.0', 'trades_count': 0}, {'group': 'order', 'min': 79, 'sec': 6})
```

```python
# 매수
print(upbit.buy_limit_order("KRW-XRP", 500, 20))
```

튜플 객체를 리턴하는데 0번에는 주문 정보 (파이썬 딕셔너리)가 1번에는 호출 제한 데이터 (파이썬 딕셔너리)가 있다.
```
({'uuid': '82e211da-21f6-4355-9d76-83e7248e2c0c', 'side': 'bid', 'ord_type': 'limit', 'price': '200.0', 'avg_price': '0.0', 'state': 'wait', 'market': 'KRW-XRP', 'created_at': '2018-07-21T05:39:40+09:00', 'volume': '20.0', 'remaining_volume': '20.0', 'reserved_fee': '2.0', 'remaining_fee': '2.0', 'paid_fee': '0.0', 'locked': '4002.0', 'executed_volume': '0.0', 'trades_count': 0}, {'group': 'order', 'min': 78, 'sec': 6})
```

#### 시장가 매수/매도 주문 
업비트 API는 공식으로 시장가 주문 API를 제공하지 않습니다. pyupbit에서는 호가를 조회한 후 시장가처럼 주문이 되는 API를 제공합니다. 

```python
# 시장가 매수
print(upbit.buy_market_order("KRW-XRP", 10000))     # 10,000원 어치 리플 시장가 매수 

# 시장가 매도
print(upbit.sell_market_order("KRW-XRP", 30))       # 리플 30개 시장가 매도  
```
 
#### 매수/매도 주문 취소
주문 함수의 리턴 값 중 uuid 값을 사용해서 주문을 취소할 수 있다. 

```python
print(upbit.cancel_order('e57a3bc0-0b0b-4540-96f2-f35f19c51e8d'))
```

튜플 객체를 리턴하는데 0번에는 주문 취소 정보 (파이썬 딕셔너리)가 1번에는 호출 제한 데이터 (파이썬 딕셔너리)가 있다.
```
({'uuid': '82e211da-21f6-4355-9d76-83e7248e2c0c', 'side': 'bid', 'ord_type': 'limit', 'price': '200.0', 'avg_price': '0.0', 'state': 'wait', 'market': 'KRW-XRP', 'created_at': '2018-07-21T05:39:40+09:00', 'volume': '20.0', 'remaining_volume': '20.0', 'reserved_fee': '2.0', 'remaining_fee': '2.0', 'paid_fee': '0.0', 'locked': '4002.0', 'executed_volume': '0.0', 'trades_count': 0}, {'group': 'default', 'min': 1799, 'sec': 29})
```
