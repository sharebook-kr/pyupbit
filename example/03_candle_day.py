# 일봉
import pyupbit

# 기본 요청시 200일 (최대)
df = pyupbit.get_ohlcv("KRW-BTC", "day")
print(df)

# 200개 미만의 경우 count 인자에 설정 가능
df = pyupbit.get_ohlcv("KRW-BTC", "day", count=10)
print(df)
