# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import JsonResponse
from general.methods import *
from contests.models import contest_data
from .models import *
from general.serializers import get_json_serializable, serialize
from general.checker import assert_allowed, assert_found, assert_valid
from execute.utils import write_file, delete_folder_files, create_folder, IN, EXPECTED
from onlinecompiler.settings import MEDIA_ROOT
# @JWT
# @ROLE('USER', 'ADMIN')
def contest_problems_GET(request, body, contest_code):
	response = {}
	response['success'] = True
	contest = get_or_none(contest_data, code = contest_code)
	print contest
	assert_found(contest, 'no contest with this code')
	assert_allowed(contest.is_running or contest.is_ended, 'contest hasn\'t started yet')
	response['problems'] = serialize(problems_data, 'get_submission_count', contest = contest, enabled = True)
	response['contest'] = get_json_serializable(contest)
	return JsonResponse(response)

@JWT
@ROLE('ADMIN')
def contest_problems_POST(request, body, user, response, contest_code):
	contest = get_or_none(contest_data, code = contest_code)
	assert_found(contest, 'no contest with this code')
	assert_allowed(contest.owner == user, "you are not allowed to update this contest")

	title = body['title']
	code = body['code']	
	description = body['description']
	enabled = bool(body['enabled'])

	problem = get_or_none(problems_data, code = code)
	if problem:
		assert_allowed(problem.contest.owner == user, "problem with this code already exists")
		problem.title = title
		problem.description = description
		problem.enabled = enabled
		problem.save()
	else:
		problem = problems_data.objects.create(
			title = title,
			code = code,
			description = description,
			contest = contest,
			enabled = enabled
			)
	
	response['problem'] = get_json_serializable(problem)
	return JsonResponse(response)

def problem_GET(request, body, problem_code):
	response = {}
	response['success'] = True
	problem = get_or_none(problems_data, code = problem_code)
	assert_found(problem, "no problem with this code found")
	response['problem'] = get_json_serializable(problem)

	return JsonResponse(response)

@JWT
@ROLE('ADMIN')
def problem_POST(request, body, user, response, problem_code):
	problem = get_or_none(problems_data, code = problem_code)
	assert_found(problem, 'problem not found')
	assert_allowed(problem.contest.owner == user, "you cannot update the problem")
	
	id = body['id']
	score = int(body['score'])
	enabled = bool(body['enabled'])
	time_limit = int(body['time_limit'])

	if id == False:
		print"new testcase"
		testcase = testcase_data.objects.create(
			score = score,
			enabled = True,
			time_limit = time_limit,
			problem = problem
			)
		id = testcase.id
	else:
		print "old testcase"
		id = int(id)
		testcase = get_or_none(testcase_data, id = id)
		assert_found(testcase, "testcase with this id not found")
		assert_allowed(testcase.problem.contest.owner == user)
		testcase.score = score
		testcase.enabled = enabled
		testcase.time_limit = time_limit
		testcase.save()

	contest_code = testcase.problem.contest.code	
	# location = "%s/%s/%s/%s"%(MEDIA_ROOT, contest_code, problem_code, id)
	contest_folder = "%s/%s"%(MEDIA_ROOT, contest_code)
	problem_folder = "%s/%s"%(contest_folder, problem_code)
	location = "%s/%s"%(problem_folder, id)
	create_folder(contest_folder)
	create_folder(problem_folder)
	create_folder(location)
	
	input_file_path = '%s/%s'%(location, IN)
	output_file_path = '%s/%s'%(location, EXPECTED)
	
	input_file = request.FILES.get('input_file', False)
	output_file = request.FILES.get('output_file', False)

	if input_file:
		delete_folder_files(input_file_path)
		write_file(input_file_path, input_file.read())
		testcase.input = input_file_path
		testcase.save()

	if output_file:
		delete_folder_files(output_file_path)
		write_file(output_file_path, output_file.read())
		testcase.output = output_file_path
		testcase.save()
	
	response['testcase'] = get_json_serializable(testcase)
	return JsonResponse(response)

@JWT
@ROLE('ADMIN')
def testcases_GET(request, body, user, response, problem_code):
	problem = get_or_none(problems_data, code = problem_code)
	assert_found(problem, 'problem not found')
	assert_allowed(problem.contest.owner == user, "access denied to the problem details")
	response['testcases'] = serialize(testcase_data, problem = problem)

	return JsonResponse(response)