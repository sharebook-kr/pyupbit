# Upbit Quatation (시세 조회) API
import datetime
import pandas as pd
import sys
import time
from pyupbit.request_api import _call_public_api
from pyupbit.errors import UpbitError, TooManyRequests, raise_error
import requests
import re


def parse_remaining_req(data):
    """요청 제한 데이터 파싱 함수

    Args:
        data (str): "{'group': 'market', 'min': '573', 'sec': '2'}"

    Returns:
        dict: {'group': 'market', 'min': 573, 'sec': 2}
    """
    p = re.compile("group=([a-z]+); min=([0-9]+); sec=([0-9]+)")
    m = p.search(data)
    ret = {
        'group': m.group(1),
        'min': int(m.group(2)),
        'sec': int(m.group(3))
    }
    return ret


def fetch_market(isDetails=False, limit_info=False):
    """업비트에서 거래 가능한 마켓 목록

    Args:
        isDetails (bool, optional): True: 상세조회, False: 비 상세조회. Defaults to False.
        limit_info (bool, optional): True: 요청 수 제한 정보 리턴, False: 요청 수 제한 정보 리턴 받지 않음. Defaults to False.

    Returns:
        list, (dict): 마켓 목록 리스트, 요청 제한 정보 딕셔너리
    """
    url = "https://api.upbit.com/v1/market/all"

    if isDetails:
        query_string = {"isDetails": "true"}
    else:
        query_string = {"isDetails": "false"}
    resp = requests.get(url, params=query_string)

    if resp.status_code == 200:
        remaining_req = resp.headers.get('Remaining-Req')
        limit = parse_remaining_req(remaining_req)
        data = resp.json()
        if limit_info:
            return data, limit
        else:
            return data
    else:
        raise_error(resp.status_code)


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


def get_ohlcv(ticker="KRW-BTC", interval="day", count=200, to=None, period=0.1):
    """
    캔들 조회
    :return:
    """
    MAX_CALL_COUNT = 200
    try:
        url = get_url_ohlcv(interval=interval)

        if to == None:
            to = datetime.datetime.now()
        elif isinstance(to, str):
            to = pd.to_datetime(to).to_pydatetime()
        elif isinstance(to, pd._libs.tslibs.timestamps.Timestamp):
            to = to.to_pydatetime()

        dfs = []
        count = max(count, 1)
        for pos in range(count, 0, -200):
            query_count = min(MAX_CALL_COUNT, pos)

            if to.tzinfo is None:
                to = to.astimezone()
            to = to.astimezone(datetime.timezone.utc)
            to = to.strftime("%Y-%m-%d %H:%M:%S")

            contents = _call_public_api(url, market=ticker, count=query_count, to=to)[0]
            dt_list = [datetime.datetime.strptime(x['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S") for x in contents]
            df = pd.DataFrame(contents, columns=['opening_price', 'high_price', 'low_price', 'trade_price',
                                                'candle_acc_trade_volume', 'candle_acc_trade_price'],
                            index=dt_list)
            df = df.sort_index()
            if df.shape[0] == 0:
                break
            dfs += [df]

            to = df.index[0].to_pydatetime()

            if pos > 200:
                time.sleep(period)

        df = pd.concat(dfs).sort_index()
        df = df.rename(
            columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close",
                     "candle_acc_trade_volume": "volume", "candle_acc_trade_price": "value"})
        return df
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
    # try:
    #     for i in range(20):
    #         market_all, limit = fetch_market(isDetails=True, limit_info=True)
    # except TooManyRequests as e:
    #     print(e)
    # except UpbitError as e:
    #     print(e)


    # 모든 티커 목록 조회
    all_tickers = get_tickers()
    print(all_tickers)

    # 특정 시장의 티커 목록 조회
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

    # to = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
    # df = get_ohlcv(ticker="KRW-BTC", interval="day", to=to)
    # print(df)

    # string Test
    # df = get_ohlcv("KRW-BTC", interval="minute1", to="2018-08-25 12:00:00")
    # print(df)

    # time stamp Test
    # df = get_ohlcv("KRW-BTC", interval="minute1")
    # print(df)
    df = get_ohlcv("KRW-BTC", interval="minute1", count=401)
    df = get_ohlcv("KRW-BTC", interval="minute1", count=400)
    df = get_ohlcv("KRW-BTC", interval="minute1", count=4)
    print(len(df))
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


    # print(get_current_price("KRW-BTC"))
    # print(get_current_price(["KRW-BTC", "KRW-XRP"]))

    # print(get_orderbook(tickers=["KRW-BTC"]))
    # print(get_orderbook(tickers=["KRW-BTC", "KRW-XRP"]))
