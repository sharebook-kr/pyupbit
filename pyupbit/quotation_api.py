# -*- coding: utf-8 -*-

"""
pyupbit.quotation_api

This module provides quatation api of the Upbit API.
"""

import datetime
import pandas as pd
import time
from pyupbit.request_api import _call_public_api


def get_tickers(fiat="", is_details=False, limit_info=False, verbose=False):
    """업비트 티커 조회

    Args:
        fiat (str, optional): Fiat (KRW, BTC, USDT). Defaults to empty string.
        limit_info (bool, optional): True: 요청 수 제한 정보 리턴, False: 요청 수 제한 정보 리턴 받지 않음. Defaults to False.

    Returns:
        tuple/list: limit_info가 True이면 튜플, False이면 리스트 객체
    """
    url = "https://api.upbit.com/v1/market/all"
    detail = "true" if is_details else "false"
    markets, req_limit_info = _call_public_api(url, isDetails=detail)

    if verbose:
        tickers = [x for x in markets if x['market'].startswith(fiat)]
    else:
        tickers = [x['market'] for x in markets if x['market'].startswith(fiat)]

    if limit_info:
        return tickers, req_limit_info
    else:
        return tickers


def get_url_ohlcv(interval):
    """ohlcv 요청을 위한 url을 리턴하는 함수

    Args:
        interval (str): "day", "minute1", "minute3", "minute5", "week", "month"

    Returns:
        str: upbit api url
    """

    if interval in ["day", "days"]:
        url = "https://api.upbit.com/v1/candles/days"
    elif interval in ["minute1", "minutes1"]:
        url = "https://api.upbit.com/v1/candles/minutes/1"
    elif interval in ["minute3", "minutes3"]:
        url = "https://api.upbit.com/v1/candles/minutes/3"
    elif interval in ["minute5", "minutes5"]:
        url = "https://api.upbit.com/v1/candles/minutes/5"
    elif interval in ["minute10", "minutes10"]:
        url = "https://api.upbit.com/v1/candles/minutes/10"
    elif interval in ["minute15", "minutes15"]:
        url = "https://api.upbit.com/v1/candles/minutes/15"
    elif interval in ["minute30", "minutes30"]:
        url = "https://api.upbit.com/v1/candles/minutes/30"
    elif interval in ["minute60", "minutes60"]:
        url = "https://api.upbit.com/v1/candles/minutes/60"
    elif interval in ["minute240", "minutes240"]:
        url = "https://api.upbit.com/v1/candles/minutes/240"
    elif interval in ["week",  "weeks"]:
        url = "https://api.upbit.com/v1/candles/weeks"
    elif interval in ["month", "months"]:
        url = "https://api.upbit.com/v1/candles/months"
    else:
        url = "https://api.upbit.com/v1/candles/days"

    return url


def get_ohlcv(ticker="KRW-BTC", interval="day", count=200, to=None, period=0.1):
    MAX_CALL_COUNT = 200
    try:
        url = get_url_ohlcv(interval=interval)

        if to == None:
            to = datetime.datetime.now()
        elif isinstance(to, str):
            to = pd.to_datetime(to).to_pydatetime()
        elif isinstance(to, pd._libs.tslibs.timestamps.Timestamp):
            to = to.to_pydatetime()

        to = to.astimezone(datetime.timezone.utc)

        dfs = []
        count = max(count, 1)
        for pos in range(count, 0, -200):
            query_count = min(MAX_CALL_COUNT, pos)

            to = to.strftime("%Y-%m-%d %H:%M:%S")

            contents, req_limit_info = _call_public_api(url, market=ticker, count=query_count, to=to)
            dt_list = [datetime.datetime.strptime(x['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S") for x in contents]
            df = pd.DataFrame(contents,
                              columns=[
                                  'opening_price',
                                  'high_price',
                                  'low_price',
                                  'trade_price',
                                  'candle_acc_trade_volume',
                                  'candle_acc_trade_price'],
                              index=dt_list)
            df = df.sort_index()
            if df.shape[0] == 0:
                break
            dfs += [df]

            to = datetime.datetime.strptime(contents[-1]['candle_date_time_utc'], "%Y-%m-%dT%H:%M:%S")

            if pos > 200:
                time.sleep(period)

        df = pd.concat(dfs).sort_index()
        df = df.rename(columns={"opening_price": "open",
                                "high_price": "high",
                                "low_price": "low",
                                "trade_price": "close",
                                "candle_acc_trade_volume": "volume",
                                "candle_acc_trade_price": "value"})
        return df
    except Exception as x:
        return None


def get_ohlcv_from(ticker="KRW-BTC", interval="day", fromDatetime=None, to=None, period=0.1):
    MAX_CALL_COUNT = 200
    try:
        url = get_url_ohlcv(interval=interval)

        if fromDatetime is None:
            fromDatetime = datetime.datetime(2000, 1, 1, 0 ,0, 0)
        elif isinstance(fromDatetime, str):
            fromDatetime = pd.to_datetime(fromDatetime).to_pydatetime()
        elif isinstance(fromDatetime, pd._libs.tslibs.timestamps.Timestamp):
            fromDatetime = fromDatetime.to_pydatetime()
        fromDatetime = fromDatetime.astimezone(datetime.timezone.utc)

        if to == None:
            to = datetime.datetime.now()
        elif isinstance(to, str):
            to = pd.to_datetime(to).to_pydatetime()
        elif isinstance(to, pd._libs.tslibs.timestamps.Timestamp):
            to = to.to_pydatetime()
        to = to.astimezone(datetime.timezone.utc)

        dfs = []
        while to > fromDatetime:
            query_count = MAX_CALL_COUNT

            to = to.strftime("%Y-%m-%d %H:%M:%S")

            contents, req_limit_info = _call_public_api(url, market=ticker, count=query_count, to=to)
            dt_list = [datetime.datetime.strptime(x['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S").astimezone() for x in contents]
            # set timezone for time comparison
            # timezone will be removed before DataFrame returned

            df = pd.DataFrame(contents,
                              columns=[
                                  'opening_price',
                                  'high_price',
                                  'low_price',
                                  'trade_price',
                                  'candle_acc_trade_volume',
                                  'candle_acc_trade_price'],
                              index=dt_list)
            df = df.sort_index()
            if df.shape[0] == 0:
                break
            dfs += [df]

            to = datetime.datetime.strptime(contents[-1]['candle_date_time_utc'], "%Y-%m-%dT%H:%M:%S")
            to = to.replace(tzinfo=datetime.timezone.utc)
            # to compare fromTs and to, set tzinfo

            if to > fromDatetime:
                time.sleep(period)

        df = pd.concat(dfs).sort_index()
        df = df[ df.index >= fromDatetime ]
        df.index = df.index.tz_localize(None)
        df = df.rename(columns={"opening_price": "open",
                                "high_price": "high",
                                "low_price": "low",
                                "trade_price": "close",
                                "candle_acc_trade_volume": "volume",
                                "candle_acc_trade_price": "value"})
        return df
    except Exception as x:
        return None


def get_daily_ohlcv_from_base(ticker="KRW-BTC", base=0):
    """

    :param ticker:
    :param base:
    :return:
    """
    try:
        df = get_ohlcv(ticker, interval="minute60")
        df = df.resample('24H', base=base).agg(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
        return df
    except Exception as x:
        return None


def get_current_price(ticker="KRW-BTC", limit_info=False, verbose=False):
    """현재가 정보 조회

    Args:
        ticker (str/list, optional): 단일 티커 또는 티커 리스트 Defaults to "KRW-BTC".
        limit_info (bool, optional): True: 요청 제한 정보 리턴. Defaults to False.
        verbose (bool, optional): True: 원본 API 파라미터 리턴. Defaults to False.

    Returns:
        [type]: [description]
    """
    url = "https://api.upbit.com/v1/ticker"
    data, req_limit_info = _call_public_api(url, markets=ticker)

    if isinstance(ticker, str) or (isinstance(ticker, list) and len(ticker)==1):
        # 단일 티커
        if verbose is False:
            price = data[0]['trade_price']
        else:
            price = data[0]
    else:
        # 여러 티커로 조회한 경우
        if verbose is False:
            price = {x['market']: x['trade_price'] for x in data}
        else:
            price = data

    if limit_info:
        return price, req_limit_info
    else:
        return price


def get_orderbook(ticker="KRW-BTC", limit_info=False):
    """호가 정보 조회

    Args:
        ticker (str/list, optional): 티커 또는 티커 리스트. Defaults to "KRW-BTC".
        limit_info (bool, optional): True: 요청 수 제한 정보 리턴, False: 요청 수 제한 정보 리턴 받지 않음. Defaults to False.

    Returns:
        [type]: [description]
    """
    url = "https://api.upbit.com/v1/orderbook"
    orderbook, req_limit_info = _call_public_api(url, markets=ticker)

    if isinstance(ticker, str) or (isinstance(ticker, list) and len(ticker)==1):
        orderbook = orderbook[0]

    if limit_info:
        return orderbook, req_limit_info
    else:
        return orderbook



if __name__ == "__main__":
    import pprint

    # 모든 티커 목록 조회
    #all_tickers = get_tickers()
    #print(len(all_tickers))

    #all_tickers = get_tickers(fiat="KRW")
    #print(len(all_tickers))

    #all_tickers = get_tickers(fiat="KRW", verbose=True)
    #print(all_tickers)

    # krw_tickers = get_tickers(fiat="KRW")
    # print(krw_tickers, len(krw_tickers))

    #btc_tickers = get_tickers(fiat="BTC")
    # print(btc_tickers, len(btc_tickers))

    #usdt_tickers = get_tickers(fiat="USDT")
    # print(usdt_tickers, len(usdt_tickers))

    # 요청 수 제한 얻기
    #all_tickers, limit_info = get_tickers(limit_info=True)
    # print(limit_info)

    # print(get_tickers(fiat="KRW"))
    # print(get_tickers(fiat="BTC"))
    # print(get_tickers(fiat="USDT"))

    #------------------------------------------------------
    # print(get_ohlcv("KRW-BTC"))
    # print(get_ohlcv("KRW-BTC", interval="day", count=5))
    # print(get_ohlcv("KRW-BTC", interval="day", to="2020-01-01 00:00:00"))
    df = get_ohlcv('KRW-XRP', interval='minute5', count=1000)
    print(df)

    # to = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
    # df = get_ohlcv(ticker="KRW-BTC", interval="day", to=to)
    # print(df)

    # string Test
    # df = get_ohlcv("KRW-BTC", interval="minute1", to="2018-08-25 12:00:00")
    # print(df)

    # time stamp Test
    # df = get_ohlcv("KRW-BTC", interval="minute1")
    # print(df)
    # df = get_ohlcv("KRW-BTC", interval="minute1", count=401)
    # df = get_ohlcv("KRW-BTC", interval="minute1", count=400)
    # df = get_ohlcv("KRW-BTC", interval="minute1", count=4)
    # print(len(df))
    # print(get_ohlcv("KRW-BTC", interval="minute1", to=df.index[0]))

    # # DateTime Test
    # now = datetime.datetime.now() - datetime.timedelta(days=1000)
    # print(get_ohlcv("KRW-BTC", interval="minute1", to=now))
    # print(get_ohlcv("KRW-BTC", interval="minute1", to="2018-01-01 12:00:00"))
    # print(get_ohlcv("KRW-BTC", interval="minute3"))
    # print(get_ohlcv("KRW-BTC", interval="minute5"))
    # print(get_ohlcv("KRW-BTC", interval="minute10"))
    # print(get_ohlcv("KRW-BTC", interval="minute15"))
    # print(get_ohlcv("KRW-BTC", interval="minute30"))
    # print(get_ohlcv("KRW-BTC", interval="minute60"))
    # print(get_ohlcv("KRW-BTC", interval="minute240"))
    # print(get_ohlcv("KRW-BTC", interval="week"))
    # print(get_daily_ohlcv_from_base("KRW-BTC", base=9))
    # print(get_ohlcv("KRW-BTC", interval="day", count=5))


    # krw_tickers = get_tickers(fiat="KRW")
    # print(len(krw_tickers))

    # krw_tickers1 = krw_tickers[:100]
    # krw_tickers2 = krw_tickers[100:]

    # prices1 = get_current_price(krw_tickers1)
    # prices2 = get_current_price(krw_tickers2)

    # print(prices1)
    # print(prices2)


    #price = get_current_price("KRW-BTC")
    #print(price)
    # price, limit = get_current_price("KRW-BTC", limit_info=True)
    #print(price, limit)
    #price = get_current_price(["KRW-BTC", "KRW-XRP"])
    #print(price)
    #price, limit = get_current_price(["KRW-BTC", "KRW-XRP"], limit_info=True)
    #print(price, limit)
    #price = get_current_price("KRW-BTC", verbose=True)
    #print(price)
    #price = get_current_price(["KRW-BTC", "KRW-XRP"], verbose=True)
    #print(price)

    # print(get_current_price(["KRW-BTC", "KRW-XRP"]))

    # orderbook
    #orderbook = get_orderbook(ticker="KRW-BTC")
    #print(orderbook)

    #orderbook, req_limit_info = get_orderbook(ticker="KRW-BTC", limit_info=True)
    #print(orderbook, req_limit_info)

    #orderbook = get_orderbook(tickers=["KRW-BTC", "KRW-XRP"])
    #for ob in orderbook:
    #    print(ob)