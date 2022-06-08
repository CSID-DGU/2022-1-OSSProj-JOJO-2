/*!
* Start Bootstrap - Landing Page v6.0.5 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// 로딩 화면 구현할 경우 수정
var downloading = false;
const GifSocket = new WebSocket(
  'ws://'
  + window.location.host
);
GifSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  if (data.message == 'Done'){
    window.location = 'gif';
    document.getElementById("submitButton").disabled = false;
    downloading = true
    document.getElementById("message").textContent = "동영상이 모두 다운로드 되었습니다!";
    spinner.style.visibility = 'visible';
  }else{
    sleep(6000);
    send_message();
    console.log("status 물어보는 중")  
  }
};

function clickSubmit(this1){
  document.getElementById("submitButton").disabled = true;
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
    downloading = true;
    document.getElementById("message").textContent = "동영상을 다운로드 중 입니다.  새로고침을 하지 말아주세요";
    this1.form.reset();
  }
  else{
    alert("올바른 값을 입력해 주세요")
    document.getElementById("message").textContent = "올바른 값을 입력해 주세요";

  }
}
function sleep(ms) {
  const wakeUpTime = Date.now() + ms;
  while (Date.now() < wakeUpTime) { continue }
}
function send_message(){
  GifSocket.send(data = JSON.stringify({
    'status' : 'yes'
  }))
}