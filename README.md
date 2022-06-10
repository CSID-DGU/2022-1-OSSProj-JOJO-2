

## youtube link 입력만으로 GIF를 만들어주는 사이트입니다.
---
&nbsp;
  
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
---
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

---

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

---

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

---

&nbsp;

## Team
&nbsp;

* [백종록](https://github.com/L-cloud) 배포 및 백엔드
* [김상윤](https://github.com/sangyun0904) 백엔드
* [장지욱](https://github.com/jjwk28) 프론트

&nbsp;

---

&nbsp;

## License

여기만 추가해 주세요
