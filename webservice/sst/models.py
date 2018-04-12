from django.db import models
import uuid

# Create your models here.

class Userlist(models.Model):
	username = models.CharField(max_length=200,unique=True)
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	worker = models.BooleanField(default=True)
	dateAdded = models.DateTimeField('date published',auto_now=True)
	