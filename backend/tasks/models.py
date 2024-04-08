from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Label(models.Model):
    name = models.CharField(max_length=200, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_label')
        ]


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completion_status = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['title', 'owner'], name='unique_task')
    #     ]
