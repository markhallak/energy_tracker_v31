from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_control

from users.models import User
from .forms import CustomUserCreationForm
from .forms import UpdateUserForm


# Create your views here.

@login_required
def home(request):
    return redirect(to='/dashboard')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=username, password=password)
            login(request, user)
            messages.success(request, 'You have been registered sucessfully, now update your profile')
            return redirect('user_profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_index(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'user_index.html', context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_detail(request, pk):
    user = User.objects.get(pk=pk)
    context = {
        'user': user
    }
    return render(request, 'user_detail.html', context)


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        # profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid():  # and profile_form.is_valid():
            user_form.save()
            # profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user_profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        # profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'user_profile.html', {'user_form': user_form})
    # return render(request, 'user_profile.html')
