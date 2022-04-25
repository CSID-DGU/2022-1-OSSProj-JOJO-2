from django import forms

class URLform(forms.Form):
    your_name = forms.CharField(label='유투브 링크')
    start_point = forms.IntegerField(label="시작 시간")
    end_point = forms.IntegerField(label ="끝 시간")