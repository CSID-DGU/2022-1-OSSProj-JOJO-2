from dataclasses import field
from .models import FormModel
from django import forms
class URLform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control', 'ALIGN': 'center'})
    class Meta:
        model = FormModel
        fields = ["youtube_link","start_minute","start_second","end_minute","end_second"] # 일단 해상도 없이
    