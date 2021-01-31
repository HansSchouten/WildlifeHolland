<?php

namespace App\Console\Commands;

use App\Models\Observation;
use Illuminate\Console\Command;

class ImportSinceDate extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'observations:import {since}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Import observations into elastic since the given date.';

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
        $since = basename($this->argument('since'));

        $period = new \DatePeriod(
            new \DateTime($since),
            new \DateInterval('P1D'),
            now()
        );
        foreach ($period as $key => $date) {
            $this->importForDate($date->format('Y-m-d'));
        }
    }

    protected function importForDate($date)
    {
        $query = [
            'index' => (new Observation)->getIndexName(),
            'body' => [
                'query' => [
                    'bool' => [
                        'must' => [
                            ['match' => ['date' => $date]]
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

        $observations = Observation::getUnseenJsonObservationsOfDate($knownObservationIds, $date);
        $observations->addToIndex();
    }
}
