from asyncio import tasks
from django.shortcuts import render,redirect
from .forms import URLform
from django.views import View
from django.contrib import messages
import json
from .tasks import downloand_video
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage
from moviepy.editor import *
import time
import os

# Create your views here.
class MainView(View): 
    template_name = 'gif_to_mp4/index.html'

    def get(self, request):
        form = URLform()
        ctx = {'form':form}
        try:
            while not task_id.ready():
               if task_id.failed():
                    messages.add_message(request,30, '오류가 발생했습니다 다시 시도해 주세요')
                    return render(request, self.template_name, ctx)
            messages.add_message(request,30, '동영상이 모두 다운로드 되었습니다!')
            title = "video"
            clip = VideoFileClip(title + '.mp4')
            clip.write_gif(title + '.gif')
            clip.close()
            os.remove('video.mp4')
            file_path = os.path.abspath("./")
            file_name = os.path.basename("./" + title + ".gif")
            fs = FileSystemStorage(file_path)
            response = FileResponse(fs.open(file_name, 'rb'),
                                    content_type='image/gif')
            response['Content-Disposition'] = f'attachment; filename=video.gif'
            # 여기서 return 하면 새로고침 할 때 계속 post라서 문제임.. 고쳐야함
            return response
        except:
            print("task 로 안 들어옴")
            #print(task_id.ready())
            pass
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = URLform(request.POST)
        ctx = {'form':form}
        if form.is_valid():
            url = form.cleaned_data.get("youtube_link")
            start_min = form.cleaned_data.get("start_minute")
            start_sec = form.cleaned_data.get("start_second")
            end_min = form.cleaned_data.get("end_minute")
            end_sec = form.cleaned_data.get("end_second")
            resolution = form.cleaned_data.get("resolution")
            diff =  60 * end_min + end_sec - (60 * start_min + start_sec)
            if diff <0 or 5 < diff:
                messages.add_message(request, 30, '시작 시간과 끝 시간의 차이를 1~5초 사이로 맞춰주세요')
                print(request)
                return render(request, self.template_name, ctx) 
        else:
            return render(request, self.template_name,ctx)
        ss = f"00:{start_min:02}:{start_sec:02}.00"
        to = f"00:{end_min:02}:{end_sec:02}.00"
        dic = {'url' : url, "ss" : ss, "to" : to}
        data = json.dumps(dic, indent = 4)
        global task_id 
        t = downloand_video.delay(data)
        print(t.ready())
        print(task_id.ready())
        messages.add_message(request, 30, '유투브를 다운로드 중 입니다 <br/> 창을 닫거나 새로고침하지 말아주세요')
        return redirect('gif_to_mp4:home') 
