from .views import *
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
import json
from general.methods import VMS, get_view, ROLE

exec(VMS)

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
