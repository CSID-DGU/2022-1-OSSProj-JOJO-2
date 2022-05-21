from django.shortcuts import render
from .forms import URLform
from django.views import View

import youtube_dl
import moviepy

# Create your views here.
class MainView(View): 
    template_name = 'gif_to_mp4/main.html'

    def my_hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    def get(self, request):
        form = URLform()
        ctx = {'form':form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = URLform(request.POST)
        print(form['youtube_link'].value())
        #print(form['your_name'])
        #ctx = {'form':form}

        start = 0
        end = 0
        if form.is_valid():
            url = form.cleaned_data.get("youtube_link")
            start_min = form.cleaned_data.get("start_minute")
            start_sec = form.cleaned_data.get("start_second")
            end_min = form.cleaned_data.get("end_minute")
            end_sec = form.cleaned_data.get("end_second")

        ss = f"00:{start_min:02}:{start_sec:02}.00"
        to = f"00:{end_min:02}:{end_sec:02}.00"

        filename = "video.mp4"

        ydl_opts = {
            'format': "best",
            'videoformat' : "mp4",
            'outtmpl' : filename,
            'external_downloader': 'ffmpeg',
            'external_downloader_args':  ["-ss", ss, "-to", to],
            'progress_hooks': [my_hook]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        ctx = {'form':form, 'start':start, 'end':end}
        return render(request, self.template_name,ctx)
