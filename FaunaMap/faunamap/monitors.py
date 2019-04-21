from datetime import date as d, timedelta
from pprint import pprint

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
		Sync observations with the remote data source.

		"""
		# load today's observations from disk
		date = d.today()
		observations = Observations(self.config, date)
		observations.load()

		# add new observations from the remote source
		self.remoteSource.syncObservations(observations)

		return observations