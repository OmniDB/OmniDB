/*
Copyright 2016 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Startup function.
/// </summary>
$(function() {

	listUsers();
	checkSessionMessage();

});

/// <summary>
/// Opens admin config window.
/// </summary>
function showConfigUser() {

	document.getElementById('txt_confirm_new_pwd').value = '';
	document.getElementById('txt_new_pwd').value = '';

	$('#div_config_user').show();

}

/// <summary>
/// Hides admin config window.
/// </summary>
function hideConfigUser() {
	
	$('#div_config_user').hide();

}

/// <summary>
/// Saves admin config.
/// </summary>
function saveConfigUser() {

	var v_confirm_pwd = document.getElementById('txt_confirm_new_pwd');
	var v_pwd = document.getElementById('txt_new_pwd');

	if ((v_confirm_pwd.value!='' || v_pwd.value!='') && (v_pwd.value!=v_confirm_pwd.value))
		showAlert('New Password and Confirm New Password fields do not match.');
	else {

		var input = JSON.stringify({"p_pwd" : v_pwd.value});

		execAjax('Users.aspx/SaveConfigUser',
				input,
				function(p_return) {

					$('#div_config_user').hide();
					showAlert('Password changed.');

				});

	}

}

/// <summary>
/// Creates new user.
/// </summary>
function newUserConfirm() {

	execAjax('Users.aspx/NewUser',
			JSON.stringify({}),
			function(p_return) {
				listUsers();
			},
			null,
			'box');

}

/// <summary>
/// Displays question to create new user.
/// </summary>
function newUser() {

	if (v_users_data.v_cellChanges.length>0)
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

	execAjax('Users.aspx/RemoveUser',
			input,
			function(p_return) {
				document.getElementById('div_save').style.visibility = 'hidden';
				listUsers();
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

					if (v_users_data.v_cellChanges.length>0)
					showConfirm2('There are changes on the users list, would you like to save them?',
					            function() {

					            	saveUsers();
					            	removeUserConfirm(p_id);

					            },
					            function() {

					            	removeUserConfirm(p_id);

					            });
					else
						removeUserConfirm(p_id);

	            });

}

/// <summary>
/// Saves all changes in the user list.
/// </summary>
function saveUsers() {

	if (v_users_data.v_cellChanges.length==0)
			return;

	var v_unique_rows_changed = [];
	var v_data_changed = [];
	var v_user_id_list = [];

	$.each(v_users_data.v_cellChanges, function(i, el){
	    if($.inArray(el['rowIndex'], v_unique_rows_changed) === -1) v_unique_rows_changed.push(el['rowIndex']);
	});

	$.each(v_unique_rows_changed, function(i, el){
	    v_data_changed[i] = v_users_data.ht.getDataAtRow(el);
	    v_user_id_list[i] = v_users_data.v_user_ids[el];
	});

	var input = JSON.stringify({"p_data": v_data_changed, "p_user_id_list": v_user_id_list});

	execAjax('Users.aspx/SaveUsers',
			input,
			function() {

				v_users_data.v_cellChanges = [];
				document.getElementById('div_save').style.visibility = 'hidden';
				listUsers();

			},
			null,
			'box');

}

/// <summary>
/// Retrieving and displaying users.
/// </summary>
function listUsers() {

	execAjax('Users.aspx/GetUsers',
			JSON.stringify({}),
			function(p_return) {

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Username';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Password';
				col.type = 'password';
				col.hashLength = 10;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.renderer = 'html';
				col.readOnly = true;
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_user_list');

				if (v_div_result.innerHTML!='')
					v_users_data.ht.destroy();

				v_users_data = new Object();
				v_users_data.v_user_ids = p_return.v_data.v_user_ids;
				v_users_data.v_cellChanges = [];

				var container = v_div_result;
				v_users_data.ht = new Handsontable(container,
													{
														data: p_return.v_data.v_data,
														columns : columnProperties,
														colHeaders : true,
														manualColumnResize: true,
														maxRows: p_return.v_data.v_data.length,
														beforeChange: function (changes, source) {

														    if (!changes)
														        return;
														    
														    $.each(changes, function (index, element) {
														        var change = element;
														        var rowIndex = change[0];
														        var columnIndex = change[1];
														        var oldValue = change[2];
														        var newValue = change[3];

														        var cellChange = {
														            'rowIndex': rowIndex,
														            'columnIndex': columnIndex
														        };
														        if(oldValue != newValue){

														        	v_users_data.v_cellChanges.push(cellChange);

														            document.getElementById('div_save').style.visibility = 'visible';

														        }
														    });

														},
														afterRender: function () {

														    $.each(v_users_data.v_cellChanges, function (index, element) {
														        var cellChange = element;
														        var rowIndex = cellChange['rowIndex'];
														        var columnIndex = cellChange['columnIndex'];
														        var cell = v_users_data.ht.getCell(rowIndex, columnIndex);
														        var foreColor = '#000';
														        var backgroundColor = 'rgb(255, 251, 215)';
														        cell.style.color = foreColor;
														        cell.style.background = backgroundColor;
														    });

														},
														cells: function (row, col, prop) {

														    var cellProperties = {};
														    if (row % 2 == 0)
																cellProperties.renderer = blueHtmlRenderer;
														    return cellProperties;

														}

													});
				},
				null,
				'box');

}