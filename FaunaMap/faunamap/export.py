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
