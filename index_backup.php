<?php
//phpinfo();
// File containing System Variables

define("LOCAL_PATH_ROOT", $_SERVER["DOCUMENT_ROOT"]);
require LOCAL_PATH_ROOT . '/uas_tools/system_management/centralized_management.php';

// To check if User has the role required to access the page
require_once("Resources/PHP/SetDBConnection.php");
//require_once("../system_management/centralized.php");

$mysqli = SetDBConnection();

if (session_status() == PHP_SESSION_NONE) {
    session_start();
}

$userName = $_SESSION["email"] ?? '';
$userapproved = $_SESSION['admin_approved'] ?? '';

// SELECT the role_name for each users_roles for the logged on user
// ? is a place holder for our parameter `user_id`
$sql = "
    SELECT r.role_name FROM users_roles AS ur
        JOIN roles AS r ON r.role_id = ur.role_id
    WHERE ur.user_id = ?
";

$query = $mysqli->prepare($sql);                // Prepare the query
$query->bind_param("i", $_SESSION["user_id"]);  // Bind the parameter (wherever you store user_id in $_SESSION)
$query->execute();                              // Run the query
$query->store_result();                         // Store the result
$query->bind_result($role_name);                // Bind the result to a variable

$user_role_array = [];                          // Initialise the user roles array
while ($query->fetch()) {                         // Loop returned records
    $user_role_array[] = $role_name;            // Add user role to array
}

if (mysqli_connect_errno()) {
    echo "Failed to connect to database server: " . mysqli_connect_error();
} else {
    if (!$user_role_array || $userapproved == "Disapproved") {
        echo '<script>alert("You do not have permission to access this page. You will be logout now.")</script>';
        echo "<html>";
        echo "<script>";
        echo "window.top.open('/index.php?logout=true')"; //$_SERVER['HTTP_HOST'] . '/index.php?logout=true'
        echo "</script>";
        echo "</html>";
    } else {
        $pageName = basename(__DIR__);
        if ($pageName == "V2") {
            $pageName = basename(realpath(__DIR__ . "/.."));
        }

        $sql1 = "SELECT * FROM page_access WHERE Page = '$pageName'";
        $allowedGroups = array();
        if ($result1 = mysqli_query($mysqli, $sql1)) {
            if ($row1 = mysqli_fetch_assoc($result1)) {
                $allowedGroups = explode(";", $row1["Page_Groups"]);
                $accessGroupsStr = $row1["Page_Groups"];
            }
        }

        $intersect = array_intersect($user_role_array, $allowedGroups);

        if (sizeof($intersect) > 0) {// if match found
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name=”viewport” content=”width=device-width, initial-scale=1″>
    <!--    <title>Visualization Page Generator</title>-->
    <title>Visualization Generator</title>

    <!-- Google Fonts -->
    <!-- <link href="https://fonts.googleapis.com/css?family=Roboto+Condensed" rel="stylesheet"> -->
    <link href="<?php echo $header_location; ?>/libraries/css/Roboto+Condensed.css" rel="stylesheet">

    <!-- Styles -->
    <link rel="stylesheet" type="text/css" href="/uas_tools/upload_product/Resources/css/bootstrap.min.css">
    <link rel="stylesheet" type="text/css" href="Resources/style.css">

    <script type="text/javascript" src="Resources/JS/jquery.min.js"></script>

    <script src="Resources/JS/Chosen/chosen.jquery.min.js"></script>
    <link rel="stylesheet" type="text/css" href="Resources/JS/Chosen/chosen.css">
    <script src="Resources/JS/JqueryUI/jquery-ui.min.js"></script>
    <link rel="stylesheet" type="text/css" href="Resources/JS/JqueryUI/jquery-ui.css">
    <link rel="stylesheet" type="text/css" href="Resources/style.css">
    <script type="text/javascript" src="Resources/JS/main.js"></script>
    <script src="Resources/JS/FixedTable/fixed_table_rc.js"></script>
    <link rel="stylesheet" type="text/css" href="Resources/JS/FixedTable/fixed_table_rc.css">
    <link rel="stylesheet" href="Resources/JS/Leaflet/leaflet.css" />
    <script src="Resources/JS/Leaflet/leaflet.js"></script>
    <link rel="stylesheet" href="Resources/JS/ControlGeocoder/Control.Geocoder.css" />
    <script src="Resources/JS/ControlGeocoder/Control.Geocoder.js"></script>

    <style>

    #mainForm{
        margin: 0px;
        padding: 0px;
    }

    #orthomosaic_attribute_table_div{
    	display: none;
    	margin-top: 20px;
    }

/* Loader - Loading screen styling*/

      .box {
        background:black;
        position:fixed;
        height: 200%;
        width: 100%;
        top:0;
        left:0;
        opacity:.5;
        display:none;
      }

      .loader-wrapper {
      width: 300px;
      height: 300px;
      position: fixed;
      top: 30%;
      left: 40%;
      display: none;
      justify-content: center;
      align-items: center;
      content:url('https://agrilife-project1.uashubs.com/uas_tools/canopy_attribute_generator/Resources/Images/loading_animated.gif')
    }

    #chm_attribute_table_div{
    	display: none;
      margin-top: 20px;
    }

        #uploaded-list-container {
            width: 93%;
        }

        #warning {
            width: 100%;
            margin-top: 10px;
            text-align: center;
            color: red;
            display: none;
        }

		#project_chosen {
			width: 100% !important;
		}

        .project {
            margin: 0px 0px 0px 0px;
            /*padding: 25px 35px;*/
            padding: 25px 35px;
            border-radius: 15px;
            background: #f6f7f9;
        }

		.row {
			margin-left: auto;
			margin-right: auto;
			width: 80%;
		}

        .form-control-1 {
            background: #ededed;
            box-shadow: inset 0px 0px 5px 0px rgb(0 0 0 / 5%);
            margin: 0px 0px 0px 0px;
            padding: 0px 10px 0px 15px;
            font-weight: normal;
            font-size: 18px;
            color: #000000;
            display: block;
            background-color: #ededed;
            line-height: 55px;
            border-radius: 5px;
            border: none;
        }

        input.btnNew {
            padding: 0;
            font-weight: 500;
            font-size: 17px;
            color: #ffffff;
            background: linear-gradient(#2c539e, #254488);
            line-height: 36px;
            border-radius: 5px;
            width: 208px;
            border: 1px solid #00236f;
			margin-left: auto;
			margin-right: auto;
			margin-top: 15px;
        }

        p {
            font-size: 18px !important;
        }

        #project_chosen {
            width: 100% !important;
        }

		.chosen-container {
			position: relative;
			display: inline-block;
			vertical-align: middle;
			font-size: 13px;
			-webkit-user-select: none;
			-moz-user-select: none;
			-ms-user-select: none;
			user-select: none;
}

		.chosen-container-single .chosen-single {
			position: relative;
			display: block;
			overflow: hidden;
			padding: 0 0 0 8px;
			height: 25px;
			border: 1px solid #aaa;
			border-radius: 5px;
			background-color: #fff;
			background: -webkit-gradient(linear, left top, left bottom, color-stop(20%, #fff), color-stop(50%, #f6f6f6), color-stop(52%, #eee), to(#f4f4f4));
			background: linear-gradient(#fff 20%, #f6f6f6 50%, #eee 52%, #f4f4f4 100%);
			background-clip: padding-box;
			-webkit-box-shadow: 0 0 3px #fff inset, 0 1px 1px rgb(0 0 0 / 10%);
			box-shadow: 0 0 3px #fff inset, 0 1px 1px rgb(0 0 0 / 10%);
			color: #444;
			text-decoration: none;
			white-space: nowrap;
			line-height: 24px;
}

		.chosen-container .chosen-drop {
			position: absolute;
			top: 100%;
			z-index: 1010;
			width: 100%;
			border: 1px solid #aaa;
			border-top: 0;
			background: #fff;
			-webkit-box-shadow: 0 4px 5px rgb(0 0 0 / 15%);
			box-shadow: 0 4px 5px rgb(0 0 0 / 15%);
			clip: rect(0, 0, 0, 0);
			-webkit-clip-path: inset(100% 100%);
			clip-path: inset(100% 100%);
}

		.col, .col-1, .col-10, .col-11, .col-12, .col-2, .col-3, .col-4, .col-5, .col-6, .col-7, .col-8, .col-9, .col-auto, .col-lg, .col-lg-1, .col-lg-10, .col-lg-11, .col-lg-12, .col-lg-2, .col-lg-3, .col-lg-4, .col-lg-5, .col-lg-6, .col-lg-7, .col-lg-8, .col-lg-9, .col-lg-auto, .col-md, .col-md-1, .col-md-10, .col-md-11, .col-md-12, .col-md-2, .col-md-3, .col-md-4, .col-md-5, .col-md-6, .col-md-7, .col-md-8, .col-md-9, .col-md-auto, .col-sm, .col-sm-1, .col-sm-10, .col-sm-11, .col-sm-12, .col-sm-2, .col-sm-3, .col-sm-4, .col-sm-5, .col-sm-6, .col-sm-7, .col-sm-8, .col-sm-9, .col-sm-auto, .col-xl, .col-xl-1, .col-xl-10, .col-xl-11, .col-xl-12, .col-xl-2, .col-xl-3, .col-xl-4, .col-xl-5, .col-xl-6, .col-xl-7, .col-xl-8, .col-xl-9, .col-xl-auto {
			position: relative;
			width: 100%;
			padding-right: 15px;
			padding-left: 15px;
}

		.col-7 {
			-ms-flex: 0 0 58.333333%;
			flex: 0 0 58.333333%;
			max-width: 58.333333%;
		}

		.arrowpopup {
			position: relative;
			display: inline-block;
			cursor: pointer;
		}

		.arrowpopup .tooltiptext {
			visibility: hidden;
			display: block;
			position: absolute;
			width: 720px;
			background: #fff;
			border-radius: 6px;
			padding: 5px 5px;
			left: 10px;
			border: 2px solid grey;
			line-height: normal;
			text-decoration: none;
			z-index: 1;

		}

		.arrowpopup .tooltiptext::after {
			content: "";

		}

		.arrowpopup .show {
			visibility: visible;
		}

		.infobox {
			display: inline-block;
			vertical-align: top;
		}

		.canopytitle {
			position: relative;
			top: 18px;
			right: 10px;
		}

    /* New code */
    .dropdown-check-list {
      display: inline-block;
    }

    .dropdown-check-list .anchor {
      position: relative;
      cursor: pointer;
      display: inline-block;
      padding: 5px 50px 5px 10px;
      border: 1px solid #ccc;
    }

    .dropdown-check-list .anchor:after {
      position: absolute;
      content: "";
      border-left: 2px solid black;
      border-top: 2px solid black;
      padding: 5px;
      right: 10px;
      top: 20%;
      transform: rotate(225deg);
    }

    .dropdown-check-list .anchor:active:after {
      right: 10px;
      top: 21%;
    }

    .dropdown-check-list ul.items {
      padding: 2px;
      display: none;
      margin: 0;
      border: 1px solid #ccc;
      border-top: none;
    }

    .dropdown-check-list ul.items li {
      list-style: none;
    }

    .dropdown-check-list.visible .items {
      display: block;
    }

  </style>

</head>

<body>
    <div id="processing"></div>
    <div class="container py-3">
        <div class="project" >
                    <div style="display: inline-block;">
						<h3>Canopy Attributes Generator</h3>
					</div>

					<div class = "arrowpopup" >
						<img src="Resources/Images/infobox_icon.png" width="30" height="30" id="infobox" onclick="tooltipFunction();">

						<span class="tooltiptext" id="tooltipdemo">
              To use the tool, the user first needs to specify the project's name, an Orthomosaic file, a Boundary file,
              the sensor and platform that were used to take the Orthomosaic image and optionally a Canopy Height
              Model file. After choosing an Orthomosaic/Canopy Height Model file, the user can specify
              what canopy attributes to generate including the Canopy Cover, Canopy Height, Canopy Volume
              and Excess Greeness. It's important to note, the Canopy Height and Volume can not be generated unless a
              Canopy height Model file is specified. After clicking the "Generate Results" button, the user can
              then select the canopy attributes and file formats (Shape, GeoJSON, CSV and XLSX) they would like
              to download. The generated files are available to download through the "Download Generated Files"
              button, which will then download a Zip file of the specified attributes and file formats.
							<a href="HowToUseCanopyAttributesGeneratorTool.txt" download="HowToUseCanopyAttributesGeneratorTool.txt">Download user guide here!</a>
						</span>
					</div>

					<!-- MOVE TO MAIN.JS -->
					<script>
						function tooltipFunction() {
							var tt = document.getElementById("tooltipdemo");
							tt.classList.toggle("show");
						}
					</script>

                    <div class = "row">

						<!--Select project div-->
						<div class="col-md-12" style="margin-top: 15px;">
                                        <div class="form-group">
                                            <label>Project</label>
                                            <select id="project" name="project" class="form-control">
                                              <option value="0" selected="selected">--Select a Project--</option>
                                            </select>
                                        </div>
                          </div>

                          <!--Select Platform div-->
                          <div class="col-md-6" style="margin-top: 15px;">
                                        <div class="form-group">
                                            <label>Platform</label>
                                            <select id="platform" class="form-control">
                                              <option value="0" selected="selected">--Select a Platform--</option>
                                            </select>
                                        </div>
                          </div>

                          <!--Select Sensor div-->
                          <div class="col-md-6" style="margin-top: 15px;">
                                        <div class="form-group">
                                            <label>Sensor</label>
                                            <select id="sensor" class="form-control">
                                              <option value="0" selected="selected">--Select a Sensor--</option>
                                            </select>
                                        </div>
                          </div>

                          <!--Select Boundary div-->
                          <div class="col-md-12" style="margin-top: 15px;">
                                        <div class="form-group">
                                            <label>Boundary</label>
                                            <select id="boundary" name="boundary" class="form-control">
                                              <option value="0" selected="selected">--Select a Boundary File--</option>
                                            </select>
                                        </div>
                          </div>

                          <!--Select Orthomosaic div-->
                          <div class="col-md-6" style="margin-top: 15px;">
                            <div class="form-group">
                              <label>Orthomosaic</label> <br>
                                <div id="orthomosaic_list" name="orthomosaic_list" class="dropdown-check-list" tabindex="100">
                                  <span class="anchor">--Select Orthomosaic File--</span>
                                    <ul class="items">
                                      <div id="orthomosaic" name="orthomosaic"></div>
                                    </ul>
                                </div>
                              </div>
                            </div>

                            <!--Select Canopy Height Model (CHM) div-->
                          <div class="col-md-6" style="margin-top: 15px;">
                            <div class="form-group">
                            <label>Canopy Height Model</label>
                              <div id="canopy_list" name="canopy_list" class="dropdown-check-list" tabindex="100">
                                <span class="anchor">--Select a Canopy Height Model File--</span>
                                  <ul class="items">
                                    <div id="canopy_height_model" name="canopy_height_model"></div>
                                  </ul>
                              </div>
                            </div>
                          </div>


                          <!--Select canopy attribute selection code-->
                  <div class="col-lg-12">
                      <label>Select Canopy Attributes to Generate:</label>

                            <div class="col-md-12" id="product-list-wrapper-0" style="margin-top: 15px;   max-height: 230px; display: inline-block;">
                            <table id="product-table-0" class="table table-bordered">
                              <thead style="">
                                <tr style="color: white; background: black;">
                                  <th style="border: none;">
                                    <input id="check-all-caTable" type="checkbox" checked="" onchange="ToggleAllRowData_caTable();">
                                  </th>
                                  <th style="border: none;">--Select All--</th>
                                </tr>
                              </thead>
                              <tbody id="product-list-0">
                                <tr>
                                  <td style="">
                                    <input id="ch_cb" name="ch_cb" type="checkbox" value="CanopyHeight" checked="" onchange="ToggleRowData_caTable();">
                                  </td>
                                  <td style="">
                                    <span>CanopyHeight</span>
                                  </td>
                                </tr>
                                <tr>
                                  <td style="">
                                    <input id="cv_cb" name="cv_cb" type="checkbox" value="CanopyVolume" checked="" onchange="ToggleRowData_caTable();">
                                  </td>
                                  <td style="">
                                    <span>CanopyVolume</span>
                                  </td>
                                </tr>
                              <tr>
                                <td style="">
                                  <input id="cc_cb" name="cc_cb" type="checkbox" value="CanopyCover" checked="" onchange="ToggleRowData_caTable();">
                                </td>
                                <td style="">
                                  <span>CanopyCover</span>
                                </td>
                              </tr>
                              <tr>
                                <td style="">
                                  <input id="exg_cb" name="exg_cb" type="checkbox" value="Exg" checked="" onchange="ToggleRowData_caTable();">
                                </td>
                                <td style="">
                                  <span>ExG</span>
                                </td>
                              </tr>
                            </tbody>
                            </table>
                            </div>
                        </div>


          <div class="col-lg-12" style="margin-top: 20px; text-align: center;">
			             <input name="generateResultsBtn" type="button" class="btnNew" value="Generate Results" style="margin-top: 20px; width: 350px" onclick="call_generateResults(); return false;" >
         </div>
			  <!--Select result files to download-->
          <div class="col-lg-12" style="margin-top: 20px;">
            <label>Select result files to download:</label>
          </div>

                  <div class="col-md-12" id="product-list-wrapper-0" style="margin-top: 15px;   max-height: 230px; display: inline-block;">
                  <table id="product-table-0" class="table table-bordered">
                    <thead style="">
                      <tr style="color: white; background: black;">
                        <th style="border: none;">
                          <input id="check-all-formatsTable" type="checkbox" checked="" onchange="ToggleAllRowData_formatsTable();">
                        </th>
                        <th style="border: none;">--Select All--</th>
                      </tr>
                    </thead>
                    <tbody id="product-list-0">
                      <tr>
                        <td style="">
                          <input id="csv_cb" name="csv_cb" type="checkbox" checked="" onchange="ToggleRowData_formatsTable();"> <!--<input id="check-data-2-92" name="check-data-2" type="checkbox" checked="" onchange="ToggleRowData(2);">-->
                        </td>
                        <td style="">
                          <span>.csv</span>
                        </td>
                      </tr>
                      <tr>
                        <td style="">
                          <input id="xls_cb" name="xls_cb" type="checkbox" checked="" onchange="ToggleRowData_formatsTable();"> <!--<input id="check-data-2-82" name="check-data-2" type="checkbox" checked="" onchange="ToggleRowData(2);">-->
                        </td>
                        <td style="">
                          <span>.xls</span>
                        </td>
                      </tr>
                      <tr>
                        <td style="">
                          <input id="geojson_cb" name="geojson_cb" type="checkbox" checked="" onchange="ToggleRowData_formatsTable();"> <!--<input id="check-data-2-83" name="check-data-2" type="checkbox" checked="" onchange="ToggleRowData(2);">-->
                        </td>
                        <td style="">
                          <span>.geoJSON</span>
                        </td>
                      </tr>
                      <tr>
                        <td style=""><input id="shp_cb" name="shp_cb" type="checkbox" checked="" onchange="ToggleRowData_formatsTable();"></td><td style=""> <!--<td style=""><input id="check-data-2-84" name="check-data-2" type="checkbox" checked="" onchange="ToggleRowData(2);"></td><td style="">-->
                          <span>.shp</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

        <div class="col-lg-12" style="margin-top: 20px; text-align: center;">
              <input name="downloadGeneratedFilesBtn" type="button" class="btnNew" value="Download Generated Files" style="margin-top: 20px; width: 350px;" onclick="generateZip(); return false;"/>
      </div>

            </div>
        </div>

        <div class="box" id="loader2">
        </div>

        <div class="loader-wrapper" id="loader">
        </div>

      </div>

</body>
</html>







<!----------------------------------------------------------------------------------------------------------------------------->
<?php
        } else {
            $memberOf = (implode("; ", $user_role_array));
            ?>
<!DOCTYPE html>
<html lang="en">

<head>
    <title><?php echo $pageName; ?></title>
</head>

<body>
    </br>
    <p>You do not currently have permission to access this tool.</p>
    <p>Please contact admin at
        <a href="mailto:<?= $admin_email ?>?
        &subject=Requesting%20access%20to%20the%20crop_analysis%20tool
        &body=Hi,%0D%0A%0D%0AThis%20is%20<?= $admin_email ?>.%20Please%20provide%20me%20access%20to%20the%20tool.">
            <?= $admin_email ?></a>
        to request access to this tool.</p>
</body>

</html>
<?php
        }
    }
}
?>
