from datetime import date as d, timedelta
from datetime import datetime
from pprint import pprint

from faunamap.data import Storage
from faunamap.data import Observations
from faunamap.data import Species

class ObsExporter:
	"""
	This class can export observations.

	"""

	def __init__(self, config):
		self.config = config
		self.storage = Storage(config)

	def exportCsv(self):
		"""
		Export all observations as CSV file.

		"""
		entries = []

		for dataFile in self.storage.list():
			dateString = dataFile.replace('.json', '').split('-', 1)[1]
			date = datetime.strptime(dateString, '%Y-%m-%d')
			observations = Observations(self.config, date)
			observations.load()

			specieGroups = ['Vogels', 'Zoogdieren', 'Reptielen en amfibieën']
			provinces = ['Utrecht', 'Noord-Holland', 'Friesland', 'Groningen', 'Drenthe', 'Overijssel', 'Gelderland', 'Flevoland', 'Zuid-Holland', 'Noord-Brabant', 'Limburg', 'Zeeland']

			for (id, rawObservation) in observations.getList().items():
				observation = {}
				observation['id'] = rawObservation['id']
				observation['timestamp'] = dateString
				if (rawObservation['time'] != None):
					observation['timestamp'] += ' ' + rawObservation['time']
				observation['specieName'] = rawObservation['specieName']
				observation['specieGroup'] = specieGroups[int(rawObservation['specieGroup']) - 1]
				observation['province'] = provinces[int(rawObservation['province']) - 1]
				observation['latitude'] = rawObservation['lat']
				observation['longitude'] = rawObservation['long']

				entries.append(observation)

		entries = sorted(entries, key=lambda k: k['id'])
		self.storage.writeCsv('export', entries)
