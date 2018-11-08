from datetime import datetime
import pytz
from django.utils.dateparse import parse_datetime

def str_to_time(time_str):
	return parse_datetime(time_str)

def time_now():
	return make_aware(datetime.now())

def make_aware(time):
	timezone = pytz.timezone('Asia/Kolkata')
	return timezone.localize(time)
