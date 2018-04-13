from django.db import models
import uuid

# Create your models here.

class Userlist(models.Model):
	username = models.CharField(max_length=200,unique=True)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	worker = models.BooleanField(default=True)
	dateAdded = models.DateTimeField('date added',auto_now=True)
	
class Rates(models.Model):
	datum = models.CharField(max_length=200)
	currency = models.CharField(max_length=20)
	rate = models.DecimalField(max_digits=20, decimal_places=5,null=True)
	dateAdded = models.DateTimeField('date added',auto_now=True)