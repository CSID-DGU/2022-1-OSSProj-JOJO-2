from django.shortcuts import render,redirect
from .forms import URLform
from django.views import View
from django.contrib import messages
import os
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
# Create your views here.
class MainView(View): 
    template_name = 'gif_to_mp4/index.html'

    def get(self, request):
        form = URLform()
        ctx = {'form':form}
        # try:
        #     while not task_id.ready():
        #         print("기다리는중")
        #         if task_id.failed():
        #             messages.add_message(request,30, '오류가 발생했습니다 다시 시도해 주세요')
        #             return render(request, self.template_name, ctx)
        #     messages.add_message(request,30, '동영상이 모두 다운로드 되었습니다!')
        #     print("다 다운로드 됨")
        #     os.remove('video.mp4')
        #     file_path = os.path.abspath("./")
        #     file_name = os.path.basename("./" + title + ".gif")
        #     fs = FileSystemStorage(file_path)
        #     response = FileResponse(fs.open(file_name, 'rb'),
        #                             content_type='image/gif')
        #     response['Content-Disposition'] = f'attachment; filename=video.gif'
        #     # 여기서 return 하면 새로고침 할 때 계속 post라서 문제임.. 고쳐야함
        #     return response
        # except:
        #     print("task 로 안 들어옴")
        #     #print(task_id.ready())
        #     pass
        return render(request, self.template_name, ctx)

    def post(self, request):
        # 나중에 socket 잘 돌아가면 필요없는 것 지우기
        form = URLform(request.POST)
        ctx = {'form':form}
        if form.is_valid():
            start_min = form.cleaned_data.get("start_minute")
            start_sec = form.cleaned_data.get("start_second")
            end_min = form.cleaned_data.get("end_minute")
            end_sec = form.cleaned_data.get("end_second")
            diff =  60 * end_min + end_sec - (60 * start_min + start_sec)
            if diff <0 or 5 < diff:
                messages.add_message(request, 30, '시작 시간과 끝 시간의 차이를 1~5초 사이로 맞춰주세요')
                print(request)
                return render(request, self.template_name, ctx) 
        else:
            messages.add_message(request, 30, '입력값에 문제가 있습니다. 올바른 입력값을 넣어주십시오')
            return render(request, self.template_name,ctx)

        messages.add_message(request, 30, '유투브를 다운로드 중 입니다 <br/> 창을 닫거나 새로고침하지 말아주세요')
        return redirect('gif_to_mp4:home') 

def gif(request):
    title = 'video'
    # os.remove('video.mp4')
    file_path = os.path.abspath("./")
    file_name = os.path.basename("./" + title + ".mp4")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type='video/mp4')
    response['Content-Disposition'] = f'attachment; filename=video.mp4'
    return response