# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import transaction
from django.db import models
from login.models import user_data
from contests.models import contest_data, contest_result_data, leaderboard_data
from django.contrib.postgres.fields import JSONField
from execute.commands import ERROR_CODE
# Create your models here.

class problems_data(models.Model):
	contest = models.ForeignKey(contest_data)
	title = models.CharField(max_length = 120, blank = False, null = False)
	code = models.CharField(max_length = 10, blank = False, null = False, primary_key = True)
	description = models.CharField(max_length=15000, blank=True, null=False)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
	enabled = models.BooleanField(default = True)

	@property
	def get_submission_count(self):
		problem = problems_data.objects.get(code = self.code)
		submissions = best_submission_data.objects.filter(problem = problem)

		data = {}
		for submission in submissions:
			try:
				data[submission.score] = data[submission.score] + 1
			except:
				data[submission.score] = 0
		return data


	def __unicode__(self):
		return str(self.code)

class testcase_data(models.Model):
	id = models.AutoField(primary_key = True)
	problem = models.ForeignKey(problems_data)
	enabled = models.BooleanField(default = True)
	score = models.IntegerField()
	input = models.FileField(null = True)
	output = models.FileField(null = True)
	time_limit = models.IntegerField(default = 1)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)

class submission_data(models.Model):
	id = models.AutoField(primary_key = True)
	program = models.CharField(max_length=20000, null = False, blank = False)
	lang = models.CharField(max_length=10, null = False, blank = False)
	user = models.ForeignKey(user_data)
	problem = models.ForeignKey(problems_data)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
	score = models.IntegerField(default = 0)
	stats = JSONField(default = {
		'Exit_status' : 'waiting',
		'time' : 0
		})

	def save(self, *args, **kwargs):
		print "starts from here"
		super(submission_data, self).save(*args, **kwargs)
		
		submissions = submission_data.objects.filter(
			user = self.user,
			problem = self.problem
			).order_by('-score','created')

		best_submission,created = best_submission_data.objects.get_or_create(
			user = self.user,
			problem = self.problem,
			submission = submissions[0]
			)

class testcase_submission_data(models.Model):
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)
	stats = JSONField(default = {})
	testcase = models.ForeignKey(testcase_data)
	submission = models.ForeignKey(submission_data)

	def save(self, *args, **kwargs):
		print "2starts from here"
		super(testcase_submission_data, self).save(*args, **kwargs)

		total_score = 0
		status = 1000
		time = 0

		for tsd in testcase_submission_data.objects.filter(submission = self.submission):
			if tsd.stats['Exit_status'] < status:
				status = tsd.stats['Exit_status']
			if tsd.stats['Exit_status'] == 0:
				t_time = tsd.stats["User_time_(seconds)"] + tsd.stats["System_time_(seconds)"]			
				if t_time > time:
					time = t_time
				total_score = total_score + tsd.testcase.score

		stats = {}
		stats['Exit_status'] = ERROR_CODE[status]
		stats['time'] = time
		submission = submission_data.objects.get(id = self.submission.id)
		submission.stats = stats
		submission.score = total_score
		submission.save()

class best_submission_data(models.Model):
	submission = models.ForeignKey(submission_data)
	user = models.ForeignKey(user_data)
	problem = models.ForeignKey(problems_data)
	modified = models.DateTimeField(auto_now = True, auto_now_add = False)
	created = models.DateTimeField(auto_now = False, auto_now_add = True)

	def save(self, *args, **kwargs):
		super(best_submission_data, self).save(*args, **kwargs)

		print "chere1"

		participant, created = contest_result_data.objects.get_or_create(
			user = self.user,
			contest = self.problem.contest
			)
		print "chere",participant

		total_score = 0
		total_time = 0

		for bs in best_submission_data.objects.filter(
			user = self.user,
			problem__contest = self.problem.contest
			):
			print bs, bs.submission

			total_score = total_score + bs.submission.score
			total_time = total_time + (bs.submission.modified - bs.problem.contest.start_time).total_seconds()

		participant.score = total_score
		participant.time = total_time
		participant.save()
		print "completed"