from login.views import *
from problems.views import *
from contests.views import *
from execute.views import *

from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
import json, copy

INTERNAL_ERROR = JsonResponse({
	'success' : False,
	'message' : 'something went wrong'
	}, status = 500)

NOT_FOUND = JsonResponse({
	'success' : False,
	'message' : 'method not found'
	}, status = 400)


def get_view(function_name, method):
	return '%s_%s(request, *args, body = body, **kwargs)'%(function_name, method)

def VMS(*methods):
	def _function_wrapper(function):
		def view_name_segregator(request, *args, **kwargs):
			if request.method in methods:
				try:
					if request.body:
						body = json.loads(request.body)
					else:
						body = {}
					return eval(get_view(function.__name__, request.method))
				except Exception as e:
					print "// " , e , " //"
					err_data = e.message
					try:
						return JsonResponse(err_data, status = err_data['status_code'])
					except :
						return  INTERNAL_ERROR
			elif request.method == 'OPTIONS':
				resp = HttpResponse('watch middleware for this')
				return resp
			else :
				return NOT_FOUND
		return view_name_segregator
	return _function_wrapper

@VMS('POST')
def login(request):
	pass

@VMS('POST')
def register(request):
	pass

@VMS('GET')
def access_token(request):
	pass

@VMS('GET')
def usernames(request):
	pass

@VMS('GET')
def usernames(request):
	pass

@VMS('GET', 'POST')
def contest_problems(request, contest_code):
	pass

@VMS('GET', 'POST')
def problem(request, problem_code):
	pass

@VMS('GET')
def testcases(request, problem_code):
	pass

@VMS('GET', 'POST')
def contest(request):
	pass

@VMS('POST')
def submit(request, problem_code):
	pass