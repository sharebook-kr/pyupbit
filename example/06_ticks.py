import requests

url = "https://api.upbit.com/v1/trades/ticks?market=KRW-BTC&count=300"
resp = requests.get(url)
ticks = resp.json()

for tick in ticks:
    print(tick)
