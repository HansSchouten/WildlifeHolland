import os, json
import glob
import csv

class Storage:
	"""
	This class is responsible for retrieving and storing different types of data.

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

	def delete(self, identifier):
		"""
		Delete the data stored with the given identifier.

		"""
		if os.path.isfile(self.dataDir + identifier + '.json'):
			os.remove(self.dataDir + identifier + '.json')
		elif os.path.isfile(self.dataDir + identifier + '.csv'):
			os.remove(self.dataDir + identifier + '.csv')

	def writeCsv(self, identifier, data):
		"""
		Store the passed data using the given identifier.

		"""
		with open(self.dataDir + identifier + '.csv', 'w') as csvFile:
			writer = csv.DictWriter(csvFile, fieldnames=data[0].keys())
			writer.writeheader()
			for entry in data:
				writer.writerow(entry)

	def list(self):
		"""
		List all stored data files.

		"""
		dataFiles = glob.glob(self.dataDir + "/observations-*.json")
		dataFiles.sort()
		return dataFiles


class Observations:
	"""
	This class represents a collection of observations.

	"""

	def __init__(self, config, date):
		self.config = config
		self.date = date
		self.storage = Storage(config)
		self.identifier = 'observations-' + date.strftime('%Y-%m-%d')
		self.data = {}
		self.flattened = {}

	def store(self):
		"""
		Store all observations using the given identifier.

		"""
		self.storage.store(self.identifier, self.data)

	def load(self):
		"""
		Load observations stored at the given given identifier.

		"""
		self.data = self.storage.get(self.identifier)

		# map data to flattened observations
		for specieGroup in self.data:
			for province in self.data[specieGroup]:
				for specieName in self.data[specieGroup][province]:
					for observationId in self.data[specieGroup][province][specieName]:
						observation = self.data[specieGroup][province][specieName][observationId]
						self.flattened[observationId] = observation.copy()

	def add(self, observationData):
		"""
		Add specie observations to this collection of all observations.

		"""
		obs = observationData
		if obs['specieGroup'] not in self.data:
			self.data[obs['specieGroup']] = {}

		if obs['province'] not in self.data[obs['specieGroup']]:
			self.data[obs['specieGroup']][obs['province']] = {}

		if obs['specieName'] not in self.data[obs['specieGroup']][obs['province']]:
			self.data[obs['specieGroup']][obs['province']][obs['specieName']] = {}

		self.data[obs['specieGroup']][obs['province']][obs['specieName']][obs['id']] = observationData
		self.flattened[obs['id']] = observationData

		# save observations to storage
		self.store()

	def needsUpdate(self, specieGroup, province, specieName, observationCount):
		"""
		Return whether the given specie observations are already part of this observations collection.

		"""
		if specieGroup not in self.data:
			return True

		if province not in self.data[specieGroup]:
			return True

		if specieName not in self.data[specieGroup][province]:
			return True

		if len(self.data[specieGroup][province][specieName]) < int(observationCount):
			return True

		return False

	def contains(self, observationId):
		"""
		Return whether an observation with the given id is known.

		"""
		return observationId in self.flattened

	def getList(self):
		"""
		Get a flattened list of all observations.

		"""
		return self.flattened


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

	def contains(self, name):
		"""
		Return whether a specie with the given name is known.

		"""
		return name in self.data

	def add(self, specie):
		"""
		Add a new specie with the given specie data.

		"""
		self.data[specie['name']] = specie

		# save species to storage
		self.store()
