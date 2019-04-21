import datetime

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

	def log(self, message):
		"""
		Log the given message.
		
		"""
		self.logFile.write(str(datetime.datetime.now()) + "\n")
		self.logFile.write(message + "\n\n")
		if self.logToConsole:
			print(message + "\n")