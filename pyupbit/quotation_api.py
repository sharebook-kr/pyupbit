# UPbit Quatation (시세 조회) API
import datetime
import pandas as pd
import sys
from pyupbit.request_api import _call_public_api


def get_tickers(fiat="ALL", limit_info=False):
    """
    마켓 코드 조회 (업비트에서 거래 가능한 마켓 목록 조회)
    :param fiat: "ALL", "KRW", "BTC", "USDT"
    :param limit_info: 요청수 제한 리턴
    :return:
    """
    try:
        url = "https://api.upbit.com/v1/market/all"

        # call REST API 
        ret = _call_public_api(url)
        if isinstance(ret, tuple):
            contents, req_limit_info = ret 
        else:
            contents = None 
            req_limit_info = None

        tickers = None
        if isinstance(contents, list):
            markets = [x['market'] for x in contents]

            if fiat != "ALL":
                tickers = [x for x in markets if x.startswith(fiat)]
            else:
                tickers = markets

        if limit_info is False: 
            return tickers 
        else:
            return tickers, req_limit_info

    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_url_ohlcv(interval):
    """
    candle에 대한 요청 주소를 얻는 함수
    :param interval: day(일봉), minute(분봉), week(주봉), 월봉(month)
    :return: candle 조회에 사용되는 url
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


def get_ohlcv(ticker="KRW-BTC", interval="day", count=200, to=None):
    """
    캔들 조회
    :return:
    """
    try:
        url = get_url_ohlcv(interval=interval)

        if datetime.datetime == type(to):
            if to.tzinfo is None:
                to = to.astimezone()
            to = to.astimezone(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        contents = _call_public_api(url, market=ticker, count=count, to=to)[0]
        dt_list = [datetime.datetime.strptime(x['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S") for x in contents]
        df = pd.DataFrame(contents, columns=['opening_price', 'high_price', 'low_price', 'trade_price',
                                             'candle_acc_trade_volume'],
                          index=dt_list)
        df = df.rename(
            columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close",
                     "candle_acc_trade_volume": "volume"})
        return df.iloc[::-1]
    except Exception as x:
        print(x.__class__.__name__)
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
        print(x.__class__.__name__)
        return None


def get_current_price(ticker="KRW-BTC"):
    """
    최종 체결 가격 조회 (현재가)
    :param ticker:
    :return:
    """
    try:
        url = "https://api.upbit.com/v1/ticker"
        contents = _call_public_api(url, markets=ticker)[0]
        if not contents:
            return None

        if isinstance(ticker, list):
            ret = {}
            for content in contents:
                market = content['market']
                price = content['trade_price']
                ret[market] = price
            return ret
        else:
            return contents[0]['trade_price']
    except Exception as x:
        print(x.__class__.__name__)


def get_orderbook(tickers="KRW-BTC"):
    '''
    호가 정보 조회
    :param tickers: 티커 목록을 문자열
    :return:
    '''
    try:
        url = "https://api.upbit.com/v1/orderbook"
        contents = _call_public_api(url, markets=tickers)[0]
        return contents
    except Exception as x:
        print(x.__class__.__name__)
        return None


if __name__ == "__main__":
    #------------------------------------------------------
    # 모든 티커 목록 조회
    #all_tickers = get_tickers()
    #print(all_tickers)

    # 특정 시장의 티커 목록 조회 
    #krw_tickers = get_tickers(fiat="KRW")
    #print(krw_tickers, len(krw_tickers))

    #btc_tickers = get_tickers(fiat="BTC")
    #print(btc_tickers, len(btc_tickers))

    #usdt_tickers = get_tickers(fiat="USDT")
    #print(usdt_tickers, len(usdt_tickers))

    # 요청 수 제한 얻기
    #all_tickers, limit_info = get_tickers(limit_info=True)
    #print(limit_info)

    # print(get_tickers(fiat="KRW"))
    # print(get_tickers(fiat="BTC"))
    # print(get_tickers(fiat="USDT"))

    #------------------------------------------------------
    #print(get_ohlcv("KRW-BTC"))
    #print(get_ohlcv("KRW-BTC", interval="day", count=5))
    #print(get_ohlcv("KRW-BTC", interval="day", to="2020-01-01 00:00:00"))

    #to = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
    #df = get_ohlcv(ticker="KRW-BTC", interval="day", to=to)
    #print(df)

    # print(get_ohlcv("KRW-BTC", interval="minute1"))
    # print(get_ohlcv("KRW-BTC", interval="minute3"))
    # print(get_ohlcv("KRW-BTC", interval="minute5"))
    # print(get_ohlcv("KRW-BTC", interval="minute10"))
    #print(get_ohlcv("KRW-BTC", interval="minute15"))
    #print(get_ohlcv("KRW-BTC", interval="minute30"))
    #print(get_ohlcv("KRW-BTC", interval="minute60"))
    #print(get_ohlcv("KRW-BTC", interval="minute240"))
    #print(get_ohlcv("KRW-BTC", interval="week"))
    #print(get_daily_ohlcv_from_base("KRW-BTC", base=9))
    #print(get_ohlcv("KRW-BTC", interval="day", count=5))

    krw_tickers = get_tickers(fiat="KRW")
    print(len(krw_tickers))

    krw_tickers1 = krw_tickers[:100]
    krw_tickers2 = krw_tickers[100:]

    prices1 = get_current_price(krw_tickers1)
    prices2 = get_current_price(krw_tickers2)

    #print(prices1)
    print(prices2)


    #print(get_current_price("KRW-BTC"))
    #print(get_current_price(["KRW-BTC", "KRW-XRP"]))

    #print(get_orderbook(tickers=["KRW-BTC"]))
    #print(get_orderbook(tickers=["KRW-BTC", "KRW-XRP"]))
