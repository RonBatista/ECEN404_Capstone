<?php
/*
Function - GetCanopyHeightModelList
Description - Calls SQL query to fetch a list of Canopy Height Model (CHM) files from the database returning them to main.js in JSON format.
parameters - con: connection to database
*/
	function GetCanopyHeightModelList($con, $flight_id){
		$sql =  "select * from imagery_product where type=11 AND Flight=$flight_id order by FileName";						//SQL query

	//call query to database
		$result = mysqli_query($con,$sql);

		$CanopyHeightModelList = array();
		while($row = mysqli_fetch_assoc($result)) {
			$CanopyHeightModelList[] = $row;										//While each row is truturned from the database, add them to an array
		}
		echo json_encode($CanopyHeightModelList);								//Send CHM array in JSON format.
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

					$flight_id = $_GET["flightID"];						//get the Flight ID from the selected Project, Platform and Sensor.
					GetCanopyHeightModelList($con, $flight_id);					//call GetCanopyHeightModel function.

	}

	mysqli_close($con);								//close the connection
?>
