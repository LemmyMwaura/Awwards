from .models import Project, Profile, Rating 
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages 
from .forms import ProjectForm, UserRegistrationForm

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
    form =  UserRegistrationForm

    try:
        if request.method == 'POST':
            form = UserRegistrationForm(request.POST)
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

def submit_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid:
            user = form.save(commit=False)
            user.user_project_id = request.user.id
            user.save()
            return redirect('home')

    context = { 'form': form }
    return render(request, 'base/submit_project_form.html', context)

@login_required(login_url='login')
def manage_follow(request, pk):
    user_profile = Profile.objects.get(id=pk)
    all_profiles_followers = user_profile.followers.all()
    
    current_user = Profile.objects.get(id=request.user.id)
    all_current_user_is_following = current_user.following.all()

    if user_profile.id != current_user.id:   
        if current_user in all_profiles_followers:
            user_profile.followers.remove(current_user)
        else:  
            user_profile.followers.add(current_user) 

        if user_profile in all_current_user_is_following:
            current_user.following.remove(user_profile)  
        else:
            current_user.following.add(user_profile) 

    return HttpResponseRedirect(reverse('profile', args=[user_profile.id]))