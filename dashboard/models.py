from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    assigned_to = models.ManyToManyField(User, related_name="assignee")
    created_by = models.ForeignKey(User, related_name="creator", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
