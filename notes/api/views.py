from rest_framework import mixins
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import NoteSerializer, NoteSerializerShort

from notes import models
from notes.api import permissions


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
            if self.get_object().author == self.request.user or self.request.user.subscription.is_active:
                return NoteSerializer
        except AttributeError:
            return NoteSerializerShort


class UserNotesListView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Note.objects.all()
    serializer_class = NoteSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return models.Note.objects.filter(author__email=self.request.user.email)
