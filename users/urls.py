from django.urls import path
from .api import views

app_name = 'users'

urlpatterns = [
    path('register/', views.CustomUserCreateView.as_view(), name='register'),
    path('logout/', views.BlackListTokenView.as_view(), name='logout'),
]
