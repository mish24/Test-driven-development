from django.db import models

# Create your models here.
class Item(models.Model):
	text = models.TextField(default = '')
#the above thing gives an error where there is a missing attribute called save. 
#we have to inherit it from the model class

