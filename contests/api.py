from .views import *
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
import json
from general.methods import VMS, get_view, ROLE

exec(VMS)

@VMS('GET', 'POST')
def contest(request):
	pass