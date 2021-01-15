
from django import forms

class QnaForm(forms.Form):
    question = forms.CharField(max_length=200, required=True)
    answer = forms.CharField(max_length=500, required=True)
