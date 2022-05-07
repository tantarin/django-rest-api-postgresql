from django.db import models
from django.conf import settings
from django.utils import timezone


class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=300)
   # author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
