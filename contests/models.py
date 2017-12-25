# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from login.models import user_data
from datetime import datetime
from general.time_utils import time_now
# Create your models here.
ENDED = 'Ended'
PRESENT = 'Present'
FUTURE = 'Future'

class contest_data(models.Model):
	title = models.CharField(max_length = 120, blank = False, null = False)
	code = models.CharField(max_length = 10, blank = False, null = False, primary_key = True)
	description = models.CharField(max_length=15000, blank=True, null=False)
	start_time = models.DateTimeField()
	end_time = models.DateTimeField()
	# image = models.ImageField(upload_to='contest/%s'%self.code)
	owner = models.ForeignKey(user_data)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
	
	@property
	def is_running(self):
		now =time_now()
		return (now > self.start_time and now < self.end_time)

	@property
	def is_ended(self):
		now = time_now()
		return (now > self.end_time)

	def __unicode__(self):
		return str(self.code)

class contest_result_data(models.Model):
	contest = models.ForeignKey(contest_data)
	user = models.ForeignKey(user_data)
	score = models.IntegerField(default = 0)
	time = models.IntegerField(default = 100000)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)

	def save(self, *args, **kwargs):
		super(contest_result_data, self).save(*args, **kwargs)

		results = contest_result_data.objects.filter(
			user = self.user,
			contest = self.contest
			).order_by('-score','time')

		rank = 0
		print "uptil here"
		for result in results:
			participant, created = leaderboard_data.objects.get_or_create(
				user = result.user,
				contest = result.contest
				)
			print "h1", participant.rank
			rank = rank + 1
			participant.rank = rank
			print"h2"
			participant.save()
		######################################################################################
		
class leaderboard_data(models.Model):
	user = models.ForeignKey(user_data)
	contest = models.ForeignKey(contest_data)
	rank = models.IntegerField(default = 100000)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)