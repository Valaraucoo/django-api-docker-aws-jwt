import uuid

from django.db import models
from django.core.exceptions import ValidationError

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ('name',)


class Note(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey('users.User', related_name='my_notes', on_delete=models.CASCADE)

    categories = models.ManyToManyField('Category', related_name='notes', blank=True)
    bookmarks = models.ManyToManyField('users.User', related_name='bookmarks', blank=True)
    likes = models.ManyToManyField('users.User', related_name='likes', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('title',)

    def __str__(self) -> str:
        return f'Note: {self.title}, {self.author}'

    def like(self, user: User) -> None:
        self.likes.add(user)

    def bookmark(self, user: User) -> None:
        self.bookmarks.add(user)

    def categorize(self, category: Category) -> None:
        self.categories.add(category)

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    @property
    def short_content(self) -> str:
        if len(self.content) > 300:
            return self.content[:300]
        return self.content
