from datetime import date as d, timedelta
from datetime import datetime
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
		# return if the SyncDelay has not passed since the previous sync
		if not self.canSync():
			return

		# load today's observations from disk
		date = d.today()
		observations = Observations(self.config, date)
		observations.load()

		# add new observations from the remote source
		self.remoteSource.syncObservations(observations)

		return observations

	def canSync(self):
		"""
		Return whether a sync can be performed, based on the SyncDelay.
		
		"""
		status = self.storage.get('status')
		if status == {}:
			return True

		# compute number of seconds from the last sync update till now
		lastSyncUpdate = datetime.strptime(status['lastSyncUpdate'], '%Y-%m-%d %H:%M:%S.%f')
		delta = datetime.now() - lastSyncUpdate

		# return true/false based on the period since the last update and the SyncDelay
		return delta.total_seconds() > int(self.config.get('ObsMonitor', 'SyncDelay'))