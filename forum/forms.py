from django import forms



class CreateThreadForm(forms.Form):
    text = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    board = forms.CharField(required=True)
    is_op = forms.BooleanField(required=False)
