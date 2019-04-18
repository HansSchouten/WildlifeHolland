import time, sys
from pyquery import PyQuery as pq

from faunamap.data import Observation
from faunamap.data import Observations

class ObsScraper:
	"""
	This class can scrape observations.

	"""

	def __init__(self, config):
		self.config = config
		self.baseUrl = config.get('ObsMonitor', 'BaseUrl')
		self.speciesGroups = config.get('ObsMonitor', 'SpeciesGroups').split(',')
		self.provinces = config.get('ObsMonitor', 'Provinces').split(',')
		self.minRarity = config.get('ObsMonitor', 'MinRarity')

	def getObservations(self, date):
		"""
		Return the observations of a specific date

		"""
		print('Gathering observations...')
		observations = Observations(self.config)

		for group in self.speciesGroups:
			daylist_url = self.baseUrl + 'fieldwork/observations/daylist/?species_group=' + str(group) + '&rarity=' + str(self.minRarity)
			
			for province in self.provinces:
				d = pq(url=daylist_url + '&date=' + date.strftime('%Y-%m-%d') + '&province=' + str(province))
				
				# loop through all species and extract interesting information
				for specie in d.find('.app-content-section tbody tr'):
					specie = pq(specie)
					if "geen resultaten" in specie.text():
						continue

					# get the number of observations and largest observed group size
					specie_count = specie.find('td').eq(0).text().strip()
					specie_groupSize = specie.find('td').eq(1).text().strip()

					# extract link to observation(s)
					specie_link = specie.find('td').eq(3).find('a').attr('href')
					specie_link = self.baseUrl + observation_link

					# extract specie name
					specie_name_with_latin = specie.find('td').eq(3).text()
					specie_name = specie_name_with_latin[:specie_name_with_latin.rfind('-')]

					# extract observation(s) location(s)
					specie_location = specie.find('td').eq(4).html()
					specie_location = specie_location.replace('href="', 'href="' + self.config.get('ObsMonitor', 'BaseUrl'))

					# add observation instances for this specie

					sys.exit()

				
				# relax of the hard work and reduce server workload
				time.sleep(1)
		
		return observations

	#def getObservationsFromSpecie(self, )