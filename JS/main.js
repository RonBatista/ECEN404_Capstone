var pageID = 0;

$(document).ready(function () {

    //$.noConflict();

    GetPageList();
    GetProjectList();

//--------------------------------------------------------------------------New functions
    GetPlatformList();
    GetSensorList();
    OrthoDropdown();
    CanopyDropdown();
    //GetOrthomosaicList();
    //GetCanopyHeightModelList();
    //GetBoundaryList();
//--------------------------------------------------------------------------------------------------------

    $("#project").on('change', function () {
      GetOrthomosaicList();
      GetCanopyHeightModelList();
      GetBoundaryList();
      Toggle_True_Checkboxes();
      ToggleProject();
    });


    $("#platform").on('change', function () {
      GetOrthomosaicList();
      GetCanopyHeightModelList();
      GetBoundaryList();
      Toggle_True_Checkboxes();
      TogglePlatform();
    });


    $("#sensor").on('change', function () {
      GetOrthomosaicList();
      GetCanopyHeightModelList();
      GetBoundaryList();
      Toggle_True_Checkboxes();
      ToggleSensor();
    });

    $("#boundary").on('change', function () {
      GetOrthomosaicList();
      GetCanopyHeightModelList();
      Toggle_True_Checkboxes();
      ToggleBoundary();
    });

    //AddGroup();


    $(":button").mouseup(function () {
        $(this).blur();
    });

});

function GetPageList() {
    $.ajax({
        url: "Resources/PHP/Page.php",
        dataType: 'text',
        data: {
            action: 'list'
        },
        success: function (response) {
            var data = JSON.parse(response);
            if (data.length > 0) {
                var table = "<table id='pages' >" +
                    "<thead>" +
                    "<tr style='background: #555555; color: #ffffff;'>" +
                    "<th style='border: none;'>&nbsp;</th>" +
                    "<th style='border: none;'>Pagze Name</th>" +
                    "<th style='border: none;'>Project Name</th>" +
                    "</tr>" +
                    "</thead>" +
                    "<tbody id='page-list'>" +
                    "</tbody>" +
                    "</table>";

                $("#page-list-wrapper").html(table);
                var items = "";
                var type = "Delete";

                $.each(data, function (index, item) {
                    /*
                    image-button edit-button
                    image-button tms-button
                    image-button apply-button
                    image-button apply-mobile-button
                    image-button delete-button
                    image-button confirm-delete-button
                    image-button cancel-delete-button
                    */
                    items += "<tr>" +
                        "<td>" +
                        "<input style='padding: 8px !important; background: #f0ad4e; margin-right: 3px;' id='edit-" + item.ID + "' type='image' class='' src='Resources/Images/edit.png' alt='Edit' onclick='EditVisualizationPage(" + item.ID + "); return false;' title='Edit'>" +

                        "<input style='padding: 7px !important; background: #449d44; margin-right: 3px;' id='view-" + item.ID + "' type='image' class='' src='Resources/Images/tms.png' alt='Preview' onclick='Preview(\"" + item.Path + "\"); return false;' title='Preview'>" +

                        "<input style='padding: 7px !important; background: #52FF33; margin-right: 3px;' id='apply-" + item.ID + "' type='image' class='' src='Resources/Images/apply.png' alt='Apply' onclick='Apply(\"" + item.ID + "\"); return false;' title='Apply'>" +
                        // added
                        "<input style='padding: 7px !important; background: lightseagreen; margin-right: 3px;' id='apply-" + item.ID + "' type='image' class='' src='Resources/Images/phone-new.png' alt='Apply' onclick='Apply_Mobile(\"" + item.ID + "\"); return false;' title='Apply'>" +
                        // Added
                        "<input style='padding: 7px !important; background: #d9534f; margin-right: 3px;' id='delete-" + type + "-" + item.ID + "' type='image' class='' src='Resources/Images/delete.png' alt='Delete' onclick='Delete(" + item.ID + ", \"" + type + "\"); return false;' title='Delete'>" +
                        "<input style='padding: 7px !important; background: #d9534f; margin-right: 3px; display:none;' id='confirmDelete-" + type + "-" + item.ID + "' type='image' class='' src='Resources/Images/confirm.png' alt='Confirm' style='display:none' onclick='ConfirmDelete(" + item.ID + ", \"" + type + "\"); return false;' title='Confirm'>" +
                        "<input style='padding: 7px !important; background: #ccc; margin-right: 3px; display:none;' id='cancelDelete-" + type + "-" + item.ID + "' type='image' class='' src='Resources/Images/cancel.png' alt='Cancel' style='display:none' onclick='CancelDelete(" + item.ID + ", \"" + type + "\"); return false;' title='Cancel'>" +
                        // Added
                        "</td>" +
                        "<td style='overflow:hidden'>" +
                        "<span>" + item.Name + "</span>" +
                        "</td>" +
                        "<td style='overflow:hidden'>" +
                        "<span>" + item.ProjectName + "</span>" +
                        "</td>" +
                        "</tr>";
                });

                $("#page-list").html(items);

                var rowHeight = 41;
                var padding = 10;
                var actualHeight = (data.length + 1) * rowHeight + padding;
                var maxHeight = 300;
                var height = actualHeight < maxHeight ? actualHeight : maxHeight;
                // var width = 1120;
                var width = 1040;

                $("#pages").fxdHdrCol({
                    fixedCols: 0,
                    width: width,
                    height: height,

                    colModal: [

                        {
                            width: 270,
                            align: 'center'
                        }, // Edit & Link & Apply & Mobile & Delete
                        // {
                        //     width: 408,
                        //     align: 'center'
                        // },
                        // {
                        //     width: 408,
                        //     align: 'center'
                        // },
                        {
                            width: 360,
                            align: 'center'
                        },
                        {
                            width: 360,
                            align: 'center'
                        },
					],
                    sort: false
                });

            }
        }
    });
}

// updated GetProjectList : Function calls Projects.php file via ajax and returns projects from the database populating the project drop down list.
function GetProjectList() {
    $.ajax({
        url: "Resources/PHP/Project.php",
        dataType: 'text',
        data: {
        },
        success: function (response) {
            var data = JSON.parse(response);
            if (data.length > 0) {

                $.each(data, function (index, item) {
                    var project = "<option value='" + item.Name   + "::" + item.ID    //Name of project was added to items value so we can pass info to functions when posted.
                                + "'>" + item.Name + "</option>";
                    $("#project").append(project);

                });
            }

            $("#name").val($("#project option:selected").text());
            GetProjectInfo();
        }
    });
}

function GetProjectInfo() {
    var lat = $("#project").find(":selected").attr("lat");
    var lng = $("#project").find(":selected").attr("lng");
    var zoom = $("#project").find(":selected").attr("zoom");
    var minZoom = $("#project").find(":selected").attr("minZoom");
    var maxZoom = $("#project").find(":selected").attr("maxZoom");
    $("#lat").html(lat);
    $("#lng").html(lng);
    $("#zoom").html(zoom);
    $("#min-zoom").html(minZoom);
    $("#max-zoom").html(maxZoom);
}

//--------------------------------------------------------------------------------------------------------------------------------------------------------- New Functions

/*
Function - GetPlatformList
Description - makes AJAX call to Platform.PHP which returns Platform items in JSON that are then cut up and organized into the drop down menu.
Parameters - none
*/
function GetPlatformList() {                                                              //AJAX call to Sensor php file that grabs Sensor types/info from database
    $.ajax({
        url: "Resources/PHP/Platform.php",
        dataType: 'text',
        data: {
        },
        success: function (response) {                                                             //Grab response from AJAX call
            var data = JSON.parse(response);                                                      //Parse results into JSON format
            if (data.length > 0) {                                                                  //If respose is not empty
              $.each(data, function (index, item) {                                                 //for each row/item in response. make value of item in dropdown menu equal to everything we need to pass to python file that generates attributes
                    var platform = "<option value='" + item.ID                                          //Platform value
                    + "'>" + item.Name + "</option>";                                             //what displays in the dropdown menu
                    $("#platform").append(platform);                                              //add item to dropdown menu
                  });
            }
        }
    });
}

/*
Function - GetSensorList
Description - makes AJAX call to Sensor.PHP which returns Sensor items in JSON that are then cut up and organized into the drop down menu.
Parameters - none
*/
function GetSensorList() {                                                              //AJAX call to Sensor php file that grabs Sensor types/info from database
    $.ajax({
        url: "Resources/PHP/Sensor.php",
        dataType: 'text',
        data: {
        },
        success: function (response) {                                                                //Grab response from AJAX call
            var data = JSON.parse(response);                                                          //Parse results into JSON format
            if (data.length > 0) {                                                                    //If respose is not empty

                $.each(data, function (index, item) {                                                 //for each row/item in response. make value of item in dropdown menu equal to everything we need to pass to python file that generates attributes
                    var sensor = "<option value='" + item.ID                                          //Sensor value
                    + "'>" + item.Name + "</option>";                                                 //what displays in the dropdown menu
                    $("#sensor").append(sensor);                                                      //add item to dropdown menu with id="sensor"

                });
            }
        }
    });
}

var empty_ortho = 0;
var empty_canopy = 0;
var empty_boundary = 0;
function ToggleProject(){
  empty_ortho = empty_ortho + 1;
  empty_canopy = empty_canopy + 1;
  empty_boundary = empty_boundary + 1;
}
function ToggleSensor(){
  empty_ortho = empty_ortho + 1;
  empty_canopy = empty_canopy + 1;
  empty_boundary = empty_boundary + 1;
}
function TogglePlatform(){
  empty_ortho = empty_ortho + 1;
  empty_canopy = empty_canopy + 1;
  empty_boundary = empty_boundary + 1;
}
function ToggleBoundary(){
  empty_ortho = empty_ortho + 1;
  empty_canopy = empty_canopy + 1;
  empty_boundary = empty_boundary + 1;
}

/*
Function - GetOrthomosaicList
Description - makes AJAX call to Orthomosaic.PHP which returns Orthomosaic items with respect to what Project is selected in JSON that are then cut up and organized into the drop down menu.
Parameters - none
*/
var ortho_cnt = 0;
var ortho_total = 0;
function GetOrthomosaicList() {
  //console.log("-------------------------------------------GetOrthomosaicList()");

  if(empty_ortho != 0 && ortho_cnt != 0){
    $('#orthomosaic').empty();
    empty_ortho = 0;
    ortho_cnt = 0;
    ortho_total = 0;
  }

  var selected_project_id = $('#project').val();
  selected_project_id = selected_project_id.split("::")[1];
  //console.log("This is the selected project id:  ");
  //console.log(selected_project_id);

  var selected_platform_id = $('#platform').val();
  //console.log("This is the selected platform id:  ");
  //console.log(selected_platform_id);

  var selected_sensor_id = $('#sensor').val();
  //console.log("This is the selected sensor id:  ");
  //console.log(selected_sensor_id);

  var selected_boundary = $('#boundary').val();
  selected_boundary = selected_boundary.split("::")[0];
  //console.log("This is the selected boundary:  ");
  //console.log(selected_boundary);

  $.ajax({                                                                              //AJAX call to Orthomosiac php file that grabs orthomosiac files/info from database
      url: "Resources/PHP/FlightIDs.php",
      dataType: 'text',
      data: {
          selected_projectID: selected_project_id,
          selected_platformID: selected_platform_id,
          selected_sensorID: selected_sensor_id,
      },
      success: function (response) {                                                    //Grab response from AJAX call
          var data = JSON.parse(response);                                              //Parse results into JSON format
          if (data.length > 0) {                                                        //If respose is not empty

              $.each(data, function (index, item) {                                     //for each row/item in response. make value of item in dropdown menu equal to everything we need to pass to python file that generates attributes
                  var flight_id = item.ID;                 //what displays in the dropdown menu
                  //console.log("Getting Orthos with flight ID: ");
                  //console.log(flight_id);

                          $.ajax({                                                                              //AJAX call to Orthomosiac php file that grabs orthomosiac files/info from database
                              url: "Resources/PHP/Orthomosaic.php",
                              dataType: 'text',
                              data: {
                                  flightID: flight_id,
                              },
                              success: function (response) {                                                    //Grab response from AJAX call
                                  var data = JSON.parse(response);                                              //Parse results into JSON format
                                  if (data.length > 0) {                                                        //If respose is not empty

                                      $.each(data, function (index, item) {                                     //for each row/item in response. make value of item in dropdown menu equal to everything we need to pass to python file that generates attributes
                                          var name = item.FileName;
                                          name = name.split("_");
                                          var boundary_name = item.BoundaryFile;

                                          if(ortho_total == 0){
                                            var checkAll = "<li><input class=checkbox type=checkbox name=check-all-orthomosaic id=check-all-orthomosaic" +
                                            " onchange=ToggleAllOrthomosaics();" + " value=>" + "All" + "</li>";
                                            $("#orthomosaic").append(checkAll);
                                            ortho_total += 1;
                                          }

                                          if(boundary_name == selected_boundary){
                                            ortho_cnt = ortho_cnt + 1;
                                            var ortho = "<li><input class=checkbox type=checkbox id=orthomosaic" + ortho_cnt +" value='" + item.FileName                   //Orthomosaic file name
                                                            + "::" + item.UploadFolder + "/" + item.FileName      //Orthomosaic file path
                                                            + "::" + item.EPSG                                    //ESPG associated with orthomosiac
                                                            + "'" + " onchange=ToggleOrthomosaics();" + ">" + item.FileName + "</li>";

                                          $("#orthomosaic").append(ortho);
                                        }

                                      });
        /*        Took this out as I was unable to emtpy the drop down menu after selecting another Project - Christian Leal
                                      $("#orthomosaic").chosen({
                                          inherit_select_classes: true
                                      });
        */
                                  }
                              }
                            });
              });
          }
      }
  });
}

function OrthoDropdown(){
  var checkList = document.getElementById('orthomosaic_list');
  checkList.getElementsByClassName('anchor')[0].onclick = function(evt) {
    if (checkList.classList.contains('visible')){
      checkList.classList.remove('visible');
    }
    else {
      checkList.classList.add('visible');
    }
  };
}

function ToggleOrthomosaics() {
  let i = 1;
  while(($("#orthomosaic" + i).checked == true)) {
    $("#check-all-orthomosaic").prop("checked", true);
    if(i == ortho_cnt){
      break;
    }
    i++;
  }
  if(i != ortho_cnt || ortho_cnt == 1){
    $("#check-all-orthomosaic").prop("checked", false);
  }
}

function ToggleAllOrthomosaics() {
    if($("#check-all-orthomosaic").is(':checked')) {
      for(let i = 1; i <= ortho_cnt; i++){
        $("#orthomosaic" + i).prop("checked", true);
      }
    }
    else {
      for(let i = 1; i <= ortho_cnt; i++){
        $("#orthomosaic" + i).prop("checked", false);
      }
    }
}

/*
Function - GetCanopyHeightModel
Description - makes AJAX call to CanopyHeightModel.PHP which returns CHM items with respect to what Project is selected in JSON that are then cut up and organized into the drop down menu.
Parameters - none
*/
var canopy_cnt = 0;
var canopy_total = 0;
function GetCanopyHeightModelList() {
    //console.log("----------------------------------------GetCanopyHeightModelList()");

    if(canopy_cnt != 0 && empty_canopy != 0){
      $('#canopy_height_model').empty();
      canopy_cnt = 0;
      empty_canopy = 0;
      canopy_total = 0;
    }
    var selected_project_id = $('#project').val();
    selected_project_id = selected_project_id.split("::")[1];
    //console.log("This is the selected project id:  ");
    //console.log(selected_project_id);

    var selected_platform_id = $('#platform').val();
    //console.log("This is the selected platform id:  ");
    //console.log(selected_platform_id);

    var selected_sensor_id = $('#sensor').val();
    //console.log("This is the selected sensor id:  ");
    //console.log(selected_sensor_id);

    var selected_boundary = $('#boundary').val();
    selected_boundary = selected_boundary.split("::")[0];
    //console.log("This is the selected boundary:  ");
    //console.log(selected_boundary);

    $.ajax({                                                                              //AJAX call to Orthomosiac php file that grabs orthomosiac files/info from database
        url: "Resources/PHP/FlightIDs.php",
        dataType: 'text',
        data: {
            selected_projectID: selected_project_id,
            selected_platformID: selected_platform_id,
            selected_sensorID: selected_sensor_id,
        },
        success: function (response) {                                                    //Grab response from AJAX call
            var data = JSON.parse(response);                                              //Parse results into JSON format
            if (data.length > 0) {                                                        //If respose is not empty

                $.each(data, function (index, item) {                                     //for each row/item in response. make value of item in dropdown menu equal to everything we need to pass to python file that generates attributes
                    var flight_id = item.ID;                 //what displays in the dropdown menu

                    $.ajax({                                                                                      //AJAX call to CanopyHeightModel php file that grabs CHM files/info from database
                        url: "Resources/PHP/CanopyHeightModel.php",
                        dataType: 'text',
                        data: {
                            flightID: flight_id,
                        },
                        success: function (response) {                                                              //Grab response from AJAX call
                            //console.log(response);
                            var data = JSON.parse(response);                                                        //Parse results into JSON format
                            if (data.length > 0) {                                                                  //If respose is not empty

                                $.each(data, function (index, item) {                                               //for each row/item in response. Make value of item in dropdown menu equal to everything we need to pass to python file that generates attributes
                                  var name = item.FileName;
                                  name = name.split("_");
                                  var boundary_name = item.BoundaryFile;

                                    if(canopy_total == 0){
                                      canopy_total += 1;
                                      var checkAll = "<li><input class=checkbox type=checkbox name=check-all-chm id=check-all-chm" +
                                      " onchange=ToggleAllCHM();" + " value=>" + "All" + "</li>";
                                      $("#canopy_height_model").append(checkAll);
                                    }


                                    if(boundary_name == selected_boundary){
                                      canopy_cnt = canopy_cnt + 1;
                                      Canopy = "<li><input class=checkbox type=checkbox id=chm" + canopy_cnt +" value='" + item.FileName                       //CHM file name
                                                          + "::" + item.UploadFolder + "/" + item.FileName          //CHM file path
                                                          + "'" + " onchange=ToggleCHM();" + ">" + item.FileName + "</li>";

                                    $("#canopy_height_model").append(Canopy);
                                  }
                                });
/*
                                $("#canopy_height_model").chosen({
                                    inherit_select_classes: true
                                });
*/
                            }
                        }
                    });
                });
            }
        }
    });
}

function CanopyDropdown(){
  var checkList = document.getElementById('canopy_list');
  checkList.getElementsByClassName('anchor')[0].onclick = function(evt) {
    if (checkList.classList.contains('visible')){
      checkList.classList.remove('visible');
    }
    else {
      checkList.classList.add('visible');
    }
  }
}

function ToggleCHM() {
  let i = 1;
  while(($("#chm" + i).checked == true)) {
    $("#check-all-chm").prop("checked", true);
    if(i == canopy_cnt){
      break;
    }
    i++;
  }
  if(i != canopy_cnt || canopy_cnt == 1){
    $("#check-all-chm").prop("checked", false);
  }
}

function ToggleAllCHM() {
    if($("#check-all-chm").is(':checked')) {
      for(let i = 1; i <= canopy_cnt; i++){
        $("#chm" + i).prop("checked", true);
      }
    }
    else {
      for(let i = 1; i <= canopy_cnt; i++){
        $("#chm" + i).prop("checked", false);
      }
    }
}

/*
Function - GetBoundaryList
Description - makes AJAX call to Boundary.PHP which returns Boundary items with respect to what Project is selected in JSON that are then cut up and organized into the drop down menu.
Parameters - none
*/
function GetBoundaryList() {
  //console.log("----------------------------------------GetBoundaryList()");

  $('#boundary').empty();
  $('#boundary').append($('<option>', {
      value: 0,
      text: '--Select a Boundary File--'
  }));

  var selected_project_name = $('#project').val();
  selected_project_name = selected_project_name.split("::")[0];
  //console.log("This is the selected project name:  ");
  //console.log(selected_project_name);

    $.ajax({                                                              //AJAX call to CanopyHeightModel php file that grabs CHM files/info from database
        url: "Resources/PHP/Boundary.php",
        dataType: 'text',
        data: {
            selected_projectName: selected_project_name
        },
        success: function (response) {                                          //Grab response from AJAX call
            var data = JSON.parse(response);                                    //Parse results into JSON format
            if (data.length > 0) {                                              //If respose is not empty

                $.each(data, function (index, item) {                               //for each row/item in response. Make value of item in dropdown menu equal to everything we need to pass to python file that generates attributes
                    var boundary = "<option id=" + item.ID + " value='" + item.FileName                //Boundary File name
                                 + "::" + item.UploadFolder + "/" + item.FileName   //Boundary file path
                                 + "'>" + item.FileName + "</option>";            //what displays in the dropdown menu

                    $("#boundary").append(boundary);                                 //add item to dropdown menu with id="boundary"

                });

            }
        }
    });
}

/*
Function - showdiv
Description - Shows and hides attributes tables when an Orthomosoaic or Canopy Height Model is selected on the webpage.
Parameters - divID: ID of the div trying to show/hide | element: context of div being changed (this)
*/
function showdiv(divID, element){
  document.getElementById(divID).style.display = element.value == 0 ? 'none' : "block";       //if the value selected is 0 (nothing selcted) hide, else show.
}

/*
Function - call_generateResults
Description - called when the user presses generate results button. Grabs vars and makes call via AJAX to generateResults.PHP showing the loading screen before and after the request is completed.
Parameters - none
*/
var ortho_copy = []; var chm_copy = []; var generate_cnt = 0;
var cc = false; var ch = false; var cv = false; var exg = false;
var val = 0;
var attributes = [];
function call_generateResults() {
  //console.log("----------------------------------------call_generateResults()");

  generate_cnt += 1;
  //creating local variables equal to their respective global variable
  if(checkCount != 0){
    var old_ortho_copy = ortho_copy;
    var old_chm_copy = chm_copy;
    var prev_cc = cc; var prev_ch = ch;
    var prev_cv = cv; var prev_exg = exg;
  }

  var selected_project = $('#project').val();               //grab vars from fields
  var selected_project_name = selected_project.split("::")[0];
  //console.log("This is the selected project: ");
  //console.log(selected_project);

  var selected_platform = $('#platform').val();              //grab vars from fields
  //console.log("This is the selected platform: ");
  //console.log(selected_platform);

  var selected_sensor = $('#sensor').val();                  //grab vars from fields
  //console.log("This is the selected sensor: ");
  //console.log(selected_sensor);
  var index = 1;

  var selected_orthomosaic = "";
  var checkCount = 0;

  ortho_copy = [];
  chm_copy = [];
  cc = $('#cc_cb').is(":checked"); ch = $('#ch_cb').is(":checked");            //grab vars from fields
  cv = $('#cv_cb').is(":checked"); exg = $('#exg_cb').is(":checked");          //grab vars from fields

  // Creating a string of the selected orthomosaic(s) seperated by a comma
  for (let x = 1; x <= ortho_cnt; x++) {
    if ($('#orthomosaic' + x).is(':checked')) {
      //selected_orthomosaic.push($('#orthomosaic' + x).val());
      if (checkCount != 0) {
        selected_orthomosaic += ',';
      }
      selected_orthomosaic += $('#orthomosaic' + x).val();
      checkCount += 1;
    }
  }

  var selected_orthomosaic_list = selected_orthomosaic.split(",");              //split the string into an array with the comma as a delimeter
  var selected_orthomosaic_name = selected_orthomosaic.replace('.tiff','');               //string manipulation to to remove the .tif and .tiff file extention of the selected Orthomosaic
  selected_orthomosaic_name = selected_orthomosaic_name.replace('.tif','');
  selected_orthomosaic_name = selected_orthomosaic_name.replace(/ /gi,'_');
  selected_orthomosaic_name= selected_orthomosaic_name.replace(/\./g,'');           //string manipulation to change spaces to underscores and to remove periods
  selected_orthomosaic_name = selected_orthomosaic_name.split("::")[0];
  //console.log(selected_orthomosaic_name);

  for(let i = 0; i < checkCount; i++){
    ortho_copy.push(selected_orthomosaic_list[i].split("::")[0]);
    ortho_copy[i] = ortho_copy[i].split("_")[0];
  }
  //console.log("This is the new ortho copy:");
  //console.log(ortho_copy);


  var selected_shape = $('#boundary').val();
  //console.log("This is the selected boundary: ");
  //console.log(selected_shape);

  // creating a string of the selected CHM files seperated by a comma
  var selected_chm = "";
  var chm_date = '';
  checkCount = 0;
  for (let y = 1; y <= canopy_cnt; y++) {
    if ($('#chm' + y).is(':checked')) {
      if (checkCount != 0) {
        selected_chm += ',';
        chm_date += ',';
      }
      //selected_chm.push($('#chm' + y).val());
      selected_chm += $('#chm' + y).val();
      temp = $('#chm' + y).val();
      chm_date += temp.split("_")[0];
      checkCount += 1;
    }
  }
  console.log(chm_date);
  var selected_chm_list = selected_chm.split(",");
  var selected_shape_name = selected_shape.replace('.shp','');                        //string manipulation to to remove the .shp file extention of the selected Boundary
  selected_shape_name = selected_shape_name.replace(/ /gi,'_');                   //string manipulation to change spaces to underscores and to remove periods
  selected_shape_name= selected_shape_name.replace(/\./g,'');
  selected_shape_name = selected_shape_name.split("::")[0];

  for(let i = 0; i < checkCount; i++){
    chm_copy.push(selected_chm_list[i].split("::")[0]);
    chm_copy[i] = chm_copy[i].split("_")[0];
  }
  //console.log("This is the new chm copy:");
  //console.log(chm_copy);

  //console.log("cc count: ");
  //console.log(canopy_cnt);

  // if there is no CHM file than a 0 is placed letting the python code know chm = false
  if (selected_chm == "") {
    selected_chm = "0";
  }

  var generated_results = [];
  var cc_checked = $('#cc_cb').is(":checked");              //See if checkboxes have been checked
  //console.log("This is the Canopy Cover checkbox state: ");
  //console.log(cc_checked);

  var exg_checked = $('#exg_cb').is(":checked");
  //console.log("This is the Excess Greeness checkbox state: ");
  //console.log(exg_checked);

  var ch_checked = $('#ch_cb').is(":checked");
  //console.log("This is the Canopy Height checkbox state: ");
  //console.log(ch_checked);

  var cv_checked = $('#cv_cb').is(":checked");
  //console.log("This is the Canopy Volume checkbox state: ");
  //console.log(cv_checked);

//error handling
  if(selected_project == 0){                                                                // If Project is not selected, display error.
    alert("A Project was not specified. Please select a Project.");
    return 0;
  }

  if(selected_platform == 0){                                                                  // If Platform is not selected, display error.
    alert("A Platform was not specified. Please select a Platform.");
    return 0;
  }

  if(selected_sensor == 0){                                                                  // If Sensor is not selected, display error.
    alert("A Sensor was not specified. Please select a Sensor.");
    return 0;
  }

  if(selected_shape == 0){                                                                  // If Boundary is not selected, display error.
    alert("A Boundary File was not specified. Please select a Boundary File.");
    return 0;
  }
  if(selected_orthomosaic == 0){                                                              // If Orthomosaic is not selected, display error.
    alert("An Orthomosiac file was not specified. Please select an Orthomosaic file.");
    return 0;
  }

  if(chm_copy.length > ortho_copy.length){
    alert("Must have less or equal amount of Canopy Height Model files selected than Orthomosaic Files. Please select more Orthomosaic files or less CHM files.");
    return 0;
  }

  if(($('#ch_cb').is(":checked") || $('#cv_cb').is(":checked")) && selected_chm == 0){
    alert("A Canopy Height Model file is needed to generate Canopy Volume or Canopy Height. Please select a CHM file.");
    return 0;
  }

  if($('#exg_cb').is(":checked") == false && $('#ch_cb').is(":checked") == false && $('#cc_cb').is(":checked") == false && $('#cv_cb').is(":checked") == false){
    alert("No attributes were selected please select at least one attribute to generate.");
    return 0;
  }

  var equivalence_check = 0;
  for(let i = 0; i < ortho_copy.length; i++){
    for(let j = 0; j < chm_copy.length; j++){
      if(ortho_copy[i] == chm_copy[j]){
        equivalence_check++;
      }
    }
  }

  if(equivalence_check == 0 && ortho_copy.length > 0 && chm_copy.lenth > 0){
    alert("There is no matching CHM and Orthomosaic. Please select at least one matching pair of Orthomosaic and CHM files.")
    return 0;
  }

// creating a string of the selected orthomosaic names seperated by a comma
// selected_ortho_temp is used for file nameing and check_zip_ortho_temp is used for checkZipStatus.php
var selected_ortho_temp = '';
var check_zip_ortho_temp = '';
checkCount = 0;
for (let x = 1; x <= ortho_cnt; x++) {
  if ($('#orthomosaic' + x).is(':checked')) {
    if (checkCount != 0) {
      //selected_ortho_temp += '_';
      check_zip_ortho_temp += ',';
    }
    selected_orthomosaic_temp = ($('#orthomosaic' + x).val());
    selected_orthomosaic_parts  = selected_orthomosaic_temp.split("::");
    selected_orthomosaic_file = selected_orthomosaic_parts[0];
    selected_orthomosaic_name_array = selected_orthomosaic_file.split(".");
    selected_orthomosaic_name = selected_orthomosaic_name_array[0];
    //selected_ortho_temp += selected_orthomosaic_name;
    check_zip_ortho_temp += selected_orthomosaic_name;
    checkCount += 1;
  }
}
ortho_array = check_zip_ortho_temp.split(",");
ortho_array = ortho_array.sort();
// sorting the array for consistent naming and changing the comma to an underscore
// could probably use .replace() for faster computation
for (let y = 0; y < ortho_array.length; y++) {
  if (y != 0) {
    selected_ortho_temp += '_';
  }
  selected_ortho_temp += ortho_array[y];
}

// file paths for the existing zip file, these are input into CheckZipStatus.php
var base_path = "https://agrilife-project1.uashubs.com/uas_data/download/product/";
var zip_file_path = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_ortho_temp + "_" + selected_shape_name + "/" + "resultsZip.zip";
var zip_file_path_url = base_path + selected_project_name + "/" + selected_ortho_temp + "_" + selected_shape_name + "/" + "resultsZip.zip";
var zip_file_path_noExt = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_ortho_temp + "_" + selected_shape_name + "/" + "resultsZip";

// this function acts as a callback function to update the global variable var from inside the ajax success branch
// this variable is used to determine whether generate results is run.
function store(input) {
    val = input;
  return;
}

//  array of the selected attributes
if (cc_checked == 'true'){
    attributes.push("cc_boundary");
  }
if (exg_checked == 'true'){
    attributes.push("exg_boundary");
  }
if (ch_checked == 'true'){
    attributes.push("ch_boundary");
  }
if (cv_checked == 'true'){
    attributes.push("cv_boundary");
  }

$.ajax({                                          //AJAX call to generateResults.php
       async: false,
       url: "Resources/PHP/checkZipStatus.php",
       datatype: "POST",
       data: {                                             // Data being sent to PHP file
         zipfile_path_noExt: zip_file_path_noExt,
         cc_ckd: cc_checked,
         exg_ckd: exg_checked,
         ch_ckd: ch_checked,
         cv_ckd: cv_checked,
         ortho_temp: check_zip_ortho_temp,
         project: selected_project,
         chm: chm_date
       },
       beforeSend: function(){
         $("#loader").css({display: 'flex'});                       //Show loading screen
         $("#myProgress").show();
         $("#loader2").show();
       },

       success: function (response) {
         //console.log("response:")
         //console.log(response);
         chm_array = [];
         var temp = 0;
         for (let a = 0; a < attributes.length; a ++) {
           if (response.indexOf(attributes[a]) == -1) {
             return;
           }
         }
         var targetString = "The temp results directory and zip file have already been generated, you can download the generated results.";
         if(response.indexOf(targetString) > -1){
           files = [];
           if (response.indexOf('csv') > -1) {
             files.push('csv');
           }
           if (response.indexOf('xls') > -1) {
             files.push(' xls');
           }
           if (response.indexOf('geoJSON') > -1) {
             files.push(' geoJSON');
           }
           if (response.indexOf('shp') > -1) {
             files.push(' shp');
           }
           console.log(files);
           var orthomosaic_date = '';
           if (response.indexOf('all') == -1) {
             orthomosaic_array = selected_ortho_temp.split(',');
             orthomosaic_array.sort();
             console.log(orthomosaic_array);
             for (let o = 0; o < orthomosaic_array.length; o++) {
               orthomosaic_date = orthomosaic_array[o].split("_")[0];
               if (response.indexOf(orthomosaic_date + "_CHM") > -1) {
                 chm_array.push(orthomosaic_array[o].split("_")[0]);
                 console.log(chm_array);
                 //alert(files);
               }
             }
             alert("The file types listed already exist. You're free to download. [" + files + "]. The Canopy Height and Volume only exist for these orthomosaics: " + chm_array);
             alert("If you wouldn't like to redownload the exisitng files or the existing package is missing desired data, Click the \"Generate Results\" button again.");
           } else {
             alert("The file types listed already exist. You're free to download them. " + files);
             alert("If you wouldn't like to redownload the exisitng files or the existing package is missing desired data, Click the \"Generate Results\" button again.");
           }

           //alert("The files listed already exist. You're free to download", files);
           $('#loader').hide();
           $('#loader2').hide();                                 //When complete, hide the loading screen.
           $('#myProgress').hide();
           temp = 1;
           store(temp);
           //generateZip();
           return;

         }
         //console.log("The checkZipStatus file was called!");
       },
       //complete: function(){}
     });

     if (generate_cnt > 1) {
       val = 0;
     }

     if (val == 1) {
       return;
     }

    $.ajax({                                          //AJAX call to generateResults.php
        url: "Resources/PHP/generateResults.php",
        datatype: "POST",
        data: {                                             // Data being sent to PHP file
            project: selected_project,
            orthomosaic: selected_orthomosaic,
            shape: selected_shape,
            chm: selected_chm,
            cc_ckd: cc_checked,
            exg_ckd: exg_checked,
            ch_ckd: ch_checked,
            cv_ckd: cv_checked
        },

        beforeSend: function(){
          $("#loader").css({display: 'flex'});                       //Show loading screen
          $("#myProgress").show();
          $("#loader2").show();
        },

          onprogress: function(e){
              var percent = (e.loaded / e.total) * 100;
              var elem =  document.getElementById("myBar");

              elem.style.width = percent + '%';
              elem.innerHTML = percent * 1  + '%';s
          },

        success: function (response) {
          //console.log("The specified attributes were generated successfully! Hiding Loading div...");
          if(generate_cnt != 0){
            alert("Results have been successfully generated.");
            generate_cnt = 0;
          }
        },

        complete: function(){
          $('#loader').hide();
          $('#loader2').hide();                                 //When complete, hide the loading screen.
          $('#myProgress').hide();
        }

    });

}

/*
Function - generateZip
Description - called when the user presses the "Download Generated Files" button. Grabs vars and makes call via AJAX to generateZip.PHP showing the loading screen before and after the request is completed.
Parameters - none
*/
var generate_zip = 0;
function generateZip(){

  if(generate_zip == 0){
    generate_zip += 1;
  }
                                                //get vars from webpage
  var selected_project = $('#project').val();               //get selected project value
  var selected_project_name = selected_project.split("::")[0];
  selected_project_name = selected_project_name.replace(/ /gi,'_');   //string manipulation to change spaces to underscores and to remove periods for the project name that is selected
  selected_project_name= selected_project_name.replace(/\./g,'');
  //console.log(selected_project_name);

  if (selected_project == 0){                                                               // If Project is not selected, display error.
    alert("Error generating Zip file! Please specify a Project before downloading files.");
    return 0;
  }

  var selected_orthomosaic = "";
  var checkCount = 0;
  for (let x = 1; x <= ortho_cnt; x++) {
    if ($('#orthomosaic' + x).is(':checked')) {
      //selected_orthomosaic.push($('#orthomosaic' + x).val());
      if (checkCount != 0) {
        selected_orthomosaic += ',';
      }
      selected_orthomosaic += $('#orthomosaic' + x).val();
      checkCount += 1;
    }
  }

    if (selected_orthomosaic == 0){                                                              // If Orthomosaic is not selected, display error.
      alert("Error generating Zip file! Please specify an Orthomosaic file before downloading files.");
      return 0;
    }
    //console.log(selected_orthomosaic);

  var selected_shape = $('#boundary').val();                //get selected boundary value
  //selected_shape = selected_shape.replace('.shp', '');
  //selected_shape = selected_shape.split("::")[0];
  //console.log(selected_shape);

  if (selected_shape == 0){                                                                         // If Boundary is not selected, display error.
    alert("Error generating Zip file! Please specify a Boundary file before downloading files.");
    return 0;
  }

  // creating a string of the selected CHM files seperated by a comma
  var selected_chm = "";
  checkCount = 0;
  for (let y = 1; y <= canopy_cnt; y++) {
    if ($('#chm' + y).is(':checked')) {
      if (checkCount != 0) {
        selected_chm += ',';
      }
      //selected_chm.push($('#chm' + y).val());
      selected_chm += $('#chm' + y).val();
      checkCount += 1;
    }
  }
  if (selected_chm == "") {
    selected_chm = "0";
  }
  //console.log(selected_chm);

  var cc_checked = $('#cc_cb').is(":checked");            //check to see if checkboxes are checked
  //console.log(cc_checked);

  var exg_checked = $('#exg_cb').is(":checked");
  //console.log(exg_checked);

  var ch_checked = $('#ch_cb').is(":checked");
  //console.log(ch_checked);

  var cv_checked = $('#cv_cb').is(":checked");
  //console.log(cv_checked);

  var csv_checked = $('#csv_cb').is(":checked");
  //console.log(csv_checked);

  var xls_checked = $('#xls_cb').is(":checked");
  //console.log(xls_checked);

  var geojson_checked = $('#geojson_cb').is(":checked");
  //console.log(geojson_checked);

  var shp_checked = $('#shp_cb').is(":checked");
  //console.log(shp_checked);
  var cz_val = val;

  $("#loader").css({display: 'flex'});       //Show the loading screen
  $("#loader2").show();
 $.ajax({                                     //AJAX call to generateZip.PHP
     url: "Resources/PHP/generateZip.php",
     datatype: "POST",
     data: {                                  //Data being passed to PHP file
         project: selected_project,
         orthomosaic: selected_orthomosaic,
         shape: selected_shape,
         chm: selected_chm,
         cc_ckd: cc_checked,
         exg_ckd: exg_checked,
         ch_ckd: ch_checked,
         cv_ckd: cv_checked,
         csv_ckd: csv_checked,
         xls_ckd: xls_checked,
         geo_ckd: geojson_checked,
         shp_ckd: shp_checked,
         check_zip_val: cz_val
     },
     success: function (response) {     //when a response is received (File finished being generated) call downloadZip function.
       console.log('selected_shape: ');
       console.log(selected_shape);
       var targetString1 = "The specified project\\/orthomosaic results do not exist!";
       var targetString2 = "The specified canopy attribute results do not exist!";
       if(response.indexOf(targetString1) > -1){                                          //Error handling: If project/Ortho results do not exist, kill process
         $("#loader").hide();
         $("#loader2").hide();
         alert("The generated result files specified do not exist. Please generate all canopy attributes specified before downloading them.");
       }
       else if(response.indexOf(targetString2) > -1){                                   //Error handling: If specified attribute results do not exist, kill process
         //console.log("ERROR: The specified canopy attribute results do not exist!");
         $("#loader").hide();
         $("#loader2").hide();
         alert("Unable to generate the Zip file! Please generate all canopy attributes specified before downloading them.");
       }
       else{                                                      //Else, no errors. Call function to download the generated zip file.
         //console.log("The zip file was generated successfully!");
         /*if(generate_zip != 0){
           alert("Files have been downloaded successfully.");
           var generate_zip = 0;
         } */

         downloadZip();
         //ZipZips();
       }
     }
 });

}



/*
Function - downloadZip
Description - called when a response is received from the AJAX called in generateZip(). Grabs vars and downloads the requested results Zip file.
parameters - none
*/
function downloadZip(){
    //grab vars
var selected_project = $('#project').val();
selected_project = selected_project.replace(/ /gi,'_');           //string manipulation to change spaces to underscores and to remove periods for the project name that is selected
selected_project= selected_project.replace(/\./g,'');
var selected_project_name = selected_project.split("::")[0];
//console.log(selected_project_name);

// creating a string of the selected orthomosaics seperated by a comma
var checkCount = 0;
var selected_orthomosaic = '';
var selected_ortho_temp = '';
for (let x = 1; x <= ortho_cnt; x++) {
  if ($('#orthomosaic' + x).is(':checked')) {
    if (checkCount != 0) {
        selected_ortho_temp += ',';
    }
    selected_orthomosaic = ($('#orthomosaic' + x).val());
    selected_orthomosaic_parts  = selected_orthomosaic.split("::");
    selected_orthomosaic_file = selected_orthomosaic_parts[0];
    selected_orthomosaic_name_array = selected_orthomosaic_file.split(".");
    selected_orthomosaic_name = selected_orthomosaic_name_array[0];
    selected_ortho_temp += selected_orthomosaic_name;
    checkCount += 1;
  }
}

// making an array of the selected orthomosaics and sorting it
selected_ortho_temp_list = selected_ortho_temp.split(",");
selected_ortho_temp_list = selected_ortho_temp_list.sort();
//console.log("sorted: ", selected_ortho_temp_list);

// creating a string of the selected orthomosaics seperated by an underscore for consistent naming
selected_ortho_temp = '';
for (let x = 0; x < checkCount; x++) {
  if (x != 0) {
    selected_ortho_temp += '_';
  }
  selected_ortho_temp += selected_ortho_temp_list[x];
}

var selected_shape = $('#boundary').val();
selected_shape_name = selected_shape.replace('.shp','');                        //string manipulation to to remove the .shp file extention of the selected Boundary
selected_shape_name = selected_shape_name.replace(/ /gi,'_');                   //string manipulation to change spaces to underscores and to remove periods
selected_shape_name= selected_shape_name.replace(/\./g,'');
selected_shape_name = selected_shape_name.split("::")[0];


// creating a list of selected CHM files seperated by a comma
var selected_chm = '';
checkCount = 0;
for (let y = 1; y <= canopy_cnt; y++) {
  if ($('#chm' + y).is(':checked')) {
    if (checkCount != 0) {
      selected_chm += ',';
    }
    selected_chm += ($('#chm' + y).val());
    checkCount += 1;
  }
}

selected_chm_list = selected_chm.split(",");
selected_chm = selected_chm_list[0];
selected_chm_parts  = selected_chm.split("::");
selected_chm_name = selected_chm_parts[0];
selected_chm_name_array = selected_chm_name.split(".");
selected_chm_name = selected_chm_name_array[0];
//console.log("MainCHM: ", selected_chm);

// base path for website where result directories are located
var base_path = "https://agrilife-project1.uashubs.com/uas_data/download/product/";

//path to results Zip file being requested for download.
var zip_file_path = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_ortho_temp + "_" + selected_shape_name + "/" + "resultsZip.zip";
var zip_file_path_url = base_path + selected_project_name + "/" + selected_ortho_temp + "_" + selected_shape_name + "/" + "resultsZip.zip";
var zip_file_path_noExt = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_ortho_temp + "_" + selected_shape_name + "/" + "resultsZip";
//console.log("This is the zip_file_path_url: ");
//console.log(zip_file_path_url);

var zip_file = window.open(zip_file_path_url, '_blank');
if (zip_file) {
//Browser has allowed it to be opened
zip_file.focus();                           //if able to find ZIP file, download the file.
$("#loader").hide();
$("#loader2").hide();
}
else {
//Browser has blocked it
$("#loader").hide();
$("#loader2").hide();
alert('Please allow popups for this website');          //if unable to download ZIP file, alert the user.
}
 $.ajax({                                          //AJAX call to generateResults.php
url: "Resources/PHP/deleteTempResults.php",
datatype: "POST",
data: {                                             // Data being sent to PHP file
zipfile_path: zip_file_path,
zipfile_path_noExt: zip_file_path_noExt,
selected_ortho: selected_ortho_temp,
selected_shape: selected_shape_name,
},
success: function (response) {
  ////console.log("response:")
  ////console.log(response);
  //var targetString = "The temp results directory and zip file were deleted successfully!";
  //if(response.indexOf(targetString) > -1){                                          //Error handling: If project/Ortho results do not exist, kill process
  //  return;
  //}
  //console.log("The deleteTempResults file was called!");
}
});

// //path to results Zip file being requested for download.
// var zip_file_path_url = base_path + selected_project_name + "/" + selected_orthomosaic_name + "_" + selected_shape_name + "/" + selected_project_name + "_" + selected_orthomosaic_name + "_" + selected_shape_name + "_results" + ".zip";

// var zip_file_path = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_orthomosaic_name + "_" + selected_shape_name + "/" + selected_project_name + "_" + selected_orthomosaic_name + "_" + selected_shape_name + "_results.zip";
// var zip_file_path_noExt = "/var/www/html/uas_data/download/product/" + selected_project_name + "/" + selected_orthomosaic_name + "_" + selected_shape_name + "/" + selected_project_name + "_" + selected_orthomosaic_name + "_" + selected_shape_name + "_results";

// //console.log("This is the zip_file_path_url: ");
// //console.log(zip_file_path_url);

// var zip_file = window.open(zip_file_path_url, '_blank');
// if (zip_file) {
// //Browser has allowed it to be opened
// zip_file.focus();                           //if able to find ZIP file, download the file.
// $("#loader").hide();
// $("#loader2").hide();
// }
// else {
// //Browser has blocked it
// $("#loader").hide();
// $("#loader2").hide();
// alert('Please allow popups for this website');          //if unable to download ZIP file, alert the user.
// }
// $.ajax({                                          //AJAX call to generateResults.php
// url: "Resources/PHP/deleteTempResults.php",
// datatype: "POST",
// data: {                                             // Data being sent to PHP file
// zipfile_path: zip_file_path,
// zipfile_path_noExt: zip_file_path_noExt,
// },
// complete: function (response) {
// //console.log("The deleteTempResults file was called!")
// }
// });
}
/*
Function - ToggleRowData_caTable
Description - function used to check select all checkbox when all canopy attributes are selected when selecting attributes.
parameters - none
*/
function ToggleRowData_caTable() {
    if (($("#ch_cb").is('checked')) && ($("#cv_cb").is('checked')) && ($("#cc_cb").is('checked')) && ($("#exg_cb").is('checked'))) {
        $("#check-all-caTable").prop("checked", true);
    } else {
        $("#check-all-caTable").prop("checked", false);
    }
}

/*
Function - ToggleALLRowData_caTable
Description - function used to check and uncheck all checkboxes when the select all checkbox is checked/unchecked in the table where the user is specifying what canopy attributes they want generated.
parameters - none
*/
function ToggleAllRowData_caTable() {
    if($("#check-all-caTable").is(':checked')) {
        $("#ch_cb").prop("checked", true);
        $("#cv_cb").prop("checked", true);
        $("#cc_cb").prop("checked", true);
        $("#exg_cb").prop("checked", true);
    }else {
        $("#ch_cb").prop("checked", false);
        $("#cv_cb").prop("checked", false);
        $("#cc_cb").prop("checked", false);
        $("#exg_cb").prop("checked", false);
    }
}

/*
Function - ToggleRowData_formatsTable
Description - function used to check select all checkbox when all file format are selected when downloading results.
parameters - none
*/
function ToggleRowData_formatsTable() {
    if (($("#csv_cb").is(':checked')) && ($("#xls_cb").is(':checked')) && ($("#geojson_cb").is(':checked')) && ($("#shp_cb").is(':checked'))) {
        $("#check-all-formatsTable").prop("checked", true);
    } else {
        $("#check-all-formatsTable").prop("checked", false);
    }
}

/*
Function - ToggleAllRowData_formatsTable
Description - function used to check and uncheck all checkboxes when the select all checkbox is checked/unchecked in the table where the user is specifying what file formats they want to download.
parameters - none
*/
function ToggleAllRowData_formatsTable() {
    if ($("#check-all-formatsTable").is(':checked')) {
        $("#csv_cb").prop("checked", true);
        $("#xls_cb").prop("checked", true);
        $("#geojson_cb").prop("checked", true);
        $("#shp_cb").prop("checked", true);
    } else {
        $("#csv_cb").prop("checked", false);
        $("#xls_cb").prop("checked", false);
        $("#geojson_cb").prop("checked", false);
        $("#shp_cb").prop("checked", false);
    }
}


/*
Function - Toggle_True_Checkboxes
Description - Function is used to toggle all the checkboxes in the ccExgTable and chCvTable to True when either the Project, Platform or Sensor are changed.
parameters - none
*/
function Toggle_True_Checkboxes(){
  if(!$('#check-all-caTable').is(":checked")){
    $("#check-all-caTable").prop("checked", true);
  }

  if(!$('#cc_cb').is(":checked")){
    $("#cc_cb").prop("checked", true);
  }

  if(!$('#exg_cb').is(":checked")){
    $("#exg_cb").prop("checked", true);
  }

  if(!$('#ch_cb').is(":checked")){
    $("#ch_cb").prop("checked", true);
  }

  if(!$('#cv_cb').is(":checked")){
    $("#cv_cb").prop("checked", true);
  }
}

//----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
function AddGroup() {
    var index = $("#group-headers li").length;
    var newGroupHeader = "<li><a href='#group-" + index + "'>Group " + (index + 1) + "</a></li>";
    $("#group-headers").append(newGroupHeader);

    var newGroup = "<div id='group-" + index + "' class='row'>" +
        "<div class='col-md-12'>" +
            "<div class='form-inline mb-2'>" +
                "<label>Group Name</label>" +
                "<input type='text' id='group-" + index + "-name' class='form-control'>" +
            "</div>";
        "</div>";
    "</div>";
    $("#groups").append(newGroup);

    AddSearchCriteria(index);
    //AddPageControl(index);
    AddResultSection(index);

    if (index == 0) {
        $("#groups").tabs({
            active: 0
        });
    } else {
        $("#groups").tabs("refresh");
    }
}

function AddSearchCriteria(index) {
    var criteiaSectionStr = "<div class='project'>" +
        "<h3>Criteria</h3>";
    var criteiaList = [
        {
            label: "Type",
            id: "product_type"
        },
						];

    $.each(criteiaList, function (i, criteia) {
        criteiaSectionStr += "<div class='row'>" +
            "<div class='form-inline'>" +

            "<label class='mr-1' for='" + criteia.id + "-" + index + "'>" + criteia.label + "</label>" +
            "<select id='" + criteia.id + "-" + index + "' class='form-control'></select>" ;


        if (i == criteiaList.length / 2 - 1) {
            criteiaSectionStr += "<div style='clear:both'></div>";
        }

    });

    criteiaSectionStr +=

        "<input type='button' class='button right-button btnNew' value='Search' onclick='GetProductList(" + index + "," + 0 + "); return false;' />" +

        "</div>"+
    "</div>" ;

    $("#group-" + index).append(criteiaSectionStr);

    $.each(criteiaList, function (i, criteia) {
        GetList(criteia.id, index);
    });
}

function AddResultSection(index) {
    var str = "<div class='project' style='margin-top: 25px;'>" +
        "<h3>Result</h3>" +
            "<div class='row'>" +
                "<div class='col-md-12' id='product-list-wrapper-" + index + "' style='    max-height: 230px; overflow: auto; display: inline-block;'>" +

                "</div>" +
            "</div>" +
        "</div>" +
        "<br>" +
        "<div style='clear:both'></div>";
    $("#group-" + index).append(str);
}

function GetList(name, index) {
    $.ajax({
        url: 'Resources/PHP/GetList.php',
        dataType: 'text',
        data: {
            name: name
        },
        success: function (response) {
            var items = "<option value='%' >All</option>";
            var data = JSON.parse(response);

            $.each(data, function (index, item) {
                items += "<option value='" + item.ID + "'>" + item.Name + "</option>";
            });
            $("#" + name + "-" + index).html(items);
        }
    });
}

function GetProductList(index, groupID) {
    var type = $("#product_type-" + index).val();
    var project = $("#project").val();

    $("#loading").show();

    $.ajax({
        url: "Resources/PHP/GetProductList.php",
        dataType: "text",
        data: {
            project: project,
            type: type
        },
        success: function (response) {
            var data = JSON.parse(response);
            if (data.length > 0) {
                var table = "<table id='product-table-" + index + "' class='table table-bordered'>" +
                    "<thead style=''>" +
                    "<tr style='color: white; background: black;'>" +
                    "<th style='border: none;'><input id='check-all-" + index + "' type='checkbox' checked onchange='ToggleAllRowData(" + index + ");'></th>" +
                    "<th style='border: none;'>Name</th>" +

                    "</tr>" +
                    "</thead>" +
                    "<tbody id='product-list-" + index + "'>" +
                    "</tbody>" +
                    "</table>";

                $("#product-list-wrapper-" + index).html(table);

                var items = "";

                $.each(data, function (i, item) {

                    items += "<tr>" +
                        "<td style=''><input id='check-data-" + index + "-" + item.ID + "' name ='check-data-" + index + "' type='checkbox' checked onchange='ToggleRowData(" + index + ");'></td>" +
                        "<td style=''><span>" + item.FileName + "</span></td>" +
                        "</tr>";
                });

                $("#product-list-" + index).html(items);

                if (groupID > 0) {
                    SetSelectedLayer(index, groupID);
                }

            } else {
                $("#product-list-wrapper-" + index).html("No data found.");
            }
            $("#loading").hide();

        },
        error: function (request, status, error) {

            $("#loading").hide();
            alert(request.responseText);
        }
    });

}

function GetGroupSelection(index) {
    var name = $("#group-" + index + "-name").val();
    var type = $("#product_type-" + index).val();
    var idList = "";

    $.each($("input[name=check-data-" + index + "]:checked"), function (i, item) {
        var id = item.id.replace("check-data-" + index + "-", "");
        idList += id + ";";
    });

    idList = idList.slice(0, -1);

    return {
        GroupName: name,
        Type: type,
        IDs: idList
    };
}

function Generate() {
    var project = $("#project").val();
    var name = $("#name").val();
    var center = $("#lat").html() + "," + $("#lng").html();
    var zoom = $("#zoom").html();
    var minZoom = $("#min-zoom").html();
    var maxZoom = $("#max-zoom").html();

    var num = $("#group-headers li").length;
    var groups = new Array();
    for (var i = 0; i < num; i++) {
        var group = GetGroupSelection(i);
        groups.push(group);
    }

    $.ajax({
        url: "Resources/PHP/Generate.php",
        dataType: 'text',
        data: {
            pageid: pageID,
            project: project,
            groups: groups,
            name: name,
            center: center,
            zoom: zoom,
            minZoom: minZoom,
            maxZoom: maxZoom
        },
        success: function (response) {
            $("#result-link").val(response);
            GetPageList();
            $("#page-info").hide();
            alert("The visualization page has been created successfully.");
            //$("#result").show();
        }
    });
}

function View() {
    var link = $("#result-link").val();
    var win = window.open(link, '_blank');
    if (win) {
        //Browser has allowed it to be opened
        win.focus();
    } else {
        //Browser has blocked it
        alert('Please allow popups for this website');
    }
}

function EditVisualizationPage(id) {
    $.ajax({
        url: "Resources/PHP/Page.php",
        dataType: 'text',
        data: {
            action: "info",
            id: id
        },
        success: function (response) {
            var page = JSON.parse(response);
            $("#project").val(page.Project);
            $("#project").trigger("chosen:updated");

            GetProjectInfo();

            GetPageGroups(page.ID);
            $("#name").val(page.Name);
            pageID = page.ID;
            $("#project_chosen").width(350);
            $("#page-info").show();
        }
    });
}

function GetPageGroups(id) {
    $.ajax({
        url: "Resources/PHP/Group.php",
        dataType: 'text',
        data: {
            pageid: id
        },
        success: function (response) {
            var groups = JSON.parse(response);
            if (groups.length > 0) {
                $("#group-wrapper").html("<div id='groups'><ul id='group-headers'></ul></div>");

                $.each(groups, function (index, group) {
                    AddGroup();
                    setTimeout(function () {
                        $("#group-" + index + "-name").val(group.Name);
                        $("#product_type-" + index).val(group.Type);
                        GetProductList(index, group.ID);
                    }, 500);


                });

            }
        }
    });
}

function Apply(id) {
    $.ajax({
        url: "Resources/PHP/Apply.php",
        dataType: 'text',
        data: {
            pageid: id
        },
        success: function (response) {
            //alert("The visualization has been applied. Review: " + response);
            if (response.indexOf("Failed") < 0) { //Success
                $("#result-text").text("The visualization has been applied.");

                $("#dialog-review").dialog({
                    resizable: false,
                    height: "auto",
                    position: {
                        my: "top+50",
                        at: "top+50",
                        of: window
                    },
                    width: 400,
                    modal: true,
                    buttons: {
                        "Preview": function () {
                            Preview(response);
                        }
                    }
                });
            } else { //Failed
                $("#result-text").text(response);

                $("#dialog-review").dialog({
                    resizable: false,
                    height: "auto",
                    position: {
                        my: "top+50",
                        at: "top+50",
                        of: window
                    },
                    width: 400,
                    modal: true,
                    buttons: {
                        "OK": function () {
                            $(this).dialog("close");
                        }
                    }
                });
            }
        }
    });
}

// Added
function Delete(id, type) {
    $('#confirmDelete-' + type + '-' + id).show();
    $('#cancelDelete-' + type + '-' + id).show();
    $('#delete-' + type + '-' + id).hide();
    // CancelEdit(id);
}

function CancelDelete(id, type) {
    $('#confirmDelete-' + type + '-' + id).hide();
    $('#cancelDelete-' + type + '-' + id).hide();
    $('#delete-' + type + '-' + id).show();
}

function ConfirmDelete(id, type) {
    $.ajax({
        url: 'Resources/PHP/' + type + '.php',
        dataType: 'text',
        data: {
            id: id,
            action: 'delete'
        },
        success: function (response) {
            // if (response == "1") {
            $('#confirmDelete-' + type + '-' + id).hide();
            $('#cancelDelete-' + type + '-' + id).hide();
            $('#delete-' + type + '-' + id).show();

            //alert("The " + type + " has been deleted.");

            // Added
            // $.each(criteiaList,function(i,criteia) {
            // 	GetList(criteia.id , index);
            // });
            // Added

            // } else {
            // 	alert("Could not delete the " + type + ". Error: " + response + ".");
            // }

            // Reload the page after deleting
            location.reload();
        }
    });
}
// Added

// Added
function Apply_Mobile(id) {
    $.ajax({
        url: "Resources/PHP/Apply_Mobile.php",
        dataType: 'text',
        data: {
            pageid: id
        },
        success: function (response) {
            //alert("The visualization has been applied. Review: " + response);
            if (response.indexOf("Failed") < 0) { //Success
                $("#result-text").text("The visualization has been applied.");

                $("#dialog-review").dialog({
                    resizable: false,
                    height: "auto",
                    position: {
                        my: "top+50",
                        at: "top+50",
                        of: window
                    },
                    width: 400,
                    modal: true,
                    buttons: {
                        "Preview": function () {
                            Preview(response);
                        }
                    }
                });
            } else { //Failed
                $("#result-text").text(response);

                $("#dialog-review").dialog({
                    resizable: false,
                    height: "auto",
                    position: {
                        my: "top+50",
                        at: "top+50",
                        of: window
                    },
                    width: 400,
                    modal: true,
                    buttons: {
                        "OK": function () {
                            $(this).dialog("close");
                        }
                    }
                });
            }
        }
    });
}
//

function ValidURL(str) {
    var pattern = new RegExp('^(https?:\/\/)?' + // protocol
        '((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|' + // domain name
        '((\d{1,3}\.){3}\d{1,3}))' + // OR ip (v4) address
        '(\:\d+)?(\/[-a-z\d%_.~+]*)*' + // port and path
        '(\?[;&a-z\d%_.~+=-]*)?' + // query string
        '(\#[-a-z\d_]*)?$', 'i'); // fragment locater
    if (!pattern.test(str)) {
        alert("Please enter a valid URL.");
        return false;
    } else {
        return true;
    }
}

function SetSelectedLayer(index, groupID) {
    $.ajax({
        url: "Resources/PHP/SelectedLayer.php",
        dataType: 'text',
        data: {
            groupID: groupID
        },
        success: function (response) {
            var layers = JSON.parse(response);
            if (layers.length > 0) {
                $("#check-all-" + index).prop('checked', false);
                ToggleAllRowData(index);
                $.each(layers, function (i, layer) {
                    $("#check-data-" + index + "-" + layer.Layer).prop('checked', true);
                    //console.log("#check-data-" + index + "-" + layer.Layer);

                });

            }
        }
    });
}

function AddPage() {
    $("#group-wrapper").html("<div id='groups'><ul id='group-headers'></ul></div>");
    AddGroup();
    $("#project_chosen").width(350);
    $("#name").val($("#project option:selected").text());
    $("#page-info").show();

}

function Preview(link) {
    var win = window.open(link, '_blank');
    if (win) {
        //Browser has allowed it to be opened
        win.focus();
    } else {
        //Browser has blocked it
        alert('Please allow popups for this website');
    }
}

function showAlert(index) {
	if(index == 1)
	{
		alert("Attributes generated.");
	}
	else
	{
		alert("Files downloaded.");
	}
}
