from dataclasses import field
from .models import FormModel
from django import forms
class URLform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control form-control-lg', 'ALIGN': 'center'})
    
    class Meta:
        model = FormModel
        fields = ["youtube_link","start_minute","start_second","end_minute","end_second","resolution"] # 일단 해상도 없이
        widgets = {
            'youtube_link': forms.URLInput(
                attrs={
                    'placeholder': "https://www.youtube.com",
                    'autocomplete': "off",
                    'id' : 'youtube_link'
                }
            ),
            'start_minute': forms.NumberInput(
                attrs={
                    'placeholder': "분(시작)",
                    'id' : "start_minute"
                }
            ),
            'start_second': forms.NumberInput(
                attrs={
                    'placeholder': "초(시작)",
                    'id' : 'start_second'
                }
            ),
            'end_minute': forms.NumberInput(
                attrs={
                    'placeholder': "분(끝)",
                    'id':'end_minute'
                }
            ),
            'end_second': forms.NumberInput(
                attrs={
                    'placeholder': "초(끝)",
                    'id' : 'end_second'
                }
            ),
        }
    