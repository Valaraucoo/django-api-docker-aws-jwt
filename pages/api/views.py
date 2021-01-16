from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework import generics
from rest_framework import response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from pages import models
from pages.api import serializers


class PageRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        return self.queryset.filter(is_created=True)


class UserPageRetrieveUpdateView(PageRetrieveView, mixins.UpdateModelMixin):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_object(self):
        return self.queryset.get(user=self.request.user)


class PublishPageView(APIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Page.objects.all()

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        page = self.get_object()
        page.is_created = True
        page.save()
        return response.Response(data={'message': 'ok'}, status=status.HTTP_200_OK)
