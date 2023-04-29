<?php
	//require_once("SetDBConnection.php");
	require_once("../../../../resources/database/SetDBConnection.php");

	$con = SetDBConnection();

 	if(mysqli_connect_errno())
	{
		echo "Failed to connect to database server: ".mysqli_connect_error();
	}
	else
	{
		$pageID = $_GET["pageid"];
		// visualization_group table is empty
		$sql =  "select * from visualization_group where visualization_group.Project = $pageID order by ID";
		//_log('select * from visualization_group: '.$sql);


		$result = mysqli_query($con,$sql);

		$list = array();
		while($row = mysqli_fetch_assoc($result)) {
			$list[] = $row;
		}
		echo json_encode($list);
	}

	mysqli_close($con);
?>
