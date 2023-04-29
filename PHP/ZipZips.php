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

# This PHP code grabs the specified files by the user, creates and copys them to a temporary directory which is then ziped.

#Value of items consist of a large string with multiple variables delimited my "::". See Get List functions in main JavaScript file
     #$_GET["project"] = <Project name>::
     $selected_project = str_replace(".", "", $_GET["project"]);      #string manipulation to take our periods and replace spaces with underscores (_).
     $selected_project = str_replace(" ", "_", $selected_project);

     $selected_project_parts = explode("::", $selected_project);           #string manipulation to grab the project name
     $selected_project_name = $selected_project_parts[0];

     #$_GET['orthomosaic'] = <File nmme>::<path to file>::<EPSG value>
     $selected_orthomosaic = $_GET["orthomosaic"];                        #string that contains orthomosiacs name, Path to file and orthomosaic's EPSG value.
     //$selected_orthomosaic_parts = explode("::", $selected_orthomosaic);                 #string manipulation to grab orthomosaics name w/o extension.
     //$selected_orthomosaic_FileName = explode(".", $selected_orthomosaic_parts[0]);
     //$selected_orthomosaic_FileName_noExt = $selected_orthomosaic_FileName[0];

     $selected_CanopyHeightModel = $_GET["chm"];
     //$selected_CanopyHeightModel = $_GET["chm"] ?? "0::0"; //0 if not selected to allow $generateZip_command from executing.
     //$selected_CanopyHeightModel = "0::0"; //0 if not selected to allow $generateZip_command from executing.

     $selected_boundary = $_GET["shape"];

     // _log('Show selected project: '.$selected_project);
     // _log('Show selected orthomosaic: '.$selected_orthomosaic);
     // _log('Show selected CHM: '.$selected_CanopyHeightModel);
     // _log('Show selected boundary: '.$selected_boundary);

     $cc_checked = $_GET["cc_ckd"];       // check what atribute checkboxes are checked
     $exg_checked = $_GET["exg_ckd"];

     if($selected_CanopyHeightModel == "0"){         // if a CHM is not specified, set the state of the Canopy Height and Canopy Volume checkboxes to False
       $ch_checked = "false";
       $cv_checked = "false";
     }else{
       $ch_checked = $_GET["ch_ckd"];                // if a CHM is specified, grab the Canopy Height and Canopy Volume checkboxes states.
  //     array_push($returningArray, $ch_checked);
       $cv_checked = $_GET["cv_ckd"];
  //     array_push($returningArray, $cv_checked);
     }

     $csv_checked = $_GET["csv_ckd"];             // check what file format checkboxes are checked
     $xls_checked = $_GET["xls_ckd"];
     $geojson_checked = $_GET["geo_ckd"];
     $shape_checked = $_GET["shp_ckd"];

     $returningArray = array();
    // array_push($returningArray, $selected_project);
    // array_push($returningArray, $selected_orthomosaic);
    // array_push($returningArray, $selected_boundary);

     # Call Python code with field information to generate a Zip file with the results.
     $generateZip_command = "python3 /var/www/html/uas_tools/canopy_attribute_generator/Resources/Python/ZipZips.py $selected_project $selected_orthomosaic $selected_CanopyHeightModel $selected_boundary $csv_checked $xls_checked $geojson_checked $shape_checked $cc_checked $exg_checked $ch_checked $cv_checked";
    // array_push($returningArray, $generateZip_command);
     $result = shell_exec($generateZip_command);
     _log('Command to generate zip file : '.$generateZip_command);
     //_log('Result from command : '.$result);



     if($result){                                     // If there is a result push result to array being passed back in JSON format
       # echo "Python has been executed!";
    //   array_push($returningArray, $result);
        }else{
    //      array_push($returningArray, "ERROR: Was unable to call to the generateZip python executable!");     // Else, push Error on to returning JSON object.
        }
     _log('Zip Zips:')
     _log('Show selected project: '.$selected_project);
     _log('Show selected orthomosaic: '.$selected_orthomosaic);
     _log('Show selected CHM: '.$selected_CanopyHeightModel);
     _log('Show selected boundary: '.$selected_boundary);
     echo json_encode($result);     //return returning array regarding this call in JSON format.
     die();

?>
