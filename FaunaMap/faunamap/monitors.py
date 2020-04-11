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
		Sync the latest observations with the remote data source.

		"""
		return self.syncForDate(d.today())

	def syncForDate(self, date):
		"""
		Sync observations with the remote data source for the given date.

		"""
		# store starting timestamp
		startTimestamps = self.storage.get('start-timestamps')
		if len(startTimestamps) == 0:
			startTimestamps['list'] = []
		startTimestamps['list'].append(str(datetime.now()))
		self.storage.store('start-timestamps', startTimestamps)

		# load earlier observations from disk
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
