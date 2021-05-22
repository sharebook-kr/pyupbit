import pytest
from pyupbit.request_api import _parse_remaining_req
from pyupbit.request_api import _call_public_api
from pyupbit.errors import RemainingReqParsingError


def test_parse_remaining_req_defaults():
    limit_info = "group=market; min=573; sec=9"
    expected = {
        'group': 'market',
        'min': 573,
        'sec': 9
    }
    ret = _parse_remaining_req(limit_info) 
    assert ret == expected


def test_parse_remaining_req_raises():
    """_parse_remaining_req shold raise an exception with wrong parameter
    """
    with pytest.raises(RemainingReqParsingError):
        _parse_remaining_req("")


def test_call_public_api():
    url = "https://api.upbit.com/v1/market/all"
    querystring = {"isDetails":"false"}
    data, limit = _call_public_api(url, **querystring)
    assert isinstance(limit, dict)

