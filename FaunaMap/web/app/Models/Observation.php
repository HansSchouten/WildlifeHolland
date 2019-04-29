<?php

namespace App\Models;

use App\Enums\Province;
use Elasticquent\ElasticquentTrait;
use Illuminate\Database\Eloquent\Model;

class Observation extends Model
{
    use ElasticquentTrait;

    /**
     * Return the ElasticSearch index name of this model.
     *
     * @return string
     */
    function getIndexName()
    {
        return env('ELASTIC_INDEX') . '_observations';
    }

    /**
     * The ElasticSearch settings.
     *
     * @var array
     */
    protected $indexSettings = [
        'analysis' => [
            'char_filter' => [
                'replace' => [
                    'type' => 'mapping',
                    'mappings' => [
                        '&=> and '
                    ],
                ],
            ],
            'filter' => [
                'word_delimiter' => [
                    'type' => 'word_delimiter',
                    'split_on_numerics' => false,
                    'split_on_case_change' => true,
                    'generate_word_parts' => true,
                    'generate_number_parts' => true,
                    'catenate_all' => true,
                    'preserve_original' => true,
                    'catenate_numbers' => true,
                ]
            ],
            'analyzer' => [
                'default' => [
                    'type' => 'custom',
                    'char_filter' => [
                        'html_strip',
                        'replace',
                    ],
                    'tokenizer' => 'whitespace',
                    'filter' => [
                        'lowercase',
                        'word_delimiter',
                    ],
                ],
            ],
        ],
    ];

    /**
     * ElasticSearch mapping.
     */
    protected $mappingProperties = [
        'id' => [
            'type' => 'keyword'
        ],
        'count' => [
            'type' => 'integer'
        ],
        'provinces' => [
            'type' => 'text'
        ],
        'specieName' => [
            'type' => 'text'
        ],
        'specieAbundance' => [
            'type' => 'integer'
        ],
        'date' => [
            'type' => 'keyword',
        ],
        'timestamp' => [
            'type' => 'date',
            'format' => 'yyyy-MM-dd HH:mm||yyyy-MM-dd'
        ],
    ];


    /**
     * Return a collection of observations based on the observation data stored in JSON files.
     */
    public static function getObservationsFromJson()
    {
        // load species data
        $speciesFile = self::getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        // get all json observation files
        $dataFolder = self::getDataPath();
        $observationsFiles = glob($dataFolder . '/observations-*');

        $observations = (new Observation)->newCollection();
        foreach ($observationsFiles as $observationsFile) {
            $date = str_replace('observations-', '', basename($observationsFile, '.json'));
            $jsonObservations = file_get_contents($observationsFile);
            $structuredObservations = json_decode($jsonObservations,true);
            self::addFlattenedObservations($observations, $species, $structuredObservations, $date);
        }

        return $observations;
    }

    /**
     * Flatten a multidimensional array of observations into an array containing all data per observation.
     *
     * @param $observations
     * @param array $species
     * @param array $structuredObservations
     * @param string $date
     */
    protected static function addFlattenedObservations(&$observations, array $species, array $structuredObservations, string $date)
    {
        foreach ($structuredObservations as $specieGroup => $observationsPerProvince) {
            foreach ($observationsPerProvince as $province => $observationsPerSpecie) {
                foreach ($observationsPerSpecie as $specieName => $specieObservations) {
                    // ignore observations of which no specie data is present
                    if (! isset($species[$specieName])) {
                        continue;
                    }
                    $specie = $species[$specieName];

                    foreach ($specieObservations as $observationId => $observation) {
                        $obsInstance = new Observation;
                        $obsInstance->id = $observationId;
                        $obsInstance->province = Province::getKey($province);
                        $obsInstance->specieGroup = $specieGroup;
                        $obsInstance->specieName = $specieName;
                        $obsInstance->specieAbundance = $specie['observationCount'];
                        $obsInstance->date = $date;
                        $obsInstance->timestamp = $date . ' ' . $observation['time'];

                        $observations->push($obsInstance);
                    }
                }
            }
        }
    }




    /**
     * Load a filtered collection of Observations.
     *
     * @param array $filters
     * @return array
     */
    public static function loadFromJson(array $filters = [])
    {
        $date = $filters['date'];

        $observationsFile = self::getDataPath('observations-' . date('Y-m-d', strtotime($date)) . '.json');
        $jsonObservations = file_get_contents($observationsFile);
        $observations = json_decode($jsonObservations,true)[1];

        $speciesFile = self::getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        // map observations per province to a general list of observed species
        $observationList = [];
        foreach ($observations as $province => $provinceObservations) {
            foreach ($provinceObservations as $specieName => $specieObservations) {
                // ignore observations of which no specie data is present
                if (! isset($species[$specieName])) {
                    continue;
                }

                // get time of last the observation
                $lastTime = 0;
                $lastTimeString = null;
                foreach ($specieObservations as $observationId => $observation) {
                    $observationTime = strtotime($observation['time']);
                    if ($observationTime > $lastTime) {
                        $lastTime = $observationTime;
                        $lastTimeString = $observation['time'];
                    }
                }

                // add to observationList or update observation information based on province data
                $specie = $species[$specieName];
                if (! isset($observationList[$specieName])) {
                    $observationList[$specieName] = [
                        'name' => $specieName,
                        'count' => sizeof($specieObservations),
                        'provinces' => Province::getKey($province),
                        'specieImage' => $specie['imageUrl'],
                        'specieAbundance' => $specie['observationCount'],
                        'lastObservationTime' => $lastTimeString,
                        'date' => $date
                    ];
                } else {
                    $observationList[$specieName]['provinces'] .= ', ' . Province::getKey($province);
                    $observationList[$specieName]['count'] += sizeof($specieObservations);

                    // replace time of last observation, if a more recent observation is encountered
                    if ($observationList[$specieName]['lastObservationTime'] === null ||
                        $lastTime > strtotime($observationList[$specieName]['lastObservationTime'])) {
                        $observationList[$specieName]['lastObservationTime'] = $lastTimeString;
                    }
                }
            }
        }

        // sort observations
        usort($observationList, function($a, $b) {
            return $a['specieAbundance'] - $b['specieAbundance'];
        });

        return $observationList;
    }


    /**
     * Return the full data file path with the given filename.
     *
     * @param string $fileName
     * @return bool|string
     */
    public static function getDataPath(string $fileName = '')
    {
        return realpath(base_path() . '/' . env('FAUNAMAP_DATA') . '/' . $fileName);
    }

}
