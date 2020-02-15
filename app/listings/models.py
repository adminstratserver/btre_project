from django.db import models
from datetime import datetime
from developers.models import Developer

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Listing(models.Model):

  developer = models.ForeignKey(Developer, on_delete=models.CASCADE)

  title = models.CharField(max_length=200)

  MKTBIAS_CHOICES = [('BEAR', 'Bearish'), ('BULL', 'Bullish'), ('NEUTRAL', 'Neutral'),]
  marketbias = models.CharField(max_length=8, choices=MKTBIAS_CHOICES, default='NEUTRAL', )
  description = models.TextField(blank=True)
  promotion = models.CharField(max_length=10)
  price = models.IntegerField()
  maxloss = models.DecimalField(max_digits=4, decimal_places=2)
  maxprofit = models.DecimalField(max_digits=4, decimal_places=2)
  photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
  photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
  is_published = models.BooleanField(default=True)
  list_date = models.DateTimeField(default=datetime.now, blank=True)
  def __str__(self):
    return self.title