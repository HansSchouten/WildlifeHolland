import sys, time
import urllib, urllib.request, json

from datetime import date, timedelta
from pyquery import PyQuery as pq
from lxml import etree

# variables
today = date.today()
yesterday = date.today() - timedelta(1)

# read main files
with open('data/species.json') as file:
	species = json.load(file)


def main(argv):
	species_observed = getDayData(today)
	appendSpeciesData(species_observed, species)


def appendSpeciesData(species_observed, species):
	for specie_observed in species_observed:
		storeSpecieDetails(specie_observed['name'])


def storeSpecieDetails(name):
	# skip if species is already known
	if name in species:
		return
	# request specie id
	id = getSpecieIdByName(name)
	if id is None:
		return
	# request specie details
	d = pq(url="https://waarneming.nl/species/" + id)
	specie = {'name': name, 'id': id}
	# extract image
	el = d.find('img.app-ratio-box-image').eq(0)
	if pq(el).attr('src') == None:
		return
	specie['image'] = pq(el).attr('src')
	# extract number of observations
	html = d.html()
	index_start = html.rfind('num_observations') + 19
	index_end = int(html.find('}', index_start))
	observation_count = html[index_start:index_end]
	if not observation_count.isdigit():
		return
	specie['observation_count'] = observation_count.strip()
	# append species
	species[name] = specie
	# write updated species to disk
	with open('species.json', 'w') as file:
		json.dump(species, file)
	# relax of the hard work and reduce server workload
	print('Details of ' + name + ' saved')
	time.sleep(1)

def getSpecieIdByName(name):
	d = pq(url="https://waarneming.nl/species/search/?species_group=1&q=" + name)
	el = d.find('#search-results-table tr').eq(1)
	if pq(el).text() == '':
		return None
	href = pq(el.find('a')).attr('href')
	if len(href) < 11:
		return None
	return href[9:-1]


def getDayData(date):
	provinces = [9, 10]
	rarity = 2
	daylist_url = 'https://waarneming.nl/fieldwork/observations/daylist/?species_group=1&rarity=' + str(rarity)
	d = pq(url=daylist_url + '&date=' + date.strftime('%Y-%m-%d') + '&province=' + str(provinces[1]))
	
	species_observed = []
	# loop through all species and extract interesting information
	for specie in d.find('.app-content-section tbody tr'):
		specie = pq(specie)
		observation_count = specie.find('td').eq(0).text()
		observation_max = specie.find('td').eq(1).text()
		name_with_latin = specie.find('td').eq(3).text()
		name = name_with_latin[:name_with_latin.rfind('-')]
		location = specie.find('td').eq(4).html()
		# add specie observations
		species_observed.append({
			'observation_count' : observation_count.strip(),
			'observation_max' : observation_max.strip(),
			'name' : name.strip(),
			'location' : location.strip(),
		})
	
	with open('data/observations.json', 'w') as file:
		json.dump(species_observed, file)
	
	return species_observed

if __name__ == "__main__":
	main(sys.argv)