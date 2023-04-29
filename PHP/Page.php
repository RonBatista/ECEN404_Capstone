<?php
// ERRORS
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

function GetPageList($con)
{
    $sql = "select visualization_project.*, project.Name as ProjectName " .
        "from visualization_project, project " .
        "where visualization_project.Project = project.ID " .
        "order by Name";

    $result = mysqli_query($con, $sql);

    $list = array();
    while ($row = mysqli_fetch_assoc($result)) {
        $list[] = $row;
    }
    echo json_encode($list);
}

function GetPageInfo($con, $id)
{
    $sql = "select * from visualization_project where ID = $id";
    $result = mysqli_query($con, $sql);
    $page = mysqli_fetch_assoc($result);
    echo json_encode($page);
    //echo $page;
}

//require_once("SetDBConnection.php");
require_once("../../../../resources/database/SetDBConnection.php");

$con = SetDBConnection();

if (mysqli_connect_errno()) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
    $action = $_GET["action"];

    switch ($action) {
        case "list":
            {
                GetPageList($con);
            }
            break;
        case "info":
            {
                $id = $_GET["id"];
                GetPageInfo($con, $id);
            }
            break;
    }
}

mysqli_close($con);
?>
