from operator import mod
from django.db import models

# Create your models here.


class FormModel(models.Model):
    youtube_link = models.URLField()
    start_minute = models.IntegerField()
    start_second = models.IntegerField()
    end_minute = models.IntegerField()
    end_second = models.IntegerField()
    resolution = models.IntegerField()