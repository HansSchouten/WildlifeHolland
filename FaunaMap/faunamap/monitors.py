from datetime import date as d, timedelta
import pprint as pp

from faunamap.sources import ObsScraper
from faunamap.data import Storage
from faunamap.data import Observations
from faunamap.data import Species

class ObsMonitor:
	"""
	This class can monitor observations.

	"""

	def __init__(self, config):
		self.config = config
		self.remoteSource = ObsScraper(config)
		self.storage = Storage(config)

	def sync(self):
		"""
		Sync with the remote data source.

		"""
		observations = self.syncObservations()
		self.syncSpecies(observations)

	def syncObservations(self):
		"""
		Sync the local observations with the remote source.

		"""
		date = d.today()
		observations = self.remoteSource.getObservations(date)

		# store today's observations
		observations.store('observations-' + date.strftime('%Y-%m-%d'))

		return observations

	def syncSpecies(self, observations):
		"""
		Sync the local species list with the remote source based on the new observations.

		"""
		# load the current collection of species
		species = Species()