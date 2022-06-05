from django.urls import path
from . import views
app_name = 'gif_to_mp4'
urlpatterns = [
    path('',views.MainView.as_view(), name = 'home'),
    path('gif',views.gif, name = 'gif'),

]