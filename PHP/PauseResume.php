<?php
require_once("SetDBConnection.php");
//$con = SetDBConnection();
require_once("../../../../resources/database/SetDBConnection.php");

if (mysqli_connect_errno($con)) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
    $type = $_GET["type"];
    $identifier = $_GET["identifier"];

    if ($type == "Pause") {
        $status = "Paused";
    } else {
        $status = "Uploading";
    }

    $sql = "UPDATE pointcloud " .
        "SET Status='" . $status . "' " .
        "WHERE Identifier = '$identifier'";
    echo $sql;
    mysqli_query($con, $sql);
    mysqli_close($con);
}

?>
