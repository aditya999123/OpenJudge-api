from .views import *
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
import json
from general.methods import VMS, get_view, ROLE

exec(VMS)

@VMS('POST')
def submit(request, problem_code):
	pass