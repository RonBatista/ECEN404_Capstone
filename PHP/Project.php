<?php
/*
Function - GetProjectList
Description - Calls SQL query to fetch a list of Project names from the database returning them to main.js in JSON format.
parameters - con: connection to database
*/
	function GetProjectList($con){
		$sql =  "select * from project order by Name";				//SQL query

		$result = mysqli_query($con,$sql);						//call query to database

		$projectList = array();
		while($row = mysqli_fetch_assoc($result)) {					//While each row is returned from the database, add them to an array
			$projectList[] = $row;
		}
		echo json_encode($projectList);						//Send project array in JSON format.
	}

	//require_once("SetDBConnection.php");
	require_once("../../../../resources/database/SetDBConnection.php");

	$con = SetDBConnection();					//establsh connection to database

 	if(mysqli_connect_errno())
	{
		echo "Failed to connect to database server: ".mysqli_connect_error();							//return an error if we fail to establish a connection.
	}
	else
	{
					GetProjectList($con);				//call GetProjectList function.
	}

	mysqli_close($con);							//close the connection
?>
