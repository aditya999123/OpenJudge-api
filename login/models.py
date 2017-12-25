# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib
from django.db import models
import uuid
# Create your models here.
ROLE_CHOICES = (
    ('USER', 'USER'),
    ('ADMIN', 'ADMIN'),
    )

class user_data(models.Model):
	name = models.CharField(max_length = 120, blank = False, null = False)
	username = models.CharField(max_length = 120, blank = False, null = False, primary_key = True)
	role = models.CharField(max_length = 120, blank = False, null = False, choices = ROLE_CHOICES)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)

	def save(self, *args, **kwargs):
		super(user_data, self).save(*args, **kwargs)
		user = user_data.objects.get(username = self.username)
		user_auth_data,created = auth_user.objects.get_or_create(user = user)
		if created:
			user_auth_data.password = hashlib.sha256(str(uuid.uuid4())).hexdigest()
			user_auth_data.save()

	def __unicode__(self):
		return str(self.username)

class auth_user(models.Model):
	user = models.ForeignKey(user_data)
	password = models.CharField(max_length = 120, blank = False, null = False)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)

	def __unicode__(self):
		return str(self.username)