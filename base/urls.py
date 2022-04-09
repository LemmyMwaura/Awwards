from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('submit_project/', views.submit_project, name='submit-project'),

    path('login/', views.login_page, name='login'),
    path('register/', views.register_user, name='register'),
    path('profile/<str:pk>/', views.profile, name='profile')
]