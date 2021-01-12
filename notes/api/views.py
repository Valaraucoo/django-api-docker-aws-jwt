import datetime

from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import generics
from rest_framework import response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import CategorySerializer, NoteSerializer, NoteSerializerShort

from notes import models
from notes.api import permissions

from users import models as users_models
from users.api import serializers as users_serializers


class BaseNoteListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NoteListView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializerShort
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        qs = models.Note.objects.all()
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(categories__name=category)

        author = self.request.query_params.get('author')
        if author:
            qs = qs.filter(author__name=author)
        return qs


class NoteRetrieveView(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (permissions.IsAuthorOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get_serializer_class(self):
        try:
            if not self.request.user.is_authenticated:
                return NoteSerializerShort
            if self.get_object().author == self.request.user or self.request.user.is_subscriber:
                return NoteSerializer
        except AttributeError:
            return NoteSerializerShort


class LikeNoteView(generics.GenericAPIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        obj.like(user)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        obj.likes.remove(user)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)


class BookmarkNoteView(generics.GenericAPIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        obj.bookmark(user)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        obj.bookmarks.remove(user)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)


class CategoryNoteView(generics.GenericAPIView):
    """
    POST/DELETE data must contains `category`: id of category
    """
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        category_pk = self.request.POST.get('category')
        category = get_object_or_404(models.Category, pk=category_pk)
        obj.categorize(category)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        category_pk = self.request.POST.get('category')
        category = get_object_or_404(models.Category, pk=category_pk)
        obj.categories.remove(category)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)


class SubscriptionView(generics.GenericAPIView):
    serializer_class = users_serializers.UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> users_models.User:
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        return response.Response(data={
            'is_subscriber': user.is_subscriber,
            'subscription_to': user.subscription_to,
            'time_left': user.subscription_to.replace(tzinfo=None) - datetime.datetime.now(),
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        data = {
            'is_subscriber': user.is_subscriber,
            'subscription_to': user.subscription_to,
            'time_left': user.subscription_to.replace(tzinfo=None) - datetime.datetime.now(),
        }

        if user.is_subscriber:
            return response.Response(data={
                'message': 'User is already a subscriber.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # subscription logic
        # user.subscription_to += days(30)

        return response.Response(data=data, status=status.HTTP_200_OK)


class UserLikesListView(BaseNoteListView):
    def get_queryset(self):
        return models.Note.objects.filter(likes__email=self.request.user.email)


class UserBookmarksListView(BaseNoteListView):
    def get_queryset(self):
        return models.Note.objects.filter(bookmarks__email=self.request.user.email)


class UserNotesListView(BaseNoteListView):
    def get_queryset(self):
        return models.Note.objects.filter(author__email=self.request.user.email)
