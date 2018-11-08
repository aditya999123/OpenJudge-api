# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from general.checker import assert_valid, assert_allowed, assert_found
from .models import *
from general.serializers import get_json_serializable, serialize
from general.methods import *
from general.time_utils import time_now

from general.time_utils import str_to_time
# Create your views here.

# @JWT
# @ROLE('USER', 'ADMIN')
def contest_GET(request, body):
	response = {}
	response['success'] = True
	response['contests'] = serialize(contest_data, 'is_running', 'is_ended')
	return JsonResponse(response)

@JWT
@ROLE('ADMIN')
def contest_POST(request, body, user, response):
	title = body['title']
	code = body['code']
	description = body['description']
	start_time = body['start_time']
	end_time = body['end_time']

	start_time = str_to_time(start_time)
	end_time = str_to_time(end_time)

	contest = get_or_none(contest_data, code = code)

	if contest:
		assert_allowed(contest.owner == user, "contest with this code already exists")
		contest.title = title
		contest.description = description
		assert_valid(end_time > start_time, "timing mismatched")
		assert_valid(time_now() < start_time, "timing mismatched")
		contest.start_time = start_time
		contest.end_time = end_time
		contest.save()
	else :
		contest = contest_data.objects.create(
			title = title,
			code = code,
			description = description,
			start_time = start_time,
			end_time = end_time,
			owner = user
			)
	
	response['contest'] = get_json_serializable(contest)
	return JsonResponse(response)