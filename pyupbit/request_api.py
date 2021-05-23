import re
import requests
import json
from pyupbit.errors import (UpbitError, 
                           TooManyRequests, 
                           raise_error, 
                           RemainingReqParsingError)

HTTP_RESP_CODE_START = 200
HTTP_RESP_CODE_END   = 400


def _parse_remaining_req(remaining_req):
    """parse the request limit data of the Upbit API

    Args:
        remaining_req (str): "group=market; min=573; sec=9" 

    Returns:
        dict: {'group': 'market', 'min': 573, 'sec': 2}
    """
    try:
        p = re.compile(r"group=([a-z\-]+); min=([0-9]+); sec=([0-9]+)")
        m = p.search(remaining_req)
        ret = {
            'group': m.group(1),
            'min': int(m.group(2)),
            'sec': int(m.group(3))
        }
        return ret
    except:
        raise RemainingReqParsingError


def _call_public_api(url, **params):
    """call get type api

    Args:
        url (str): REST API url 

    Returns:
        tuple: (data, req_limit_info) 
    """
    resp = requests.get(url, params=params)
    if HTTP_RESP_CODE_START <= resp.status_code < HTTP_RESP_CODE_END:
        remaining_req = resp.headers.get('Remaining-Req')
        limit = _parse_remaining_req(remaining_req)
        data = resp.json()
        return data, limit
    else:
        raise_error(resp)


def _send_post_request(url, headers=None, data=None):
    resp = requests.post(url, headers=headers, data=data)
    if HTTP_RESP_CODE_START <= resp.status_code < HTTP_RESP_CODE_END:
        remaining_req = resp.headers.get('Remaining-Req')
        limit = _parse_remaining_req(remaining_req)
        contents = resp.json()
        return contents,limit 
    else:
        raise_error(resp)


def _send_get_request(url, headers=None, data=None):
    resp = requests.get(url, headers=headers, data=data)
    if HTTP_RESP_CODE_START <= resp.status_code < HTTP_RESP_CODE_END:
        remaining_req = resp.headers.get('Remaining-Req')
        limit = _parse_remaining_req(remaining_req)
        contents = resp.json()
        return contents, limit 
    else: 
        raise_error(resp)


def _send_delete_request(url, headers=None, data=None):
    resp = requests.delete(url, headers=headers, data=data)
    if HTTP_RESP_CODE_START <= resp.status_code < HTTP_RESP_CODE_END:
        remaining_req = resp.headers.get('Remaining-Req')
        limit = _parse_remaining_req(remaining_req)
        contents = resp.json()
        return contents,limit 
    else:
        raise_error(resp)
