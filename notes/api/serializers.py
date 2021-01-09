from rest_framework import serializers

from notes import models
from users.api import serializers as users_serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name',)


class NoteSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    author = users_serializers.UserSerializer(read_only=True)

    class Meta:
        model = models.Note
        fields = ('id', 'title', 'content',
                  'categories', 'author', 'likes_count')


class NoteSerializerShort(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    author = users_serializers.UserSerializer(read_only=True)
    content = serializers.CharField(source='short_content', read_only=True)

    class Meta:
        model = models.Note
        fields = ('id', 'title', 'content',
                  'categories', 'author', 'likes_count')
