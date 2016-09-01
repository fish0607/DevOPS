from __future__ import unicode_literals

from django.db import models

# Create your models here.

class svn_info(models.Model):
	svn_id = models.AutoField(primary_key=True)
	svn_url = models.CharField(max_length=800)
	svn_user = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	notes = models.CharField(max_length=100)
