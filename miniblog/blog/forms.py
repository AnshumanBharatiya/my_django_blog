from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Post

class SignupForm(UserCreationForm):
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-control'}))
	password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']
		labels = {'username':'User Name','first_name':'First Name','last_name':'Last Name','email':'Email Id'}
		widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
		'first_name':forms.TextInput(attrs={'class':'form-control'}),
		'last_name':forms.TextInput(attrs={'class':'form-control'}),
		'email':forms.TextInput(attrs={'class':'form-control'})}


class LoginForm(AuthenticationForm):
	username = UsernameField(label="Enter User Name", strip=False, widget=forms.TextInput(attrs={'class':'form-control','autofocus':True}))
	password = forms.CharField(label="Enter Password", strip=False, widget=forms.PasswordInput(attrs={'class':'form-control', 'autocomplete':'current-password'}))
	class Meta:
		model = User
		labels = {'username':'User Name'}
		widgets = {'username':forms.TextInput(attrs={'class':'form-control'})}


class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ['title','desc']
		labels = {'title':'Enter Title', 'desc':'Enter Description'}
		widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),
					'desc':forms.Textarea(attrs={'class':'form-control'})}