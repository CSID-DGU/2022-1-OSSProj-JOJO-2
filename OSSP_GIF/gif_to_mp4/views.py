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
            start = form.cleaned_data.get("start_minute")*60 + form.cleaned_data.get("start_second")
            end = form.cleaned_data.get("end_minute")*60 + form.cleaned_data.get("end_second")
        print(start, end)

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        ctx = {'form':form, 'start':start, 'end':end}
        return render(request, self.template_name,ctx)