from django.db import models

# Create your models here.
class Contact(models.Model):
    department = models.TextField()
    name = models.TextField()
    title = models.TextField()
    phone = models.TextField()