BAD_REQUEST = 502
FORBIDDEN = 403
NOT_FOUND = 404
UNAUTHORIZED = 401
SERVER_ERROR = 500

def build_body(message, status_code):
	body = {}
	body['success'] = False
	if message is not None:
		body['message'] = message
	if status_code is not None:
		body['status_code'] = status_code
	return body

def assert_custom(cond, message = None, status_code = None):
	if cond == False:
		body = build_body(message, status_code)
		raise Exception(body)

def assert_valid(cond, message = None):
	assert_custom(cond, message, BAD_REQUEST)

def assert_allowed(cond, message = None):
	assert_custom(cond, message, FORBIDDEN)

def assert_authorized(cond, message = None):
	assert_custom(cond, message, UNAUTHORIZED)

def assert_found(obj, message = None):
	if obj is None:
		assert_custom(False, message, NOT_FOUND)
