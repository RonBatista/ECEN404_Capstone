<?php
#PHP code that grabs the path to the zip file and the temporary results directory. The code then calls to a python file (deleteTempResults.py) which then deletes them.
    $zip_file_path_noExt = str_replace(".", "", $_GET["zipfile_path_noExt"]);
    $zip_file_path_noExt = str_replace(" ", "_", $zip_file_path_noExt);
    $zip_result = $zip_file_path_noExt . ".zip";

    $zip_file_path = str_replace(".", "", $_GET["zipfile_path"]);
    $zip_file_path = str_replace(" ", "_", $zip_file_path);

    $selected_ortho_temp = str_replace(".", "", $_GET["selected_ortho"]);
    $selected_ortho_temp = str_replace(" ", "_", $selected_ortho_temp);

    $selected_shape_name = str_replace(".", "", $_GET["selected_shape"]);
    $selected_shape_name = str_replace(" ", "_", $selected_shape_name);

     $returningArray = array();
     array_push($returningArray, $zip_file_path);
     array_push($returningArray, $zip_file_path_noExt);
     array_push($returningArray, $selected_ortho_temp);
     array_push($returningArray, $selected_shape_name);

     # Call Python code with field information to delete Zip file and temp results directory.
     $generateZip_command = "python3 /var/www/html/uas_tools/canopy_attribute_generator/Resources/Python/deleteTempResults.py $zip_result $zip_file_path $selected_ortho_temp $selected_shape_name";
     array_push($returningArray, $generateZip_command);
     $result = shell_exec($generateZip_command);
     if($result){                                     // If there is a result push result to array being passed back in JSON format
       # echo "Python has been executed!";
       $command = "rm -r /var/www/html/uas_data/download/product/'".$selected_ortho_temp."_".$selected_shape_name."'";
       $cmd = shell_exec($command);



       array_push($returningArray, $result);
       array_push($returningArray, $cmd);
        }else{
          array_push($returningArray, "ERROR: Was unable to call to the deleteTempResults python executable!");     // Else, append Error on to returning JSON object.
        }

     echo json_encode($returningArray);     //return returning array regarding this call in JSON format.
     die();
?>
