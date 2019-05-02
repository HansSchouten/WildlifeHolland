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
        $observations = [];
        foreach ($this->collection as $observation) {
            $observationArray = $observation->toArray();

            $latLong = explode(',', $observationArray['location']);
            $observationArray['lat'] = $latLong[0];
            $observationArray['long'] = $latLong[1];
            $observationArray['timestamp'] = date('d-m-Y H:i', strtotime($observationArray['timestamp']));

            $observations[] = $observationArray;
        }
        return $observations;
    }
}
