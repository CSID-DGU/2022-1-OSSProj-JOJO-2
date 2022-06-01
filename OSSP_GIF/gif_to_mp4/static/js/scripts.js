/*!
* Start Bootstrap - Landing Page v6.0.5 (https://startbootstrap.com/theme/landing-page)
* Copyright 2013-2022 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-landing-page/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

// 로딩 화면 구현할 경우 수정
var submitFlag = false;

function submitCheck() {
  if(submitFlag) {
    return submitFlag;
  }else{
    submitFlag = true;
    return false;
  }
}

function clickSubmit(this1){
  if(submitCheck()){
    return;
  }
  this1.form.submit();
  this1.form.reset();
}