import time
from pyupbit.quotation_api import *
import jwt
from urllib.parse import urlencode
import re

getframe_expr = 'sys._getframe({}).f_code.co_name'


def _send_post_request(url, headers=None, data=None, remaining_req=None):
    try:
        resp = requests_retry_session().post(url, headers=headers, data=data)
        remaining = resp.headers.get('Remaining-Req')
        if isinstance(remaining_req, dict) and remaining is not None:
            group, min, sec = _parse_remaining_req(remaining)
            remaining_req['group'] = group
            remaining_req['min'] = min
            remaining_req['sec'] = sec
        contents = resp.json()
        return contents
    except Exception as x:
        print("send post request failed", x.__class__.__name__)
        print("caller: ", eval(getframe_expr.format(2)))
        return None

def _parse_remaining_req(remaining_req):
    try:
        p = re.compile("group=([a-z]+); min=([0-9]+); sec=([0-9]+)")
        m = p.search(remaining_req)
        return m.group(1), int(m.group(2)), int(m.group(3))
    except:
        return None, None, None

def _send_get_request(url, headers=None, remaining_req=None):
    try:
        resp = requests_retry_session().get(url, headers=headers)
        remaining = resp.headers.get('Remaining-Req')
        if isinstance(remaining_req, dict) and remaining is not None:
            group, min, sec = _parse_remaining_req(remaining)
            remaining_req['group'] = group
            remaining_req['min'] = min
            remaining_req['sec'] = sec
        contents = resp.json()
        return contents
    except Exception as x:
        print("send get request failed", x.__class__.__name__)
        print("caller: ", eval(getframe_expr.format(2)))
        return None


def _send_delete_request(url, headers=None, data=None, remaining_req=None):
    try:
        resp = requests_retry_session().delete(url, headers=headers, data=data)
        remaining = resp.headers.get('Remaining-Req')
        if isinstance(remaining_req, dict) and remaining is not None:
            group, min, sec = _parse_remaining_req(remaining)
            remaining_req['group'] = group
            remaining_req['min'] = min
            remaining_req['sec'] = sec
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

    def get_balances(self, remaining_req=None):
        '''
        전체 계좌 조회
        :return:
        '''
        url = "https://api.upbit.com/v1/accounts"
        headers = self._request_headers()
        return _send_get_request(url, headers=headers, remaining_req=remaining_req)

    def buy_limit_order(self, ticker, price, volume, remaining_req=None):
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
            return _send_post_request(url, headers=headers, data=data, remaining_req=remaining_req)
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def sell_limit_order(self, ticker, price, volume, remaining_req=None):
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
            return _send_post_request(url, headers=headers, data=data, remaining_req=remaining_req)
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def cancel_order(self, uuid, remaining_req=None):
        '''
        주문 취소
        :param uuid: 주문 함수의 리턴 값중 uuid
        :return:
        '''
        try:
            url = "https://api.upbit.com/v1/order"
            data = {"uuid": uuid}
            headers = self._request_headers(data)
            return _send_delete_request(url, headers=headers, data=data, remaining_req=remaining_req)
        except Exception as x:
            print(x.__class__.__name__)
            return None


if __name__ == "__main__":
    with open("upbit.txt") as f:
        lines = f.readlines()
        access = lines[0].strip()
        secret = lines[1].strip()

    # Upbit
    upbit = Upbit(access, secret)

    # 잔고 조회
    print(upbit.get_balances())

    # 잔고 조회 w/ 요청 수 제한 얻기
    remaining_req = {}
    print(upbit.get_balances(remaining_req))
    print(remaining_req)

    # 매도
    #print(upbit.sell_limit_order("KRW-XRP", 1000, 20))

    # 매도 w/ 요청 수 제한 얻기
    #remaining_req = {}
    #print(upbit.sell_limit_order("KRW-XRP", 1000, 20, remaining_req))
    #print(remaining_req)

    # 매수
    #print(upbit.buy_limit_order("KRW-XRP", 500, 20))

    # 매수 w/ 요청 수 제한 얻기
    #remaining_req = {}
    #print(upbit.buy_limit_order("KRW-XRP", 200, 20, remaining_req))
    #print(remaining_req)

    # 주문 취소
    #print(upbit.cancel_order('e57a3bc0-0b0b-4540-96f2-f35f19c51e8d'))

    # 주문 취소 w/ 요청 수 제한 얻기
    # remaining_req = {}
    # print(upbit.cancel_order('7afbd861-bb9d-423f-870a-a87b414ffc5b', remaining_req))
    # print(remaining_req)








