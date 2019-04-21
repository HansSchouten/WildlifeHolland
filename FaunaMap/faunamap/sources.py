import time, sys
from pyquery import PyQuery as pq
from pprint import pprint

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
		observations = Observations(self.config, date)
		observations.load()
		observationData = {}

		for specieGroup in self.speciesGroups:
			observationData['specieGroup'] = specieGroup
			daylistUrl = self.baseUrl + 'fieldwork/observations/daylist/?species_group=' + str(specieGroup) + '&rarity=' + str(self.minRarity)
			
			for province in self.provinces:
				observationData['province'] = province
				doc = pq(url=daylistUrl + '&date=' + date.strftime('%Y-%m-%d') + '&province=' + str(province))
				
				# loop through all species and extract necessary information
				for specieRow in doc.find('.app-content-section tbody tr'):
					specieRow = pq(specieRow)
					if "geen resultaten" in specieRow.text():
						break

					# get observation count
					observationCount = specieRow.find('td').eq(0).text()

	                # extract specie name
					nameWithLatin = specieRow.find('td').eq(3).text()
					observationData['specieName'] = nameWithLatin[:nameWithLatin.rfind('-')].strip()

					# extract specie observations list link
					specieObservationsLink = specieRow.find('td').eq(3).find('a').attr('href')
					specieObservationsLink = self.baseUrl + specieObservationsLink[1::]

					# only add/update these specie observations if they are not already part of the observations collection
					if observations.needsUpdate(specieGroup, province, observationData['specieName'], observationCount):
						self.loadSpecieObservations(observations, specieObservationsLink, observationData)

					pprint(observations.data)
					sys.exit()

				
				# relax of the hard work and reduce server workload
				time.sleep(1)
		
		return observations

	def loadSpecieObservations(self, observations, specieObservationsLink, observationData):
		"""
		Load all specie observations from the remote source using the provided link.

		"""
		doc = pq(url=specieObservationsLink)

		# loop through all observations and extract necessary information
		for observationRow in doc.find('.app-content-section tbody tr'):
			observationRow = pq(observationRow)

			# extract observation time
			observationTimeParts = observationRow.find('td').eq(0).text().split(' ')
			observationData['time'] = None
			if len(observationTimeParts) == 2:
				observationData['time'] = observationTimeParts[1]

			# extract observation link
			observationUrl = observationRow.find('td').eq(0).find('a').attr('href')
			observationData['url'] = self.baseUrl + observationUrl[1::]
			
			# extract observation id
			observationData['id'] = observationUrl.split('/')[-2:][0]

			# add the observation details if this observation is not yet in specieObservations
			if not observations.contains(observationData['id']):
				self.loadObservation(observations, observationData)

	def loadObservation(self, observations, observationData):
		"""
		Create a new observation into the passed collection using the info stored at the passed link.

		"""
		doc = pq(url=observationData['url'])

		# extract the latitude and longitude of the observation
		latLong = doc.find('.teramap-coordinates-coords').eq(0).text().split(', ')
		observationData['lat'] = latLong[0]
		observationData['long'] = latLong[1]

		# add observation to specieObservations
		observations.add(observationData.copy())