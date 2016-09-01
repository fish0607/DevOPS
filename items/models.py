from __future__ import unicode_literals

from django.db import models

# Create your models here.

class items_info(models.Model):
	items_id = models.AutoField(primary_key=True)
	host = models.GenericIPAddressField()
	name = models.CharField(max_length=100)
	service = models.CharField(max_length=100)
	path = models.CharField(max_length=100)
	shell = models.CharField(max_length=100)
	process = models.CharField(max_length=100,null=True)
	port = models.CharField(max_length=100,null=True)
	status = models.CharField(max_length=100,null=True)
	group = models.CharField(max_length=100,null=True)
	notes = models.CharField(max_length=100,null=True)
