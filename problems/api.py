from .views import *
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
import json
from general.methods import VMS, get_view, ROLE

exec(VMS)

@VMS('GET', 'POST')
def contest_problems(request, contest_code):
	pass

@VMS('GET', 'POST')
def problem(request, problem_code):
	pass

@VMS('GET')
def testcases(request, problem_code):
	pass