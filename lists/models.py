from django.db import models

# Create your models here.

class List(models.Model):
	pass
	
class Item(models.Model):
	text = models.TextField(default = '')
	list = models.ForeignKey(List, default = None)
	

#the above thing gives an error where there is a missing attribute called save. 
#we have to inherit it from the model class

