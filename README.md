

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



## Team
&nbsp;

* [백종록](https://github.com/L-cloud) 배포 및 백엔드
* [김상윤](https://github.com/sangyun0904) 백엔드
* [장지욱](https://github.com/jjwk28) 프론트

&nbsp;

&nbsp;

## License

* [GNU GENERAL PUBLIC LICENSE](https://github.com/CSID-DGU/2022-1-OSSProj-JOJO-2/blob/main/LICENSE.md)
