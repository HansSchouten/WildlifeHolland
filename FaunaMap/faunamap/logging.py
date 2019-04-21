from datetime import datetime

from faunamap.data import Storage

class Logger:
	"""
	This class can log events to file.

	"""

	def __init__(self, config):
		self.config = config

		# open log file in write mode
		logFilePath = self.config.get('Logging', 'logFile')
		self.logToConsole = self.config.get('Logging', 'logToConsole')
		self.logFile = open(logFilePath, "a")
		self.storage = Storage(config)

	def log(self, message):
		"""
		Log the given message.
		
		"""
		self.logFile.write(str(datetime.now()) + "\n")
		self.logFile.write(message + "\n\n")
		if self.logToConsole:
			print(message + "\n")

	def updateStatus(self):
		"""
		Update the status in storage, indicating this process is still running.

		"""
		self.storage.store('status', {'lastSyncUpdate': str(datetime.now()) })