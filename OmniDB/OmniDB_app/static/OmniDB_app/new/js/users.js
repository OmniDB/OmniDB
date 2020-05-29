/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Creates new user.
/// </summary>
function newUserConfirm() {

	execAjax('/new_user/',
			JSON.stringify({}),
			function(p_return) {
				listUsers(true);
			},
			null,
			'box');

}

/// <summary>
/// Displays question to create new user.
/// </summary>
function newUser() {

	if (v_usersObject.v_cellChanges.length>0)
		showConfirm2('There are changes on the users list, would you like to save them?',
					function() {

						saveUsers();
						newUserConfirm();

					},
					function() {

						newUserConfirm();

					});
	else
		newUserConfirm();

}

/// <summary>
/// Removes specific user.
/// </summary>
/// <param name="p_index">Connection index in the connection list.</param>
function removeUserConfirm(p_id) {

	var input = JSON.stringify({"p_id": p_id});

	execAjax('/remove_user/',
			input,
			function(p_return) {
				document.getElementById('div_save_users').style.visibility = 'hidden';
				listUsers(true);
			},
			null,
			'box');

}

/// <summary>
/// Displays question to remove specific user.
/// </summary>
/// <param name="p_id">User ID.</param>
function removeUser(p_id) {

	showConfirm('Are you sure you want to remove this user?',
	            function() {

								removeUserConfirm(p_id);

					// if (v_usersObject.v_cellChanges.length>0)
					// showConfirm2('There are changes on the users list, would you like to save them?',
					//             function() {
					//
					//             	saveUsers();
					//             	removeUserConfirm(p_id);
					//
					//             },
					//             function() {
					//
					//             	removeUserConfirm(p_id);
					//
					//             });
					// else
					// 	removeUserConfirm(p_id);

	});

}

/// <summary>
/// Saves all changes in the user list.
/// </summary>
function saveUsers() {

	if (v_usersObject.v_cellChanges.length==0)
			return;

	var v_unique_rows_changed = [];
	var v_data_changed = [];
	var v_user_id_list = [];

	$.each(v_usersObject.v_cellChanges, function(i, el){
	    if($.inArray(el['rowIndex'], v_unique_rows_changed) === -1) v_unique_rows_changed.push(el['rowIndex']);
	});

	$.each(v_unique_rows_changed, function(i, el){
	    // v_data_changed[i] = v_usersObject.ht.getDataAtRow(el);
			v_data_changed[i] = v_usersObject.v_cellChanges[i].p_data;
	    v_user_id_list[i] = v_usersObject.v_user_ids[el];
	});
	var input = JSON.stringify({"p_data": v_data_changed, "p_user_id_list": v_user_id_list});

	console.log(input);

	execAjax('/save_users/',
			input,
			function() {

				v_usersObject.v_cellChanges = [];
				document.getElementById('div_save_users').style.visibility = 'hidden';
				listUsers(true);

			},
			null,
			'box');

}

/// <summary>
/// Hides users window.
/// </summary>
function hideUsers() {

	$('#div_users').removeClass('isActive');

	// v_usersObject.ht.destroy();

	document.getElementById('div_user_list').innerHTML = '';

}

$('#modal_users').on('shown.bs.modal', function (e) {

  getUsers();

});

function changeUser(event, p_row_index, p_col_index) {
	var v_user_id = v_usersObject.v_user_ids[p_row_index];
	var v_user_is_superuser = (document.getElementById("user_item_superuser_" + p_row_index).checked) ? 1 : 0;
	var p_data_template = [
		document.getElementById("user_item_username_" + p_row_index).value,
		document.getElementById("user_item_password_" + p_row_index).value,
		v_user_is_superuser,
		"<i title=\"Remove User\" class='fas fa-times action-grid action-close' onclick='removeUser(\"" + v_user_id + "\")'></i>"
	];

	var cellChange = {
			'rowIndex': p_row_index,
			'columnIndex': p_col_index,
			'p_data': p_data_template
	};
	v_usersObject.v_cellChanges.push(cellChange);
	document.getElementById('div_save_users').style.visibility = 'visible';

	$('omnidb__user-list__item--changed').removeClass('omnidb__user-list__item--changed');
	for (var i = 0; i < v_usersObject.v_cellChanges.length; i++) {
		$('#omnidb_user_item_' + i).addClass('omnidb__user-list__item--changed');
	}

	console.log(v_usersObject);
}

function getUsers() {

  execAjax('/get_users/',
			JSON.stringify({}),
			function(p_return) {

				v_usersObject = new Object();
				v_usersObject.v_user_ids = p_return.v_data.v_user_ids;
				v_usersObject.v_cellChanges = [];
				v_usersObject.list = p_return.v_data.v_data;

				console.log(p_return.v_data.v_data);
				var v_user_list_data = p_return.v_data.v_data;
				var v_user_list_element = document.createElement('div');
				v_user_list_element.classList = ["omnidb__user-list"];
				var v_user_list_html =
				"<form class='d-none' autofill='false' onsubmit='(event)=>{event.preventDefault();};'>" +
					"<input id='fake_username' type='text' placeholder='User name' value=''>" +
					"<input id='fake_password' type='password' placeholder='Password' value=''>" +
					"<button type='submit' disabled aria-hidden='true'></button>" +
				"</form>" +
				"<form class='omnidb__user-list__form' autofill='false' autocomplete='disabled'>" +
					"<input tabIndex='-1' style='opacity:0;height:0px;overflow:hidden;pointer-events:none;' autofill='false' autocomplete='disabled' name='no-autofill' id='no-autofill-autofill-name' type='text' class='m-0 p-0' placeholder='Username' value=''>" +
					"<input tabIndex='-1' style='opacity:0;height:0px;overflow:hidden;pointer-events:none;' autofill='false' autocomplete='disabled' name='no-autofill' id='no-autofill-password' type='password' class='m-0 p-0' placeholder='Password' value=''>" +
					"<div class='form-inline mb-4'>" +
						"<h5 class='mr-2'>Select an user</h5>" +
						"<select id='omnidb_user_select' onchange='renderSelectedUser(event)' class='form-control'>" +
						"<option value='' selected> </option>";
						for (var i = 0; i < v_user_list_data.length; i++) {
							var v_user_item = v_user_list_data[i];
							v_user_list_html +=
							"<option value='" + i + "'>" + v_user_item[0] + "</option>";
						}
						v_user_list_html +=
						"</select>" +
						"<button type='button' class='btn btn-primary ml-2' onclick='newUser()'><i class='fas fa-user-plus'></i><span class='ml-2'>Add new user</span></button>" +
					"</div>" +
					"<div id='omnidb_user_content' class='row'>" +
					"</div>" +
					"<button type='submit' disabled style='display: none' aria-hidden='true'></button>" +
				"</div>";
				v_user_list_element.innerHTML = v_user_list_html;

				$('#div_users').addClass('isActive');

				window.scrollTo(0,0);

				// var columnProperties = [];
				//
				// var col = new Object();
				// col.title =  'Username';
				// col.width = '120';
				// columnProperties.push(col);
				//
				// var col = new Object();
				// col.title =  'Password';
				// col.type = 'password';
				// col.width = '120';
				// col.hashLength = 10;
				// columnProperties.push(col);
				//
				// var col = new Object();
				// col.title =  'Super User';
				// col.type = 'checkbox';
				// col.checkedTemplate = 1;
        // col.uncheckedTemplate = 0;
				// columnProperties.push(col);
				//
				// var col = new Object();
				// col.title =  'Actions';
				// col.renderer = 'html';
				// col.readOnly = true;
				// columnProperties.push(col);

				var v_div_result = document.getElementById('div_user_list');

				var container = v_div_result;
				// v_usersObject.ht = new Handsontable(container,
				// 									{
				// 										licenseKey: 'non-commercial-and-evaluation',
				// 										data: p_return.v_data.v_data,
				// 										columns : columnProperties,
				// 										colHeaders : true,
				// 										manualColumnResize: true,
				// 										maxRows: p_return.v_data.v_data.length,
				// 										fillHandle:false,
        //                     stretchH: 'all',
				// 										beforeChange: function (changes, source) {
				//
				// 										    if (!changes)
				// 										        return;
				//
				// 										    $.each(changes, function (index, element) {
				// 										        var change = element;
				// 										        var rowIndex = change[0];
				// 										        var columnIndex = change[1];
				// 										        var oldValue = change[2];
				// 										        var newValue = change[3];
				//
				// 										        var cellChange = {
				// 										            'rowIndex': rowIndex,
				// 										            'columnIndex': columnIndex
				// 										        };
				// 										        if(oldValue != newValue){
				//
				// 										        	v_usersObject.v_cellChanges.push(cellChange);
				//
				// 									            document.getElementById('div_save_users').style.visibility = 'visible';
				//
				// 										        }
				// 										    });
				//
				// 										},
				// 										afterRender: function () {
				//
				// 										    $.each(v_usersObject.v_cellChanges, function (index, element) {
				// 										        var cellChange = element;
				// 										        var rowIndex = cellChange['rowIndex'];
				// 										        var columnIndex = cellChange['columnIndex'];
				// 										        var cell = v_usersObject.ht.getCell(rowIndex, columnIndex);
				// 										        var foreColor = '#000';
				// 										        var backgroundColor = 'rgb(255, 251, 215)';
				// 										        cell.style.color = foreColor;
				// 										        cell.style.background = backgroundColor;
				// 										    });
				//
				// 										},
				// 										cells: function (row, col, prop) {
				//
				// 										    var cellProperties = {};
				// 										    cellProperties.renderer = whiteHtmlRenderer;
				// 										    return cellProperties;
				//
				// 										}
				//
				// 									});

					container.appendChild(v_user_list_element);
					$('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips
          endLoading();
				},
				null,
				'box');

}

/// <summary>
/// Retrieving and displaying users.
/// </summary>
function listUsers(p_refresh) {

  startLoading();

  document.getElementById('div_save_users').style.visibility = 'hidden';

  var v_div_result = document.getElementById('div_user_list');

  // if (v_div_result.innerHTML!='')
  //   v_usersObject.ht.destroy();

	if (v_div_result.innerHTML!='')
    v_div_result.innerHTML = '';

  if (p_refresh==null)
    $('#modal_users').modal();
  else
    getUsers();


}

/// <summary>
/// Rendering selected user.
/// </summary>
function renderSelectedUser(event) {
	var v_index = event.target.value;
	for (var i = 0; i < v_usersObject.list.length; i++) {
		var v_user_item = v_usersObject.list[i];
		var v_superuser_checked = (v_user_item[2] === 1) ? 'checked' : '';
		var v_user_div_content = document.getElementById('omnidb_user_content');
		if (i == v_index) {
			v_user_div_content.innerHTML =
			"<div class='col-12 mb-4'>" +
			"<div id='omnidb_user_item_" + i + "' class='omnidb__user-list__item card'>" +
			"<div class='d-flex align-items-center'>" +
				"<div class='input-group mb-2'>" +
					"<div class='input-group-prepend'>" +
						"<label for='user_item_username_" + i  + "' type='button' class='input-group-text'>" +
							"<i class='fas fa-user'></i>" +
						"</label>" +
					"</div>" +
					"<input autofill='false' autocomplete='disabled' name='notChromeUsername' id='user_item_username_" + i  + "' type='text' class='form-control my-0' placeholder='User name' value='" + v_user_item[0] + "' onchange='changeUser(event," + i + ",0)'>" +
				"</div>" +
				"<span class='ml-2'>Superuser?</span>" +
				"<div class='ml-2 mb-2'>" +
					// "<input id='user_item_superuser_" + i  + "' type='checkbox' " + v_superuser_checked + ">" +
					// "<label for='user_item_superuser_" + i  + "' class='ml-2'>superuser</label>" +
					"<div class='omnidb__switch mr-2' data-toggle='tooltip' data-placement='bottom' data-html='true' title='<h5>Toggle superuser status. To enable again, simply turn the switch on.</h5>'>" +
						"<input type='checkbox' id='user_item_superuser_" + i  + "' class='omnidb__switch--input' " + v_superuser_checked + " onchange='changeUser(event," + i + ",2)'>" +
						"<label for='user_item_superuser_" + i  + "' class='omnidb__switch--label'><span><i class='fas fa-star'></i></span></label>" +
					"</div>" +
				"</div>" +
			"</div>" +
			"<div class='input-group w-100 mb-2'>" +
			"<div class='input-group-prepend'>" +
			"<label for='user_item_password_" + i  + "' type='button' class='input-group-text'>" +
			"<i class='fas fa-key'></i>" +
			"</label>" +
			"</div>" +
			"<input autofill='false' autocomplete='disabled' name='new-password' id='user_item_password_" + i  + "' type='password' class='form-control my-0' placeholder='New password' value='" + v_user_item[1] + "' onchange='changeUser(event," + i + ",1)'>" +
			"</div>" +
			"<span class='mr-2 text-danger omnidb__user-list__close'>" +
			v_user_item[3] +
			"</span>" +
			"</div>" +
			"</div>";
		}
	}
	if (v_index == "") {
		v_user_div_content.innerHTML = "";
	}
}
