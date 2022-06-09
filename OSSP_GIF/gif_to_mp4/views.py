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
        return render(request, self.template_name, ctx)


def gif(request):
    title = 'video'
    # os.remove('video.mp4')
    # file_path = os.path.abspath("./")
    # file_name = os.path.basename("./" + title + ".mp4")
    # fs = FileSystemStorage(file_path)
    # response = FileResponse(fs.open(file_name, 'rb'),
    #                         content_type='video/mp4')
    file_path = os.path.abspath("./")
    file_name = os.path.basename("./" + title + ".gif")
    fs = FileSystemStorage(file_path)
    response = FileResponse(fs.open(file_name, 'rb'),
                            content_type='image/gif')
    response['Content-Disposition'] = f'attachment; filename=video.gif'
    return response