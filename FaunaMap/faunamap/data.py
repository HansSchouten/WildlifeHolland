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

class Observations:
	"""
	This class represents a collection of observations, of different types and in different provinces.

	"""

	def __init__(self, config):
		self.config = config
		self.storage = Storage(config)
		self.data = {}

	def store(self, identifier):
		"""
		Store all observations using the given identifier.

		"""
		self.storage.store(identifier, self.data)

	def load(self, identifier):
		"""
		Load observations stored at the given given identifier.

		"""
		self.data = self.storage.get(identifier)

class Species:
	"""
	This class represents a collection of all known species

	"""

	def __init__(self, config):
		self.config = config
		self.storage = Storage(config)
		self.data = self.storage.get('species')

	def store(self):
		"""
		Store the current list of species.

		"""
		self.storage.store('species', self.data)