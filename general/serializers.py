from django.db.models.fields.files import ImageFieldFile, FileField, FieldFile
from django.db.models import Model
from datetime import datetime

def get_json_serializable(instance, *args):
	data = {}
	fields = get_all_fields(instance)
	for field in args:
		if field in fields:
			continue
		fields.append(field)
	for field in fields:
		val = getattr(instance, field, None)
		if isinstance(val, datetime):
			val = str(val)
		if isinstance(val, ImageFieldFile) or isinstance(val, FileField) or isinstance(val, FieldFile):
			try:
				val = val.url
			except:
				continue
		if isinstance(val, Model):
			val = get_json_serializable(val)
		data[field] = val
	return data

def serialize(classmodel, *args, **kwargs):
	response = []
	for model_object in classmodel.objects.filter(**kwargs):
		data = get_json_serializable(model_object, *args)
		response.append(data)

	return response

def get_all_fields(classmodel):
	return [ f.name for f in classmodel._meta.fields + classmodel._meta.many_to_many ]
