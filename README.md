

# youtube link 입력만으로 GIF를 만들어주는 사이트

  
## 사용한 오픈소스 및 툴
* [Youtube-dl](https://github.com/ytdl-org/youtube-dl)
* [Moviepy](https://github.com/Zulko/moviepy)
* [celery](https://github.com/celery/celery)
* [Rabbitmq](https://github.com/rabbitmq/rabbitmq-server)
* [FFmepeg](https://github.com/FFmpeg/FFmpeg)
* Django
* Nginx
* AWS EC2
* Ubuntu

## 시스템 구조

![](https://velog.velcdn.com/images/l_cloud/post/0426d824-c71d-4cc4-8107-fcb857f14f28/image.png)

&nbsp;

> web server는 NGINX를 사용하였습니다. <Br>
websocket 통신은 위해 Daphne를 사용하였습니다. <Br>
Youtube 다운을 비동기로 하기 위해 celery를 사용하였습니다. <Br>
celery의 메세지 브로커로는 Rabbitmq를 사용하였습니다.

&nbsp;
### 동작방식

1. user가 url로 들어와서 HTTP Get 요청을 한다.
2. user가 입력한 값이 적절한지 확인하고 적절하면 websocket으로 내용을 보내고 아니라면 alert 창을 보낸다.
3. ws:// 으로 들어오면 Nginx가 Daphne로 연결하여 Django websocket과 연결 될 수 있게 해줍니다.
4. Django는 입력값을 바탕으로 celery로 Youtube 다운로드를 비동기로 처리합니다.
5. user는 일정 시간마다 websocket으로 다운로드 되고 있는 상태를 요청하고 Django는 진행 상태를 user에게 알려줍니다.
6. 다운로드가 완료되면 gif file을 return 합니다.

입력값은 1초 이상 6초 미만입니다. <Br>
이 범위를 넘어갈 경우 안내 문구가 등장합니다.



&nbsp;


## 동작화면 

&nbsp;

### 1. 화면
![](https://velog.velcdn.com/images/l_cloud/post/8b5a0af6-4faa-4899-aac4-5e719928a34c/image.png)

&nbsp;

### 2. 입력값 초과

![](https://velog.velcdn.com/images/l_cloud/post/e7c7248f-ec22-4ad9-8348-890641f94f19/image.png)
![](https://velog.velcdn.com/images/l_cloud/post/cff26a56-c5e1-43aa-ae6e-e269ff9ab415/image.png)

&nbsp;

### 3. 다운로드 및 완료

![자바 스크립트 console로 상태 확인 가능](https://velog.velcdn.com/images/l_cloud/post/d3302448-8676-4058-920a-d9b122349fa9/image.png)

![](https://velog.velcdn.com/images/l_cloud/post/1c5a0604-c3a3-4e62-a9f9-941ab9405370/image.png)


&nbsp;


 
## 간략한 코드로 보는 동작 방식

 <Br>

#### 1. URL로 들어오면 Get 요청에 대한 응답

```python
# urls.py URL 확인 후 올바른 view로 가도록 지시
...
urlpatterns = [
    path('',views.MainView.as_view(), name = 'home'),
    ...
# Views.py 
...
class MainView(View): 
    template_name = 'gif_to_mp4/index.html'

    def get(self, request):
        form = URLform()
        ctx = {'form':form}
        return render(request, self.template_name, ctx)
    ...

```

#### 2. User에서 웹소켓 연결

```javascript
# 웹소켓 연결
const GifSocket = new WebSocket(
  'ws://'
  + window.location.host + ":8000"
  + '/'
);
# Youtube 링크 및 정보 server에 보내는 코드
function clickSubmit(this1){
  var url = document.querySelector('#youtube_link').value;
  var s_m = document.querySelector('#start_minute').value;
  var s_s = document.querySelector('#start_second').value;
  var e_m = document.querySelector('#end_minute').value;
  var e_s = document.querySelector('#end_second').value;
  var diff = 60 * e_m + e_s - (60 * s_m + s_s)
  console.log(diff)
  if (5 < diff){
    alert("최대 변환 길이는 5초 입니다")
    document.getElementById("message").textContent = "최대 변환 길이는 5초 입니다.";
  }else if (diff < 0){
    alert("1초 이상의 값을 입력해 주세요.")
    document.getElementById("message").textContent = "1초 이상의 값을 입력해 주세요.";
  }else if (diff < 6 && 0 < diff){
    spinner.style.visibility = 'visible';
    document.getElementById("submitButton").disabled = true;
    console.log("form 보냄 socekt도 보냄")
    GifSocket.send(data = JSON.stringify({
      'status' : '',
      'youtube_link' : url,
      'start_minute': s_m,
      'start_second' : s_s,
      'end_minute' : e_m,
      'end_second' : e_s
    }))
    // this1.form.submit(); 그냥 socket으로 처리
    document.getElementById("message").textContent = "동영상을 다운로드 중 입니다.  새로고침을 하지 말아주세요";
    this1.form.reset();
  }
  else{
    alert("올바른 값을 입력해 주세요")
    document.getElementById("message").textContent = "올바른 값을 입력해 주세요";
  }
}
```
#### 3. Server에서 websocket 응답 처리

```python
# routing.py 일부 소켓 path에 따른 연결 정보 처리
websocket_urlpatterns = [
    re_path(r'', sockets.GifConsumer.as_asgi()),
# sockets.py 일부 메세지 받으면 다운로드 처리
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
            ...
```

#### 4.Youtube download celery를 통한 비동기 처리

```python
# task.py
...
@shared_task() 
def downloand_video(data):
    try:
        data = json.loads(data)
        url, ss ,to = data['url'], data['ss'],data['to']

        if os.path.exists('video.mp4'):
            os.remove('video.mp4')

        if os.path.exists('video.gif'):
            os.remove('video.gif')

        ydl_opts = {
            'format': "best",
            'videoformat' : "mp4",
            'outtmpl' : "video.mp4",
            'external_downloader': 'ffmpeg',
            'external_downloader_args':  ["-ss", ss, "-to", to],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        title = "video"
        clip = VideoFileClip(title + '.mp4')
        clip.write_gif(title + '.gif')
        clip.close()
    except:
        raise Ignore()
        
```

#### 5. client의 다운로드 상태확인 요청과 그 응답

```javascript
function send_message(){
  GifSocket.send(data = JSON.stringify({
    'status' : 'yes'
  }))
}
... 
    # 메세지 확인하며 상태에 따라 보내느 함수 일부
    sleep(6000);
    send_message();
    console.log("status 물어보는 중")
```

server의 응답
```python
if self.t and self.t.ready(): # 작업 끝
                self.send(text_data = json.dumps({
                    'message': "Done" # 완료 메세지
                }))
            else: # 작업 진행 중
                self.send(text_data = json.dumps({
                    'message': "Doing"
                }))


```
#### 6. 다운로드 완료 후 그 응답
client
```javascript
if (data.message == 'Done'){
    window.location = 'gif'; # gif 요청
    document.getElementById("submitButton").disabled = false;
    document.getElementById("message").textContent = "동영상이 모두 다운로드 되었습니다!";
    spinner.style.visibility = 'hidden';
```

server
```python
def gif(request):
    title = 'video'
    file_path = os.path.abspath("./")
    file_name = os.path.basename("./" + title + ".gif")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type='image/gif')
    response['Content-Disposition'] = f'attachment; filename=video.gif'
    return response
```
  

### Linux systemctl Demon 설정 파일 및 설명


&nbsp;

*Uwsgi*

```ini
[Unit]
Description=uWSGI service
After=syslog.target
 
[Service]
# 가상환경 path // 프로젝트 위치
ExecStart=/home/ubuntu/venv/bin/uwsgi -i /srv/2022-1-OSSProj-JOJO-2/OSSP_GIF/.config/uwsgi/mysite.ini
 
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all
 
[Install]
WantedBy=multi-user.target
```

&nbsp;

*Nginx*
``` ini
server {
    listen 80;
    server_name *.compute.amazonaws.com;
    charset utf-8;
    client_max_body_size 128M;

    location / {
        uwsgi_pass  unix:///tmp/mysite.sock;
        include     uwsgi_params;
    }
    location /ws {
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_pass http://127.0.0.1:8000; #websocket port 번호
    }
    location /static/{
      alias  /srv/2022-1-OSSProj-JOJO-2/OSSP_GIF/static/; # static 파일 위치
    }
}
```

&nbsp;

*Daphne*
``` ini
[Unit]
Description=daphne daemon

[Service]
User=root 
Group=root
# 프로젝트 위치
WorkingDirectory=/srv/2022-1-OSSProj-JOJO-2/OSSP_GIF

Environment="DJANGO_SETTINGS_MODULE=OSSP_GIF.settings"
# Daphne 명령어 위치 & 포트번호 & asgi위치
ExecStart=/home/ubuntu/venv/bin/daphne -b 0.0.0.0 -p 8000 OSSP_GIF.asgi:application

ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s TERM $MAINPID
Restart=on-abort
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```
 
&nbsp;

*celery*
```python
import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OSSP_GIF.settings')
# broker로 무엇을 사용할지 설정 backend는 Django-db 사용
app = Celery('OSSP_GIF',broker='pyamqp://')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()
app.conf.update(
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'], 
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Seoul',
    CELERY_ENABLE_UTC=False,
    CELERYD_CONCURRENCY=1, # cpu 갯수에 따라 조정 가능 aws ec2 기본은 1로 설정
)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
```

&nbsp;


&nbsp;

## Team
&nbsp;

* [백종록](https://github.com/L-cloud) 배포 및 백엔드
* [김상윤](https://github.com/sangyun0904) 백엔드
* [장지욱](https://github.com/jjwk28) 프론트

&nbsp;

&nbsp;

## License

* [GNU GENERAL PUBLIC LICENSE](https://github.com/CSID-DGU/2022-1-OSSProj-JOJO-2/blob/main/LICENSE.md)
