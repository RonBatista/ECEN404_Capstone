<?php
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
    #project contains a string with attributes of the projects. As of right now the only attribute it has is it's name, this can be added upon later if needed.

     $selected_project = str_replace(".", "", $_GET["project"]);      #string manipulation to take our periods and replace spaces between words with underscores (_).
     $selected_project = str_replace(" ", "_", $selected_project);

     $selected_project_parts = explode("::", $selected_project);           #string manipulation to grab the project name
     $selected_project_name = $selected_project_parts[0];

     $selected_orthomosaic = $_GET["orthomosaic"];                        #string that contains orthomosiacs name, Path to file and orthomosaic's EPSG value.

     $selected_CanopyHeightModel = $_GET["chm"];
     //$selected_CanopyHeightModel = explode(",", $selected_CanopyHeightModel_list);
     //_log("CHM: " .$selected_CanopyHeightModel);
     $selected_boundary = $_GET["shape"];

     $returningArray = array();           //Create an array that we can send back in JSON format


     $cc_checked = $_GET["cc_ckd"];
//     array_push($returningArray, $cc_checked);
     $exg_checked = $_GET["exg_ckd"];
//     array_push($returningArray, $exg_checked);

    array_push($returningArray, $selected_CanopyHeightModel);

    if($selected_CanopyHeightModel == "0"){         // if a CHM is not specified, set the state of the Canopy Height and Canopy Volume checkboxes to False
      $ch_checked = "false";
      $cv_checked = "false";
    }else{
      $ch_checked = $_GET["ch_ckd"];                // if a CHM is specified, grab the Canopy Height and Canopy Volume checkboxes states.
 //     array_push($returningArray, $ch_checked);
      $cv_checked = $_GET["cv_ckd"];
 //     array_push($returningArray, $cv_checked);
    }


// command to call python file that generates the canopy attributes with the selected project, orthomosaic, CHM, boundary files as well as the checked attributes.
     $generate_dat_files_command = "python3 /var/www/html/uas_tools/canopy_attribute_generator/Resources/Python/generate_dat_files_new.py $selected_project $selected_orthomosaic $selected_CanopyHeightModel $selected_boundary $cc_checked $exg_checked $ch_checked $cv_checked";
     $result = shell_exec($generate_dat_files_command);

     array_push($returningArray, $generate_dat_files_command);

     if($result){
       # echo "Python has been executed!";
       array_push($returningArray, $result);                    // If the call to the python file is successful. Push the results (things printed in Python file) to the reurning array.
     }else{
       array_push($returningArray, "ERROR: Was unable to call to the python executable!");    // If unable to call python file, push an error message to the returning array
     }

     echo json_encode($returningArray);     //return returning array regarding this call in JSON format.
     die();

?>
