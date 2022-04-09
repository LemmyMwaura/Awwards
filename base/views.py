from .models import Project, Profile, Rating 
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages 

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    projects = Project.objects.filter(
        Q(title__icontains = q) |
        Q(description__icontains = q) |
        Q(user_project__user_profile__username__icontains = q)
    )

    context = {'projects': projects }
    return render(request, 'base/home.html', context)

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        messages.success(request, 'Already Logged in')
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(e)
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist.')

    context={ 'page':page }
    return render(request, 'base/login_register.html', context)

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('home')

def register_user(request):
    page = 'register'
    form = UserCreationForm

    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'An error occured during registration')
    except Exception as e:
        print(e)
        messages.error('Something went wrong. Probably a connection issue. Try again')

    context = { 'page':page, 'form':form }
    return render(request, 'base/login_register.html', context)

def profile(request,pk):
    user = Profile.objects.get(id=pk)
    projects = user.project_set.all()
    followers = user.followers.all()
    following = user.following.all()

    context = { 'user':user, 'projects':projects, 'followers':followers, 'following':following }
    return render(request, 'base/profile.html', context)
