<?php

/**
* Return the full data file path with the given filename.
*
* @param string $fileName
* @return bool|string
*/
function getDataPath(string $fileName = '')
{
    return realpath(base_path() . '/' . env('FAUNAMAP_DATA') . '/' . $fileName);
}
