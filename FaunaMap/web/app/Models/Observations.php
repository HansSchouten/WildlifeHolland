<?php

namespace App\Models;

use App\Enums\Province;

class Observations
{

    /**
     * Get the (filtered) collection of Observations from the given date.
     *
     * @param string $date
     * @param array $filters
     * @return array
     */
    public static function loadFromDate(string $date, array $filters = [])
    {
        $observationsFile = self::getDataPath('observations-' . date('Y-m-d', strtotime($date)) . '.json');
        $jsonObservations = file_get_contents($observationsFile);
        $observations = json_decode($jsonObservations,true)[1];

        $speciesFile = self::getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        // map observations per province to a general list of observed species
        $observationList = [];
        foreach ($observations as $province => $provinceObservations) {
            foreach ($provinceObservations as $specieName => $specieObservations) {
                // ignore observations of which no specie data is present
                if (! isset($species[$specieName])) {
                    continue;
                }

                // get time of last the observation
                $lastTime = 0;
                $lastTimeString = null;
                foreach ($specieObservations as $observationId => $observation) {
                    $observationTime = strtotime($observation['time']);
                    if ($observationTime > $lastTime) {
                        $lastTime = $observationTime;
                        $lastTimeString = $observation['time'];
                    }
                }

                // add to observationList or update observation information based on province data
                $specie = $species[$specieName];
                if (! isset($observationList[$specieName])) {
                    $observationList[$specieName] = [
                        'name' => $specieName,
                        'count' => sizeof($specieObservations),
                        'provinces' => Province::getKey($province),
                        'specieImage' => $specie['imageUrl'],
                        'specieAbundance' => $specie['observationCount'],
                        'lastObservationTime' => $lastTimeString
                    ];
                } else {
                    $observationList[$specieName]['provinces'] .= ', ' . Province::getKey($province);
                    $observationList[$specieName]['count'] += sizeof($specieObservations);

                    // replace time of last observation, if a more recent observation is encountered
                    if ($observationList[$specieName]['lastObservationTime'] === null ||
                        $lastTime > strtotime($observationList[$specieName]['lastObservationTime'])) {
                        $observationList[$specieName]['lastObservationTime'] = $lastTimeString;
                    }
                }
            }
        }

        // sort observations
        usort($observationList, function($a, $b) {
            return $a['specieAbundance'] - $b['specieAbundance'];
        });

        return $observationList;
    }


    /**
     * Return the full data file path with the given filename.
     *
     * @param string $fileName
     * @return bool|string
     */
    public static function getDataPath(string $fileName)
    {
        return realpath(base_path() . '/' . env('FAUNAMAP_DATA') . '/' . $fileName);
    }

}
