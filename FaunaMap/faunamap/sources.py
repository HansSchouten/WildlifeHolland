import time
from pyquery import PyQuery as pq

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
		observations = {}

		for group in self.speciesGroups:
			daylist_url = self.baseUrl + 'fieldwork/observations/daylist/?species_group=' + str(group) + '&rarity=' + str(self.minRarity)
			observations[group] = []
			
			for province in self.provinces:
				d = pq(url=daylist_url + '&date=' + date.strftime('%Y-%m-%d') + '&province=' + str(province))
				
				# loop through all species and extract interesting information
				for specie in d.find('.app-content-section tbody tr'):
					specie = pq(specie)
					if "geen resultaten" in specie.text():
						continue
					observation_count = specie.find('td').eq(0).text()
					observation_max = specie.find('td').eq(1).text()
					# extract link to observation(s)
					observation_link = specie.find('td').eq(3).find('a').attr('href')
					observation_link = self.baseUrl + observation_link
					# extract specie name
					name_with_latin = specie.find('td').eq(3).text()
					name = name_with_latin[:name_with_latin.rfind('-')]
					# extract observation(s) location(s)
					location = specie.find('td').eq(4).html()
					location = location.replace('href="', 'href="' + self.baseUrl)
					# add observation instance
					observations[group].append({
						'observation_count': observation_count.strip(),
						'observation_max': observation_max.strip(),
						'observation_link': observation_link.strip(),
						'name': name.strip(),
						'location': location.strip(),
						'province': province
					})
				
				# relax of the hard work and reduce server workload
				time.sleep(1)
		
		return observations