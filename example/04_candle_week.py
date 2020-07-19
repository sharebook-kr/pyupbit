# 주봉
import pyupbit

# 기본 요청시 200개
df = pyupbit.get_ohlcv("KRW-BTC", "week")
print(df)
