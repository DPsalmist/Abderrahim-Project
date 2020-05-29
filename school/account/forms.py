from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username','first_name', 'last_name', 'email', )


class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('date_of_birth', 'photo','gender', 'nationality', \
		 'phone_number', 'address', 'course', 'description') 

class UserRegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', 
								widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat password',
								widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'email')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password'] != cd['password2']:
			raise forms.ValidationError('passwords don\'t match!')
		return cd['password2']

class LoginForm(forms.Form):
	username = forms.CharField(label='Enter your username or email')
	password = forms.CharField(label='Enter your password', widget=forms.PasswordInput)