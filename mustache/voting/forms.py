# forms.py
from django import forms
from voting.models import Gentleman

class LoginForm(forms.Form):
	username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Your name','class':'form-control'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Secret phrase only you will know','class':'form-control'}))

class SignupForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Your username','class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Secret phrase only you will know','class':'form-control'}))
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Name to use for the contest','class':'form-control'}))
    tagline = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder':'Your tagline','class':'form-control'}))
    before_pic = forms.ImageField()

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Gentleman
		fields = ('name', 'tagline', 'before_pic', 'after_pic')

		widgets = {
			'name': forms.TextInput(attrs={'placeholder':'Name to use for the contest','class':'form-control'}),
			'tagline': forms.TextInput(attrs={'placeholder':'Your tagline','class':'form-control'})
		}