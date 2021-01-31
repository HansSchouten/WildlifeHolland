import sys, getopt, os
from configparser import ConfigParser
from datetime import datetime

from faunamap.monitors import ObsMonitor
from faunamap.export import ObsExporter

def main(argv):
	"""
	FaunaMap entry point.

	"""
	# default arguments
	command = 'monitor'
	parameter = None

	# parse command line arguments
	usage = 'Usage:\n\n$ faunamap.py -c monitor\n'
	try:
		opts, args = getopt.getopt(argv,"hc:p:",["command=","parameter="])
	except getopt.GetoptError:
		print(usage)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(usage)
			sys.exit()
		if opt in ('-c', '--command'):
			command = arg
		if opt in ('-p', '--parameter'):
			parameter = arg

	# parse config
	baseDir = os.path.dirname(os.path.realpath(__file__))
	configFile = baseDir + '/config/faunamap.conf'
	if not os.path.isfile(configFile):
		print('Config file: %s does not exist' % configFile)
		exit(2)
	config = ConfigParser()
	config.read(configFile)
	config.add_section('Global')
	config.set('Global', 'BaseDir', baseDir)

	# run FaunaMap with the passed command
	if command == 'monitor':
		monitor = ObsMonitor(config)
		if monitor.canSync():
			monitor.sync()
	elif command == 'sync-date':
		monitor = ObsMonitor(config)
		date = datetime.strptime(parameter, '%Y-%m-%d').date()
		monitor.syncForDate(date)
	elif command == 'export':
		exporter = ObsExporter(config)
		exporter.exportCsv()


if __name__ == "__main__":
	print(r"""
  _____                       __  __
 |  ___|_ _ _   _ _ __   __ _|  \/  | __ _ _ __
 | |_ / _` | | | | '_ \ / _` | |\/| |/ _` | '_ \
 |  _| (_| | |_| | | | | (_| | |  | | (_| | |_) |
 |_|  \__,_|\__,_|_| |_|\__,_|_|  |_|\__,_| .__/
                                          |_|
	""")
	main(sys.argv[1:])
