from rest_framework import serializers

from pages import models
from users.api import serializers as users_serializers


class PageSerializer(serializers.ModelSerializer):
    user = users_serializers.UserRetrieveSerializer(read_only=True)

    class Meta:
        model = models.Page
        fields = ('id', 'slug', 'user', 'is_created', 'name', 'page_type',
                  'header_title', 'header_description',
                  'created_at', 'updated_at')
