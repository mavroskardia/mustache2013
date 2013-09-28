# forms.py
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(max_length=256, widget=forms.TextInput(attrs={'placeholder':'Your name','class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Secret phrase only you will know','class':'form-control'}))