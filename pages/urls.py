from django.urls import path, include

from pages.api import views


app_name = 'pages'

urlpatterns = [
    path('', views.UserPageRetrieveUpdateView.as_view(), name='my-page'),
    path('publish/', views.PublishPageView.as_view(), name='page-publish'),
    path('analytics/', views.PageAnalyticsSummaryView.as_view(), name='page-analytics-summary'),
    path('main-analytics/', views.MainPageAnalyticsView.as_view(), name='main-page-analytics'),

    path('<slug:slug>/', views.PageRetrieveView.as_view(), name='page'),
]
