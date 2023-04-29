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


// File containing System Variables
define("LOCAL_PATH_ROOT", $_SERVER["DOCUMENT_ROOT"]);
require LOCAL_PATH_ROOT . '/uas_tools/system_management/centralized_management.php';

//require_once("SetDBConnection.php");
require_once("../../../../resources/database/SetDBConnection.php");
// To find particular elements within an HTML page
require_once('simple_html_dom.php');

//Remove special characters, replace spaces with underscores, replace all proceeding underscores with 1 underscore
function FormatFileName($rawName)
{
    $formattedName = str_replace(' ', '_', $rawName);
    $formattedName = preg_replace('/[^A-Za-z0-9\_]/', '', $formattedName);
    return preg_replace('/_+/', '_', $formattedName);
}

// Function to generate random string
function GenerateRandomString()
{
    //$characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $characters = '0123456789';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < 10; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

//$text = $_POST['notes'];
//_log('text: ' .$text);

session_start();
//$userName = $_SESSION["email"];
//_log($_SESSION);

if (isset($_FILES['myFile'])) {

//    $dest_dir = 'uploads/';
//    // create the final destination file
//    if (!is_dir($dest_dir)) {
//        //echo "make dir";
//        mkdir($dest_dir, 0777, true);
//        //_log('Final Destination Dir Created '.$dest_dir);
//    }


    // Example:
    // if image was moved successfully
    $path =$_POST['path'];
    //_log("path: ".$path);
    //_log("name: ".$_FILES["myFile"]["name"]);

    $temp = explode(".", $_FILES["myFile"]["name"]);
        $newfilename = $_POST['rand_name']. '.' . end($temp);
    if (move_uploaded_file($_FILES['myFile']['tmp_name'], $path."/" . $newfilename) == false) { // Change file name
        echo 'Image could not be uploaded.';
    } //move_uploaded_file($_FILES['myFile']['tmp_name'], "uploads/" . $_FILES['myFile']['name']);
    else {
        echo 'Image has been uploaded.';

        //print_r($_FILES['myFile']);

        $con = SetDBConnection();

        // If session hasn't been started, start it
//    if (session_status() == PHP_SESSION_NONE) {
//        session_start();
//    }

//    if (mysqli_connect_errno()) {
//        echo "Failed to connect to database server: " . mysqli_connect_error();
//    } else {
//        $sql = "select * from visualization_project where ID = '$pageID'";
//        $result = mysqli_query($con, $sql);
//        if ($result) {
//            $page = mysqli_fetch_assoc($result);
//            //print_r($page);
//            if ($page) {
//                //_log('page ' . $page['Project']);
//                $projectID = $page['Project'];
//            }
//        }
//    }

        // FileName
        //$fileNameParts = pathinfo($_GET['resumableFilename']);
        $fileNameParts = pathinfo($newfilename);
        //_log('$fileNameParts: '.$fileNameParts);
        $fileName = FormatFileName($fileNameParts["filename"]) . "." . $fileNameParts["extension"];
        //$fileName = $_FILES['myFile']['name'];
        //_log('$fileName: ' . $fileName);

        // FileSize
        $size = $_FILES['myFile']['size'];
        //_log('$size: ' . $size);

        //TotalChunk
        $totalChunkNum = 1;

        // Status
        $status = 'Finished';

        // Temporary Directory
        $temp_dir = '';

        // Destination Directory
        $dest_dir3 = getcwd() . '/uploads/';
        // Remove /var/www/html
        $dest_dir2 = str_replace("/var/www/html", "", $dest_dir3);
        // Include $header_location at beginning
        $dest_dir2 = $header_location . $dest_dir2;
        // Add image Name


        // _log('$dest_dir: ' . $dest_dir2);
        //_log('$dest_dir3: ' . $dest_dir3);

        // Identifier
        // random data of 10 characters + file name with no dots
        // ex: 2324447011-20160427_p4_cotton_sorghumtargz
        // strip file name from dots
        $identifier = strtolower(GenerateRandomString() . '-' . str_replace('.', '', $fileName));
        //_log('$identifier: ' . $identifier);

        // Notes
        $notes = $_POST['notes'];
        //_log('$notes: ' . $notes);

        // User who uploaded the file
        $userName = $_SESSION["email"] ?? '';// verify user uploading image
        //_log('userName: ' . $userName);

        if (mysqli_connect_errno()) {
            echo "Failed to connect to database server: " . mysqli_connect_error();
        } else {

            $latitude = $_POST['coord_latitude'];
            //_log('latitude: ' .$latitude);

            $longitude = $_POST['coord_longitude'];
            //_log('longitude: ' .$longitude);

            // Load the webpage into the DOM
            //$html = file_get_html('https://chub.gdslab.org/uas_tools/visualization/mobile/2016_Corpus_Christi_Cotton_and_Sorghum/index.html');
            $title = $_POST['page_url'];
//            $html = file_get_html($url);
//
//            // FIND THE NAME FROM THE <title>
//            $matches = array();
//            $pattern = '#<title>(.*?)</title>#'; // note I changed the pattern a bit
//            preg_match($pattern, $html, $matches);
//            $title = $matches[1];

            // USE THIS NAME TO FIND THE PROJECT ID
            //select ID from project where Name = '2016 Corpus Christi Cotton and Sorghum';
            $sql = "select ID from project where Name = '$title'";
            // Execute the query
            $result = mysqli_query($con, $sql);
            // Create array from query
            $row = mysqli_fetch_assoc($result);

            // Project ID
            $project_id = $row["ID"];

//            $pageContents = ob_get_contents (); // Get all the page's HTML into a string
//            ob_end_clean (); // Wipe the buffer
//
//            $matches = array();
//            $pattern = '#<title>(.*?)</title>#'; // note I changed the pattern a bit
//            preg_match($pattern, $pageContents, $matches);
//            $title = $matches[1];

            $sql = "INSERT INTO photos_upload (Project, FileName, Size, ChunkCount, Status, UploadFolder, Identifier, Uploader, Notes, Coordinate) " .
                //"VALUES ('$flightID', '$fileName', '$size', '$totalChunkNum', '$status', '$dest_dir', '$identifier', '$userName', '$notes', POINT('$latitude', '$longitude'))";
                "VALUES ('$project_id', '$fileName', '$size', '$totalChunkNum', '$status', '$dest_dir3', '$identifier', '$userName', '$notes', POINT('$latitude', '$longitude'))"; // $dest_dir3 needs to be changed
                //"VALUES ('$project_id', '$fileName', '$size', '$totalChunkNum', '$status', '$dest_dir3', '$identifier', '$userName', '$notes', POINT('32.775050', '-101.947929'))"; // $dest_dir3 needs to be changed

            //_log("sql: " .$sql);
            //mysqli_query($con, $sql);
//
        $result = mysqli_query($con, $sql);

//            if ($result){
//                echo "File has been deleted.";
//            } else {
//                echo mysqli_error($con);
//            }

            if (!$result){
                echo mysqli_error($con);
            }

//        if ($result) {
//            $page = mysqli_fetch_assoc($result);
//            //print_r($page);
//            if ($page) {
//                //_log('page ' . $page['Project']);
//                $projectID = $page['Project'];
//            }
//        }
        }
        mysqli_close($con);
    }
}
//mysqli_close($con);
?>
