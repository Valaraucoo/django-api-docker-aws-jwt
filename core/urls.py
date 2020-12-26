from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from users import views


urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls', namespace='users')),
    path('api/user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('schema/', get_schema_view(title='wozniak-dev: API Docs', description='Noteneo app API'), name='api-schema'),
    path('docs/', include_docs_urls(title='wozniak-dev: API Docs'), name='docs'),
]
