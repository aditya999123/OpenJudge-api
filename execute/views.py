from __future__ import unicode_literals
import shlex
from django.http import JsonResponse
import os, re, uuid
from datetime import datetime
from utils import *
from celery.utils.log import get_task_logger
from general.methods import *
import time, os
from onlinecompiler.settings import BASE_DIR
from django.db import transaction
from general.celery import app
from general.serializers import get_json_serializable
from general.methods import *
from general.checker import assert_found, assert_allowed, assert_valid
from problems.models import submission_data, problems_data, testcase_data, testcase_submission_data
from execute.utils import copy_folder_file
# @transaction.atomic
logger = get_task_logger(__name__)

@JWT
@ROLE('USER', 'ADMIN')
def submit_POST(request, user, response, problem_code):
	program = body['program']
	username = user.username
	lang = body['lang'].upper()

	problem = get_or_none(problems_data, code = problem_code)
	assert_found(problem, 'problem with this code not found')

	submission = submission_data.objects.create(
		program = program,
		lang = lang,
		user = user,
		problem = problem
		)

	print "submission created"

	for testcase in testcase_data.objects.filter(problem = problem):
		# execute_program.delay(submission.id, testcase.id)
		execute_program(submission.id, testcase.id)
		print "xyz"

	response['message'] = 'submission queued'
	response['submission'] = get_json_serializable(submission)
	return JsonResponse(response)

@app.task
def execute_program(submission_id, testcase_id):
	response = {}
	submission = get_or_none(submission_data, id = submission_id)
	testcase = get_or_none(testcase_data, id = testcase_id)
	assert_found(testcase)
	assert_found(submission)
	lang = submission.lang
	time_limit = testcase.time_limit
	username = submission.user.username
	path = get_path(username)
	create_folder(path)

	code_filename = '%s.%s'%(username, LANG_COMMAND[lang]['ext'])

	code_file_path = '%s/%s'%(path, code_filename)
	input_file_path = '%s/%s'%(path, IN)
	expected_output_file_path = '%s/%s'%(path, EXPECTED)
	output_file_path = '%s/%s'%(path, OUT)
	time_output = "%s/%s"%(path, TIME_OUTPUT)

	# error in program
	error_file_path = "%s/%s"%(path, ERROR)

	#error code in execution of program
	error_code_file_path = '%s/%s'%(path, ERR_CODE_FILE)

	#error in comparison of output
	error_compare_path = '%s/%s'%(path, ERR_COMPARE_FILE)

	script_path = '%s/%s'%(path, SCRIPT_FILE)
	SAND_COMMAND = SAND%(path)#, SCRIPT_FILE)

	write_file(code_file_path, submission.program)

	testcase_input = "%s/%s"%(BASE_DIR, testcase.input)
	testcase_output = "%s/%s"%(BASE_DIR, testcase.output)

	copy_folder_file(testcase_input, input_file_path)
	copy_folder_file(testcase_output, expected_output_file_path)

	for command in LANG_COMMAND[lang]['commands']:
		current_command = eval(command['command'])
		script = SCRIPTS[command['script']]
		current_script = script % (current_command, command['error_code'], ERR_CODE_FILE, OUT, TIME_OUTPUT)
		delete_folder_files(script_path)
		write_file(script_path, current_script)
		execute(SAND_COMMAND)
		err_code = get_err_code(error_code_file_path)

		if err_code != 0 :
			break

	if err_code != 406:
		response = read_stats(read_file(time_output))
		print response
		# program_output = read_file(output_file_path, response['Number_of_characters'])
		# response['program_output'] = program_output
		# print response

	error_txt = read_file(error_file_path)

	if err_code == 0:
		#compare files
		delete_folder_files(script_path)
		script = SCRIPTS['COMPARE']
		current_script = script % (expected_output_file_path, output_file_path, error_compare_path)
		write_file(script_path, current_script)
		execute(SAND_COMMAND)
		err_code = get_err_code(error_compare_path)

	response['error'] = error_txt
	response['Exit_status'] = err_code
	response['status'] = ERROR_CODE[err_code]

	testcase_submission = testcase_submission_data.objects.create(
		testcase = testcase,
		submission = submission,
		stats = response
		)

	# return testcase_submission
	# logger.info("completed test")
	print "completed test"
	# delete_folder_files(path)
	return response
	# return JsonResponse(response)