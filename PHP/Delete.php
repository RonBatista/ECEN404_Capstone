<?php
// File containing System Variables
define("LOCAL_PATH_ROOT", $_SERVER["DOCUMENT_ROOT"]);
require LOCAL_PATH_ROOT . '/uas_tools/system_management/centralized_management.php';

//require_once("SetDBConnection.php");
require_once("../../../../resources/database/SetDBConnection.php");

// Log Document
//function _log($str)
//{
//    // log to the output
//    $log_str = date('d.m.Y') . ": {$str}\r\n";
//    echo $log_str;
//
//    // log to file
//    if (($fp = fopen('upload_log.txt', 'a+')) !== false) {
//        fputs($fp, $log_str);
//        fclose($fp);
//    }
//}

$con = SetDBConnection();

if (mysqli_connect_errno()) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
    $id = $_GET["id"];
    //$type = $_GET["type"];
    // Raw type is being hardcoded. No need to change this as we are just deleting info
    $type = "raw";

    //_log("id: " . $id);
    //_log("type: " . $type);

    if ($type == "raw") {
        $sql = "select * from visualization_project where id = '$id'";
    }
// else if ($type == "product") {
//        $sql = "select * from imagery_product where id = $id";
//    }
//
//    //_log("sql: " . $sql);
//
    $result = mysqli_query($con, $sql);
    if ($result) {
//        // Create an array containing the columns from the table
//        $upload = mysqli_fetch_assoc($result);
//        ////////////////////////////////////////////////////////////
//        // Delete Temp Path Folder
//        $uploadFolder = $upload["Path"];
//        //_log('$header_location: '.$header_location);
//        // Strip from header
//        $uploadFolderNoHeader = str_replace($header_location.'/', '',$uploadFolder);
//        // Strip from /index.html
//        // This is the correct path that should be deleted
//        $uploadFolderNoIndex = str_replace('/index.html', '',$uploadFolderNoHeader);
//        $to_delete_uploadFolder = $uploadFolderNoIndex .'/';
//
//        //_log('$to_delete_uploadFolder: '.$to_delete_uploadFolder); // Returns: $to_delete_uploadFolder: temp/2016_Corpus_Christi_Cotton_and_Sorghum/
//
//        //if (file_exists($to_delete_uploadFolder)) {
//
//        //exec('rm -rf '.escapeshellarg('var/www/html/web/'.$to_delete_uploadFolder).'2>&1', $output);
//        //exec('rm -rf '.escapeshellarg('var/www/html/web/'.$to_delete_uploadFolder), $output);
//
//        $cmd = "rm -rf ".escapeshellarg('var/www/html/web/'.$to_delete_uploadFolder);
//
//        exec($cmd, $output);
//        //_log('$cmd: '.$cmd);
//
////$cmd = "rm -rf ". $to_delete_uploadFolder;
////_log('cmd: '.$cmd);
//// Returns: cmd: rm -rf temp/2016_Corpus_Christi_Cotton_and_Sorghum/
////exec($cmd.'2>&1', $output);
////print_r($output);
//// Returns: Array ( )
//
//
//            //_log('$result_code: '.$result_code);
//            //print_r($output);
//        //}
//        ////////////////////////////////////////////////////////////
//        // Delete Temp PathMobile Folder
//        $uploadFolder = $upload["PathMobile"];
//        //_log('$header_location: '.$header_location);
//        // Strip from header
//        $uploadFolderNoHeader = str_replace($header_location.'/', '',$uploadFolder);
//        // Strip from /index.html
//        // This is the correct path that should be deleted
//        $uploadFolderNoIndex = str_replace('/index.html', '',$uploadFolderNoHeader);
//        $to_delete_uploadFolder = $uploadFolderNoIndex .'/';
//
//        //_log('$to_delete_uploadFolder: '.$to_delete_uploadFolder);
//
//        //if (file_exists($to_delete_uploadFolder)) {
//        $cmd = "rm -rf $to_delete_uploadFolder";
//        _log('$cmd1: '.$cmd);
//        //exec($cmd, $output);
//        //}
//        ////////////////////////////////////////////////////////////
//        // Delete Main Path Folder
//        $uploadFolder = $upload["Path"];
//        //_log('$header_location: '.$header_location);
//        // Strip from header
//        $uploadFolderNoHeader = str_replace($header_location.'/temp/', '',$uploadFolder);
//        // Strip from /index.html
//        // This is the correct path that should be deleted
//        $uploadFolderNoIndex = str_replace('/index.html', '',$uploadFolderNoHeader);
//        $to_delete_uploadFolder = 'uas_tools/visualization/'.$uploadFolderNoIndex .'/';
//
//        //_log('$to_delete_uploadFolder: '.$to_delete_uploadFolder);
//
//        //if (file_exists($to_delete_uploadFolder)) {
//        $cmd = "rm -rf $to_delete_uploadFolder";
//        _log('$cmd2: '.$cmd);
//        //exec($cmd, $output);
//        //}
//        ////////////////////////////////////////////////////////////
//        // Delete Main PathMobile Folder
//        $uploadFolder = $upload["PathMobile"];
//        //_log('$header_location: '.$header_location);
//        // Strip from header
//        $uploadFolderNoHeader = str_replace($header_location.'/temp/mobile/', '',$uploadFolder);
//        // Strip from /index.html
//        // This is the correct path that should be deleted
//        $uploadFolderNoIndex = str_replace('/index.html', '',$uploadFolderNoHeader);
//        $to_delete_uploadFolder = 'uas_tools/visualization/mobile/'.$uploadFolderNoIndex .'/';
//
//        //_log('$to_delete_uploadFolder: '.$to_delete_uploadFolder);
//
//        //if (file_exists($to_delete_uploadFolder)) {
//        $cmd = "rm -rf $to_delete_uploadFolder";
//        _log('$cmd3: '.$cmd);
//        //exec($cmd, $output);
//        //}
        ////////////////////////////////////////////////////////////
        // Delete Visualization Project from table on Database
        $sql = "delete from visualization_project where id = '$id'";
        //_log("sql: " . $sql);
        $result = mysqli_query($con, $sql);
//
        if ($result){
            echo "File has been deleted.";
        } else {
            echo mysqli_error($con);
        }

//        $uploadFolder = $upload["UploadFolder"];
//        $filePath = $upload["UploadFolder"] . "/" . $upload["FileName"];
//        $tempFolder = $upload["TempFolder"];
//
//        // Strip the string from characters after and including "RGB_Ortho"
//        $variable = substr($uploadFolder, 0, strpos($uploadFolder, "RGB_Ortho"));
//        //Find the last 10 characters where the date is str2: /20160427/
//        $str2 = substr($variable, -10);
//        // This is the correct path that should be deleted
//        $to_delete_uploadFolder = str_replace($str2, '', $variable);


        //_log("filePath: " . $filePath);
//        _log("tempFolder: " . $tempFolder);
//        _log("uploadFolder: " . $uploadFolder);
//        _log("variable: " . $variable);
//        _log("str2: " . $str2);
//        _log("goodUrl: " . $to_delete_uploadFolder);

//        if ($type == "raw") {
//            $sql = "delete from raw_data_upload_status where id = $id";
//        } else if ($type == "product") {
//            $sql = "delete from imagery_product where id = $id";
//        }
//
//        $result = mysqli_query($con, $sql);
//
//        if (mysqli_query($con, $sql)) {
//            if ($type == "raw") {
//                if (file_exists($filePath)) {
//                    unlink($filePath);
//                    //echo "File exists";
//                }
//            } else if ($type == "product") {
//                if (file_exists($uploadFolder)) {
//                    //$cmd = "rm -rf $uploadFolder";
//                    $cmd = "rm -rf $to_delete_uploadFolder";
//                    exec($cmd, $output);
//                }
//            }
//
//            if (file_exists($tempFolder)) {
//                $cmd = "rm -rf $tempFolder";
//                exec($cmd, $output);
//            }

        //echo "File has been deleted.";
    } else {
        echo mysqli_error($con);
    }

//    } else {
//        echo mysqli_error($con);
//    }

}
mysqli_close($con);
?>
