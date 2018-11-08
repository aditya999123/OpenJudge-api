import jwt
from datetime import datetime
from .checker import assert_valid, assert_allowed, assert_found, assert_authorized
import json, pytz
from login.models import user_data
from general.serializers import get_json_serializable
from .time_utils import str_to_time, time_now, make_aware

key = "jashojdadsadk"
version = 1.0

REFRESH_TOKEN  = 'HTTP_X_AUTH_TOKEN'
ACCESS_TOKEN = 'HTTP_AUTHORIZATION'

#10 years
refreshTokenTTL = 10 * 365 * 24 * 60 * 60 ;
#10 hours
accessTokenTTL = 10 * 60 * 60 ;

def token_builder(user, millis):
	data = {
		'user' : get_json_serializable(user),
		'expiry_date' : calculate_expiry_date(millis),
		'version' : version
	}
	return data	

def create_refresh_token(user):
	token_data = token_builder(user, refreshTokenTTL)	
	return jwt.encode(token_data, key, algorithm='HS256')

def create_access_token(user):
	token_data = token_builder(user, accessTokenTTL)
	return jwt.encode(token_data, key, algorithm='HS256')

def parse_token(token):
	try:
		token = jwt.decode(token, key, algorithms='HS256')
	except Exception as e:
		print e
		return assert_valid(False, "token error")

	assert_authorized(not expired(token), "token expired")
	assert_authorized(version_check(token), "token of older version")
	return token

def get_user(token):
	token = parse_token(token)
	try :
		user = user_data.objects.get(username = token['user']['username'])
	except:
		assert_found(None, 'User with this username not found')
	return user

def calculate_expiry_date(millis):
	now = time_now()
	ref = make_aware(datetime(1970,1,1))
	exp = (now - ref).total_seconds() + millis
	exp = make_aware(datetime.utcfromtimestamp(exp))
	return str(exp)

def expired(obj):
	expiry_str = obj['expiry_date']
	exp = str_to_time(expiry_str)
	return exp < time_now()

def version_check(obj):
	return obj['version'] == version
