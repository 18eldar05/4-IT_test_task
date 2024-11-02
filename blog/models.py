from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.TextField(blank=True)
    article = models.ForeignKey('Blog', on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
