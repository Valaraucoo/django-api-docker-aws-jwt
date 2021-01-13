from django.urls import path, include

from notes.api import views


app_name = 'notes'

urlpatterns = [
    path('', views.NoteListView.as_view(), name='notes-list'),
    path('categories/', views.CategoryListView.as_view(), name='notes-categories'),

    path('<int:pk>/', views.NoteRetrieveView.as_view(), name='notes-details'),
    path('<int:pk>/like/', views.LikeNoteView.as_view(), name='notes-like'),
    path('<int:pk>/bookmark/', views.BookmarkNoteView.as_view(), name='notes-bookmark'),
    path('<int:pk>/category/', views.CategoryNoteView.as_view(), name='notes-category'),

    path('my-notes/', views.UserNotesListView.as_view(), name='my-notes'),
    path('likes/', views.UserLikesListView.as_view(), name='my-likes'),
    path('bookmarks/', views.UserBookmarksListView.as_view(), name='my-bookmarks'),
    path('payment/', views.SubscriptionView.as_view(), name='payment'),
    path('payment/notification/', views.PaymentNotificationView.as_view(), name='payment-notification'),
]
