from .tokens import get_user, ACCESS_TOKEN
from django.http import JsonResponse
from .checker import assert_valid, assert_allowed, assert_found

def JWT(function):
	def check_validity(request, *args, **kwargs):
		token = request.META.get(ACCESS_TOKEN, None)
		assert_found(token, 'access_token not found')
		# print token,"aaa"
		user = get_user(token)

		response = {
		'success' : True
		}

		return function(request, user, copy.deepcopy(response), *args, **kwargs)
	return check_validity

def ROLE(*roles):
	def wrapper(function):
		def check_role(request, user, *args, **kwargs):
			if user.role in roles or 'ALL' in roles:
				return function(request, user, *args, **kwargs)
			else:
				return JsonResponse({'success':False, 'message':'Access Denied'}, status = 403)
		return check_role
	return wrapper

def get_or_none(classmodel, **kwargs):
	try:
		return classmodel.objects.get(**kwargs)
	except classmodel.DoesNotExist:
		return None
