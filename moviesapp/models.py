from django.db import models
import uuid
from django.contrib.auth.models import User


class Collection(models.Model):
    title = models.CharField(max_length=200)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.CharField(max_length=255, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    collection = models.ForeignKey(Collection, related_name='movies', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title
