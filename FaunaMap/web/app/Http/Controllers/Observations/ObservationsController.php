<?php

namespace App\Http\Controllers\Observations;

use App\Http\Resources\ObservationsCollection;
use App\Http\Resources\SpecieObservationsCollection;
use App\Models\Observation;
use Carbon\Carbon;
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
        $hoursPeriod = 24;
        if (isset($request->period)) {
             $hoursPeriod = intval(json_decode($request->period)->id);
        }
        $timestamp = Carbon::now()->subHours($hoursPeriod)->format('Y-m-d H:i');

        $parameters = [
            'must' => [
                'date' => $request->date ?? null,
            ],
            'timestamp' => $timestamp
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
    public function list(Request $request)
    {
        $hoursPeriod = 24;
        if (isset($request->period)) {
            $hoursPeriod = intval(json_decode($request->period)->id);
        }
        $timestamp = Carbon::now()->subHours($hoursPeriod)->format('Y-m-d H:i');

        $parameters = [
            'must' => [
                'date' => $request->date ?? null,
                'specieName' => $request->specie ?? null
            ],
            'timestamp' => $timestamp
        ];
        $observations = Observation::search($parameters);
        return new ObservationsCollection($observations);
    }
}
