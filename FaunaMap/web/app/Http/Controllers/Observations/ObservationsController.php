<?php

namespace App\Http\Controllers\Observations;

use App\Http\Resources\SpecieObservationsCollection;
use App\Models\Observation;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class ObservationsController extends Controller
{

    /**
     * Return a list of observations based on the filters passed in the request.
     *
     * @param Request $request
     * @return SpecieObservationsCollection
     */
    public function index(Request $request)
    {
        $filters = [
            'date' => date('Y-m-d')
        ];
        $observations = Observation::search($filters);

        return new SpecieObservationsCollection($observations);
    }
}
