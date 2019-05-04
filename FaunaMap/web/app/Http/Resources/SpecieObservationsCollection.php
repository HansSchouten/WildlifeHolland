<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\ResourceCollection;
use Illuminate\Support\Facades\Request;

class SpecieObservationsCollection extends ResourceCollection
{
    /**
     * Transform the resource collection into an array.
     *
     * @param  Request  $request
     * @return array
     */
    public function toArray($request)
    {
        // get all observations grouped by specie
        $perSpecie = [];
        foreach ($this->collection as $observation) {
            if (! isset($perSpecie[$observation['specieName']])) {
                $perSpecie[$observation['specieName']] = [];
            }
            $perSpecie[$observation['specieName']][] = $observation;
        }

        // load species data
        $speciesFile = getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        // aggregate observations per specie
        $specieAggregated = [];
        foreach ($perSpecie as $specieName => $observations) {
            $specie = $species[$specieName];

            // get aggregated statistics of all specie observations
            $provinces = [];
            $lastTime = 0;
            $lastTimeString = null;
            foreach ($observations as $observation) {
                $provinces[$observation->province] = true;
                $observationTime = strtotime($observation['timestamp']);
                if ($observationTime > $lastTime) {
                    $lastTime = $observationTime;
                    $lastTimeString = $observation['timestamp'];
                }
            }
            ksort($provinces);
            $provinces = implode(', ', array_keys($provinces));

            $specieAggregated[$specieName] = [
                'name' => $specieName,
                'count' => sizeof($observations),
                'provinces' => $provinces,
                'specieImage' => $specie['imageUrl'],
                'specieAbundance' => $specie['observationCount'],
                'lastObservationTime' => date("H:i", strtotime($lastTimeString)),
            ];
        }

        return $specieAggregated;
    }
}
