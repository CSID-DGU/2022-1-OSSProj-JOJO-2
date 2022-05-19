from dataclasses import field
from .models import FormModel
from django import forms
class URLform(forms.ModelForm):
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields:
                self.fields[field].widget.attrs.update({'class': 'form-control', 'ALIGN': 'center'})
    choices=(("240" ,240),("360", 360),("480", 480),("720", 720))
    resolution = forms.ChoiceField(choices=choices)
    
    class Meta:
        model = FormModel
        fields = ["youtube_link","start_minute","start_second","end_minute","end_second","resolution"] # 일단 해상도 없이
        widgets = {
            'youtube_link': forms.URLInput(
                attrs={
                    'placeholder': "https://www.youtube.com",
                }
            ),
            'start_minute': forms.NumberInput(
                attrs={
                    'placeholder': '분(시작)'
                }
            ),
            'start_second': forms.NumberInput(
                attrs={
                    'placeholder': "초(시작)"
                }
            ),
            'end_minute': forms.NumberInput(
                attrs={
                    'placeholder': '분(끝)'
                }
            ),
            'end_second': forms.NumberInput(
                attrs={
                    'placeholder': "분(끝)"
                }
            ),
            # "resolution" : forms.NumberInput(
            #     attrs ={
            #         'placeholder': "해상도를 선택해주세요"
            #     },

            #     choices=(("240" ,240),("360", 360),("480", 480),("720", 720))
            # )

        }
    