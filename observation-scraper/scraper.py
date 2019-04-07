import sys, time, os
import urllib, urllib.request, json

from datetime import date, timedelta
from pyquery import PyQuery as pq
from lxml import etree


# settings
species_groups = [1, 2, 3]
provinces = [9, 10]
rarity = 2

# constants
dir = os.path.dirname(__file__)
base_url = 'https://waarneming.nl/'
today = date.today() - timedelta(0)
date = today


def main(argv):
    observations = getObservations(date)
    storeObservations(observations, date)
    appendSpeciesData(observations)
    
def getObservations(date):
    observations = {}

    for group in species_groups:
        daylist_url = base_url + 'fieldwork/observations/daylist/?species_group=' + str(group) + '&rarity=' + str(rarity)
        observations[group] = []
    
        for province in provinces:
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
                observation_link = base_url + observation_link
                # extract specie name
                name_with_latin = specie.find('td').eq(3).text()
                name = name_with_latin[:name_with_latin.rfind('-')]
                # extract observation(s) location(s)
                location = specie.find('td').eq(4).html()
                location = location.replace('href="', 'href="' + base_url)
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


def storeObservations(observations, date):
    with open(dir + '/data/observations-' + date.strftime('%Y-%m-%d') + '.json', 'w') as file:
        json.dump(observations, file)


def appendSpeciesData(observations):
    # read current species database
    with open(dir + '/data/species.json') as file:
        species = json.load(file)
    # extend species database if this species has not been encountered before
    for group in observations:
        for observation in observations[group]:
            storeSpecieDetails(species, observation['name'])

def storeSpecieDetails(species, name):
    # skip if species is already known
    if name in species:
        return
    # request specie id
    id = getSpecieIdByName(name)
    if id is None:
        return
    # request specie details
    d = pq(url=base_url + "species/" + id)
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
    with open(dir + '/data/species.json', 'w') as file:
        json.dump(species, file)
    # relax of the hard work and reduce server workload
    print('Details of ' + name + ' saved')
    time.sleep(1)

def getSpecieIdByName(name):
    d = pq(url=base_url + "species/search/?species_group=1&deep=on&q=" + name)
    el = d.find('#search-results-table tr').eq(1)
    if pq(el).text() == '':
        return None
    href = pq(el.find('a')).attr('href')
    if len(href) < 11:
        return None
    return href[9:-1]


if __name__ == "__main__":
    main(sys.argv)