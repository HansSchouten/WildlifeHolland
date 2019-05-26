<?php

namespace App\Models;

use App\Enums\Province;
use Elasticquent\ElasticquentResultCollection;
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
        'province' => [
            'type' => 'keyword'
        ],
        'location' => [
            'type' => 'geo_point'
        ],
        'specieGroup' => [
            'type' => 'keyword'
        ],
        'specieName' => [
            'type' => 'keyword'
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
        $speciesFile = getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        // get all json observation files
        $dataFolder = getDataPath();
        $observationsFiles = glob($dataFolder . '/observations-*');

        $observations = (new Observation)->newCollection();
        foreach ($observationsFiles as $observationsFile) {
            $date = str_replace('observations-', '', basename($observationsFile, '.json'));
            $jsonObservations = file_get_contents($observationsFile);
            $structuredObservations = json_decode($jsonObservations,true);
            self::addFlattenedObservations($observations, [], $species, $structuredObservations, $date);
        }

        return $observations;
    }

    /**
     * Return all observations stored in today's JSON file with ids different than the given list of ids.
     *
     * @param array $knownObservationIds
     * @return \Elasticquent\ElasticquentCollection
     */
    public static function getUnseenJsonObservationsOfToday(array $knownObservationIds)
    {
        $observations = (new Observation)->newCollection();

        $date = date('Y-m-d');
        $observationsFile = getDataPath('observations-' . $date . '.json');
        if (! file_exists($observationsFile)) {
            return $observations;
        }

        // load species data
        $speciesFile = getDataPath('species.json');
        $jsonSpecies = file_get_contents($speciesFile);
        $species = json_decode($jsonSpecies, true);

        $jsonObservations = file_get_contents($observationsFile);
        $structuredObservations = json_decode($jsonObservations,true);
        self::addFlattenedObservations($observations, $knownObservationIds, $species, $structuredObservations, $date);

        return $observations;
    }

    /**
     * Flatten a multidimensional array of observations into an array containing all data per observation.
     *
     * @param $observations
     * @param array $skipObservations
     * @param array $species
     * @param array $structuredObservations
     * @param string $date
     */
    protected static function addFlattenedObservations(&$observations, array $skipObservations, array $species, array $structuredObservations, string $date)
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
                        if (in_array($observationId, $skipObservations)) {
                            continue;
                        }
                        $obsInstance = new Observation;
                        $obsInstance->id = $observationId;
                        $obsInstance->province = Province::getKey($province);
                        $obsInstance->location = $observation['lat'] . ',' . $observation['long'];
                        $obsInstance->specieGroup = $specieGroup;
                        $obsInstance->specieName = $specieName;
                        $obsInstance->specieAbundance = $specie['observationCount'];
                        $obsInstance->date = $date;
                        $obsInstance->timestamp = trim($date . ' ' . $observation['time']);

                        $observations->push($obsInstance);
                    }
                }
            }
        }
    }

    /**
     * Return a collection of observations based on a passed array of search parameters.
     *
     * @param array $parameters
     * @return ElasticquentResultCollection
     */
    public static function search(array $parameters = [])
    {
        $must = [];
        foreach ($parameters['must'] as $key => $value) {
            if (! $value) continue;
            $must[] = ['match' => [$key => $value]];
        }

        $filters = [
            [
                'range' => [
                    'timestamp' => [
                        'gte' => $parameters['timestamp']
                    ]
                ]
            ]
        ];

        if (isset($parameters['geofilter'])) {
            list($lat, $lon) = explode(',', $parameters['geofilter']['coordinates']);
            $filters[] = [
                'geo_distance' => [
                    'distance' => $parameters['geofilter']['distance'],
                    'location' => [
                        'lat' => $lat,
                        'lon' => $lon
                    ]
                ]
            ];
        }

        $query = [
            'index' => (new self())->getIndexName(),
            'body' => [
                'query' => [
                    'bool' => [
                        'must' => $must,
                        'filter' => $filters
                    ]
                ],
                'sort' => [
                    ['specieAbundance' => 'asc']
                ]
            ],
            'size' => 10000
        ];
        return self::complexSearch($query);
    }

}
