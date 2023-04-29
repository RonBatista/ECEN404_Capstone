<?php
/*
Function - GetSensorList
Description - Calls SQL query to fetch a list of sensor types from the database returning them to main.js in JSON format.
parameters - con: connection to database
*/
	function GetSensorList($con){
		$sql =  "select * from sensor where ID=10 order by Name";					//SQL query

		$result = mysqli_query($con,$sql);								//call query to database

		$sensorList = array();
		while($row = mysqli_fetch_assoc($result)) {						//While each row is returned from the database, add them to an array
			$sensorList[] = $row;
		}
		echo json_encode($sensorList);				//Send sensor array in JSON format.
	}

	//require_once("SetDBConnection.php");
	require_once("../../../../resources/database/SetDBConnection.php");

	$con = SetDBConnection();							//establsh connection to database

 	if(mysqli_connect_errno())
	{
		echo "Failed to connect to database server: ".mysqli_connect_error();				//return an error if we fail to establish a connection.
	}
	else
	{
					GetSensorList($con);				//call GetSensorList function.
	}

	mysqli_close($con);							//close the connection
?>
