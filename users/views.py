from django.shortcuts import render, redirect
from users.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    return render(request, "success.html", {})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_index(request):
    users = User.objects.all()
    context = {
        'users' : users
    }
    return render(request, 'user_index.html', context)

def user_detail(request, pk):
    user = User.objects.get(pk = pk)
    context = {
        'user' : user
    }
    return render(request, 'user_detail.html', context)