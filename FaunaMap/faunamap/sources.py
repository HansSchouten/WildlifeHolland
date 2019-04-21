import time, sys
import random
from pyquery import PyQuery as pq
from pprint import pprint
from datetime import date as d
from urllib.parse import quote

from faunamap.data import Observations
from faunamap.data import Species

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

	def getDoc(self, url):
		"""
		Return the HTML document stored at the given url.

		"""
		print(url)

		# relax of the hard work and reduce remote server workload
		time.sleep(1 + random.uniform(0, 2))

		# request the document
		return pq(url=url)

	def syncObservations(self, observations):
		"""
		Add new observations to the passed observations collection.

		"""
		species = Species(self.config)
		date = observations.date
		observationData = {}
		
		print('Gathering observations...')

		for specieGroup in self.speciesGroups:
			observationData['specieGroup'] = specieGroup
			daylistUrl = self.baseUrl + 'fieldwork/observations/daylist/?species_group=' + str(specieGroup) + '&rarity=' + str(self.minRarity)
			
			for province in self.provinces:
				observationData['province'] = province
				doc = self.getDoc(daylistUrl + '&date=' + date.strftime('%Y-%m-%d') + '&province=' + str(province))
				
				# loop through all species and extract necessary information
				for specieRow in doc.find('.app-content-section tbody tr'):
					specieRow = pq(specieRow)
					if "geen resultaten" in specieRow.text():
						break

					try:
						# get observation count
						observationCount = specieRow.find('td').eq(0).text()

						# extract specie name
						nameWithLatin = specieRow.find('td').eq(3).text()
						observationData['specieName'] = nameWithLatin[:nameWithLatin.rfind('-')].strip()

						# if specie is unknown, retrieve specie details
						if not species.contains(observationData['specieName']):
							self.addSpecie(species, specieGroup, observationData['specieName'])

						# extract specie observations list link
						specieObservationsLink = specieRow.find('td').eq(3).find('a').attr('href')
						specieObservationsLink = self.baseUrl + specieObservationsLink[1::]

						# only add/update these specie observations if they are not already part of the observations collection
						if observations.needsUpdate(specieGroup, province, observationData['specieName'], observationCount):
							# in case this is a single observation, add observation directly
							if '/observation/' in specieObservationsLink:
								self.addObservation(observations, specieObservationsLink, observationData)
							else:
								self.addSpecieObservations(observations, specieObservationsLink, observationData)
					except:

		
		return observations

	def addSpecieObservations(self, observations, specieObservationsLink, observationData):
		"""
		Add all specie observations from the remote source using the provided link.

		"""
		# add species of page 1, which always exists
		doc = self.getDoc(specieObservationsLink)
		self.addSpecieObservationsFromDoc(observations, observationData, doc)

		# if document does not contain pagination return from this method
		if doc.find('.pagination').html() is None:
			return

		page = 1
		while True:
			# add observations of this page of specie observations
			page += 1
			doc = self.getDoc(specieObservationsLink + '&page=' + str(page))
			self.addSpecieObservationsFromDoc(observations, observationData, doc)

			# if no more pages exist, return from this method
			if doc.find('.pagination').eq(0).find('.last.disabled').html() is not None:
				return

	def addSpecieObservationsFromDoc(self, observations, observationData, doc):
		"""
		Add all specie observations from the remote source using the provided html document.

		"""
		# loop through all observations and extract necessary information
		for observationRow in doc.find('.app-content-section tbody tr'):
			observationRow = pq(observationRow)

			# extract observation link
			observationUrl = observationRow.find('td').eq(0).find('a').attr('href')
			observationUrl = self.baseUrl + observationUrl[1::]
			
			# add observation
			self.addObservation(observations, observationUrl, observationData)

	def addObservation(self, observations, observationUrl, observationData):
		"""
		Create a new observation into the passed collection using the info stored at the passed link.

		"""
		# extract observation id
		observationData['id'] = observationUrl.split('/')[-2:][0]

		# return this method if the observation is already present in the observations collection
		if observations.contains(observationData['id']):
			return

		# request observation page
		doc = self.getDoc(observationUrl)

		# extract observation time
		observationTimeParts = doc.find('.app-grid-table tr:first-of-type td').eq(0).text().split(' ')
		observationData['time'] = None
		if len(observationTimeParts) == 2:
			observationData['time'] = observationTimeParts[1]

		# extract the latitude and longitude of the observation
		latLong = doc.find('.teramap-coordinates-coords').eq(0).text().split(', ')
		
		# the observation is only usable if location details are present
		if len(latLong) == 2:
			observationData['lat'] = latLong[0]
			observationData['long'] = latLong[1]

			# add observation
			observations.add(observationData.copy())


	def addSpecie(self, species, specieGroup, name):
		"""
		Load details of the specie with the given name and append the species collection.

		"""
		# request specie id
		id = self.getSpecieIdByName(specieGroup, name)
		if id is None:
			return

		# request specie details
		doc = self.getDoc(self.baseUrl + "species/" + id)
		specie = {
			'name': name,
			'id': id, 'url':
			self.baseUrl + "species/" + id,
			'lastUpdateDate': d.today().strftime('%Y-%m-%d')
		}

		# extract taxonomy family
		el = doc.find('.label-group a.label-primary').eq(0)
		specie['family'] = el.text().strip()
		specie['familyUrl'] = self.baseUrl + el.attr('href')[1::]

		# extract image
		el = doc.find('img.app-ratio-box-image').eq(0)
		if pq(el).attr('src') == None:
			return
		specie['imageUrl'] = pq(el).attr('src')

		# extract number of observations
		html = doc.html()
		indexStart = html.rfind('num_observations') + 19
		indexEnd = int(html.find('}', indexStart))
		observationCount = html[indexStart:indexEnd]
		if not observationCount.isdigit():
			return
		specie['observationCount'] = observationCount.strip()

		# append species
		species.add(specie)

	def getSpecieIdByName(self, specieGroup, name):
		"""
		Return the remote specie id given a species name.

		"""
		doc = self.getDoc(self.baseUrl + "species/search/?species_group=" + str(specieGroup) + "&deep=on&q=" + quote(name))
		el = doc.find('#search-results-table tr').eq(1)

		# return None if no results are found
		if pq(el).text() == '':
			return None

		# extract specie id from search result url
		href = pq(el.find('a')).attr('href')
		if len(href) < 11:
			return None
		return href[9:-1]