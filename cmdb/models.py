from __future__ import unicode_literals

from django.db import models

# Create your models here.

class host_info(models.Model):
	hostname = models.CharField(max_length=100)
	ip = models.GenericIPAddressField(primary_key=True)
	cpu = models.CharField(max_length=100)
	men = models.CharField(max_length=10)
	disk = models.CharField(max_length=10)
	os = models.CharField(max_length=50)
	position = models.CharField(max_length=100)
	owner = models.CharField(max_length=100)
	group = models.CharField(max_length=100)
	notes = models.CharField(max_length=100)

class ssh_info(models.Model):
	hostname = models.CharField(max_length=100)
	ip = models.GenericIPAddressField(primary_key=True)
	username = models.CharField(max_length=50)
	password = models.CharField(max_length=100)
	port = models.CharField(max_length=10)
	notes = models.CharField(max_length=100)

