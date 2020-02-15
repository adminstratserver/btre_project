from django.db import models
from members.models import MemberProfile

 # Create Order Model
class Order(models.Model):
    tradeorder = models.CharField(max_length=100)
    datetime = models.CharField(max_length=100)
    sequencenumber = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) # When it was create
    updated_at = models.DateTimeField(auto_now=True) # When i was update
    creator = models.ForeignKey(MemberProfile, related_name='orders', on_delete=models.CASCADE)






