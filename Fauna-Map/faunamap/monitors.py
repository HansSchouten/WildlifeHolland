from datetime import date, timedelta
import pprint as pp

from faunamap.scrapers import ObsScraper

class ObsMonitor:
	"""
	This class can monitor observations.

	"""

	def __init__(self, config):
		self.config = config
		self.scraper = ObsScraper(config)

	def sync(self):
		"""
		Sync the local observations with the remote source.

		"""
		today = date.today()
		observations = self.scraper.getObservations(today)