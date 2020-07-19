import pyupbit

df = pyupbit.get_ohlcv("KRW-BTC", "month")
print(df)