# Quatation API
# 시세 종목 조회
import pyupbit

tickers = pyupbit.get_tickers()
print(tickers)
print(len(tickers))

krw_tickers = pyupbit.get_tickers("KRW")
print(krw_tickers)
print(len(krw_tickers))

btc_tickers = pyupbit.get_tickers("BTC")
print(btc_tickers)
print(len(btc_tickers))

eth_tickers = pyupbit.get_tickers("ETH")
print(eth_tickers)
print(len(eth_tickers))
