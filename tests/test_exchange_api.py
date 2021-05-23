from pyupbit.quotation_api import get_tickers
import pytest
from pyupbit.exchange_api import *


def test_get_tick_size_defaults():
    # hoga >= 2000000
    assert 2000000 == get_tick_size(2000100) 
    assert 2000000 == get_tick_size(2000900) 
    # hoga >= 1000000
    assert 1000000 == get_tick_size(1000100) 
    assert 1000000 == get_tick_size(1000400) 
    # hoga >= 500000
    assert 500000 == get_tick_size(500010) 
    assert 500000 == get_tick_size(500090) 
    # hoga >= 100000
    assert 100000 == get_tick_size(100010) 
    assert 100000 == get_tick_size(100040) 
    # hoga >= 10000
    assert 10000 == get_tick_size(10001) 
    assert 10000 == get_tick_size(10004) 
    # hoga >= 1000
    assert 1000 == get_tick_size(1001) 
    assert 1000 == get_tick_size(1004) 
    # hoga >= 100
    assert 101 == get_tick_size(101.1) 
    assert 104 == get_tick_size(104.9) 
    # hoga >= 10
    assert 10.1 == get_tick_size(10.11) 
    assert 10.1 == get_tick_size(10.19) 
    # hoga >= 0
    assert 0.01 == get_tick_size(0.011) 
    assert 0.01 == get_tick_size(0.019) 


