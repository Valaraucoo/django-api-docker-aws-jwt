import datetime

from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import generics
from rest_framework import response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import CategorySerializer, NoteSerializer, NoteSerializerShort

from core.rest_framework_backends import BasePagination

from notes import models
from notes.api import permissions
from notes.emails import emails

from users import models as users_models
from users.api import serializers as users_serializers


class BaseNoteListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BaseNoteManageView(APIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializerShort
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))


class CategoryListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NoteListView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = BasePagination

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

        title = self.request.query_params.get('title')
        if title:
            qs = qs.filter(title__icontains=title)
        return qs

    def get_serializer_class(self):
        if self.request and not self.request.user.is_authenticated:
            return NoteSerializerShort
        return NoteSerializer


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
        return NoteSerializerShort


class LikeNoteView(BaseNoteManageView):
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        obj.like(user)
        obj.save()
        serializer = self.serializer_class(obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        obj.likes.remove(user)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)


class BookmarkNoteView(BaseNoteManageView):
    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        obj.bookmark(user)
        obj.save()
        serializer = self.serializer_class(obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        user = self.request.user
        obj.bookmarks.remove(user)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)


class CategoryNoteView(BaseNoteManageView):
    """
    POST/DELETE data must contains `category`: id of category
    """
    def get_object(self):
        return self.queryset.get(pk=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        category_pk = self.request.POST.get('category')
        category = get_object_or_404(models.Category, pk=category_pk)
        obj.categorize(category)
        obj.save()
        serializer = self.serializer_class(obj)
        return response.Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        category_pk = self.request.POST.get('category')
        category = get_object_or_404(models.Category, pk=category_pk)
        obj.categories.remove(category)
        obj.save()
        return response.Response(data={"message": "ok"}, status=status.HTTP_200_OK)


class SubscriptionView(APIView):
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

        # TODO
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
    pagination_class = BasePagination

    def get_queryset(self):
        return models.Note.objects.filter(author__email=self.request.user.email)


class PaymentNotificationView(APIView):
    """
    PaymentNotificationView is used to send the user the time remaining until the end of the subscription.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            days = (self.request.user.subscription_to.replace(tzinfo=None) - datetime.datetime.now()).days
        except AttributeError:
            days = 0
        if days > 0:
            emails.PaymentNotificationMailFactory().create_notification_email(self.request.user).send()

        data = {
            "subscription_expires_in": days,
            'subscription': self.request.user.subscription,
            "has_expired": days <= 0
        }

        return response.Response(data=data, status=status.HTTP_200_OK)
