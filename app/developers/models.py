# developers/models.py
from django.db import models
from datetime import datetime

class Developer(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(blank=True)
    is_mvd = models.BooleanField(default=False)
    website = models.URLField(max_length=200)
    published_date = models.DateTimeField(default=datetime.now, blank=True)
  
    class Meta:
        verbose_name = 'developer'
        verbose_name_plural = 'developers'
  
    def __str__(self):
        return self.name

