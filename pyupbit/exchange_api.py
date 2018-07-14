import time
from pyupbit.quotation_api import *
import jwt
from urllib.parse import urlencode

getframe_expr = 'sys._getframe({}).f_code.co_name'


def _send_post_request(url, headers=None, data=None):
    try:
        resp = requests_retry_session().post(url, headers=headers, data=data)
        contents = resp.json()
        return contents
    except Exception as x:
        print("send post request failed", x.__class__.__name__)
        print("caller: ", eval(getframe_expr.format(2)))
        return None


def _send_get_request(url, headers=None):
    try:
        resp = requests_retry_session().get(url, headers=headers)
        contents = resp.json()
        return contents
    except Exception as x:
        print("send get request failed", x.__class__.__name__)
        print("caller: ", eval(getframe_expr.format(2)))
        return None


def _send_delete_request(url, headers=None, data=None):
    try:
        resp = requests_retry_session().delete(url, headers=headers, data=data)
        contents = resp.json()
        return contents
    except Exception as x:
        print("send post request failed", x.__class__.__name__)
        print("caller: ", eval(getframe_expr.format(2)))
        return None


def get_tick_size(price):
    if price >= 2000000:
        tick_size = round(price / 1000) * 1000
    elif price >= 1000000:
        tick_size = round(price / 500) * 500
    elif price >= 500000:
        tick_size = round(price / 100) * 100
    elif price >= 100000:
        tick_size = round(price / 50) * 50
    elif price >= 10000:
        tick_size = round(price / 10) * 10
    elif price >= 1000:
        tick_size = round(price / 5) * 5
    elif price >= 100:
        tick_size = round(price / 1) * 1
    elif price >= 10:
        tick_size = round(price / 0.1) * 0.1
    else:
        tick_size = round(price / 0.01) * 0.01
    return tick_size


class Upbit:
    def __init__(self, access, secret):
        self.access = access
        self.secret = secret

    def _request_headers(self, data=None):
        payload = {
            "access_key": self.access,
            "nonce": int(time.time() * 1000)
        }
        if data is not None:
            payload['query'] = urlencode(data)
        jwt_token = jwt.encode(payload, self.secret, algorithm="HS256").decode('utf-8')
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization_token}
        return headers

    def get_balances(self):
        '''
        전체 계좌 조회
        :return:
        '''
        url = "https://api.upbit.com/v1/accounts"
        headers = self._request_headers()
        return _send_get_request(url, headers=headers)

    def buy_limit_order(self, ticker, price, volume):
        '''
        지정가 매수
        :param ticker: 마켓 티커
        :param price: 주문 가격
        :param volume: 주문 수량
        :return:
        '''
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,
                    "side": "bid",
                    "volume": str(volume),
                    "price": str(price),
                    "ord_type": "limit"}
            headers = self._request_headers(data)
            return _send_post_request(url, headers=headers, data=data)
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def sell_limit_order(self, ticker, price, volume):
        '''
        지정가 매도
        :param ticker: 마켓 티커
        :param price: 주문 가격
        :param volume: 주문 수량
        :return:
        '''
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,
                    "side": "ask",
                    "volume": str(volume),
                    "price": str(price),
                    "ord_type": "limit"}
            headers = self._request_headers(data)
            return _send_post_request(url, headers=headers, data=data)
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def cancel_order(self, uuid):
        '''
        주문 취소
        :param uuid: 주문 함수의 리턴 값중 uuid
        :return:
        '''
        try:
            url = "https://api.upbit.com/v1/order"
            data = {"uuid": uuid}
            headers = self._request_headers(data)
            return _send_delete_request(url, headers=headers, data=data)
        except Exception as x:
            print(x.__class__.__name__)
            return None


if __name__ == "__main__":
    access = "73kVqowGQOGEjdR31221j31j2ifekjkgjekgjekg"
    secret = "egjekgj3iekeEEkej3i3j3iejjwiEejiejeEeijg"

    # Upbit
    upbit = Upbit(access, secret)

    # 잔고 조회
    print(upbit.get_balances())

    # 매도
    #print(upbit.sell_limit_order("KRW-XRP", 507, 20))

    # 매수
    #print(upbit.buy_limit_order("KRW-XRP", 500, 20))

    # 주문 취소
    #print(upbit.cancel_order('e57a3bc0-0b0b-4540-96f2-f35f19c51e8d'))









