# pyupbit
Python Wrapper for Upbit API

## Documentation

https://pyupbit.readthedocs.io/en/latest/


## Installation
파이썬 개발 환경으로 최신 버전의 Anaconda를 설치하세요. (Python3 버전용)

```sh
pip install pyupbit
```

pyjwt 모듈을 필요로 합니다. (pyjwt >= 2.0)

```sh
pip install pyjwt
```

## Import
```python
import pyupbit
```

## Quotation API
- Websocket은 초당 5회, 분당 100회 연결 요청할 수 있습니다.
- 종목, 캔들, 체결, 티커, 호가 API는 분당 600회, 초당 10회 사용 가능합니다.

####  암호화폐 목록
`get_tickers` 함수는 업비트가 지원하는 모든 암호화폐 목록을 얻어옵니다.
```python
print(pyupbit.get_tickers())
```
```
['KRW-BTC', 'KRW-DASH', 'KRW-ETH', 'BTC-NEO', 'BTC-ETH', 'BTC-LTC', ... ]
```

업비트가 지원하는 암호화폐 목록 중 특정 시장(`fiat`)에 매매가 가능한 목록만 얻어올 수 있습니다. `KRW`/`BTC`/`USDT` 시장을 조회할 수 있습니다.
```python
print(pyupbit.get_tickers(fiat="KRW"))
```
```
['KRW-BTC', 'KRW-DASH', 'KRW-ETH', 'KRW-NEO', 'KRW-MTL', 'KRW-LTC', ...]
```


#### 최근 체결가격
`get_current_price` 함수는 암호화폐의 현재가를 얻어옵니다. 함수로 티커를 넣어줘야 합니다.
```python
print(pyupbit.get_current_price("KRW-BTC"))
```

`float` 타입의 현재가가 반환됩니다.
```
8392000.0
```

리스트에 여러 개의 티커를 입력해 한 번에 현재가를 조회할 수 있습니다.
```python
print(pyupbit.get_current_price(["KRW-BTC", "KRW-XRP"]))
```

여러 종목을 조회한 경우 딕셔너리로 현재가를 리턴합니다.

```
{'KRW-BTC': 8300000.0, 'KRW-XRP': 511.0}
```

`get_current_price` 함수는 최대 100개의 암호화폐를 조회할 수 있습니다. 100개 이상일 경우 분할해서 반복 조회해야 합니다.

#### 차트 데이터
`get_ohlcv` 함수는 고가/시가/저가/종가/거래량을 DataFrame으로 반환합니다.

```python
df = pyupbit.get_ohlcv("KRW-BTC")
print(df.tail())
```

날짜가 오름차순으로 정렬돼 최근 날짜가 마지막에 위치합니다.
```
2021-03-21 09:00:00  67849000.0  68715000.0  65451000.0  67120000.0   8097.428878
2021-03-22 09:00:00  67064000.0  68380000.0  64345000.0  64725000.0   8366.410551
2021-03-23 09:00:00  64728000.0  66279000.0  63000000.0  65458000.0   9961.040596
2021-03-24 09:00:00  65458000.0  68370000.0  64500000.0  64777000.0  11366.404524
2021-03-25 09:00:00  64777000.0  65305000.0  63319000.0  64257000.0   2770.703203
```

`count` 파라미터는 조회 갯수를 지정합니다. 최근 영업일 부터 이전 `count`만큼의 이전 영업일까지 조회합니다. `count` 파라미터를 입력하지 않을 경우 default value는 200입니다.

```python
df = pyupbit.get_ohlcv("KRW-BTC", count=5)
print(len(df))
```
위 코드는 최근 영업일 부터 과거 5개의 데이터가 조회됩니다.
```
5
```

`get_ohlcv` 함수는 웹 서버로 200개씩 데이터를 요청합니다. 200개 이상의 데이터를 요청한다면 0.1(default) 주기로 데이터를 수집합니다. 다른 API와 함께 사용한다면 조회 주기(`period`)를 늘려야 합니다. 이 때 `period` 옵션을 사용해서 주기를 초(second) 단위로 지정할 수 있습니다. 조회하는 데이터의 갯수가 200개 이하라면 period 옵션은 무시됩니다.

```python
df = pyupbit.get_ohlcv("KRW-BTC", count=600, period=1)
```

`interval` 파라미터는 조회단위를 지정합니다. 파라미터에는 다음 값을 지정할 수 있습니다.
- `day`/`minute1`/`minute3`/`minute5`/`minute10`/`minute15`/`minute30`/`minute60`/`minute240`/`week`/`month`


```python
print(pyupbit.get_ohlcv("KRW-BTC", interval="day")              # 일봉 데이터 (5일)
print(pyupbit.get_ohlcv("KRW-BTC", interval="minute1"))         # 분봉 데이터
print(pyupbit.get_ohlcv("KRW-BTC", interval="week"))            # 주봉 데이터
```

`to` 파라미터에 입력된 이전 단위(`interval`)까지의 데이터를 데이터프레임으로 얻을 수 있습니다. 예를 들어, 다음 코드는 `2020-10-10`일 보다 하루 전인 `2020-10-09`을 까지의 200개 데이터를 조회합니다. 단위를 설정하지 않았으니 단위는 일봉입니다.

```python
print(pyupbit.get_ohlcv("KRW-BTC", to="20201010"))
```

`interval`을 `minute1`로 지정한 경우 `2020-10-10` 보다 1분 이전 (`2020-10-09 23:59:00`)까지의 200개 데이터를 반환합니다.
```python
print(pyupbit.get_ohlcv("KRW-BTC", interval="minute1", to="20201010"))
```

----

기준 시간 단위로 shift된 일봉을 계산할 수도 있습니다.

예) 2019-06-01 12:00:00 ~ 2019-06-02 11:59:59
```python
print(pyupbit.get_daily_ohlcv_from_base("KRW-BTC", base=12))
```

예) 2019-06-01 13:00:00 ~ 2019-06-02 12:59:59
```python
print(pyupbit.get_daily_ohlcv_from_base("KRW-BTC", base=13))
```

#### 매수/매도 호가
`get_orderbook` 함수는 매수/매도 호가 정보를 조회합니다.
```python
print(pyupbit.get_orderbook(ticker="KRW-BTC"))
```

리스트 안에 딕셔너리로 호가정보가 들어있습니다.
- market : 암호화폐 티커
- timestamp : 조회시간 (단위 ms)
- orderbook_units : 매도호가/매수호가 정보
```
[{'market': 'KRW-BTC', 'timestamp': 1532118943687, 'total_ask_size': 17.08116346, 'total_bid_size': 3.07150192, 'orderbook_units': [{'ask_price': 8390000.0, 'bid_price': 8389000.0, 'ask_size': 3.16057415, 'bid_size': 0.5515136}, {'ask_price': 8392000.0, 'bid_price': 8387000.0, 'ask_size': 0.71247596, 'bid_size': 0.95157819}, {'ask_price': 8393000.0, 'bid_price': 8386000.0, 'ask_size': 3.70536818, 'bid_size': 0.15824907}, {'ask_price': 8398000.0, 'bid_price': 8385000.0, 'ask_size': 0.00481809, 'bid_size': 0.00119147}, {'ask_price': 8399000.0, 'bid_price': 8383000.0, 'ask_size': 1.1228337, 'bid_size': 0.05}, {'ask_price': 8400000.0, 'bid_price': 8380000.0, 'ask_size': 0.48354827, 'bid_size': 0.00613734}, {'ask_price': 8401000.0, 'bid_price': 8375000.0, 'ask_size': 0.00433629, 'bid_size': 0.05}, {'ask_price': 8402000.0, 'bid_price': 8374000.0, 'ask_size': 2.7434153, 'bid_size': 0.32104953}, {'ask_price': 8420000.0, 'bid_price': 8373000.0, 'ask_size': 0.0028, 'bid_size': 0.5010063}, {'ask_price': 8428000.0, 'bid_price': 8370000.0, 'ask_size': 5.14099352, 'bid_size': 0.48077642}]}]
```

`ticker` 파라미터에 리스트로 티커를 넣으면, 한 번에 여러 종목의 호가를 조회할 수 있습니다.
```python
print(pyupbit.get_orderbook(ticker=["KRW-BTC", "KRW-XRP"]))
```


## Exchange API
주문은 초당 8회, 분당 200회 / 주문 외 요청은 초당 30회, 분당 900회 사용 가능합니다.

#### 로그인
Access Key와 Sercret Key를 사용해서 `Upbit` 객체를 생성합니다. 이는 웹페이지에서 로그인하는 것과 같습니다.

```python
import pyupbit

access = "73kVqowGQOGEjdR31221j31j2ifekjkgjekgjekg"          # 본인 값으로 변경
secret = "egjekgj3iekeEEkej3i3j3iejjwiEejiejeEeijg"          # 본인 값으로 변경
upbit = pyupbit.Upbit(access, secret)
```

#### 잔고 조회
`get_balance` 메서드는 입력받은 티커의 보유 수량 정보를 조회합니다.

```python
print(upbit.get_balance("KRW-XRP"))     # KRW-XRP 조회
print(upbit.get_balance("KRW"))         # 보유 현금 조회
```

`get_balances` 메서드는 보유 중인 모든 암호화폐의 잔고 및 단가 정보를 딕셔너리로 조회합니다.
```python
print(upbit.get_balances())
```

```
[{'currency': 'KRW',
  'balance': '0.34689181',
  'locked': '0.0',
  'avg_buy_price': '0',
  'avg_buy_price_modified': True,
  'unit_currency': 'KRW'},
 {'currency': 'BTC',
  'balance': '0.00174304',
  'locked': '0.0',
  'avg_buy_price': '64387000',
  'avg_buy_price_modified': False,
  'unit_currency': 'KRW'},]
```

#### 지정가 매수/매도 주문
지정한 가격에 주문을 요청합니다. 다음은 원화 시장에 리플을 600원에 20개 매도 합니다.

```python
# 매도
print(upbit.sell_limit_order("KRW-XRP", 600, 20))
```

주문 정보가 딕셔너리로 반환됩니다. uuid는 주문에 대한 고윳값으로 이를 사용해 추후 주문을 취소하거나 정정할 수 있습니다.

```
{'uuid': '0bcf0916-a7f5-49ed-80a9-a45e9e190cd3',
 'side': 'ask',
 'ord_type': 'limit',
 'price': '600.0',
 'state': 'wait',
 'market': 'KRW-XRP',
 'created_at': '2021-03-21T15:24:11+09:00',
 'volume': '20.0',
 'remaining_volume': '20.0',
 'reserved_fee': '0.0',
 'remaining_fee': '0.0',
 'paid_fee': '0.0',
 'locked': '20.0',
 'executed_volume': '0.0',
 'trades_count': 0}
```

다음은 원화 시장에 리플을 613원에 10개 매수 합니다.

```python
# 매수
print(upbit.buy_limit_order("KRW-XRP", 613, 10))
```

```
{'uuid': '1907dcdc-2b96-4d85-9963-866f7aa220cd',
 'side': 'bid',
 'ord_type': 'limit',
 'price': '613.0',
 'state': 'wait',
 'market': 'KRW-XRP',
 'created_at': '2021-03-21T15:10:32+09:00',
 'volume': '10.0',
 'remaining_volume': '10.0',
 'reserved_fee': '3.065',
 'remaining_fee': '3.065',
 'paid_fee': '0.0',
 'locked': '6133.065',
 'executed_volume': '0.0',
 'trades_count': 0}
```

#### 시장가 매수/매도 주문
시장가 매수는 최우선 매도호가에 즉시 매수합니다. `buy_market_order` 메서드로 티커와 매수 금액만을 입력합니다. 매수 금액은 수수료를 제외한 금액입니다. 다음 예제에서 주문한 10000원은 수수료가 제외된 금액입니다. 수수료가 0.05%라면 수수료를 포함한 10005원의 현금을 보유하고 있어야 합니다.

```python
print(upbit.buy_market_order("KRW-XRP", 10000))
```

다음은 리플 30개를 시장가 매도합니다. 매도대금이 총 10000원이라면 수수료를 제외한 금액이 입금됩니다. 만약 수수료가 0.05%라면 9995원 받을 수 있습니다.
```python
print(upbit.sell_market_order("KRW-XRP", 30))
```

#### 미체결 주문 조회

`get_order` 메서드는 입력된 암호화폐의 미체결 주문을 조회합니다.

```python
upbit.get_order("KRW-LTC")
```

미체결 주문이 있다면 리스트로 상세 내역을 반환합니다. 다음은 250000원에 매도(ask) 주문한 LTC이 1개(volume)있다는 의미입니다.
```
[{'uuid': '50e184b3-9b4f-4bb0-9c03-30318e3ff10a',
  'side': 'ask',
  'ord_type': 'limit',
  'price': '250000.0',
  'state': 'wait',
  'market': 'KRW-LTC',
  'created_at': '2021-03-25T14:10:53+09:00',
  'volume': '1.0',
  'remaining_volume': '1.0',
  'reserved_fee': '0.0',
  'remaining_fee': '0.0',
  'paid_fee': '0.0',
  'locked': '1.0',
  'executed_volume': '0.0',
  'trades_count': 0}]
```

`state` 파라미터를 사용하면 완료된 주문들을 조회할 수 있습니다.

```python
print(upbit.get_order("KRW-LTC", state="done"))
```
```
[{'uuid': '0694def7-5ada-405f-b0f3-053801d5b190',
  'side': 'ask',
  'ord_type': 'market',
  'price': None,
  'state': 'done',
  'market': 'KRW-LTC',
  'created_at': '2021-03-21T14:43:40+09:00',
  'volume': '0.07336815',
  'remaining_volume': '0.0',
  'reserved_fee': '0.0',
  'remaining_fee': '0.0',
  'paid_fee': '8.39331636',
  'locked': '0.0',
  'executed_volume': '0.07336815',
  'trades_count': 1},
 {'uuid': '48d6d451-3db5-4357-9d5a-bfb8f417c943',
  'side': 'ask',
  'ord_type': 'limit',
  'price': '230000.0',
  'state': 'done',
  'market': 'KRW-LTC',
  'created_at': '2021-03-17T01:06:55+09:00',
  'volume': '0.5',
  'remaining_volume': '0.0',
  'reserved_fee': '0.0',
  'remaining_fee': '0.0',
  'paid_fee': '58.775',
  'locked': '0.0',
  'executed_volume': '0.5',
  'trades_count': 2}]
```

`uuid`를 사용해서 특정 주문을 상세 조회할 수 있습니다. `uuid`를 사용하면 다른 파라미터는 무시됩니다.
```python
order = upbit.get_order('50e184b3-9b4f-4bb0-9c03-30318e3ff10a')
print(order)
```

결과를 참고하면 지정가 매도를 실행했으며 주문은 취소(`cancel`) 됐음을 알 수 있습니다
```
{'uuid': '50e184b3-9b4f-4bb0-9c03-30318e3ff10a', 'side': 'ask', 'ord_type': 'limit', 'price': '250000.0', 'state': 'cancel', 'market': 'KRW-LTC', 'created_at': '2021-03-25T14:10:53+09:00', 'volume': '1.0', 'remaining_volume': '1.0', 'reserved_fee': '0.0', 'remaining_fee': '0.0', 'paid_fee': '0.0', 'locked': '1.0', 'executed_volume': '0.0', 'trades_count': 0, 'trades': []}
```

#### 매수/매도 주문 취소
주문 함수의 리턴 값 중 uuid 값을 사용해서 주문을 취소할 수 있습니다.

```python
print(upbit.cancel_order('50e184b3-9b4f-4bb0-9c03-30318e3ff10a'))
```

정상 처리됐다면 다음과 같이 딕셔너리가 반환됩니다.
```
{'uuid': '50e184b3-9b4f-4bb0-9c03-30318e3ff10a', 'side': 'ask', 'ord_type': 'limit', 'price': '250000.0', 'state': 'wait', 'market': 'KRW-LTC', 'created_at': '2021-03-25T14:10:53+09:00', 'volume': '1.0', 'remaining_volume': '1.0', 'reserved_fee': '0.0', 'remaining_fee': '0.0', 'paid_fee': '0.0', 'locked': '1.0', 'executed_volume': '0.0', 'trades_count': 0}
```

#### 웹소켓

WebSocket을 이용해서 `현재가`, `호가`, `체결`에 대한 정보를 수신합니다.
- 첫 번째 파라미터에는 수신정보를 입력하며 `ticker`, `orderbook`, `transaction`을 사용할 수 있습니다.
- 두 번째 파라미터는 구독할 필터를 설정하며 암호화폐의 티커를 입력합니다. 현재 버전에서는 원화 시장만을 지원합니다.

```python
from pyupbit import WebSocketManager

if __name__ == "__main__":
    wm = WebSocketManager("ticker", ["KRW-BTC"])
    for i in range(10):
        data = wm.get()
        print(data)
    wm.terminate()
```
주의: 웹소켓의 multiprocessing을 위해 `__name__` guard를 반드시 써줘야 합니다.

PyQt5와 함께 웹소켓을 사용하는 예제는 다음 코드를 참고하세요.
- 버튼을 클릭하면 웹소켓에서 가격정보를 가져와서 화면에 출력합니다.
- https://gist.github.com/mr-yoo/a3d1f8a4152f94cf61e4bc566659cd20


WebSocketClient 클래스는 외부에서 프로세스 생성 및 큐를 전달하는 구조에서 사용합니다. WebSocketManager와 달리 사용자가 프로세스를 생성하고 사용할 큐를 입력해줘야 합니다. 

```
import multiprocessing as mp
import pyupbit


if __name__ == "__main__":
    queue = mp.Queue()
    proc = mp.Process(
        target=pyupbit.WebSocketClient,
        args=('ticker', ["KRW-BTC"], queue),
        daemon=True
    )
    proc.start()

    while True:
        data = queue.get()
        print(data)
```
