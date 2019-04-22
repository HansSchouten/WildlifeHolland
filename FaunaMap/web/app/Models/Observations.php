<?php

namespace App\Models;

class Observations
{

    /**
     * Get the collection of Observations from the given date.
     *
     * @param string $date
     * @return array
     */
    public static function loadFromDate(string $date)
    {
        $observationsFile = self::getDataPath('observations-' . date('Y-m-d', strtotime($date)) . '.json');
        $jsonObservations = file_get_contents($observationsFile);
        $observations = json_decode($jsonObservations,true);

        $speciesFile = self::getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        return [
            'observations' => $observations,
            'species' => $species
        ];
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
