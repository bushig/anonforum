from django import forms
from captcha.fields import CaptchaField


class CreateThreadForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea)
    email = forms.EmailField(required=False)
    board = forms.CharField(required=True)
    is_op = forms.BooleanField(required=False)
    captcha = CaptchaField()
