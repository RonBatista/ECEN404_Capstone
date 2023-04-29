<?php
// ERRORS
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function _log($str)
{
    // log to the output
    $log_str = date('d.m.Y') . ": {$str}\r\n";
    echo $log_str;

    // log to file
    if (($fp = fopen('upload_log.txt', 'a+')) !== false) {
        fputs($fp, $log_str);
        fclose($fp);
    }
}

function SetDBConnection()
{
    return mysqli_connect("localhost", "hub_admin", "PurdueGdsl!@2w", "uas_projects");
}

?>
