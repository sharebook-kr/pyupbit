import pyupbit 
import pprint

f = open("../upbit.txt", "r")
lines = f.readlines()
f.close()

access = lines[0].strip()
secret = lines[1].strip()

upbit = pyupbit.Upbit(access, secret)
uuid = '116d25b3-37ba-4687-bdcb-e3d09a8675b3'  # 취소하고자하는 주문의 uuid
resp = upbit.cancel_order(uuid)
pprint.pprint(resp)