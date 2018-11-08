class ModifyResponseWithHeaders:
	def __init__(self, get_response):
		self.get_response = get_response
		# One-time configuration and initialization.
	
	def __call__(self, request):

		#before
		response = self.get_response(request)
		#after

		headers = {
			'Access-Control-Allow-Origin' : '*',
			'Access-Control-Allow-Headers' : '*',
			'Access-Control-Allow-Methods' : '*'
		}

		for header, value in headers.iteritems():
			response[header] = value

		return response