/*!
* Start Bootstrap - Landing Page v6.0.5 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// 로딩 화면 구현할 경우 수정

var submitFlag = false;

// socket 유지 시켜야함 새로 get 해도..?
const GifSocket = new WebSocket(
  'ws://'
  + window.location.host
);

GifSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  if (data.message == 'Done'){
    // $.fileDownload('gif'); 파일 다운로드 안 되는데 이건 좀 더 찾아보자
    window.location ='gif'

  }
};

// function submitCheck() {
//   if(submitFlag) {
//     return submitFlag;
//   }else{
//     submitFlag = true;
//     return false;
//   }
// }


function clickSubmit(this1){
  // if(submitCheck()){
  //   return;
  // }
  console.log("여기 됨")
  var url = document.querySelector('#youtube_link').value;
  var s_m = document.querySelector('#start_minute').value;
  var s_s = document.querySelector('#start_second').value;
  var e_m = document.querySelector('#end_minute').value;
  var e_s = document.querySelector('#end_second').value;
  console.log("var 로 는 다 받음")
  var diff = 60 * e_m + e_s - (60 * s_m + s_s)
  console.log(diff)
  if (5 < diff){
    alert("최대 변환 길이는 5초 입니다")
  }else if (diff < 0){
    alert("1초 이상의 값을 입력해 주세요.")
  }else{
    console.log("form 보냄 socekt도 보냄")
    GifSocket.send(data = JSON.stringify({
      'youtube_link' : url,
      'start_minute': s_m,
      'start_second' : s_s,
      'end_minute' : e_m,
      'end_second' : e_s
    }))
    sleep(1000);
    this1.form.submit();
    this1.form.reset();
  }
}

