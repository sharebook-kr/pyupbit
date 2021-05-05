import websockets
import asyncio
import json
import uuid
import multiprocessing as mp


class WebSocketManager(mp.Process):
    """웹소켓을 관리하는 클래스

        사용 예제:

            >> wm = WebSocketManager("ticker", ["BTC_KRW"])
            >> for i in range(3):
                data = wm.get()
                print(data)
            >> wm.terminate()

        주의 :

           재귀적인 호출을 위해 다음의 guard를 반드시 추가해야 한다.
           >> if __name__ == "__main__"

    """
    def __init__(self, type: str, codes: list, qsize: int=1000):
        """웹소켓을 컨트롤하는 클래스의 생성자

        Args:
            type   (str           ): 구독 메시지 종류 (ticker/trade/orderbook)
            codes  (list          ): 구독할 암호 화폐의 리스트 [BTC_KRW, ETH_KRW, …]
            qsize  (int , optional): 메시지를 저장할 Queue의 크기
        """
        self.__q = mp.Queue(qsize)
        self.alive = False

        self.type = type
        self.codes = codes

        super().__init__()

    async def __connect_socket(self):
        uri = "wss://api.upbit.com/websocket/v1"
        async with websockets.connect(uri, ping_interval=60) as websocket:
            data = [{"ticket": str(uuid.uuid4())[:6]}, {"type": self.type, "codes": self.codes}]
            await websocket.send(json.dumps(data))

            while self.alive:
                recv_data = await websocket.recv()
                recv_data = recv_data.decode('utf8')
                self.__q.put(json.loads(recv_data))

    def run(self):
        self.__aloop = asyncio.get_event_loop()
        self.__aloop.run_until_complete(self.__connect_socket())

    def get(self):
        if self.alive == False:
            self.alive = True
            self.start()
        return self.__q.get()

    def terminate(self):
        self.alive = False
        super().terminate()


if __name__ == "__main__":
    wm = WebSocketManager("ticker", ["KRW-BTC",])
    for i in range(3):
        data = wm.get()
        print(data)
    wm.terminate()