from django.shortcuts import render
from .forms import URLform
from django.views import View

import os
import youtube_dl
from moviepy.editor import *

from django.http import FileResponse, response
from django.core.files.storage import FileSystemStorage

# Create your views here.
class MainView(View): 
    # template_name = 'gif_to_mp4/main.html'
    template_name = 'gif_to_mp4/index.html'

    def get(self, request):
        form = URLform()
        ctx = {'form':form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = URLform(request.POST)
        ctx = {'form':form}

        start = 0
        end = 0
        if form.is_valid():
            url = form.cleaned_data.get("youtube_link")
            start_min = form.cleaned_data.get("start_minute")
            start_sec = form.cleaned_data.get("start_second")
            end_min = form.cleaned_data.get("end_minute")
            end_sec = form.cleaned_data.get("end_second")
            resolution = form.cleaned_data.get("resolution")
            print("form valid", url, start_min,start_sec,end_min,end_sec,resolution)
        else:
            return render(request, self.template_name,ctx)

        ss = f"00:{start_min:02}:{start_sec:02}.00"
        to = f"00:{end_min:02}:{end_sec:02}.00"

        if os.path.exists('video.gif'):
            os.remove('video.gif')

        title = "video"

        ydl_opts = {
            'format': "best",
            'videoformat' : "mp4",
            'outtmpl' : "video.mp4",
            'external_downloader': 'ffmpeg',
            'external_downloader_args':  ["-ss", ss, "-to", to]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            #title = ydl.extract_info(url, download=False)['title']

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

        return response
    

