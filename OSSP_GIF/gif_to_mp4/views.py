from django.shortcuts import render
from .forms import URLform
from django.views import View
# Create your views here.
class MainView(View): # 회원가입 하는 View
    template_name = 'gif_to_mp4/main.html'

    def get(self, request):
        form = URLform()
        ctx = {'form':form}
        return render(request, self.template_name, ctx)

    def post(self, request):
        form = URLform(request.POST)
        ctx = {'form' : form}
        return render(request, self.template_name, ctx)