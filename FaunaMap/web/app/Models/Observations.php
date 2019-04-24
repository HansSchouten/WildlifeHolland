<?php

namespace App\Models;

use App\Enums\Province;
use Elasticquent\ElasticquentTrait;
use Illuminate\Database\Eloquent\Model;

class Observations extends Model
{
    use ElasticquentTrait;

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
        'name' => [
            'type' => 'string'
        ],
        'count' => [
            'type' => 'integer'
        ],
        'provinces' => [
            'type' => 'string'
        ],
        'specie' => [
            'type' => 'string'
        ],
        'timestamp' => [
            'type' => 'date',
            'format' => 'yyyy-MM-dd HH:mm:ss||yyyy-MM-dd'
        ],
    ];

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
    public static function getDataPath(string $fileName)
    {
        return realpath(base_path() . '/' . env('FAUNAMAP_DATA') . '/' . $fileName);
    }

}
