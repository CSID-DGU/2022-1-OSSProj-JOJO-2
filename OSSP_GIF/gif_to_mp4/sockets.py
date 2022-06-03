import json
from time import sleep
from channels.generic.websocket import WebsocketConsumer
import asyncio # 쓰레드 1개로 비동기
from .tasks import downloand_video

class GifConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass
    # 여기서 만약 비동기 안 쓰면 새로운 요청 못 받는 거니까

    def receive(self, text_data):
        print("receive 함")
        data_json = json.loads(text_data)
        url = data_json["youtube_link"]
        start_min = int(data_json["start_minute"])
        start_sec = int(data_json["start_second"])
        end_min = int(data_json["end_minute"])
        end_sec = int(data_json["end_second"])
        print(start_min,type(start_min))
        ss = f"00:{start_min:02}:{start_sec:02}.00"
        to = f"00:{end_min:02}:{end_sec:02}.00"
        dic = {'url' : url, "ss" : ss, "to" : to}
        data = json.dumps(dic, indent = 4)
        t = downloand_video.delay(data) # celery
        # 여기 너무 비효율 적인데.. 이걸 어떻게 하면 aysnc 하게 바꿀 수 있을까
        # py-script도 확인 해야함
        # javascript log도 변경 하고 convert 버튼 막는 것도 해야함
        #
        while not t.ready(): 
            print("나 확인 중")
            sleep(3)
        self.send(text_data=json.dumps({
            'message': "Done"
        }))
    


