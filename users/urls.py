from django.urls import path, include
from .api import views

app_name = 'users'

urlpatterns = [
    path('register/', views.CustomUserCreateView.as_view(), name='register'),
    path('logout/', views.BlackListTokenView.as_view(), name='logout'),
    path('profile/', views.ManageUserView.as_view(), name='profile'),
    path('profile/<int:pk>/', views.RetrieveUserProfileView.as_view(), name='profile-user'),
]
