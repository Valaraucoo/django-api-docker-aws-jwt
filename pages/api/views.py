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
        page = self.get_object()
        models.PageAnalytics.objects.create(page=page, ip_addr=self.request.ipinfo.ip,
                                            lat=self.request.ipinfo.latitude,
                                            lng=self.request.ipinfo.longitude,
                                            city=self.request.ipinfo.city,
                                            country=self.request.ipinfo.country)
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


class MainPageAnalyticsView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.PageAnalytics.objects.all()
    serializer_class = serializers.PageAnalyticsSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        qs = self.queryset.filter(page__user=self.request.user)
        country = self.request.query_params.get('country')
        if country:
            qs = qs.filter(country=country)
        return qs

    def post(self, request):
        analytics = models.MainPageAnalytics.objects.create(ip_addr=self.request.ipinfo.ip,
                                                            lat=self.request.ipinfo.latitude,
                                                            lng=self.request.ipinfo.longitude,
                                                            city=self.request.ipinfo.city,
                                                            country=self.request.ipinfo.country)
        serializer = serializers.MainPageAnalyticsSerializer(analytics)
        return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)


class PageAnalyticsSummaryView(APIView):
    queryset = models.Page.objects.all()
    serializer_class = serializers.PageAnalyticsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.queryset.get(user=self.request.user)

    def get(self, request):
        page = self.get_object()
        analytics = page.analytics.all()
        data = {
            'view_count': page.view_count,
            'week_views_count': page.week_views_count,
            'month_views_count': page.month_views_count,
            'data':  serializers.PageAnalyticsSerializer(analytics, many=True).data
        }
        return response.Response(data=data, status=status.HTTP_200_OK)
