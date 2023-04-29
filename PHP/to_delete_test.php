<!--Generate.php-->
<!---->
<?php
//require_once("SetFilePath.php");
//require_once("CommonFunctions.php");
//require_once("SetDBConnection.php");
//
//$pageID = $_GET["pageid"];
//$groups = $_REQUEST["groups"];
//$projectID = $_GET["project"];
//$pageTitle = $_GET["name"];
//$center = $_GET["center"];
//$zoom = $_GET["zoom"];
//$minZoom = $_GET["minZoom"];
//$maxZoom = $_GET["maxZoom"];
//
//$con = SetDBConnection();
//
//if(mysqli_connect_errno())
//{
//    echo "Failed to connect to database server: ".mysqli_connect_error();
//}
//else
//{
//    $deleteSQL =  "delete from visualization_project where id = $pageID";
//    mysqli_query($con,$deleteSQL);
//
//    $sql =  "select imagery_product.*, flight.Date as Date ".
//        "from imagery_product, flight ".
//        "where flight.Project = $projectID and imagery_product.Flight = flight.ID ".
//        "and imagery_product.Status = 'Finished' ".
//        "order by Filename";
//
//    $folderPath = SetTempFolderLocalPath().FormatFileName($pageTitle);
//    if(!file_exists($folderPath)){
//        if (!mkdir($folderPath, 0777, true)) {
//            die('Failed to create folders...');
//        }
//    }
//
//    $pagepath = $folderPath."/index.html";
//    //$viewPath = str_replace("/var/www/html/","https://uashub.tamucc.edu/",$pagepath);
//    $viewPath = str_replace("/var/www/html/wordpress/","http://basfhub.gdslab.org/",$pagepath);
//
//
//    $addSQL = 	"insert into visualization_project (Name, Project, Path) ".
//        "values ('$pageTitle', $projectID, '$viewPath')";
//    mysqli_query($con,$addSQL);
//    $vProjectID = $con->insert_id;
//
//    $result = mysqli_query($con,$sql);
//    $productList = array();
//    while($row = mysqli_fetch_assoc($result)) {
//        $productList[] = $row;
//    }
//
//    $zIndex = 50;
//    //print_r($productList);
//
//    $layerText = "";
//    $overLayerText = "";
//
//    $firstLayer = true;
//
//    foreach ($groups as $group) {
//        //print_r($group);
//        //$idList = explode(";",$group["IDs"]);
//        $idList = preg_split("@;@", $group["IDs"], NULL, PREG_SPLIT_NO_EMPTY);
//        if (count($idList) > 0){
//
//            $addSQL = 	"insert into visualization_group (Name, Type, Project) ".
//                "values ('".$group["GroupName"]."', '". $group["Type"] ."',$vProjectID)";
//            mysqli_query($con,$addSQL);
//            $vGroupID = $con->insert_id;
//
//            $groupText = 	"{\n".
//                "\tgroup: '".$group["GroupName"]."',\n".
//                "\tlayers: [\n";
//
//
//            foreach ($idList as $id){
//                foreach ($productList as $product){
//                    if($product["ID"] == $id){
//
//                        $addSQL = 	"insert into visualization_layer (Layer, GroupID) ".
//                            "values ($id, $vGroupID)";
//                        mysqli_query($con,$addSQL);
//
//                        $boundaryText = "";
//
//                        if ($product["Boundary"] != ""){
//                            $bounds = explode(";", $product["Boundary"]);
//                            $boundaryText = ", bounds: L.latLngBounds([";
//                            foreach ($bounds as $bound){
//                                $point = "L.latLng(".$bound."),";
//                                $boundaryText .= $point;
//                            }
//
//
//                            $boundaryText = rtrim($boundaryText,",")."])";
//                        }
//                        //$boundaryText = "";
//                        //echo "boundary text:'".$boundaryText."'";
//
//                        $layerName = "layer_".str_ireplace(".tif","",$product["FileName"]);
//                        $layer = 	"var ".$layerName." = L.tileLayer('".$product["TMSPath"].
//                            "', {tms: true, zIndex: ".$zIndex.$boundaryText."}); \n";
//                        $layerText .= $layer;
//
//                        if ($firstLayer){
//                            $activeText = "active: 'true',\n";
//                            $firstLayer = false;
//                        } else {
//                            $activeText = "";
//                        }
//
//                        $groupText .= 	"\t\t{\n".
//                            "\t\t\tname: '".str_replace("-","/",$product["Date"])."',\n".
//                            $activeText.
//                            "\t\t\tlayer: ".$layerName."\n".
//                            "\t\t},\n";
//
//                        $zIndex++;
//                    }
//                }
//            }
//
//            $groupText .= 		"\t]\n".
//                "},\n";
//
//            $overLayerText.= $groupText;
//        }
//    }
//
//    $templatePath = getcwd()."/page_template.html";
//    //echo $templatePath;
//    $pageContent = file_get_contents($templatePath);
//    //file_put_contents($templatePath, $pageContent);
//    $pageContent = str_replace("#PAGE-TITLE#",$pageTitle, $pageContent);
//    $pageContent = str_replace("#PROJECT-CENTER#",$center, $pageContent);
//    $pageContent = str_replace("#DEFAULT-ZOOM#",$zoom, $pageContent);
//    $pageContent = str_replace("#MIN-ZOOM#",$minZoom, $pageContent);
//    $pageContent = str_replace("#MAX-ZOOM#",$maxZoom, $pageContent);
//    $pageContent = str_replace("#LAYERS#",$layerText, $pageContent);
//    $pageContent = str_replace("#OVER-LAYERS#",$overLayerText, $pageContent);
//
//    //echo $pageContent;
//
//
//    $file = fopen($pagepath, "w") or die("Unable to open file!");
//    fwrite($file, $pageContent);
//    fclose($file);
//
//    //echo str_replace("/var/www/html/","https://uashub.tamucc.edu/",$pagepath);
//    //echo $layerText;
//    //echo $overLayerText;
//    echo $viewPath;
//}
//?>
<!---->
