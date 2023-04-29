<?php
/*
Function - GetFlightIDList
Description - Calls SQL query to fetch a list of Flight IDs in regard to the selected Prpject, Platform and Sensor.
parameters - con: connection to database | selected_project_id: selected project ID | selected_platform_id: selected platform ID | selected_sensor_id: selected sensor ID
*/
	function GetFlightIDList($con, $selected_project_id, $selected_platform_id, $selected_sensor_id){
		$sql =  "select * from flight where Project=$selected_project_id AND Platform=$selected_platform_id AND Sensor=$selected_sensor_id"; 			//SQL query


		$result = mysqli_query($con,$sql);													//call query to database

		$FlightIDsList = array();
		while($row = mysqli_fetch_assoc($result)) {										//While each row is returned from the database, add them to an array
			$FlightIDsList[] = $row;
		}
		echo json_encode($FlightIDsList);								//Send Orthomosaic array in JSON format.
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

		$selected_project_id = $_GET["selected_projectID"];				//get the selected Projects ID
    $selected_platform_id = $_GET["selected_platformID"];			//get the selected Platforms ID
    $selected_sensor_id = $_GET["selected_sensorID"];					//get the selected Sensors ID
  	GetFlightIDList($con, $selected_project_id, $selected_platform_id, $selected_sensor_id);					//call GetBoundaryList function.
	}

	mysqli_close($con);							//close the connection
?>
