# 분봉
# 1, 3, 5, 10, 15, 30, 60, 240분봉에 대해서 최대 200개 조회 가능
import pyupbit

# 1분봉 (최대 200개 요청가능)
minute1 = pyupbit.get_ohlcv("KRW-BTC", "minute1")
print(minute1)
print(type(minute1), minute1.shape)

# 3분봉 (최대 200개 요청가능)
minute3 = pyupbit.get_ohlcv("KRW-BTC", "minute3")
print(minute3)

# 5분봉 (최대 200개 요청가능)
minute5 = pyupbit.get_ohlcv("KRW-BTC", "minute5")
print(minute5)

# 10분봉 (최대 200개 요청가능)
minute10 = pyupbit.get_ohlcv("KRW-BTC", "minute10")
print(minute10)

# 30분봉 (최대 200개 요청가능)
minute30 = pyupbit.get_ohlcv("KRW-BTC", "minute30")
print(minute30)

# 60분봉 (최대 200개 요청가능)
minute60 = pyupbit.get_ohlcv("KRW-BTC", "minute60")
print(minute60)
