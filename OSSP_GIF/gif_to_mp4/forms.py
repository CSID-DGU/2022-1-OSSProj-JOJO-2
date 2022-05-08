from django import forms

class URLform(forms.Form):
    youtube_link = forms.URLField(label='유투브 링크', required=True)
    start_minute = forms.IntegerField(label="분(시작)")
    start_second = forms.IntegerField(label="초(시작)")
    end_miute = forms.IntegerField(label ="분 (끝)")
    end_second = forms.IntegerField(label = "초 (끝)")