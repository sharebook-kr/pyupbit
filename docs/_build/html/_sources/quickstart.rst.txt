Quickstart
======================
 
업비트 거래소 API를 이용한 파이썬 라이브러리입니다. 

Install 
----------------------

..  code::

    pip install pyupbit 


현재가 
----------------------
..  code-block:: python

    import pyupbit 

    price = pyupbit.get_current_price("KRW-BTC")
    print(price)


티커조회
----------------------
..  code-block:: python

    import pyupbit 

    tickers = pyupbit.get_tickers()
    print(tickers)
    print(type(tickers))



