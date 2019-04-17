import os, json

class Storage:
	"""
	This class is responsible for retreiving and storing different types of data.

	"""

	def __init__(self, config):
		self.config = config
		self.baseDir = config.get('Global', 'BaseDir')
		self.dataDir = self.baseDir + '/data/'

	def store(self, identifier, data):
		"""
		Store the passed data using the given identifier.

		"""
		with open(self.dataDir + identifier + '.json', 'w') as file:
			json.dump(data, file)

	def get(self, identifier):
		"""
		Retrieve the data stored at the given identifier.

		"""
		if os.path.isfile(self.dataDir + identifier + '.json'):
			with open(self.dataDir + identifier + '.json') as file:
				return json.load(file)
		else:
			return {}