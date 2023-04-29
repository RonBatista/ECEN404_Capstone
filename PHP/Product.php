<?php
//require_once("SetDBConnection.php");
require_once("../../../../resources/database/SetDBConnection.php");

$con = SetDBConnection();

if (mysqli_connect_errno($con)) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
    $projectID = $_GET["project"];
    $type = $_GET["type"];

    $sql = "select imagery_product.*" .
        "from imagery_product, flight " .
        "where flight.Project = $projectID and imagery_product.Type = $type and imagery_product.Flight = flight.ID " .
        "and imagery_product.Status = 'Finished' " .
        "order by Filename";

    $result = mysqli_query($con, $sql);
    $list = array();
    while ($row = mysqli_fetch_assoc($result)) {
        $list[] = $row;
    }
    echo json_encode($list);
}

mysqli_close($con);
?>
