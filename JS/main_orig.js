/*
var resumableInstances = new Array();
var rowColor = "#fff"; 
//var marker;
var flights = new Array();
var processing = false;
var uploading = false;
*/

var pageID = 0;

$(document).ready(function(){
	
	//$.noConflict();
	
	GetPageList();
	GetProjectList();
	$("#project").on('change', function() {
		GetProjectInfo();
		$("#name").val($("#project option:selected").text());
	});
	//AddGroup();
	
	
	$(":button").mouseup(function(){
		$(this).blur();
	});
	
});

function GetPageList(){
	$.ajax({
		url: "Resources/PHP/Page.php",
		dataType: 'text',
		data: { action: 'list'},  
		success: function(response) {
			var data = JSON.parse(response);
			if (data.length > 0)
			{
				var table =	"<table id='pages' >" +
								"<thead>" +
									"<tr>" +
										"<th>&nbsp;</th>" +
										"<th>Page Name</th>" +
										"<th>Project Name</th>" +
									"</tr>" +
								"</thead>" +
								"<tbody id='page-list'>" +
								"</tbody>" +
							"</table>";
				
				$("#page-list-wrapper").html(table);
				var items = "";
			
				$.each(data,function(index,item) 
				{
					
					items+="<tr>" + 
								"<td>" + 
									"<input id='edit-" + item.ID +"' type='image' class='image-button edit-button' src='Resources/Images/edit.png' alt='Edit' onclick='EditVisualizationPage(" + item.ID + "); return false;' title='Edit'>" + 
									"<input id='view-" + item.ID +"' type='image' class='image-button tms-button' src='Resources/Images/tms.png' alt='Preview' onclick='Preview(\"" + item.Path + "\"); return false;' title='Preview'>" + 
									"<input id='apply-" + item.ID +"' type='image' class='image-button apply-button' src='Resources/Images/apply.png' alt='Apply' onclick='Apply(\"" + item.ID + "\"); return false;' title='Apply'>" + 
									
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
				var width = 1100;
				
				$("#pages").fxdHdrCol({
					fixedCols:  0,
					width:     width,
					height:    height,
					
					colModal: [
						
						{ width: 150, align: 'center' },
						{ width: 300, align: 'center' },
						{ width: 600, align: 'center' },
					],
					sort: false
				});
				
			}
		}	
	});
}

function GetProjectList(){
	$.ajax({
		url: "Resources/PHP/Project.php",
		dataType: 'text',
		data: { action: 'list'},  
		success: function(response) {
			var data = JSON.parse(response);
			if (data.length > 0)
			{
				
				$.each(data,function(index,item) 
				{
					var project = 	"<option value='" + item.ID + "' lat='" + item.CenterLat + "' lng='" + item.CenterLng + 
									"' zoom='" + item.DefaultZoom + "' minZoom='" + item.MinZoom + 
									"' maxZoom='" + item.MaxZoom + "'>" + item.Name + "</option>";		
					$("#project").append(project);
					
				});
				
				
				$("#project").chosen({
					inherit_select_classes: true
				});

			}
			
			$("#name").val($("#project option:selected").text());
			GetProjectInfo();
		}	
	});
}

function GetProjectInfo(){
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

function AddGroup(){
	var index = $("#group-headers li").length;
	var newGroupHeader = "<li><a href='#group-" + index + "'>Group "+ (index + 1)+"</a></li>";
	$("#group-headers").append(newGroupHeader);
	
	var newGroup =  "<div id='group-" + index + "'>" +
						"<div class='label'>Group Name</div>" +
						"<div class='input'><input type='text' id='group-" + index +"-name'></div>" +
						"<div style='clear:both'></div>" +
						"<br>" +
					"</div>";
	$("#groups").append(newGroup);					
	
	AddSearchCriteria(index);
	//AddPageControl(index);
	AddResultSection(index);
	
	if (index == 0){
		$("#groups").tabs({
			active: 0
		});
	} else {
		$("#groups").tabs("refresh");
	}
}

function AddSearchCriteria(index){
	var criteiaSectionStr = "<fieldset>" +
								"<legend>Criteria</legend>";
	var criteiaList = 	[ 
							{ label: "Type", 	  id: "product_type"} ,
						];	
	
	$.each(criteiaList,function(i,criteia) {
		criteiaSectionStr += 	"<div class='one-fourth'>" +
									"<div class='label label-small'>" + criteia.label + "</div>" +
									"<div class='input'>" +
										"<select id='" + criteia.id + "-" + index  +"' class='select-small'></select>" +
									"</div>"+	
								"</div>";
		if (i == criteiaList.length / 2 - 1){
			criteiaSectionStr += "<div style='clear:both'></div>";		
		}
					
	});	
	
	criteiaSectionStr+= "</fieldset>" +
						"<div style='clear:both'></div>" +
							"<input type='button' class='button right-button' value='Search' onclick='GetProductList(" + index + "," + 0 +"); return false;' />" +
						"<div style='clear:both'></div>";
	
	$("#group-" + index).append(criteiaSectionStr);
	
	$.each(criteiaList,function(i,criteia) {
		GetList(criteia.id , index);
	});	
}

function AddResultSection(index){
	var str = 	"<fieldset>" +
					"<legend>Result</legend>" +
					"<div id='product-list-wrapper-" + index + "' style='width: 80%; margin: auto'>" +
					"</div>" +
				"</fieldset>" +
				"<br>" +
				"<div style='clear:both'></div>";
	$("#group-" + index).append(str);			
}

function GetList(name, index)
{
	$.ajax({
		url: 'Resources/PHP/GetList.php',
		dataType: 'text',
		data: { name: name},                         
		success: function(response) {
			var items= "<option value='%' >All</option>";
			var data = JSON.parse(response);
			
			$.each(data,function(index,item) 
			{
				items+="<option value='" + item.ID + "'>" + item.Name + "</option>";
			});
			$("#" + name + "-" + index).html(items); 
		}
	});
}

function GetProductList(index, groupID){
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
		success: function(response) {
			var data = JSON.parse(response);
			if (data.length > 0){
				var table = 	"<table id='product-table-" + index +"'>" +
									"<thead style='display:block'>" +
										"<tr>" +
											"<th style='width: 50px'><input id='check-all-" + index + "' type='checkbox' checked onchange='ToggleAllRowData(" + index +");'></th>" +
											"<th style='width: 750px'>Name</th>" +
											
										"</tr>" +
									"</thead>" +
									"<tbody id='product-list-" + index + "' style='display:block; height: 300px; overflow-y: auto;'>" +
									"</tbody>" +
								"</table>";
				
				$("#product-list-wrapper-" + index).html(table);
				
				var items = "";
				
				$.each(data,function(i,item) 
				{
					
					items+= "<tr>" +
								"<td style='width: 50px'><input id='check-data-" + index + "-" + item.ID + "' name ='check-data-" + index +"' type='checkbox' checked onchange='ToggleRowData(" + index + ");'></td>" +
								"<td style='width: 750px'><span>" + item.FileName  + "</span></td>" +
							"</tr>";
				});
				
				$("#product-list-" + index).html(items);
				
				if (groupID > 0){
					SetSelectedLayer(index, groupID);
				}
				
			} else{
				$("#product-list-wrapper-" + index).html("No data found.");
			}
			$("#loading").hide();
			
		},
		error: function (request, status, error){
			
			$("#loading").hide();
			alert(request.responseText);
		}
	});
	
}


function ToggleRowData(index){
	if($("input[name=check-data-" + index + "]:not(:checked)").length > 0){
		$("#check-all-" + index).prop( "checked", false );
	} else {
		$("#check-all-" + index).prop( "checked", true );
	}
	
	/*
	if($("input[name=check-data-" + index + "]:checked").length > 0){
		$("#values").show();
	} else {
		$("#values").hide();
		$("#charts").hide();
		$("#growth-table").hide();
		$("#export-growth").hide();
	}
	*/
} 

//Select all row to fit the charts
function ToggleAllRowData(index){
	if ($("#check-all-" + index).is(':checked')){
		$("[id^=check-data-" + index + "]").prop( "checked", true );
	} else {
		$("[id^=check-data-" + index + "]").prop( "checked", false );
	}
}

function GetGroupSelection (index){
	var name = $("#group-" + index + "-name").val();
	var type = $("#product_type-" + index).val();
	var idList = "";
	
	$.each($("input[name=check-data-" + index + "]:checked"),function(i,item) {
		var id = item.id.replace("check-data-" + index + "-","");
		idList += id + ";";
	});
	
	idList = idList.slice(0, -1);
	
	return {GroupName: name, Type: type, IDs: idList};
}

function Generate(){
	var project = $("#project").val();
	var name = $("#name").val();
	var center = $("#lat").html() + "," + $("#lng").html();
	var zoom = $("#zoom").html();
	var minZoom = $("#min-zoom").html();
	var maxZoom = $("#max-zoom").html();
	
	var num = $("#group-headers li").length;
	var groups = new Array();
	for (var i = 0; i < num; i++){
		var group = GetGroupSelection(i);
		groups.push(group);
	}

	$.ajax({
		url: "Resources/PHP/Generate.php",
		dataType: 'text',
		data: { 
			pageid: pageID,
			project:project, 
			groups: groups,
			name: name,
			center: center,
			zoom: zoom,
			minZoom: minZoom,
			maxZoom: maxZoom
		},  
		success: function(response) {
			$("#result-link").val(response);
			GetPageList();
			$("#page-info").hide();
			alert("The visualization page has been created successfully.");
			//$("#result").show();
		}	
	});
}

function View(){
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

function EditVisualizationPage(id){
	$.ajax({
		url: "Resources/PHP/Page.php",
		dataType: 'text',
		data: { 
			action: "info",
			id: id
		},  
		success: function(response) {
			var page = JSON.parse(response);
			$("#project").val(page.Project);
			$("#project").trigger("chosen:updated");
			
			GetPageGroups(page.ID);
			$("#name").val(page.Name);
			pageID = page.ID;
			$("#project_chosen").width(350);
			$("#page-info").show();
		}	
	});
}

function GetPageGroups(id){
	$.ajax({
		url: "Resources/PHP/Group.php",
		dataType: 'text',
		data: { 
			pageid: id
		},  
		success: function(response) {
			var groups = JSON.parse(response);
			if (groups.length > 0){
				$("#group-wrapper").html("<div id='groups'><ul id='group-headers'></ul></div>");
				
				$.each(groups,function(index,group) {
					AddGroup();
					setTimeout(function(){
						$("#group-" + index + "-name").val(group.Name);
						$("#product_type-" + index).val(group.Type);
						GetProductList(index, group.ID);
					}, 500); 
					
					
				});
				
			}
		}	
	});
}

function Apply(id){
	$.ajax({
		url: "Resources/PHP/Apply.php",
		dataType: 'text',
		data: { 
			pageid: id
		},  
		success: function(response) {
			//alert("The visualization has been applied. Review: " + response);
			if (response.indexOf("Failed") < 0 ){ //Success
				$("#result-text").text("The visualization has been applied");
			
				$("#dialog-review").dialog({
					resizable: false,
					height: "auto",
					position: { my: "top+50", at: "top+50", of: window },
					width: 400,
					modal: true,
					buttons: {
							"Preview": function() {
								Preview(response);
							}
						}
				});
			} else { //Failed
				$("#result-text").text(response);
			
				$("#dialog-review").dialog({
					resizable: false,
					height: "auto",
					position: { my: "top+50", at: "top+50", of: window },
					width: 400,
					modal: true,
					buttons: {
							"OK": function() {
								$( this ).dialog( "close" );
							}
						}
				});
			}
		}	
	});
}

function ValidURL(str) {
	var pattern = new RegExp('^(https?:\/\/)?'+ // protocol
		'((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|'+ // domain name
		'((\d{1,3}\.){3}\d{1,3}))'+ // OR ip (v4) address
		'(\:\d+)?(\/[-a-z\d%_.~+]*)*'+ // port and path
		'(\?[;&a-z\d%_.~+=-]*)?'+ // query string
		'(\#[-a-z\d_]*)?$','i'); // fragment locater
	if(!pattern.test(str)) {
		alert("Please enter a valid URL.");
		return false;
	} else {
		return true;
	}
}

function SetSelectedLayer(index, groupID){
	$.ajax({
		url: "Resources/PHP/SelectedLayer.php",
		dataType: 'text',
		data: { 
			groupID: groupID
		},  
		success: function(response) {
			var layers = JSON.parse(response);
			if (layers.length > 0){
				$("#check-all-" + index).prop('checked', false);
				ToggleAllRowData(index);
				$.each(layers,function(i,layer) {
					$("#check-data-" + index + "-" + layer.Layer).prop('checked', true);
					console.log("#check-data-" + index + "-" + layer.Layer);
					
				});
				
			}
		}	
	});
}

function AddPage(){
	$("#group-wrapper").html("<div id='groups'><ul id='group-headers'></ul></div>");
	AddGroup();
	$("#project_chosen").width(350);
	$("#name").val($("#project option:selected").text());
	$("#page-info").show();
	
}

function Preview(link){
	var win = window.open(link, '_blank');
	if (win) {
		//Browser has allowed it to be opened
		win.focus();
	} else {
		//Browser has blocked it
		alert('Please allow popups for this website');
	}
}

