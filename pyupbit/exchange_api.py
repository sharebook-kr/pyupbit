# -*- coding: utf-8 -*-

"""
pyupbit.exchange_api

This module provides exchange api of the Upbit API.
"""

import math
import jwt          # PyJWT
import re
import uuid
import hashlib
from urllib.parse import urlencode
from pyupbit.request_api import _send_get_request, _send_post_request, _send_delete_request


def get_tick_size(price, method="floor"):
    """원화마켓 주문 가격 단위
    TODO: rename this to adjust_price_per_tick_table?
    tick size is by definition the minimum allowed price increment.
    FIXME: tick size is updated. https://docs.upbit.com/docs/market-info-trade-price-detail

    Args:
        price (float]): 주문 가격 
        method (str, optional): 주문 가격 계산 방식. Defaults to "floor".

    Returns:
        float: 업비트 원화 마켓 주문 가격 단위로 조정된 가격 
    """
    if method == "floor":
        func = math.floor
    elif method == "round":
        func = round 
    else:
        func = math.ceil 

    if price >= 2000000:
        tick_size = func(price / 1000) * 1000
    elif price >= 1000000:
        tick_size = func(price / 500) * 500
    elif price >= 500000:
        tick_size = func(price / 100) * 100
    elif price >= 100000:
        tick_size = func(price / 50) * 50
    elif price >= 10000:
        tick_size = func(price / 10) * 10
    elif price >= 1000:
        tick_size = func(price / 1) * 1
    elif price >= 100:
        tick_size = func(price / 0.1) / 10
    elif price >= 10:
        tick_size = func(price / 0.01) / 100
    elif price >= 1:
        tick_size = func(price / 0.001) / 1000
    elif price >= 0.1:
        tick_size = func(price / 0.0001) / 10000
    elif price >= 0.01:
        tick_size = func(price / 0.00001) / 100000
    elif price >= 0.001:
        tick_size = func(price / 0.000001) / 1000000
    elif price >= 0.0001:
        tick_size = func(price / 0.0000001) / 10000000
    else:
        tick_size = func(price / 0.00000001) / 100000000

    return tick_size


class Upbit:
    def __init__(self, access, secret):
        self.access = access
        self.secret = secret


    def _request_headers(self, query=None):
        payload = {
            "access_key": self.access,
            "nonce": str(uuid.uuid4())
        }

        if query is not None:
            m = hashlib.sha512()
            m.update(urlencode(query, doseq=True).replace("%5B%5D=", "[]=").encode())
            query_hash = m.hexdigest()
            payload['query_hash'] = query_hash
            payload['query_hash_alg'] = "SHA512"

        #jwt_token = jwt.encode(payload, self.secret, algorithm="HS256").decode('utf-8')
        jwt_token = jwt.encode(payload, self.secret, algorithm="HS256")     # PyJWT >= 2.0
        authorization_token = 'Bearer {}'.format(jwt_token)
        headers = {"Authorization": authorization_token}
        return headers


    #--------------------------------------------------------------------------
    # 자산 
    #--------------------------------------------------------------------------
    #     전체 계좌 조회
    def get_balances(self, contain_req=False):
        """
        전체 계좌 조회
        :param contain_req: Remaining-Req 포함여부
        :return: 내가 보유한 자산 리스트
        [contain_req == True 일 경우 Remaining-Req가 포함]
        """
        url = "https://api.upbit.com/v1/accounts"
        headers = self._request_headers()
        result = _send_get_request(url, headers=headers)
        if contain_req:
            return result
        else:
            return result[0]


    def get_balance(self, ticker="KRW", verbose=False, contain_req=False):
        """
        특정 코인/원화의 잔고를 조회하는 메소드
        :param ticker: 화폐를 의미하는 영문 대문자 코드
        :param verbose: False: only the balance, True: original dictionary 
        :param contain_req: Remaining-Req 포함여부
        :return: 주문가능 금액/수량 (주문 중 묶여있는 금액/수량 제외)
        [contain_req == True 일 경우 Remaining-Req가 포함]
        """
        try:
            # fiat-ticker
            # KRW-BTC
            fiat = "KRW"
            if '-' in ticker:
                fiat, ticker = ticker.split('-')

            balances, req = self.get_balances(contain_req=True)

            # search the current currency
            balance = 0
            for x in balances:
                if x['currency'] == ticker and x['unit_currency'] == fiat:
                    if verbose is True:
                        balance = x 
                    else:
                        balance = float(x['balance'])
                    break

            if contain_req:
                return balance, req
            else:
                return balance
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_balance_t(self, ticker='KRW', contain_req=False):
        """
        특정 코인/원화의 잔고 조회(balance + locked)
        :param ticker: 화폐를 의미하는 영문 대문자 코드
        :param contain_req: Remaining-Req 포함여부
        :return: 주문가능 금액/수량 (주문 중 묶여있는 금액/수량 포함)
        [contain_req == True 일 경우 Remaining-Req가 포함]
        """
        try:
            # KRW-BTC
            if '-' in ticker:
                ticker = ticker.split('-')[1]

            balances, req = self.get_balances(contain_req=True)

            balance = 0
            locked = 0
            for x in balances:
                if x['currency'] == ticker:
                    balance = float(x['balance'])
                    locked = float(x['locked'])
                    break

            if contain_req:
                return balance + locked, req
            else:
                return balance + locked
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_avg_buy_price(self, ticker='KRW', contain_req=False):
        """
        특정 코인/원화의 매수평균가 조회
        :param ticker: 화폐를 의미하는 영문 대문자 코드
        :param contain_req: Remaining-Req 포함여부
        :return: 매수평균가
        [contain_req == True 일 경우 Remaining-Req가 포함]
        """
        try:
            # KRW-BTC
            if '-' in ticker:
                ticker = ticker.split('-')[1]

            balances, req = self.get_balances(contain_req=True)

            avg_buy_price = 0
            for x in balances:
                if x['currency'] == ticker:
                    avg_buy_price = float(x['avg_buy_price'])
                    break
            if contain_req:
                return avg_buy_price, req
            else:
                return avg_buy_price

        except Exception as x:
            print(x.__class__.__name__)
            return None

    def get_amount(self, ticker, contain_req=False):
        """
        특정 코인/원화의 매수금액 조회
        :param ticker: 화폐를 의미하는 영문 대문자 코드 (ALL 입력시 총 매수금액 조회)
        :param contain_req: Remaining-Req 포함여부
        :return: 매수금액
        [contain_req == True 일 경우 Remaining-Req가 포함]
        """
        try:
            # KRW-BTC
            if '-' in ticker:
                ticker = ticker.split('-')[1]

            balances, req = self.get_balances(contain_req=True)

            amount = 0
            for x in balances:
                if x['currency'] == 'KRW':
                    continue

                avg_buy_price = float(x['avg_buy_price'])
                balance = float(x['balance'])
                locked = float(x['locked'])

                if ticker == 'ALL':
                    amount += avg_buy_price * (balance + locked)
                elif x['currency'] == ticker:
                    amount = avg_buy_price * (balance + locked)
                    break
            if contain_req:
                return amount, req
            else:
                return amount
        except Exception as x:
            print(x.__class__.__name__)
            return None

    # endregion balance


    #--------------------------------------------------------------------------
    # 주문 
    #--------------------------------------------------------------------------
    #     주문 가능 정보
    def get_chance(self, ticker, contain_req=False):
        """
        마켓별 주문 가능 정보를 확인.
        :param ticker:
        :param contain_req: Remaining-Req 포함여부
        :return: 마켓별 주문 가능 정보를 확인
        [contain_req == True 일 경우 Remaining-Req가 포함]
        """
        try:
            url = "https://api.upbit.com/v1/orders/chance"
            data = {"market": ticker}
            headers = self._request_headers(data)
            result = _send_get_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None
    

    #    개별 주문 조회 
    def get_order(self, ticker_or_uuid, state='wait', page=1, limit=100, contain_req=False):
        """
        주문 리스트 조회
        :param ticker_or_uuid: 마켓 아이디 or 주문 UUID
        :param state: 주문 상태(wait, watch, done, cancel)
        :param page: 페이지 수
        :param limit: 요청 개수
        :param contain_req: Remaining-Req 포함여부
        :return: 주문 리스트
        """
        # TODO : states, identifiers 관련 기능 추가 필요
        try:
            p = re.compile(r"^\w+-\w+-\w+-\w+-\w+$")
            # 정확히는 입력을 대문자로 변환 후 다음 정규식을 적용해야 함
            # - r"^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-[0-9A-F]{12}$"
            is_uuid = len(p.findall(ticker_or_uuid)) > 0
            if is_uuid:
                url = "https://api.upbit.com/v1/order"
                data = {'uuid': ticker_or_uuid}
                headers = self._request_headers(data)
                result = _send_get_request(url, headers=headers, data=data)
            else :

                url = "https://api.upbit.com/v1/orders"
                data = {'market': ticker_or_uuid,
                        'state': state,
                        'page': page,
                        'limit': limit,
                        'order_by': 'desc'
                        }
                headers = self._request_headers(data)
                result = _send_get_request(url, headers=headers, data=data)

            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    def get_individual_order(self, uuid, contain_req=False):
        """
        주문 리스트 조회
        :param uuid: 주문 id
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        # TODO : states, uuids, identifiers 관련 기능 추가 필요
        try:
            url = "https://api.upbit.com/v1/order"
            data = {'uuid': uuid}
            headers = self._request_headers(data)
            result = _send_get_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    #    주문 취소 접수
    def cancel_order(self, uuid, contain_req=False):
        """
        주문 취소
        :param uuid: 주문 함수의 리턴 값중 uuid
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/order"
            data = {"uuid": uuid}
            headers = self._request_headers(data)
            result = _send_delete_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    #     주문 
    def buy_limit_order(self, ticker, price, volume, contain_req=False):
        """
        지정가 매수
        :param ticker: 마켓 티커
        :param price: 주문 가격
        :param volume: 주문 수량
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,
                    "side": "bid",
                    "volume": str(volume),
                    "price": str(price),
                    "ord_type": "limit"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def buy_market_order(self, ticker, price, contain_req=False):
        """
        시장가 매수
        :param ticker: ticker for cryptocurrency
        :param price: KRW
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,  # market ID
                    "side": "bid",  # buy
                    "price": str(price),
                    "ord_type": "price"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def sell_market_order(self, ticker, volume, contain_req=False):
        """
        시장가 매도 메서드
        :param ticker: 가상화폐 티커
        :param volume: 수량
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,  # ticker
                    "side": "ask",  # sell
                    "volume": str(volume),
                    "ord_type": "market"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    def sell_limit_order(self, ticker, price, volume, contain_req=False):
        """
        지정가 매도
        :param ticker: 마켓 티커
        :param price: 주문 가격
        :param volume: 주문 수량
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/orders"
            data = {"market": ticker,
                    "side": "ask",
                    "volume": str(volume),
                    "price": str(price),
                    "ord_type": "limit"}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    #--------------------------------------------------------------------------
    # 출금
    #--------------------------------------------------------------------------
    def get_withdraw_list(self, currency: str, contain_req=False):
        """
        출금 리스트 조회
        :param currency: Currency 코드
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/withdraws"
            data = {"currency": currency}
            headers = self._request_headers(data)

            result = _send_get_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None

    #     개별 출금 조회
    def get_individual_withdraw_order(self, uuid: str, currency: str, contain_req=False):
        """
        개별 출금 조회
        :param uuid: 출금 UUID
        :param currency: Currency 코드
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/withdraw"
            data = {"uuid": uuid, "currency": currency}
            headers = self._request_headers(data)
            result = _send_get_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    #     코인 출금하기  
    def withdraw_coin(self, currency, amount, address, secondary_address='None', transaction_type='default', contain_req=False):
        """
        코인 출금
        :param currency: Currency symbol
        :param amount: 주문 가격
        :param address: 출금 지갑 주소
        :param secondary_address: 2차 출금주소 (필요한 코인에 한해서)
        :param transaction_type: 출금 유형
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/withdraws/coin"
            data = {"currency": currency,
                    "amount": amount,
                    "address": address,
                    "secondary_address": secondary_address,
                    "transaction_type": transaction_type}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    #     원화 출금하기
    def withdraw_cash(self, amount: str, contain_req=False):
        """
        현금 출금
        :param amount: 출금 액수
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/withdraws/krw"
            data = {"amount": amount}
            headers = self._request_headers(data)
            result = _send_post_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    #--------------------------------------------------------------------------
    # 입금 
    #--------------------------------------------------------------------------
    #     입금 리스트 조회 
    def get_deposit_list(self, currency: str, contain_req=False):
        """
        입금 리스트 조회
        :currency: Currency 코드
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com//v1/deposits"
            data = {"currency": currency}
            headers = self._request_headers(data)

            result = _send_get_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None
            
    #     개별 입금 조회
    def get_individual_deposit_order(self, uuid: str, currency: str, contain_req=False):
        """
        개별 입금 조회
        :param uuid: 입금 UUID
        :param currency: Currency 코드
        :param contain_req: Remaining-Req 포함여부
        :return:
        """
        try:
            url = "https://api.upbit.com/v1/deposit"
            data = {"uuid": uuid, "currency": currency}
            headers = self._request_headers(data)
            result = _send_get_request(url, headers=headers, data=data)
            if contain_req:
                return result
            else:
                return result[0]
        except Exception as x:
            print(x.__class__.__name__)
            return None


    #     입금 주소 생성 요청 
    #     전체 입금 주소 조회
    #     개별 입금 주소 조회
    #     원화 입금하기


    #--------------------------------------------------------------------------
    # 서비스 정보 
    #--------------------------------------------------------------------------
    #     입출금 현황 
    def get_deposit_withdraw_status(self, contain_req=False):
        url = "https://api.upbit.com/v1/status/wallet"
        headers = self._request_headers()
        result = _send_get_request(url, headers=headers)
        if contain_req:
            return result
        else:
            return result[0]


    #     API키 리스트 조회
    def get_api_key_list(self, contain_req=False):
        url = "https://api.upbit.com/v1/api_keys"
        headers = self._request_headers()
        result = _send_get_request(url, headers=headers)
        if contain_req:
            return result
        else:
            return result[0]


if __name__ == "__main__":
    import pprint

    #-------------------------------------------------------------------------
    # api key
    #-------------------------------------------------------------------------
    with open("../upbit.key") as f:
        lines = f.readlines()
        access = lines[0].strip()
        secret = lines[1].strip()

    upbit = Upbit(access, secret)
    #print(upbit.get_balances())
    print(upbit.get_balance("KRW-BTC", verbose=True))

    # order 
    resp = upbit.buy_limit_order("KRW-XRP", 500, 10)
    print(resp)


    #-------------------------------------------------------------------------
    # 자산 
    #     전체 계좌 조회 
    #balance = upbit.get_balances()
    #pprint.pprint(balance)

    #balances = upbit.get_order("KRW-XRP")
    #pprint.pprint(balances)

    # order = upbit.get_order('50e184b3-9b4f-4bb0-9c03-30318e3ff10a')
    # print(order)
    # # 원화 잔고 조회
    # print(upbit.get_balance(ticker="KRW"))          # 보유 KRW
    # print(upbit.get_amount('ALL'))                  # 총매수금액
    # print(upbit.get_balance(ticker="KRW-BTC"))      # 비트코인 보유수량
    # print(upbit.get_balance(ticker="KRW-XRP"))      # 리플 보유수량

    #-------------------------------------------------------------------------
    # 주문
    #     주문 가능 정보 
    #pprint.pprint(upbit.get_chance('KRW-BTC'))

    #     개별 주문 조회
    #print(upbit.get_order('KRW-BTC'))

    # 매도
    # print(upbit.sell_limit_order("KRW-XRP", 1000, 20))

    # 매수
    # print(upbit.buy_limit_order("KRW-XRP", 200, 20))

    # 주문 취소
    # print(upbit.cancel_order('82e211da-21f6-4355-9d76-83e7248e2c0c'))

    # 시장가 주문 테스트
    # upbit.buy_market_order("KRW-XRP", 10000)

    # 시장가 매도 테스트
    # upbit.sell_market_order("KRW-XRP", 36)


    #-------------------------------------------------------------------------
    # 서비스 정보
    #     입출금 현황
    #resp = upbit.get_deposit_withdraw_status()
    #pprint.pprint(resp)

    #     API키 리스트 조회
    #resp = upbit.get_api_key_list()
    #print(resp)