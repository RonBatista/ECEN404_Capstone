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

     $selected_project = str_replace(".", "", $_GET["project"]);      #string manipulation to take our periods and replace spaces with underscores (_).
     $selected_project = str_replace(" ", "_", $selected_project);

     $selected_project_parts = explode("::", $selected_project);           #string manipulation to grab the project name
     $selected_project_name = $selected_project_parts[0];

     $selected_orthomosaic = $_GET["orthomosaic"];                        #string that contains orthomosiacs name, Path to file and orthomosaic's EPSG value.

     $selected_CanopyHeightModel = $_GET["chm"];                          # string that contains the selected CHm files

     $selected_boundary = $_GET["shape"];                                 # string that contains the selected SHP boundary file

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
     $val = $_GET["check_zip_val"];

     # returning array is the response passed back to the Main.js file
     $returningArray = array();
     array_push($returningArray, $selected_project);
     array_push($returningArray, $selected_orthomosaic);
     array_push($returningArray, $selected_boundary);

     # Call Python code with field information to generate a Zip file with the results.
     $generateZip_command = "python3 /var/www/html/uas_tools/canopy_attribute_generator/Resources/Python/generateZip.py $selected_project $selected_orthomosaic $selected_CanopyHeightModel $selected_boundary $csv_checked $xls_checked $geojson_checked $shape_checked $cc_checked $exg_checked $ch_checked $cv_checked $val";
     array_push($returningArray, $generateZip_command);
     $result = shell_exec($generateZip_command);
     //_log('Command to generate zip file : '.$generateZip_command);
     //_log('Current array : '.$returningArray);
     //_log('Result from command : '.$result);


     if($result){                                     // If there is a result push result to array being passed back in JSON format
       # echo "Python has been executed!";
       array_push($returningArray, $result);
        }else{
          array_push($returningArray, "ERROR: Was unable to call to the generateZip python executable!");     // Else, push Error on to returning JSON object.
        }

     echo json_encode($returningArray);     //return returning array regarding this call in JSON format.
     die();

?>
