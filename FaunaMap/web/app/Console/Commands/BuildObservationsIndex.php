<?php

namespace App\Console\Commands;

use App\Models\Observation;
use Illuminate\Console\Command;

class BuildObservationsIndex extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'observations:index';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Rebuild the observations elastic index.';

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
     * Rebuild the observations elastic index.
     */
    public function handle()
    {
        $observations = Observation::getObservationsFromJson();

        Observation::deleteIndex();
        Observation::createIndex();
        Observation::putMapping();

        $observations->addToIndex();
    }
}
