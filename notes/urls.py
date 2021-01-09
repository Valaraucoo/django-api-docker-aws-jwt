from django.urls import path, include

from notes.api import views


app_name = 'notes'

urlpatterns = [
    path('', views.NoteListView.as_view(), name='notes-list'),
    path('<int:pk>/', views.NoteRetrieveView.as_view(), name='notes-details'),
    path('my-notes/', views.UserNotesListView.as_view(), name='my-notes'),
]
