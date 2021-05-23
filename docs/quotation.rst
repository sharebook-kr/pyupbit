QUOTATION API
======================
 
API 신청 없이 시세 및 오더북 등을 조회할 수 있는 API입니다.

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

시세 체결 조회
----------------------

시세 티커 조회
----------------------

시세 오더북 조회
----------------------
