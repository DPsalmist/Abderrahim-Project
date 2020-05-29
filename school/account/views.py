from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, UserRegistrationForm, \
					UserEditForm, ProfileEditForm
from django.contrib import messages
from .models import Profile

# Create your views here.
def index(request):
	return render (request, 'index.html')

def register (request):
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			# Create a new user object but avoid saving it yet
			new_user = user_form.save(commit=False)
			# Set the chosen password:using the set_password() allows encryption
			new_user.set_password(user_form.cleaned_data['password'])
			# Save the User object
			new_user.save()
			# Create the user profile
			Profile.objects.create(user=new_user)
			return render (request,
							'account/register_done.html', {'new_user':new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'account/register.html', {'user_form':user_form})


@login_required
def edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileEditForm(instance=request.user.profile,
										data = request.POST,
										files = request.FILES)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()
			messages.success(request, f'Profile updated successfully!')
		else: 
			messages.warning(request, f'Error updating your profile')
	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileEditForm(instance=request.user.profile)

	return render(request, 'account/edit.html',
							{'user_form':user_form,
							'profile_form':profile_form})


@login_required
def dashboard(request):
	return render(request, 'account/dashboard.html',{'section':'dashboard'})

