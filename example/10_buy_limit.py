import pyupbit 
import pprint

f = open("../upbit.txt", "r")
lines = f.readlines()
f.close()

access = lines[0].strip()
secret = lines[1].strip()

upbit = pyupbit.Upbit(access, secret)
resp = upbit.buy_limit_order("KRW-XRP", 500, 20)
pprint.pprint(resp)
