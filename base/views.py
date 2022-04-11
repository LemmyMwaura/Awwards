from .models import Project, Profile
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import APIView
from .serializers import ProfileSerializer, ProjectSerializer, UserSerializer
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages 
from .forms import ProjectForm, UserRegistrationForm, RatingForm

# Create your views here.
class ProfilesList(APIView):
    def get(self,request, format=None):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

class UsersList(APIView):
    def get(self,request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
        
class ProjectList(APIView):
    def get(self,request, format=None):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

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

@login_required(login_url='login')
def submit_project(request):
    form = ProjectForm()
    if request.method == 'POST':
        try:
            form = ProjectForm(request.POST, request.FILES)
            if form.is_valid:
                user = form.save(commit=False)
                user.user_project_id = request.user.id
                user.save()
                return redirect('home')
        except Exception as e:
            messages.error(request, 'An error occured during submition. Try again')

    context = { 'form': form }
    return render(request, 'base/submit_project_form.html', context)

def project_page(request,pk):
    project = Project.objects.get(id=pk)
    ratings = project.rating_set.all()
    form = RatingForm

    context = {'project':project, 'form':form, 'ratings':ratings}
    return render(request, 'base/project.html', context)

@login_required(login_url='login')
def add_ratings(request,pk):
    project = Project.objects.get(id=pk)
    ratings = project.rating_set.all()
    current_user = User.objects.get(id=request.user.id)
    print(ratings)

    if current_user in ratings:
        messages.error(request, 'Your rating was already submitted')
        return redirect('project',pk=pk)

    if request.method == 'POST':
        try:
            form = RatingForm(request.POST)
            if form.is_valid():
                    rating = form.save(commit=False)
                    rating.project_id = int(pk)
                    rating.rated_by_id = request.user.id
                    rating.save()
                    messages.success(request, 'Your rating was added successfully')
                    return redirect('project',pk=pk)
        except ValueError as e:
                messages.error(request, 'Rating could not be added, Please try again. Ensure your values are between 1 and 10', e) 
                return redirect('project',pk=pk)

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

    return redirect('profile',pk=user_profile.id)