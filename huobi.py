import httplib, json, time, urllib, hashlib

class Huobi():
	def __init__(self, public_key, private_key):
		self.public_key = public_key
		self.private_key = private_key
		self.connection = httplib.HTTPSConnection('api.huobi.com')
		self.debug = True
		self.error_codes = {
			1: 'Server Error',
			2: 'There is not enough yuan',
			3: 'Transaction has started, can not be started again',
			4: 'Transaction has ended',
			10: 'There is not enough bitcoins',
			26: 'The order does not exist',
			41: 'The order has ended, can not be modified',
			42: 'The order has been canceled, can not be modified',
			44: 'Transaction price is too low',
			45: 'Transaction prices are too high',
			46: 'The small number of transactions, the minimum number 0.001',
			47: 'Too much the number of transactions',
			55: '105% of the purchase price can not be higher than the price of',
			56: 'Selling price can not be less than 95% of the price of',
			64: 'Invalid request',
			65: 'Ineffective methods',
			66: 'Access key validation fails',
			67: 'Private key authentication fails',
			68: 'Invalid price',
			69: 'Invalid quantity',
			70: 'Invalid submission time',
			71: 'Request too many times',
			87: 'The number of transactions is less than 0.1 BTC, please do not bid the price higher than the price of the 1%',
			88: 'The number of transactions is less than 0.1 BTC, please do not sell below the market price of a 1%'
		}

	def sign(self, params):
		params['secret_key'] = self.private_key
		params = self.ksort(params)
		url = urllib.urlencode(params)
		md5 = str(hashlib.md5(url))
		return md5.lower()

	def request(self, method, params):
		params['access_key'] = self.public_key
		params['created'] = time.time()
		params['method'] = method
		params['sign'] = self.sign(params)

		self.connection.request('POST', '/api.php', json.dumps(params))
		response = self.connection.getresponse()

		if (response.status == 200):
			response = json.loads(response.read())
			if 'code' in response:
				if response['code'] in self.error_codes:
					if self.debug:
						print 'Error code: %s, message: %s' % (response['code'], self.error_codes[response['code']])
					return {'success': False, 'error': self.error_codes[response['code']], 'code': response['code']}
				else:
					if self.debug:
						print 'Unknown error #%s' % response['code']
					return {'success': False, 'error': 'Unknown', 'code': response['code']}
			else:
				return {'success': True, 'result': response}
		else:
			if self.debug:
				print 'Server Error'
			return {'success': False}

	def ksort(self, d):
		return [(k,d[k]) for k in sorted(d.keys())]