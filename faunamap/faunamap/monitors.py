
class ObsMonitor:
	"""
	This class can monitor observations.

	"""

	def __init__(self, config):
		self.config = config

	def sync(self):
		"""
		Sync the local observations with the remote source.

		"""
		