import json
from channels.generic.websocket import WebsocketConsumer
from .tasks import downloand_video
from asgiref.sync import async_to_sync

import os


os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
class GifConsumer(WebsocketConsumer):
    t = None
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        # 어디에다가 보내지는거지? 한 번 확인 해봐야지
        self.send(text_data = json.dumps({
                    'message': "Doing"
        }))
        pass
    def receive(self, text_data):   
        data_json = json.loads(text_data)
        if not data_json['status']:
            print(data_json['status'])
            url = data_json["youtube_link"]
            start_min = int(data_json["start_minute"])
            start_sec = int(data_json["start_second"])
            end_min = int(data_json["end_minute"])
            end_sec = int(data_json["end_second"])
            # print(start_min,type(start_min))
            ss = f"00:{start_min:02}:{start_sec:02}.00"
            to = f"00:{end_min:02}:{end_sec:02}.00"
            dic = {'url' : url, "ss" : ss, "to" : to}
            data = json.dumps(dic, indent = 4)
            self.t = downloand_video.delay(data) # celery
            self.send(text_data=json.dumps({
                'message': "Doing"
            }))
        else:
            if self.t and self.t.ready(): # 작업 끝
                self.send(text_data = json.dumps({
                    'message': "Done"
                }))
            else:
                self.send(text_data = json.dumps({
                    'message': "Doing"
                }))



