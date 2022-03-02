import re
import requests
from requests import Response
from typing import Any, Tuple, Dict, Optional
from .errors import error_handler, RemainingReqParsingError

HTTP_RESP_CODE_START = 200
HTTP_RESP_CODE_END = 400


def _parse(remaining_req: str) -> Dict[str, Any]:
    """Parse the number of remaining requests info for Upbit API

    Args:
        remaining_req (str): String of the number of remaining requests info
         like "group=market; min=573; sec=9"
    Returns:
        Parsed dictionary of the number of remaining requests info
         like {'group': 'market', 'min': 573, 'sec': 2}
    Raises:
        RemainingReqParsingError: If the input can not be parsed.
    """
    try:
        pattern = re.compile(r"group=([a-z\-]+); min=([0-9]+); sec=([0-9]+)")
        matched = pattern.search(remaining_req)
        if matched is None:
            raise RemainingReqParsingError

        ret = {
            "group": matched.group(1),
            "min": int(matched.group(2)),
            "sec": int(matched.group(3)),
        }
        return ret
    except:
        raise RemainingReqParsingError


@error_handler
def _call_get(url: str, **kwargs: Any) -> Response:
    return requests.get(url, **kwargs)


@error_handler
def _call_post(url: str, **kwargs: Any) -> Response:
    return requests.post(url, **kwargs)


@error_handler
def _call_delete(url: str, **kwargs: Any) -> Response:
    return requests.delete(url, **kwargs)


def _call_public_api(url: str, **params: Any) -> Tuple[Any, Dict[str, Any]]:
    """Call Upbit public api

    Args:
        url (str): REST API url
        params (any): GET method parameters
    Returns:
        The contents of requested url, parsed remaining requests count info
    """
    resp = _call_get(url, params=params)
    data = resp.json()
    remaining_req = resp.headers.get("Remaining-Req", "")
    limit = _parse(remaining_req)
    return data, limit


def _send_post_request(
    url: str, headers: Dict[str, str], data: Dict[str, Any]
) -> Tuple[Any, Dict[str, Any]]:
    """Call POST method request for Upbit

    Args:
        url (str): REST API url
        headers (dict[str, str]): HTTP headers
        data (dict[str, any]): Data
    Returns:
        The contents of requested url, parsed remaining requests count info
    """
    resp = _call_post(url, headers=headers, data=data)
    data = resp.json()
    remaining_req = resp.headers.get("Remaining-Req", "")
    limit = _parse(remaining_req)
    return data, limit


def _send_get_request(
    url: str, headers: Dict[str, str], data: Dict[str, Any]
) -> Tuple[Any, Dict[str, Any]]:
    """Call GET method request for Upbit

    Args:
        url (str): REST API url
        headers (dict[str, str]): HTTP headers
        data (dict[str, any]): Data
    Returns:
        The contents of requested url, parsed remaining requests count info
    """
    resp = _call_get(url, headers=headers, data=data)
    data = resp.json()
    remaining_req = resp.headers.get("Remaining-Req", "")
    limit = _parse(remaining_req)
    return data, limit


def _send_delete_request(
    url: str, headers: Dict[str, str], data: Dict[str, Any]
) -> Optional[Tuple[Any, Dict[str, Any]]]:
    """Call DELETE method request for Upbit

    Args:
        url (str): REST API url
        headers (dict[str, str]): HTTP headers
        data (dict[str, any]): Data
    Returns:
        The contents of requested url, parsed remaining requests count info
    """
    resp = _call_delete(url, headers=headers, data=data)
    data = resp.json()
    remaining_req = resp.headers.get("Remaining-Req", "")
    limit = _parse(remaining_req)
    return data, limit
