<?php
// Log Document
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

//Remove special characters, replace spaces with underscores, replace all proceeding underscores with 1 underscore
function FormatFileName($rawName)
{
    $formattedName = str_replace(' ', '_', $rawName);
    $formattedName = preg_replace('/[^A-Za-z0-9\_]/', '', $formattedName);
    return preg_replace('/_+/', '_', $formattedName);
}

//Remove a directory recursively
function RemoveDir($dir)
{
    if (is_dir($dir)) {
        $objects = scandir($dir);
        foreach ($objects as $object) {
            if ($object != "." && $object != "..") {
                if (filetype($dir . "/" . $object) == "dir") {
                    RemoveDir($dir . "/" . $object);
                } else {
                    unlink($dir . "/" . $object);
                }
            }
        }
        reset($objects);
        rmdir($dir);
    }
}

//function CreateThumnail($sourcePath, $destPath, $fileExtension)
//{
//    $maxCoreNum = 4; // set maximum number of cores
//    $tempPath = "";
//
//    if (strtoupper($fileExtension) == "TIF" || strtoupper($fileExtension) == "TIFF") {
//        $tempPath = str_replace("thumb.jpg", "temp.tif", $destPath);
//
//        //flatten image
//        $command = 'gdal_translate -co "TILED=YES" -co "COMPRESS=LZW" -co "BIGTIFF=YES" -ot Byte -scale "' . $sourcePath . '" "' . $tempPath . '"  2>&1';
//        exec($command, $output);
//
//        $image = new Imagick($tempPath);
//
//        $image->setImageColorspace(255);
//        $image->setCompression(Imagick::COMPRESSION_JPEG);
//        $image->setCompressionQuality(60);
//        $image->setResourceLimit(6, $maxCoreNum); //Set maximum number of cores to use with ImageMagick
//        $image->setImageBackgroundColor('white');
//        $image = $image->flattenImages(); // Use this instead.
//
//        $image->setImageFormat('jpeg');
//
//        $image->resizeImage(300, 0, imagick::FILTER_UNDEFINED, 1);
//        $image->writeImage($destPath);
//
//        $command = 'rm "' . $tempPath . '"';
//        exec($command);
//
//
//    } elseif (strtoupper($fileExtension) == "GIF" || strtoupper($fileExtension) == "JPG" || strtoupper($fileExtension) == "JPEG" || strtoupper($fileExtension) == "PNG") {
//        $image = new Imagick($sourcePath);
//
//        $image->setCompressionQuality(60);
//        $image->setResourceLimit(6, $maxCoreNum); //Set maximum number of cores to use with ImageMagick
//
//        $image->setImageFormat('jpeg');
//
//        $image->resizeImage(300, 0, imagick::FILTER_UNDEFINED, 1);
//        $image->writeImage($destPath);
//    }
//}

function GetBoundary($sourcePath, $folderPath)
{
    $command = "gdalinfo $sourcePath >> " . $folderPath . "/info.txt";
    exec($command, $output, $result);
    if ($result == 0) {
        $fileContent = file_get_contents($folderPath . "/info.txt");


        $boundary = "UPPER_LEFT;UPPER_RIGHT;LOWER_RIGHT;LOWER_LEFT;UPPER_LEFT";
        $file = fopen("/var/www/html/uas_data/uploads/products/2017_Corpus_Christi_Cotton/Phantom_4_Pro/RGB/03-25-2017/20170325/RGB_Ortho/info.txt", "r");
        if ($file) {
            while (($line = fgets($file)) !== false) {
                if (strpos($line, 'Upper Left') !== false) {
                    $NWcoordinates = GetNWCoordinates($line);
                    $boundary = str_replace("UPPER_LEFT", $NWcoordinates, $boundary);
                } else if (strpos($line, 'Upper Right') !== false) {
                    $NWcoordinates = GetNWCoordinates($line);
                    $boundary = str_replace("UPPER_RIGHT", $NWcoordinates, $boundary);
                } else if (strpos($line, 'Lower Right') !== false) {
                    $NWcoordinates = GetNWCoordinates($line);
                    $boundary = str_replace("LOWER_RIGHT", $NWcoordinates, $boundary);
                } else if (strpos($line, 'Lower Left') !== false) {
                    $NWcoordinates = GetNWCoordinates($line);
                    $boundary = str_replace("LOWER_LEFT", $NWcoordinates, $boundary);
                }
            }

            return $boundary;
            fclose($file);

        } else {
            // error opening the file.
            echo "error opening the file";
        }

    }
}

function GetNWCoordinates($str)
{
    $result = "";

    $start = strrpos($str, "(") + 1;
    $length = strrpos($str, ")") - $start;
    $substr = str_replace(" ", "", substr($str, $start, $length));

    $array = explode(",", $substr);
    $long = (string)DMSToDD($array[0]);
    $lat = (string)DMSToDD($array[1]);
    return $lat . "," . $long;

}

function DMSToDD($dms)
{
    $a1 = explode("d", $dms);
    $d = (float)$a1[0];

    $a2 = explode("'", $a1[1]);
    $m = (float)$a2[0];
    $a3 = explode("\"", $a2[1]);
    $s = (float)$a3[0];
    $direction = $a3[1];

    $dd = $d + ($m / 60) + ($s / 3600);

    if ($direction == "S" || $direction == "W") {
        $dd = -$dd;
    }

    return $dd;

}

?>
