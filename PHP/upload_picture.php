<?php
// File containing System Variables
define("LOCAL_PATH_ROOT", $_SERVER["DOCUMENT_ROOT"]);
require LOCAL_PATH_ROOT . '/uas_tools/system_management/centralized_management.php';

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

$page_url = $_POST['custId'] ?? '';
//$page_url = $_POST['url'];
//


//strip string from this characters
// Replace the characters "world" in the string "Hello world!" with "Peter":
//echo str_replace("world","Peter","Hello world!");
$name = str_replace($header_location."/uas_tools/visualization/mobile/", "", $page_url);
$name2 = str_replace("/index.php", "", $name);
$name3 = str_replace("_", " ", $name2);
//$nameWithNoDot = strtok($name, '.');
//$nameWithNoDotCapitalized = strtoupper($nameWithNoDot);
//echo $nameWithNoDotCapitalized;


//_log('page_url: ' .$name3);
$uriSegments = explode("/", $page_url);
$project_name=$uriSegments[6];
$path =__DIR__ .'/../../../../uas_data/uploads/photos/'.$project_name; // chcek this path
//echo $project_name;
// echo $page_url;
// echo $path;
//include ($path);

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" content=”width=device-width, initial-scale=1″ name=”viewport”>
    <title>Take or select photo(s) and upload</title>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css?family=Roboto+Condensed" rel="stylesheet">

    <!-- Styles -->
    <link rel="stylesheet" type="text/css" href="../style.css">
    <link rel="stylesheet" type="text/css" href="/resources/css/bootstrap.min.css">

    <link href="/libraries/css/leaflet.css" rel="stylesheet" />
    <link href="/libraries/css/leaflet-panel-layers.css" rel="stylesheet" />

    <script src="/libraries/js/leaflet.js"></script>
    <script src="/libraries/js/leaflet-panel-layers.js"></script>
    <script src="/libraries/js/jquery.min.js"></script>
    <script src="/libraries/js/leaflet-ajax/dist/leaflet.ajax.js"></script>
    <script src="/libraries/js/legend.js"></script>
    <link href="/libraries/css/legend.css" rel="stylesheet" />
    <style>
        .project {
            margin: 0px 0px 0px 0px;
            padding: 25px 35px;
            border-radius: 15px;
            background: #f6f7f9;
        }

        input.btnNew {
            padding: 0;
            font-weight: 500;
            font-size: 17px;
            color: #ffffff;
            background: linear-gradient(#2c539e, #254488);
            line-height: 36px;
            border-radius: 5px;
            /* width: 108px; */
            width: 112px;
            border: 1px solid #00236f;
            float: right;
        }

    </style>

    <script>
        var radnom;

        function fileSelected() {
            radnom = rand_name();
            var count = document.getElementById('fileToUpload').files.length;
            document.getElementById('details').innerHTML = "";

            for (var index = 0; index < count; index++) {
                var file = document.getElementById('fileToUpload').files[index];
                var fileSize = 0;

                if (file.size > 1024 * 1024)
                    fileSize = (Math.round(file.size * 100 / (1024 * 1024)) / 100).toString() + 'MB';
                else
                    fileSize = (Math.round(file.size * 100 / 1024) / 100).toString() + 'KB';

                //document.getElementById('details').innerHTML += 'Name: ' + file.name + '<br>Size: ' + fileSize + '<br>Type: ' + file.type;
                document.getElementById('details').innerHTML += 'Name: ' + radnom + '<br>Size: ' + fileSize + '<br>Type: ' + file.type;
                document.getElementById('details').innerHTML += '<p>';
            }
        }

        // Initializing global variables
        var latitude = 0;
        var longitude = 0;

        function success(position) {
            latitude = position.coords.latitude; //establece la latitud con su variable
            longitude = position.coords.longitude; //establece la longitud con su variable
            status.textContent = '';
        }

        //If there are errors
        function error() {
            status.textContent = 'Unable to retrieve your location';
        }

        // Getting position
        function getPosition() {
            if (!navigator.geolocation) {
                status.textContent = 'Geolocation is not supported by your browser';
            } else {
                status.textContent = 'Locating…';
                navigator.geolocation.watchPosition(success, error, {
                    timeout: Infinity,
                    enableHighAccuracy: true,
                    maximumAge: 0
                });
            }
        }

        // Uploading picture
        function uploadFile() {
            var fd = new FormData();
            var count = document.getElementById('fileToUpload').files.length;

            for (var index = 0; index < count; index++) {
                var file = document.getElementById('fileToUpload').files[index];
                fd.append('myFile', file);
            }

            // Send input from Notes
            fd.append('notes', document.getElementById('notes').value);

            getPosition();

            // Send coordinates
            //alert("Envia variable");
            fd.append('coord_latitude', latitude);
            fd.append('coord_longitude', longitude);
            fd.append('rand_name', radnom);
            fd.append('path', '<?php echo($path); ?>');

            // Send URL
            spge = '<?php echo $name3 ;?>';
            //alert(spge);
            fd.append('page_url', spge);

            var xhr = new XMLHttpRequest();

            xhr.upload.addEventListener("progress", uploadProgress, false);
            xhr.addEventListener("load", uploadComplete, false);
            xhr.addEventListener("error", uploadFailed, false);
            xhr.addEventListener("abort", uploadCanceled, false);
            xhr.open("POST", "savetofile.php");
            xhr.send(fd);
        }
        //random Name
        function rand_name() {
            var text = "";
            var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

            for (var i = 0; i < 5; i++)
                text += possible.charAt(Math.floor(Math.random() * possible.length));
            return text;
        }

        // Show uploading progress
        function uploadProgress(evt) {
            if (evt.lengthComputable) {
                var percentComplete = Math.round(evt.loaded * 100 / evt.total);
                document.getElementById('progress').innerHTML = percentComplete.toString() + '%';
            } else {
                document.getElementById('progress').innerHTML = 'unable to compute';
            }
        }

        function uploadComplete(evt) {
            /* This event is raised when the server send back a response */
            alert(evt.target.responseText);
            //alert("There was an error attempting to upload the file.");
        }

        function uploadFailed(evt) {
            alert("There was an error attempting to upload the file.");
        }

        function uploadCanceled(evt) {
            alert("The upload has been canceled by the user or the browser dropped the connection.");
        }

    </script>
</head>

<body onload="getPosition();">
    <div class="container py-3">
        <div class="project">
            <form action="savetofile.php" enctype="multipart/form-data" id="form1" method="post">
                <div class="row">
                    <div class="col-md-12">
                        <div class="form-group">
                            <label for="fileToUpload">Take or select photo(s)</label>
                            <input class="form-control" accept="image/*" capture id="fileToUpload" name="fileToUpload" onchange="fileSelected();" type="file" />
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="form-group">
                            <label for="notes">Notes:</label>
                            <textarea class="form-control" cols="50" id="notes" maxlength="2000" name="notes" placeholder="Please enter any additional information here" rows="4"></textarea>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div id="details"></div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <input class="btnNew" onclick="uploadFile()" type="button" value="Upload" />
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div id="progress"></div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</body>

</html>
