<?php
/*
Function - GetOrthomosaicList
Description - Calls SQL query to fetch a list of Orthomosaic files from the database returning them to main.js in JSON format.
parameters - con: connection to database
*/
	function GetOrthomosaicList($con, $flight_id){
		$sql =  "select * from imagery_product where type=1 AND Flight=$flight_id order by FileName"; 			//SQL query


		$result = mysqli_query($con,$sql);													//call query to database

		$OrthomosaicList = array();
		while($row = mysqli_fetch_assoc($result)) {										//While each row is returned from the database, add them to an array
			$OrthomosaicList[] = $row;
		}
		echo json_encode($OrthomosaicList);								//Send Orthomosaic array in JSON format.
	}

	//require_once("SetDBConnection.php");
	require_once("../../../../resources/database/SetDBConnection.php");

	$con = SetDBConnection();								//establsh connection to database

 	if(mysqli_connect_errno())
	{
		echo "Failed to connect to database server: ".mysqli_connect_error();						//return an error if we fail to establish a connection.
	}
	else
	{
					$flight_id = $_GET["flightID"];							//get the Flight IDs in regard to what Project, Platform and Sensor is selected.
					GetOrthomosaicList($con, $flight_id);					//call GetOrthomosaicList function.
	}

	mysqli_close($con);							//close the connection
?>
