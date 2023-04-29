<?php
////$fileContent = file_get_contents("/var/www/html/uas_data/uploads/products/2017_Corpus_Christi_Cotton/Phantom_4_Pro/RGB/03-25-2017/20170325/RGB_Ortho/info.txt");
////print_r($fileContent);
//
////require_once("phpcoord.php"); FILE DOESN'T EXIST
//ini_set('display_errors', 'on');
//function GetNWCoordinates($str)
//{
//    $result = "";
//
//    $start = strrpos($str, "(") + 1;
//    $length = strrpos($str, ")") - $start;
//    $substr = str_replace(" ", "", substr($str, $start, $length));
//
//    $array = explode(",", $substr);
//    $long = (string)DMSToDD($array[0]);
//    $lat = (string)DMSToDD($array[1]);
//    return $lat . "," . $long;
//
//}
//
//function DMSToDD($dms)
//{
//    $a1 = explode("d", $dms);
//    $d = (float)$a1[0];
//
//    $a2 = explode("'", $a1[1]);
//    $m = (float)$a2[0];
//    $a3 = explode("\"", $a2[1]);
//    $s = (float)$a3[0];
//    $direction = $a3[1];
//
//    $dd = $d + ($m / 60) + ($s / 3600);
//
//    if ($direction == "S" || $direction == "W") {
//        $dd = -$dd;
//    }
//
//    return $dd;
//
//}
//
//function ConvertNWToLatLong($dms)
//{
//    //DD = d + (min/60) + (sec/3600)
//}
//
//$boundary = "UPPER_LEFT;UPPER_RIGHT;LOWER_RIGHT;LOWER_LEFT;UPPER_LEFT";
////$file = fopen("/var/www/html/uas_data/uploads/products/2017_Corpus_Christi_Cotton/Phantom_4_Pro/RGB/03-25-2017/20170325/RGB_Ortho/info.txt", "r");
//$file = fopen("/var/www/html/uas_data/uploads/products/2017_Corpus_Christi_Cotton/Phantom_4_Pro/RGB/03-25-2017/20170325/RGB_Ortho/info.txt", "r");
//
//if ($file) {
//    while (($line = fgets($file)) !== false) {
//        if (strpos($line, 'Upper Left') !== false) {
//            //$boundary = str_replace("UPPER_LEFT", $line, $boundary);
//            $NWcoordinates = GetNWCoordinates($line);
//            $boundary = str_replace("UPPER_LEFT", $NWcoordinates, $boundary);
//        } else if (strpos($line, 'Upper Right') !== false) {
//            //$boundary = str_replace("UPPER_RIGHT", $line, $boundary);
//            $NWcoordinates = GetNWCoordinates($line);
//            $boundary = str_replace("UPPER_RIGHT", $NWcoordinates, $boundary);
//        } else if (strpos($line, 'Lower Right') !== false) {
//            //$boundary = str_replace("LOWER_RIGHT", $line, $boundary);
//            $NWcoordinates = GetNWCoordinates($line);
//            $boundary = str_replace("LOWER_RIGHT", $NWcoordinates, $boundary);
//        } else if (strpos($line, 'Lower Left') !== false) {
//            $NWcoordinates = GetNWCoordinates($line);
//            $boundary = str_replace("LOWER_LEFT", $NWcoordinates, $boundary);
//        }
//    }
//
//    echo $boundary;
//    fclose($file);
//} else {
//    // error opening the file.
//}
//?>
