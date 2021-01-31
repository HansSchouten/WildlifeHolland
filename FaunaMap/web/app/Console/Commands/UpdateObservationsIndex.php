<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Artisan;

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
        Artisan::call("observations:import", ['since' => date("Y-m-d")]);
    }
}
