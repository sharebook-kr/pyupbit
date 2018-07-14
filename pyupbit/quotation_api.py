import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import datetime


def requests_retry_session(retries=5, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None):
    s = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('http://', adapter)
    s.mount('https://', adapter)
    return s


def _call_public_api(url, **kwargs):
    try:
        resp = requests_retry_session().get(url, params=kwargs)
        contents = resp.json()
        return contents
    except Exception as x:
        print("It failed", x.__class__.__name__)
        return None


def get_tickers(fiat="ALL"):
    """
    마켓 코드 조회 (업비트에서 거래 가능한 마켓 목록 조회)
    :return:
    """
    try:
        url = "https://api.upbit.com/v1/market/all"
        contents = _call_public_api(url)

        if isinstance(contents, list):
            markets = [x['market'] for x in contents]

            if fiat is "KRW":
                return [x for x in markets if x.startswith("KRW")]
            elif fiat is "BTC":
                return [x for x in markets if x.startswith("BTC")]
            elif fiat is "ETH":
                return [x for x in markets if x.startswith("ETH")]
            elif fiat is "USDT":
                return [x for x in markets if x.startswith("USDT")]
            else:
                return markets
        else:
            return None
    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_ohlcv(ticker="KRW-BTC", interval= "day", count=120):
    """
    일 캔들 조회
    :return:
    """
    try:
        if interval is "day":
            url = "https://api.upbit.com/v1/candles/days"
        elif interval is "minute":
            url = "https://api.upbit.com/v1/candles/minutes/1"
        elif interval is "week":
            url = "https://api.upbit.com/v1/candles/weeks"
        else:
            url = "https://api.upbit.com/v1/candles/months"

        contents = _call_public_api(url, market=ticker, count=count)
        dt_list = [ datetime.datetime.strptime(x['candle_date_time_kst'], "%Y-%m-%dT%H:%M:%S") for x in contents]
        df = pd.DataFrame(contents, columns=['opening_price', 'high_price', 'low_price', 'trade_price', 'candle_acc_trade_volume'],
                          index=dt_list)
        df = df.rename(columns={"opening_price": "open", "high_price": "high", "low_price": "low", "trade_price": "close",
                                "candle_acc_trade_volume": "volume"})
        return df
    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_current_price(ticker="KRW-BTC"):
    '''
    최종 체결 가격 조회 (현재가)
    :param ticker:
    :return:
    '''
    try:
        url = "https://api.upbit.com/v1/trades/ticks"
        contents = _call_public_api(url, market=ticker)

        if contents is not None:
            return contents[0]['trade_price']
        else:
            return None
    except Exception as x:
        print(x.__class__.__name__)
        return None


def get_orderbook(tickers="KRW-BTC"):
    '''
    호가 정보 조회
    :param tickers: 티커 목록을 문자열
    :return:
    '''
    try:
        url = "https://api.upbit.com/v1/orderbook"
        contents = _call_public_api(url, markets=tickers)
        return contents
    except Exception as x:
        print(x.__class__.__name__)
        return None


if __name__ == "__main__":
    #print(get_tickers())
    #print(get_tickers(fiat="KRW"))
    #print(get_tickers(fiat="BTC"))
    #print(get_tickers(fiat="ETH"))
    #print(get_tickers(fiat="USDT"))

    #print(get_ohlcv("KRW-BTC"))
    #print(get_ohlcv("KRW-BTC", interval="minute"))
    print(get_ohlcv("KRW-BTC", interval="week"))
    #print(get_current_price("KRW-BTC"))
    #print(get_orderbook(tickers=["KRW-BTC", "KRW-XRP"]))
