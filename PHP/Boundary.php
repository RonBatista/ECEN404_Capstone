<?php
/*
Function - GetBoundaryList
Description - Calls SQL query to fetch a list of boundary files from the database returning them to main.js in JSON format.
parameters - con: connection to database
*/
	function GetBoundaryList($con, $selected_project_name){
		$sql =  "select * from vector_data where Project='$selected_project_name' and FileName LIKE '%.shp' order by Filename";						//SQL query // and where Name = SHAPE // where FileName LIKE '%.shp'
		//echo ($sql);
		$result = mysqli_query($con,$sql);									//call query to database

		$BoundaryList = array();
		while($row = mysqli_fetch_assoc($result)) {						//While each row is returned from the database, add them to an array
			$BoundaryList[] = $row;
		}
		echo json_encode($BoundaryList);			//Send boundary array in JSON format.
	}

	//require_once("SetDBConnection.php");
	require_once("../../../../resources/database/SetDBConnection.php");

	$con = SetDBConnection();				//establsh connection to database

 	if(mysqli_connect_errno())
	{
		echo "Failed to connect to database server: ".mysqli_connect_error();				//return an error if we fail to establish a connection.
	}
	else
	{

					$selected_project_name = $_GET["selected_projectName"];				//get the selected projects name
					GetBoundaryList($con, $selected_project_name);		//call GetBoundaryList function.

	}

	mysqli_close($con);					//close the connection
?>
