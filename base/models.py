from django.db import models

# Create your models here.

class User (models.Model):
    name = models.CharField(max_length=200)
    pdf = models.FileField(upload_to="images/", null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
