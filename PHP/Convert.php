<?php
// File containing System Variables
define("LOCAL_PATH_ROOT", $_SERVER["DOCUMENT_ROOT"]);
require LOCAL_PATH_ROOT . '/uas_tools/system_management/centralized_management.php';

require_once("SetFilePath.php");
require_once("CommonFunctions.php");
//require_once("SetDBConnection.php");
require_once("../../../../resources/database/SetDBConnection.php");

function Convert($identifier, $con)
{
    $converterPath = "gdal2tiles.py";

    $sql = "SELECT imagery_product.*, product_type.Name as TypeName FROM imagery_product, product_type " .
        "WHERE Identifier = '$identifier' and imagery_product.type = product_type.ID";

    $result = mysqli_query($con, $sql);
    $file = mysqli_fetch_assoc($result);

    $fileNameParts = pathinfo($file["FileName"]);
    $fileName = FormatFileName($fileNameParts["filename"]) . "." . $fileNameParts["extension"];
    $minZoom = $file["MinZoom"];
    $maxZoom = $file["MaxZoom"];
    $epsg = $file["EPSG"];

    $old = umask(0);

    $sourcePath = $file["UploadFolder"] . "/" . $fileName;
    //echo "TypeName:".$file["TypeName"];
    if ($file["TypeName"] == "MULTI Ortho") {
        $bands = Explode(",", $file["Bands"]);
        //print_r($bands);
        $cirPath = $file["UploadFolder"] . "/" . FormatFileName($fileNameParts["filename"]) . "_cir." . $fileNameParts["extension"];
        $command = "gdal_translate -b $bands[0] -b $bands[1] -b $bands[2] -b $bands[3] --config GDAL_TIFF_INTERNAL_MASK YES '$sourcePath' '$cirPath'";
        //echo $command;
        exec($command, $output, $result);
        if ($result == 0) {
            $sourcePath = $cirPath;//use cir image as the source for tiling
        }
    }

    $folderPath = $file["UploadFolder"];
    $destPath = $file["UploadFolder"] . "/Display";
    if (!file_exists($destPath)) {
        if (!mkdir($destPath, 0777, true)) {
            die('Failed to create folders...');
        }
    }

    umask($old);

    if (($fp = fopen($file["UploadFolder"] . "/convert_log.txt", 'w+')) !== false) {
        fclose($fp);
    }

    $command = "$converterPath -z " . $minZoom . "-" . $maxZoom . " -s EPSG:" . $epsg . " '$sourcePath' '$destPath' >> " . $file["UploadFolder"] . "/convert_log.txt";
    exec($command, $output, $result);

    if ($result == 0) {

        //Modify leaflet file content for demo
        $leafletPath = $destPath . "/leaflet.html";
        $demoContent = file_get_contents($leafletPath);
        $demoContent = str_replace("http", "https", $demoContent);
        // Libraries - leaflet
        //$leaflet_js = "basfhub.gdslab.org/js/leaflet.js";
        //$leaflet_css = "basfhub.gdslab.org/css/leaflet.css";

        //$demoContent = str_replace('<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.5/leaflet.css" />','<link rel="stylesheet" href="https://uashub.tamucc.edu/css/leaflet.css" />', $demoContent);
        //$demoContent = str_replace('<script src="http://cdn.leafletjs.com/leaflet-0.7.5/leaflet.js"></script>','<script src="https://uashub.tamucc.edu/js/leaflet.js"></script>', $demoContent);


        //$demoContent = str_replace("cdn.leafletjs.com/leaflet-0.7.5/leaflet.css", $leaflet_css, $demoContent);
        //$demoContent = str_replace("cdn.leafletjs.com/leaflet-0.7.5/leaflet.js", $leaflet_js, $demoContent);
        //$demoContent = str_replace("https://cdn.leafletjs.com/leaflet-0.7.5/leaflet.css", "http://bhub.gdslab.org/leaflet/leaflet.css", $demoContent);
        //$demoContent = str_replace("https://cdn.leafletjs.com/leaflet-0.7.5/leaflet.js", "http://bhub.gdslab.org/leaflet/leaflet.js", $demoContent);

        $demoContent = str_replace("https://cdn.leafletjs.com/leaflet-0.7.5/leaflet.css", $header_location . "/leaflet/leaflet.css", $demoContent);
        $demoContent = str_replace("https://cdn.leafletjs.com/leaflet-0.7.5/leaflet.js", $header_location . "/leaflet/leaflet.js", $demoContent);

        $demoContent = str_replace("L.control.layers(basemaps, overlaymaps, {collapsed: false}).addTo(map);", "L.control.layers(basemaps, overlaymaps, {collapsed: false}).addTo(map);map.addLayer(lyr);", $demoContent);
        file_put_contents($leafletPath, $demoContent);

        //$displayPath = str_replace("/var/www/html/","https://uashub.tamucc.edu/",$destPath)."/leaflet.html";
        //$TMSPath = str_replace("/var/www/html/","https://uashub.tamucc.edu/",$destPath)."/{z}/{x}/{y}.png";
        $displayPath = str_replace($alternative_root_path, $header_location . "/", $destPath) . "/leaflet.html";
        $TMSPath = str_replace($alternative_root_path, $header_location . "/", $destPath) . "/{z}/{x}/{y}.png";
        $localThumbPath = $destPath . "/" . FormatFileName($fileNameParts["filename"]) . "_thumb.jpg";
        //$displayThumbPath = str_replace("/var/www/html/","https://uashub.tamucc.edu/",$destPath)."/".FormatFileName($fileNameParts["filename"])."_thumb.jpg";
        $displayThumbPath = str_replace($alternative_root_path, $header_location . "/", $destPath) . "/" . FormatFileName($fileNameParts["filename"]) . "_thumb.jpg";


        $boundary = GetBoundary($sourcePath, $folderPath);
        CreateThumnail($sourcePath, $localThumbPath, $fileNameParts["extension"]);


        $sql = "UPDATE imagery_product " .
            "SET Displaypath = '$displayPath', TMSPath= '$TMSPath', ThumbPath='$displayThumbPath', Boundary = '$boundary',Status = 'Finished' " .
            "WHERE Identifier = '$identifier'";
        if (mysqli_query($con, $sql)) {
            echo "converted";


            //Finished converting, find another file in queue and convert it
            $sql = "SELECT * FROM imagery_product " .
                "WHERE Identifier != '$identifier' and Status = 'Pending' Order by ID ";
            $result = mysqli_query($con, $sql);
            $file = mysqli_fetch_assoc($result);
            if ($file) { //Found a file in queue, start converting it
                $sql = "UPDATE imagery_product " .
                    "SET Status = 'Converting' " .
                    "WHERE Identifier = '" . $file["Identifier"] . "'";

                if (mysqli_query($con, $sql)) {
                    Convert($file["Identifier"], $con);
                }

            } else { //There is no other file in queue, do nothing
            }
        }
    }
}

$con = SetDBConnection();
if (mysqli_connect_errno($con)) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
    $identifier = $_GET["identifier"];

    $sql = "SELECT * FROM imagery_product " .
        "WHERE Identifier != '$identifier' and Status = 'Converting' ";

    $result = mysqli_query($con, $sql);
    $file = mysqli_fetch_assoc($result);
    if ($file) { //There is another file being converted, change this file's status to pending
        $sql = "UPDATE imagery_product " .
            "SET Status = 'Pending' " .
            "WHERE Identifier = '$identifier'";
        if (mysqli_query($con, $sql)) {
            echo "pending";
        }
    } else { // No other file is being convert, start converting this file
        Convert($identifier, $con);

    }

    mysqli_close($con);

}
?>
