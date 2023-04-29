<?php
// File containing System Variables
define("LOCAL_PATH_ROOT", $_SERVER["DOCUMENT_ROOT"]);
require LOCAL_PATH_ROOT . '/uas_tools/system_management/centralized_management.php';

//require_once("SetDBConnection.php");
require_once LOCAL_PATH_ROOT . '/uas_tools/visualization_generator/Resources/PHP/SetDBConnection.php';

$con = SetDBConnection();
$uriSegments = explode("/", parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH));
$project_name_dash=$uriSegments[4];
$project_name=str_replace("_"," ",$uriSegments[4]);

 $sql = "select * from project where Name = '$project_name'";
// Execute the query
$result = mysqli_query($con, $sql);
// Create array from query
$row = mysqli_fetch_assoc($result);

// Project ID
$project_id = $row["ID"];

// Get the images data from photos_upload
$sql = "select * from photos_upload where Project = '$project_id'";// need to be changed from 1 to variable

$result = mysqli_query($con, $sql);
if ($result) {
// Fetches all result rows as an associative array
$page = mysqli_fetch_all($result);
} else {
    echo mysqli_error($con);
}

//SELECT X(Coordinate),Y(Coordinate) FROM photos_upload;
// Get the coordinates of images for an specific project from photos_upload
$sql = "select X(Coordinate),Y(Coordinate) from photos_upload where Project = '$project_id'";// need to be changed from 1 to variable

$result = mysqli_query($con, $sql);
// This contains the coordinates of the pictures stored under the Project
// Fetches all result rows as an associative array
//$coord_pictures = array();
$coord_pictures = mysqli_fetch_all($result);
$pictures = mysqli_fetch_all( mysqli_query($con, "SELECT * FROM photos_upload where Project = '$project_id'"));

//echo ($coord_pictures[0][1]);
//
//echo "<pre>";
//print_r($coord_pictures);
//echo "</pre>";

// Get the number of images for an specific project from photos_upload
$sql = "select count(Project) from photos_upload where Project = '$project_id'";// need to be changed from 1 to variable

$result = mysqli_query($con, $sql);
// This contains the number of pictures stored under the Project
$num_pictures = mysqli_fetch_row($result);

$picture_data=array();
foreach ($coord_pictures as $key => $value) {
    $email=$pictures[$key][8];
   $picture_data[$key]['x']=$value[0];
   $picture_data[$key]['y']=$value[1];
   $picture_data[$key]['path']=$pictures[$key][6];
   $picture_data[$key]['image']=$pictures[$key][2];
   $picture_data[$key]['name']=$pictures[$key][7];
   $picture_data[$key]['date_time']=$pictures[$key][9];
   $picture_data[$key]['user_email']=$email;

   $user = mysqli_fetch_all( mysqli_query($con, "SELECT * FROM users WHERE email='$email'"));
   if (isset($user[0][1]) && isset($user[0][2])) {
      $picture_data[$key]['user_name']=$user[0][1] .' '. $user[0][2];
   }else{
    $picture_data[$key]['user_name']="";
   }


}

//echo('test: '.$num_pictures[0]);
// echo "<pre>";
//  var_dump($num_pictures);
//  var_dump($coord_pictures);
//  var_dump($pictures);
//  var_dump($picture_data);
// var_dump($uriSegments);
// var_dump($project_id);
// var_dump($row);
//  echo "</pre>";
//echo "<pre>";
//print_r($page);
//echo "</pre>";
mysqli_close($con);

//$js_array = array();
//$js_array = json_encode($coord_pictures);
//echo "var javascript_array = ". $js_array . ";\n";
?>

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en">
<head>
    <meta charset="utf-8" name=”viewport” content=”width=device-width, initial-scale=1″>
    <title>#PAGE-TITLE#</title>
    <link rel="stylesheet" href="/libraries/leaflet/leaflet.css"/>
    <link rel="stylesheet" href="/libraries/css/leaflet-panel-layers.css"/>

    <script src="/libraries/js/leaflet.js"></script>
    <script src="/libraries/js/leaflet-panel-layers.js"></script>
    <script src="/libraries/js/jquery.min.js"></script>
    <script src="/libraries/js/leaflet-ajax/dist/leaflet.ajax.js"></script>
    <script src="/libraries/js/legend.js"></script>
    <link rel="stylesheet" href="/libraries/css/legend.css"/>

    <style>
        body {
            margin: 0;
            padding: 0;
        }

        #map {
            position: absolute;
            /*z-index: -1;*/
            /*position: absolute;*/
            top: 0;
            bottom: 0;
            width: 100%;
            z-index: 1;
        }

        textarea {
            background-color: lightblue;
        }

        .container {
          position: absolute;
          height: auto;
          right: 20px;
          bottom: 1%;
          z-index: 2;
        }

        .logo_merge {
            width: 420px;
            z-index: 2;
        }

        .img_title{
          background: #444;
          color: #f6f5f5;
          font-size: 15px;
          font-weight: 700;
          padding: 8px 12px;
          z-index: 2;
          width: 397.5px;
        }

        h3{
          padding: 0px;
          margin: 0px;
        }
    </style>
<input type="hidden" value='<?php echo json_encode($picture_data); ?>' id="picture_data" name="picture_data">
    <script>
        function all() {
            (function (i, s, o, g, r, a, m) {
                i['GoogleAnalyticsObject'] = r;
                i[r] = i[r] || function () {
                    (i[r].q = i[r].q || []).push(arguments)
                }, i[r].l = 1 * new Date();
                a = s.createElement(o),
                    m = s.getElementsByTagName(o)[0];
                a.async = 1;
                a.src = g;
                m.parentNode.insertBefore(a, m)
            })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

            ga('create', 'UA-74689450-1', 'auto');
            ga('send', 'pageview');

            var map = L.map('map', {
                center: L.latLng([#PROJECT-CENTER#]),
                zoom: #DEFAULT-ZOOM#,
                minZoom
        :
            #MIN-ZOOM#,
                maxZoom
        :
            #MAX-ZOOM#,
                attributionControl
        :
            false
        });

            var osm_map = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
                zIndex: 0
            });

            // var mapbox = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            //     attribution: 'Imagery from <a href="https://mapbox.com/about/maps/">MapBox</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            //     subdomains: 'abcd',
            //     id: 'mapbox.satellite',
            //     //accessToken: 'pk.eyJ1IjoiaGFtZG9yaSIsImEiOiJjaWZmZzBwbjI4ZGdqc21seDFhOHA5dGcxIn0.4An46DNTDt97W992MRRWoQ',
            //     accessToken: 'sk.eyJ1Ijoiam9zZWx1aXNsYW5kaXZhcnMiLCJhIjoiY2tvMnpkMG12MHlyNzJwcXd6eDY5enowcSJ9.H8vS09OkK9hVtn8OYE3jrA',
            //     maxNativeZoom: 19,
            //     zIndex: 0
            // });

            var googleHybrid = L.tileLayer('https://{s}.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}',{
              maxZoom: 20,
              subdomains:['mt0','mt1','mt2','mt3']
              });

            // Layers
            #LAYERS#

            // map.addLayer(mapbox);
            map.addLayer(googleHybrid);

            var baseLayers = [
                {
                    name: "Open Street Map",
                    layer: osm_map
                },
                {
                    name: "Satellite Map",
                    // layer: mapbox
                    layer: googleHybrid
                },
            ];

            var overLayers = [
                #OVER-LAYERS#
            ];

            var panelLayers = new L.Control.PanelLayers(baseLayers, overLayers, {collapsibleGroups: true});
            map.addControl(panelLayers);

// Variable containing page URL
var siteURL = location.href;
// URL is saved on custId
document.getElementById("custId").value = siteURL;

// When click on BLUE marker, send URL and go to page
function onClick(e) {
    document.myform.submit();
}

//Start location BLUE marker
const marker = L.marker([0, 0]).on('click', onClick).addTo(map).bindTooltip("Click here to upload a picture",
    {
        permanent: true,
        direction: 'right'
    }
);

            // When mouse pass over, show message on marker
            var redIcon = new L.Icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            });

// Marker name
var dynamicname = 'marker';
//// Marker Latitude
//var picture_lat = '<?php //echo $coord_pictures[0][0];?>//';
//// Marker Longitude
//var picture_long = '<?php //echo $coord_pictures[0][1];?>//';
// Number of pictures on table
var num_pictures = '<?php echo $num_pictures[0];?>';

//Assign php generated json to JavaScript variable
var tempArray = <?php echo json_encode($coord_pictures); ?>;

// Header page
var header = '<?php echo $header_location;?>';

var picture_data=JSON.parse($('#picture_data').val());

var project_name_dash='<?php echo($project_name_dash) ?>';

// Function to create marker depending on the number of pictures
function Addmarker(markerArray) {

    for (var i = 0; i < markerArray; i++) {
    // Text and image on popup when click on RED markers
    //const src = header+"/uas_data/uploads/photos/"+project_name_dash+'/'+picture_data[i]['image']; // Needs to be fixed and not harcoded
    const src = "https://wtxcotton.uashubs.com/uas_data/uploads/photos/"+project_name_dash+'/'+picture_data[i]['image']; // Needs to be fixed and not harcoded
    var name=picture_data[i]['user_name'];
    var date_time=picture_data[i]['date_time'];
    const popupContent = document.createElement("div")
    popupContent.innerHTML = "<img style='max-height:300px; max-width:300px;' src='" + src + "'>"+"<a target='_blank' href='" + src + "'>See the image</a>"+"<p><strong>User: </strong>"+name+"</p>"+"<p><strong>Date & Time: </strong>"+date_time+"</p>";
        this[dynamicname + i] = L.marker(
            [tempArray[i][0], tempArray[i][1]],
            {icon: redIcon})
            .bindPopup(
                popupContent,
                { maxWidth: "auto" }
            )
            .addTo(map);

            // alert(i);
    }
    console.log(tempArray);
    console.log(picture_data);
}

Addmarker(num_pictures);


            //let firstime = true;
            function success(position) {
                const latitude = position.coords.latitude; // Set latitude
                const longitude = position.coords.longitude;// Set longitude
                // Update markers location
                 marker.setLatLng([latitude, longitude]).addTo(map);
                 //marker.setLatLng(["27.7823", "-97.5606"]).addTo(map);

                status.textContent = '';
            }

            //Error checking
            function error() {
                status.textContent = 'Unable to retrieve your location';
            }

            //If geolocation is not supported
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
    </script>

</head>

<body onload="all();">
<br/>

<div id="map"></div>

<form name="myform" action="/uas_tools/visualization_generator/Resources/PHP/upload_picture.php" method="POST">
    <input type="hidden" id="custId" name="custId">
    <a href="javascript: submitform()"></a>
</form>

<div class="container">
  <h3 class="img_title">West Texas Cotton UASHub is supported by</h3>
<img alt="Sponsor" class="logo_merge" src="/resources/images/supported_words.png">
</div>

</body>
</html>
