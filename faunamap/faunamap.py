import sys, getopt

from faunamap.config import Config
from faunamap.monitors import ObsMonitor

def main(argv):
	"""
	FaunaMap entry point.
	"""
	# default arguments
	command = "monitor"

	# parse command line arguments
	usage = 'Usage:\n\n$ faunamap.py -c monitor\n'
	try:
		opts, args = getopt.getopt(argv,"hc:",["command="])
	except getopt.GetoptError:
		print(usage)
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print(usage)
			sys.exit()
		if opt in ('-c', '--command'):
			command = arg

	# parse config
	config = Config()

	# run FaunaMap with the passed command
	if command == 'monitor':
		monitor = ObsMonitor(config)
		monitor.sync()
	

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