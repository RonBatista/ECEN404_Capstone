<?php
//require_once("SetDBConnection.php");
require_once("../../../../resources/database/SetDBConnection.php");

$con = SetDBConnection();

if (mysqli_connect_errno()) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
  /* ----------Oringial code -----------------------
    $name = $_GET['name'];

    $sql = "SELECT * FROM $name ORDER BY Name";
    //_log('select name: '.$sql);

    $result = mysqli_query($con, $sql);

    $list = array();
    while ($row = mysqli_fetch_assoc($result)) {
        $list[] = $row;
    }
    mysqli_close($con);
    echo json_encode($list);
    */
    $type = $_GET["type"] ?? '';

    switch ($type) {
        case "project":
            {
                GetProjectList($con);
            }
            break;

        case "platform":
            {
                $projectID = $_GET['project'] ?? '';
                GetPlatformList($projectID, $con);

            }
            break;
        case "sensor":
            {
                $projectID = $_GET['project'] ?? '';
                $platformID = $_GET['platform'] ?? '';
                GetSensorList($projectID, $platformID, $con);
            }
            break;
        case "date":
            {
                $projectID = $_GET['project'] ?? '';
                $platformID = $_GET['platform'] ?? '';
                $sensorID = $_GET['sensor'] ?? '';
                GetDateList($projectID, $platformID, $sensorID, $con);
            }
            break;
        case "flight":
            {
                $projectID = $_GET['project'] ?? '';
                $platformID = $_GET['platform'] ?? '';
                $sensorID = $_GET['sensor'] ?? '';
                $date = $_GET['date'] ?? '';
                $date = str_replace('/', "-", $date);
                GetFlighList($projectID, $platformID, $sensorID, $date, $con);
            }
            break;
        case "product-type":
            {
                GetProductTypeList($con);
            }
            break;
    }
}

mysqli_close($con);
}
?>
