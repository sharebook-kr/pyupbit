import pytest

from pyupbit.exchange_api import *


@pytest.mark.parametrize(
        "expected_output,actual_inputs",
        [
            # quote (hoga) >= 2000000
            (2000000, (2000100, 2000900)),
            # quote (hoga) >= 1000000
            (1000000, (1000100, 1000400)),
            # quote (hoga) >= 500000
            (500000, (500010, 500090)),
            # quote (hoga) >= 100000
            (100000, (100010, 100040)),
            # quote (hoga) >= 10000
            (10000, (10001, 10004)),
            # quote (hoga) >= 1000
            (1001, (1001.1, 1001.4)),
            # quote (hoga) >= 100
            (101.2, (101.21, 101.29)),
            # quote (hoga) >= 10
            (10.31, (10.314, 10.318)),
            # quote (hoga) >= 1
            (2.577, (2.5775, 2.57709)),
            # quote (hoga) >= 0.1
            (0.1728, (0.17286, 0.17287)),
            # quote (hoga) >= 0.01
            (0.01, (0.010001, 0.010006)),
            # quote (hoga) >= 0.001
            (0.001, (0.0010009, 0.0010007)),
            # quote (hoga) >= 0.0001
            (0.0002, (0.00020001, 0.000200012)),
            # quote (hoga) >= 0.00001 ("else")
            (0.00008002, (0.000080023, 0.000080024)),
        ])
def test_get_tick_size_defaults(expected_output, actual_inputs):
    """
    Given: expected output and actual inputs
    When: every actual input is passed to get_tick_size(..)
    Then: indeed expected_output == get_tick_size(actual_input)
    , consistent with https://docs.upbit.com/docs/market-info-trade-price-detail (v 1.4.4)
    """
    for actual_input in actual_inputs:
        assert expected_output == get_tick_size(actual_input)
