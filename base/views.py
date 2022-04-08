from .models import Project, Profile, Rating 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib import messages 

# Create your views here.
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    projects = Project.objects.filter(
        Q(title__icontains = q) |
        Q(description__icontains = q) |
        Q(user_project__username__icontains = q)
    )

    context = {'projects': projects }
    return render(request, 'base/home.html', context)


def profile(request):
    context = {}
    return render(request)