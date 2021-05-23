QUOTATION API
======================
 
API 신청 없이 시세 및 오더북 등을 조회할 수 있는 API입니다.

* Websocket은 초당 5회, 분당 100회 연결 요청할 수 있습니다.

* 종목, 캔들, 체결, 티커, 호가 API는 분당 600회, 초당 10회 사용 가능합니다.

시세 종목 조회
----------------------
마켓 코드 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

    # 시세 종목 조회
    import pyupbit

    # 업비트의 모든 티커목록 조회
    tickers = pyupbit.get_tickers()
    print(tickers)
    print(len(tickers))

    # 원화 시장의 티커목록 조회
    krw_tickers = pyupbit.get_tickers("KRW")
    print(krw_tickers)
    print(len(krw_tickers))

    # BTC 시장의 티커목록 조회
    btc_tickers = pyupbit.get_tickers("BTC")
    print(btc_tickers)
    print(len(btc_tickers))

    # USDT 시장의 티코목록 조회
    usdt_tickers = pyupbit.get_tickers("USDT")
    print(usdt_tickers)
    print(len(usdt_tickers))


시세 캔들 조회
----------------------

분(Minute), 일(Day), 주(Week), 월(Month) 단위로 시세 캔들을 조회합니다.


분봉(Minute) 조회
~~~~~~~~~~~~~~~~~~~~~~

분봉을 얻어올 수 있습니다. 기본적으로 한 번 조회시 200개를 분봉을 얻어옵니다. 

..  code-block:: python

    # 분봉
    # 1, 3, 5, 10, 15, 30, 60, 240분봉에 대해서 최대 200개 조회 가능
    import pyupbit

    # 1분봉 (최대 200개 요청가능)
    minute1 = pyupbit.get_ohlcv("KRW-BTC", "minute1")
    print(minute1)
    print(type(minute1), minute1.shape)

    # 3분봉 (최대 200개 요청가능)
    minute3 = pyupbit.get_ohlcv("KRW-BTC", "minute3")
    print(minute3)

    # 5분봉 (최대 200개 요청가능)
    minute5 = pyupbit.get_ohlcv("KRW-BTC", "minute5")
    print(minute5)

    # 10분봉 (최대 200개 요청가능)
    minute10 = pyupbit.get_ohlcv("KRW-BTC", "minute10")
    print(minute10)

    # 30분봉 (최대 200개 요청가능)
    minute30 = pyupbit.get_ohlcv("KRW-BTC", "minute30")
    print(minute30)

    # 60분봉 (최대 200개 요청가능)
    minute60 = pyupbit.get_ohlcv("KRW-BTC", "minute60")
    print(minute60)


일봉(Day) 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

    # 일봉
    import pyupbit

    # 기본 요청시 200일 (최대)
    df = pyupbit.get_ohlcv("KRW-BTC", "day")
    print(df)

    # 200개 미만의 경우 count 인자에 설정 가능
    df = pyupbit.get_ohlcv("KRW-BTC", "day", count=10)
    print(df)


주봉(Week) 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

    # 주봉
    import pyupbit

    # 기본 요청시 200개
    df = pyupbit.get_ohlcv("KRW-BTC", "week")
    print(df)



월봉(Month) 조회 
~~~~~~~~~~~~~~~~~~~~~~
..  code-block:: python

    import pyupbit

    df = pyupbit.get_ohlcv("KRW-BTC", "month")
    print(df)


시세 체결 조회
----------------------

시세 티커 조회
----------------------

시세 오더북 조회
----------------------
