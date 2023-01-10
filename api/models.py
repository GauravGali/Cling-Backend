from django.db import models


# Create your models here.
class User(models.Model):
    email = models.CharField(max_length=10_000)
    avatarUrl = models.URLField(max_length=10_000)
    name = models.CharField(max_length=10_000, null=True, blank=True)

    def __str__(self):
        return self.email
