import time, sys
from pyquery import PyQuery as pq

from faunamap.data import Observations
from faunamap.data import SpecieObservations
from faunamap.data import Observation

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
				for doc in d.find('.app-content-section tbody tr'):
					doc = pq(doc)
					if "geen resultaten" in specie.text():
						continue

					specieObservations = SpecieObservations(self.config)

					# 
					specieObservationsLink = doc.find('td').eq(3).find('a').attr.href
					specieObservationsLink = self.config.get('ObsMonitor', 'BaseUrl') + specieObservationsLink
					print(specieObservationsLink)
					sys.exit()

					# add observation instances for this specie
					observations.addFromSpecie(specie, getObservationsFromSpecie(specie))

					sys.exit()

				
				# relax of the hard work and reduce server workload
				time.sleep(1)
		
		return observations

	def getObservationsFromSpecie(self, specie):
		pass