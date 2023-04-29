<?php
//require_once("SetDBConnection.php");
require_once("../../../../resources/database/SetDBConnection.php");

$con = SetDBConnection();

if (mysqli_connect_errno()) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
    $groupID = $_GET["groupID"];

    $sql = "select * from visualization_layer where visualization_layer.GroupID = $groupID order by ID";
    //_log('select * from visualization_layer: '.$sql);

    $result = mysqli_query($con, $sql);

    $list = array();
    while ($row = mysqli_fetch_assoc($result)) {
        $list[] = $row;
    }
    echo json_encode($list);
}

mysqli_close($con);
?>
