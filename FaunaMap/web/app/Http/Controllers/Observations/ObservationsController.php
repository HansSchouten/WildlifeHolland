<?php

namespace App\Http\Controllers\Observations;

use App\Models\Observations;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class ObservationsController extends Controller
{
    /**
     * Return a list of observations based on the filters passed in the request.
     *
     * @param  \Illuminate\Http\Request $request
     * @return \Illuminate\Http\Response
     */
    public function index(Request $request)
    {
        $data = Observations::loadFromDate(date('Y-m-d'));

        return response()->json($data);
    }
}
