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
        'province' => [
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
     * Return a collection of observations aggregated per specie.
     *
     * @param array $filters
     * @return array
     */
    public function getSpecieAggregatedObservations(array $filters = [])
    {
        $date = $filters['date'];

        // get all observations that satisfy the given filters
        $observations = Observation::complexSearch([
            'body' => [
                'query' => [
                    'match' => [
                        'date' => $date
                    ]
                ],
                'sort' => [
                    ['specieAbundance' => 'asc']
                ]
            ],
            'size' => 1000
        ]);

        // get all observations grouped by specie
        $perSpecie = [];
        foreach ($observations as $observation) {
            if (! isset($perSpecie[$observation['specieName']])) {
                $perSpecie[$observation['specieName']] = [];
            }
            $perSpecie[$observation['specieName']][] = $observation;
        }

        // load species data
        $speciesFile = self::getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        // aggregate observations per specie
        $specieAggregated = [];
        foreach ($perSpecie as $specieName => $observations) {
            $specie = $species[$specieName];

            // get aggregated statistics of all specie observations
            $provinces = [];
            $lastTime = 0;
            $lastTimeString = null;
            foreach ($observations as $observation) {
                $provinces[$observation->province] = true;
                $observationTime = strtotime($observation['timestamp']);
                if ($observationTime > $lastTime) {
                    $lastTime = $observationTime;
                    $lastTimeString = $observation['timestamp'];
                }
            }
            ksort($provinces);
            $provinces = implode(', ', array_keys($provinces));

            $specieAggregated[$specieName] = [
                'name' => $specieName,
                'count' => sizeof($observations),
                'provinces' => $provinces,
                'specieImage' => $specie['imageUrl'],
                'specieAbundance' => $specie['observationCount'],
                'lastObservationTime' => date("H:i", strtotime($lastTimeString)),
                'date' => $date
            ];
        }

        return $specieAggregated;
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
