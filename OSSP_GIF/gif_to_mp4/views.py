from django.shortcuts import render
from .forms import URLform
from django.views import View

import youtube_dl

# Create your views here.
class MainView(View): 
    template_name = 'gif_to_mp4/main.html'

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

        ss = f"-ss 00:{start_min:02}:{start_sec:02}.00"
        to = f"-to 00:{end_min:02}:{end_sec:02}.00"
        print(ss, to)

        ydl_opts = {
            'external_downloader': 'ffmpeg',
            'external_downloader_args':  ss + " " + to,
            '0': "%(format_id)s.%(resolution)s.%(id)s.v2.%(ext)s",
            'format': "best"
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        ctx = {'form':form, 'start':start, 'end':end}
        return render(request, self.template_name,ctx)