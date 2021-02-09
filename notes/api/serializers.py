from rest_framework import serializers

from notes import models
from users.api import serializers as users_serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name',)


class NoteSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    categories = CategorySerializer(many=True, required=False)
    author = users_serializers.UserRetrieveSerializer(read_only=True)

    class Meta:
        model = models.Note
        fields = ('id', 'title', 'content', 'categories', 'author',
                  'likes_count', 'created_at', 'updated_at')

    def create(self, validated_data):
        try:
            categories = validated_data.pop('categories')
        except KeyError:
            categories = None
        instance = models.Note(**validated_data)
        instance.save()

        if categories:
            for category in categories:
                category_obj = models.Category.objects.filter(name=category['name']).first()
                if category_obj:
                    instance.categories.add(category_obj)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        try:
            categories = validated_data.pop('categories')
        except KeyError:
            categories = None

        if isinstance(categories, list):
            for category in instance.categories.all():
                instance.categories.remove(category)

        if categories:
            for category in categories:
                category_obj = models.Category.objects.filter(name=category['name']).first()
                if category_obj:
                    instance.categories.add(category_obj)

        super().update(instance, validated_data)
        return instance


class NoteSerializerShort(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    author = users_serializers.UserSerializer(read_only=True)
    content = serializers.CharField(source='short_content', read_only=True)

    class Meta:
        model = models.Note
        fields = ('id', 'title', 'content', 'categories', 'author', 'likes_count', 'created_at', 'updated_at')
