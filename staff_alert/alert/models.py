from django.db import models


class FileData(models.Model):

    file_title = models.CharField(max_length=50)
    file = models.FileField()

# Create your models here.
