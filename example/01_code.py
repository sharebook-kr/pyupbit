# Quatation API
# 시세 종목 조회
import pyupbit

# 업비트의 모든 티커목록 출력
tickers = pyupbit.get_tickers()
print(tickers)
print(len(tickers))

# 원화 시장의 티커목록 출력
krw_tickers = pyupbit.get_tickers("KRW")
print(krw_tickers)
print(len(krw_tickers))

btc_tickers = pyupbit.get_tickers("BTC")
print(btc_tickers)
print(len(btc_tickers))

usdt_tickers = pyupbit.get_tickers("USDT")
print(usdt_tickers)
print(len(usdt_tickers))
