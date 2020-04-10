# Copyright (c) 2015 LunaNode Hosting Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

class LNDynamic:
	LNDYNAMIC_URL = 'https://dynamic.lunanode.com/api/{CATEGORY}/{ACTION}/'

	def __init__(self, api_id, api_key):
		if len(api_id) != 16:
			raise LNDAPIException('supplied api_id incorrect length, must be 16')
		if len(api_key) != 128:
			raise LNDAPIException('supplied api_key incorrect length, must be 128')

		self.api_id = api_id
		self.api_key = bytes(api_key, 'utf-8')
		self.partial_api_key = api_key[:64]

	def request(self, category, action, params = {}):
		import json
		import time
		import hmac
		import hashlib
		import requests

		url = self.LNDYNAMIC_URL.format(CATEGORY=category, ACTION=action)
		request_array = dict(params)
		request_array['api_id'] = self.api_id
		request_array['api_partialkey'] = self.partial_api_key
		request_raw = json.dumps(request_array)
		nonce = str(int(time.time()))
		handler = '{CATEGORY}/{ACTION}/'.format(CATEGORY=category, ACTION=action)
		hasher = hmac.new(self.api_key, bytes('{handler}|{raw}|{nonce}'.format(handler=handler, raw=request_raw, nonce=nonce), 'utf-8'), hashlib.sha512)
		signature = hasher.hexdigest()

		data = {'req': request_raw, 'signature': signature, 'nonce': nonce}
		content = requests.post(url, data=data).json()
		# content is now a dictionary, NOT a string
		if 'success' not in content:
			raise APIException('Server gave invalid repsonse (missing success key)')
		elif content['success'] != 'yes':
			if 'error' in content:
				raise APIException('API error: ' + content['error'])
			else:
				raise APIException('Unknown API error')
		return content

class LNDAPIException(Exception):
	pass

class APIException(Exception):
	pass