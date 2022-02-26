import pytest
from unittest.mock import Mock
from requests.models import Response
from pyupbit.errors import *
from pyupbit.errors import (
    UpbitErrorMixin,
    BAD_REQUESTS,
    UNAUTHORIZED,
    TOO_MANY_REQ,
)

bad_requests = [err.name for err in BAD_REQUESTS]
unauthorized = [err.name for err in UNAUTHORIZED]
too_many_req = [err.name for err in TOO_MANY_REQ]


def test_raise_error_with_bad_requests():
    responses = list()
    for err_name in bad_requests:
        mock = Mock(spec=Response)
        mock.json.return_value = {
            "error": {
                "name": err_name,
                "message": "test_bad_requests",
            }
        }
        mock.status_code = 400
        responses.append(mock)

    for response in responses:
        with pytest.raises(UpbitErrorMixin) as exc:
            raise_error(response)

        assert exc.value.name == response.json()["error"]["name"]
        assert exc.value.code == response.status_code


def test_raise_error_with_unauthorized():
    responses = list()
    for err_name in unauthorized:
        mock = Mock(spec=Response)
        mock.json.return_value = {
            "error": {
                "name": err_name,
                "message": "test_bad_requests",
            }
        }
        mock.status_code = 401
        responses.append(mock)

    for response in responses:
        with pytest.raises(UpbitErrorMixin) as exc:
            raise_error(response)

        assert exc.value.name == response.json()["error"]["name"]
        assert exc.value.code == response.status_code


def test_raise_error_with_too_many_req():
    responses = list()
    for err_name in too_many_req:
        mock = Mock(spec=Response)
        mock.text = err_name
        mock.status_code = 429
        responses.append(mock)

    for response in responses:
        with pytest.raises(UpbitErrorMixin) as exc:
            raise_error(response)

        # too_many_request error doesn't use json response but text
        assert exc.value.name == response.text
        assert exc.value.code == response.status_code
