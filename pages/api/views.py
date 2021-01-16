from rest_framework import mixins
from rest_framework import generics
from rest_framework import response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from pages import models
from pages.api import serializers
from pages.emails import emails


class PageRetrieveView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def get_object(self):
        slug = self.kwargs.get('slug')
        return self.queryset.get(slug=slug)

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
        if page.is_created:
            return response.Response(data={'error': 'This page was created earlier'},
                                     status=status.HTTP_400_BAD_REQUEST)
        page.is_created = True
        page.save()
        emails.PagePublishedMailFactory().create_page_published_email(self.request.user, page).send()
        return response.Response(data={'message': 'ok'}, status=status.HTTP_200_OK)
