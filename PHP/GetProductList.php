<?php
//require_once("SetDBConnection.php");
require_once("CommonFunctions.php");
require_once("../../../../resources/database/SetDBConnection.php");

$con = SetDBConnection();

if (mysqli_connect_errno()) {
   echo "Failed to connect to database server: ".mysqli_connect_error();
} else {
   $projectID = $_GET["project"];
   $type = $_GET["type"];
   //_log("type: ".$type);
//if ($type != "%" && $type != "14") {
if ($type != "%" && $type != "8") {
$typeCondition =  " and imagery_product.Type = $type ";

$sql1 =  "select imagery_product.* ".
"from imagery_product, flight ".
"where flight.Project = $projectID and imagery_product.Flight = flight.ID ".
"and imagery_product.Status = 'Finished' ".
$typeCondition.
"order by Filename";
// } elseif ($type == "14"){
} elseif ($type == "8"){
$typeCondition =  " and v.Type = $type ";

$sql1 = "SELECT v.*, project.Name as ProjectName, t.Name as TypeName " .
   "from project, product_type, vector_data v inner join product_type t on v.Type = t.ID " .
   "where product_type.Type = 'V' and v.Status = 'Finished' " .
   "and v.Project =  project.Name " .
   //"order by ProjectName, TypeName";

$typeCondition.
//"order by Filename";
"";
} else {
$typeCondition = "";
}
$sql = $sql1;

//_log("sql: ".$sql);

$result = mysqli_query($con, $sql);
$list = array();
while ($row = mysqli_fetch_assoc($result)) {
$list[] = $row;
}

echo json_encode($list);
}

mysqli_close($con);

?>

<?php
// require_once("SetDBConnection.php");
//
// $con = SetDBConnection();
//
// if (mysqli_connect_errno()) {
//     echo "Failed to connect to database server: ".mysqli_connect_error();
// } else {
//     $projectID = $_GET["project"];
//     $type = $_GET["type"];
//     if ($type != "%") {
//         $typeCondition =  " and imagery_product.Type = $type ";
//     } else {
//         $typeCondition = "";
//     }
//
//     $sql =  "select imagery_product.* ".
//         "from imagery_product, flight ".
//         "where flight.Project = $projectID and imagery_product.Flight = flight.ID ".
//         "and imagery_product.Status = 'Finished' ".
//         $typeCondition.
//         "order by Filename";
//     //_log('select imagery_product and flight: '.$sql);
//
//     //echo $sql;
//
//     $result = mysqli_query($con, $sql);
//     $list = array();
//     while ($row = mysqli_fetch_assoc($result)) {
//         $list[] = $row;
//     }
//     echo json_encode($list);
// }
//
// mysqli_close($con);
?>
