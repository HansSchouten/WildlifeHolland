<?php

namespace App\Models;

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

                // add to observationList or update observation information based on province data
                $specie = $species[$specieName];
                if (! isset($observationList[$specieName])) {
                    $observationList[$specieName] = [
                        'name' => $specieName,
                        'observationCount' => sizeof($specieObservations),
                        'provinces' => [$province],
                        'specieImage' => $specie['imageUrl'],
                        'specieAbundance' => $specie['observationCount']
                    ];
                } else {
                    $observationList[$specieName]['provinces'][] = $province;
                    $observationList[$specieName]['observationCount'] += sizeof($specieObservations);
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
