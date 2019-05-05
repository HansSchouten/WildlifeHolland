<?php

namespace App\Console\Commands;

use App\Models\Observation;
use Illuminate\Console\Command;

class UpdateObservationsIndex extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'observations:update';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Update the observations elastic index.';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Update the observations elastic index by adding the latest found observations.
     */
    public function handle()
    {
        $query = [
            'index' => (new Observation)->getIndexName(),
            'body' => [
                'query' => [
                    'bool' => [
                        'must' => [
                            ['match' => ['date' => date('Y-m-d')]]
                        ],
                    ]
                ]
            ],
            'size' => 10000
        ];
        $knownObservations = Observation::complexSearch($query);
        $knownObservationIds = [];
        foreach ($knownObservations as $knownObservation) {
            $knownObservationIds[] = $knownObservation->id;
        }

        $observations = Observation::getUnseenJsonObservationsOfToday($knownObservationIds);
        $observations->addToIndex();
    }
}
