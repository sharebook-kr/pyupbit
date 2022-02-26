from requests import Response
from typing import Any

__all__ = [
    "CreateAskError",
    "CreateBidError",
    "InsufficientFundsAsk",
    "InsufficientFundsBid",
    "UnderMinTotalAsk",
    "UnderMinTotalBid",
    "WidthdrawAddressNotRegisterd",
    "ValidationError",
    "InvalidQueryPayload",
    "JwtVerification",
    "ExpiredAccessKey",
    "NonceUsed",
    "NoAutorizationIP",
    "OutOfScope",
    "TooManyRequests",
    "RemainingReqParsingError",
    "InValidAccessKey",
    "raise_error",
]


class UpbitErrorMixin:
    name: str
    code: int
    msg: str

    def __init__(self, **ctx: Any) -> None:
        self.__dict__ = ctx

    def __str__(self) -> str:
        return self.msg.format(**self.__dict__)


class UpbitError(UpbitErrorMixin, Exception):
    pass


class UpbitBadRequestError(UpbitErrorMixin, Exception):
    pass


class UpbitUnauthorizedError(UpbitErrorMixin, Exception):
    pass


class UpbitLimitError(UpbitErrorMixin, Exception):
    pass


class CreateAskError(UpbitBadRequestError):
    name = "create_ask_error"
    code = 400
    msg = "주문 요청 정보가 올바르지 않습니다."


class CreateBidError(UpbitBadRequestError):
    name = "create_bid_error"
    code = 400
    msg = "주문 요청 정보가 올바르지 않습니다."


class InsufficientFundsAsk(UpbitBadRequestError):
    name = "insufficient_funds_ask"
    code = 400
    msg = "매수/매도 가능 잔고가 부족합니다."


class InsufficientFundsBid(UpbitBadRequestError):
    name = "insufficient_funds_bid"
    code = 400
    msg = "매수/매도 가능 잔고가 부족합니다."


class UnderMinTotalAsk(UpbitBadRequestError):
    name = "under_min_total_ask"
    code = 400
    msg = "주문 요청 금액이 최소 주문 금액 미만입니다."


class UnderMinTotalBid(UpbitBadRequestError):
    name = "under_min_total_bid"
    code = 400
    msg = "주문 요청 금액이 최소 주문 금액 미만입니다."


class WidthdrawAddressNotRegisterd(UpbitBadRequestError):
    name = "withdraw_address_not_registerd"
    code = 400
    msg = "허용되지 않은 출금 주소입니다."


class ValidationError(UpbitBadRequestError):
    name = "validation_error"
    code = 400
    msg = "잘못된 API 요청입니다."


class InvalidQueryPayload(UpbitUnauthorizedError):
    name = "invalid_query_payload"
    code = 401
    msg = "JWT 헤더의 페이로드가 올바르지 않습니다."


class JwtVerification(UpbitUnauthorizedError):
    name = "jwt_verification"
    code = 401
    msg = "JWT 토큰 검증에 실패했습니다."


class ExpiredAccessKey(UpbitUnauthorizedError):
    name = "expired_access_key"
    code = 401
    msg = "API 키가 만료되었습니다."


class NonceUsed(UpbitUnauthorizedError):
    name = "nonce_used"
    code = 401
    msg = "이미 요청한 nonce값이 다시 사용되었습니다."


class NoAutorizationIP(UpbitUnauthorizedError):
    name = "no_authorization_i_p"
    code = 401
    msg = "허용되지 않은 IP 주소입니다."


class OutOfScope(UpbitUnauthorizedError):
    name = "out_of_scope"
    code = 401
    msg = "허용되지 않은 기능입니다."


class TooManyRequests(UpbitLimitError):
    name = ""
    code = 429
    msg = "요청 수 제한을 초과했습니다."


class RemainingReqParsingError(UpbitLimitError):
    name = ""
    code = -1
    msg = "요청 수 제한 파싱에 실패했습니다."


class InValidAccessKey(UpbitUnauthorizedError):
    name = ""
    code = -1
    msg = "잘못된 엑세스 키입니다."


bad_requests = [eval(err) for err in __all__[:-1] if eval(err).code == 400]
unauthorized = [eval(err) for err in __all__[:-1] if eval(err).code == 401]


def raise_error(resp: Response) -> None:
    error = resp.json().get("error")
    message = error.get("message")
    name = error.get("name")
    code = resp.status_code

    if code == 400:
        for err in bad_requests:
            if err.name == name:
                raise err
    elif code == 401:
        for err in unauthorized:
            if err.name == name:
                raise err
    elif code == 429:
        raise TooManyRequests
    else:
        raise UpbitError(name=name, code=code, msg=message)
