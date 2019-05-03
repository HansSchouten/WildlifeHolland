<?php

namespace App\Http\Controllers\Observations;

use App\Http\Resources\ObservationsCollection;
use App\Http\Resources\SpecieObservationsCollection;
use App\Models\Observation;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class ObservationsController extends Controller
{

    /**
     * Return a list of observations aggregated per specie based on the filters passed in the request.
     *
     * @param Request $request
     * @return ObservationsCollection|SpecieObservationsCollection
     */
    public function species(Request $request)
    {
        $parameters = [
            'filters' => [
                'date' => $request->date ?? date('Y-m-d')
            ]
        ];
        $observations = Observation::search($parameters);
        return new SpecieObservationsCollection($observations);
    }

    /**
     * Return a list of observations based on the filters passed in the request.
     *
     * @param Request $request
     * @return ObservationsCollection|SpecieObservationsCollection
     */
    public function map(Request $request)
    {
        $parameters = [
            'filters' => [
                'date' => $request->date ?? date('Y-m-d'),
                'specieName' => $request->specie ?? null
            ]
        ];
        $observations = Observation::search($parameters);
        return new ObservationsCollection($observations);
    }
}
