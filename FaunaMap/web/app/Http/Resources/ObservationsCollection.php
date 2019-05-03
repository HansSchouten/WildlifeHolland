<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;
use Illuminate\Support\Facades\Request;

class ObservationsCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @param  Request  $request
     * @return array
     */
    public function toArray($request)
    {
        // load species data
        $speciesFile = getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        // get min and max observation counts of all species
        $min = PHP_INT_MAX;
        $max = 0;
        foreach ($species as $specie) {
            $min = min($specie['observationCount'], $min);
            $max = max($specie['observationCount'], $max);
        }

        $observations = [];
        foreach ($this->collection as $observation) {
            $observationArray = $observation->toArray();

            $latLong = explode(',', $observationArray['location']);
            $observationArray['lat'] = $latLong[0];
            $observationArray['long'] = $latLong[1];
            $observationArray['minSpeciesCount'] = $min;
            $observationArray['maxSpeciesCount'] = $max;
            $observationArray['timestamp'] = date('d-m-Y H:i', strtotime($observationArray['timestamp']));

            $observations[] = $observationArray;
        }
        return $observations;
    }
}
