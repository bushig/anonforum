from django import forms

from captcha.fields import CaptchaField
from multiupload.fields import MultiFileField

from .models import MediaFile

class CreateThreadForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea)
    email = forms.EmailField(required=False)
    board = forms.CharField(required=True)
    is_op = forms.BooleanField(required=False)
    captcha = CaptchaField()


class MediaUpload(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ('file',)
    file = forms.ImageField(required=False)
    # file = MultiFileField(min_num=0, max_num=3, max_file_size=1024*1024*10)
