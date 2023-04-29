<?php
//require_once("SetDBConnection.php");
require_once("../../../../resources/database/SetDBConnection.php");
require_once("CommonFunctions.php");

$con = SetDBConnection();

if (mysqli_connect_errno()) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
    $identifier = $_GET["identifier"];

    $sql = "SELECT * FROM imagery_product " .
        "WHERE Identifier = '$identifier'";

    $result = mysqli_query($con, $sql);
    $file = mysqli_fetch_assoc($result);

    //echo $file["Status"];

    $directory = $file["TempFolder"] . "/";
    $uploadedChunk = 0;
    $files = glob($directory . "*");
    if ($files) {
        $uploadedChunk = count($files);
    }
    if ($file["ChunkCount"] > 0) {
        $progress = floor($uploadedChunk * 100 / $file["ChunkCount"]);
        if ($file["Progress"] < $progress) {
            $file["Progress"] = $progress;
        }
    }

    echo json_encode($file);

    mysqli_close($con);
}

?>
