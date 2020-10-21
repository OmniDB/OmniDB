/*
This file is part of OmniDB.
OmniDB is open-source software, distributed "AS IS" under the MIT license in the hope that it will be useful.

The MIT License (MIT)

Portions Copyright (c) 2015-2020, The OmniDB Team
Portions Copyright (c) 2017-2020, 2ndQuadrant Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

/// <summary>
/// Creates new users.
/// </summary>
function newUserConfirm() {

	execAjax('/new_user/',
			JSON.stringify({'p_data':window.newUsersObject.newUsers}),
			function(p_return) {

				v_usersObject.v_cellChanges = [];
				window.newUsersObject.newUsers = [];
				if (v_usersObject.v_cellChanges.length === 0 && window.newUsersObject.newUsers.length === 0)
					document.getElementById('div_save_users').style.visibility = 'hidden';
				listUsers(true);
			},
			null,
			'box');

}

/// <summary>
/// Add a virtual new user with pending information.
/// </summary>
function newUser() {
	var v_index = 0;
	if (window.newUsersObject.newUsers.length > 0) {
		v_index = window.newUsersObject.newUsers.length
		window.newUsersObject.newUsers.push(["","",0]);
	}
	else {
		v_index = 0
		window.newUsersObject.newUsers = [["","",0]];
	}

	listUsers(true,{adding_user:true});
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
				if (v_usersObject.v_cellChanges.length === 0 && window.newUsersObject.newUsers.length === 0)
					document.getElementById('div_save_users').style.visibility = 'hidden';
				listUsers(true);
			},
			null,
			'box');

}

/// <summary>
/// Displays question to remove specific user and removes if accepted.
/// </summary>
/// <param name="p_id">User ID.</param>
function removeUser(p_id) {

	showConfirm('Are you sure you want to remove this user?',
  function() {
		removeUserConfirm(p_id);
	});

}

/// <summary>
/// Undo adding specific new user.
/// </summary>
/// <param name="p_index">Connection index in the connection list.</param>
function removeNewUserConfirm(p_index) {

	if (window.newUsersObject.newUsers.length == 1)
		window.newUsersObject.newUsers = [];
	else if (p_index == 0)
		window.newUsersObject.newUsers.shift();
	else if (p_index + 1 == window.newUsersObject.newUsers.length)
		window.newUsersObject.newUsers.pop();
	else
		window.newUsersObject.newUsers.splice(p_index,1);
	listUsers(true);

}

/// <summary>
/// Undo add new user from virtual users
/// </summary>
/// <param name="p_id">User ID.</param>
function removeNewUser(p_index) {

	showConfirm('Are you sure you want to undo adding this user?',
  function() {
		removeNewUserConfirm(p_index);
	});

}

/// <summary>
/// Saves all changes in the user list, then calls to save new users.
/// </summary>
function saveUsers() {

	if (v_usersObject.v_cellChanges.length==0 && window.newUsersObject.newUsers.length==0)
			return;

	var v_unique_rows_changed = [];
	var v_data_changed = [];
	var v_user_id_list = [];

	$.each(v_usersObject.v_cellChanges, function(i, el){
	    if ($.inArray(el['rowIndex'], v_unique_rows_changed) === -1) {
				v_unique_rows_changed.push(el['rowIndex']);
			}
	});

	$.each(v_unique_rows_changed, function(i, el){
			v_data_changed[i] = v_usersObject.v_cellChanges[i].p_data;
	    v_user_id_list[i] = v_usersObject.v_user_ids[el];
	});

	var v_data = {
		edited: v_data_changed,
		new: window.newUsersObject.newUsers
	}
	var input = JSON.stringify({"p_data": v_data, "p_user_id_list": v_user_id_list});

	execAjax('/save_users/',
			input,
			function() {

				// newUserConfirm();
				v_usersObject.v_cellChanges = [];
				window.newUsersObject.newUsers = [];
				if (v_usersObject.v_cellChanges.length === 0 && window.newUsersObject.newUsers.length === 0) {
					document.getElementById('div_save_users').style.visibility = 'hidden';
				}
				listUsers(true, {users_update: v_data});

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
		"<i title=\"Remove User\" class='fas fa-times action-grid action-close text-danger' onclick='removeUser(\"" + v_user_id + "\")'></i>"
	];

	var cellChange = {
			'rowIndex': p_row_index,
			'columnIndex': p_col_index,
			'p_data': p_data_template
	};
	v_usersObject.v_cellChanges.push(cellChange);
	document.getElementById('div_save_users').style.visibility = 'visible';

	$('.omnidb__user-list__item--changed').removeClass('omnidb__user-list__item--changed');
	for (var i = 0; i < v_usersObject.v_cellChanges.length; i++) {
		var v_row_value = v_usersObject.v_cellChanges[i].rowIndex;
		$('#omnidb_user_item_' + v_row_value).addClass('omnidb__user-list__item--changed');
		$('#omnidb_user_select option[value="' + v_row_value + '"]').addClass('bg-warning');
	}
}

function changeNewUser(event, p_row_index, p_col_index) {
	var v_user_is_superuser = (document.getElementById("new_user_item_superuser_" + p_row_index).checked) ? 1 : 0;
	var p_data_template = [
		document.getElementById("new_user_item_username_" + p_row_index).value,
		document.getElementById("new_user_item_password_" + p_row_index).value,
		v_user_is_superuser,
		"<i title=\"Remove User\" class='fas fa-times action-grid action-close text-danger' onclick='removeNewUser(\"" + p_row_index + "\")'></i>"
	];

	window.newUsersObject.newUsers[p_row_index] = p_data_template;

	var v_render_index = parseInt(v_usersObject.list.length) + parseInt(p_row_index);
	var v_event = {target:{value:v_render_index}};

	renderSelectedUser(v_event);

	document.getElementById('div_save_users').style.visibility = 'visible';

}

function getUsers(p_options = false) {

	if (p_options.adding_user) {

		var v_new_value = v_usersObject.list.length + window.newUsersObject.newUsers.length - 1;
		$('#omnidb_user_select').append(new Option('(pending info)', v_new_value));
		$('#omnidb_user_select option:last-child').addClass('bg-success');
		$('#omnidb_user_select option:last-child').trigger('change');
		$('#omnidb_user_select').val(v_new_value);

		endLoading();

	}
	else {

		if (!window.newUsersObject) {
			window.newUsersObject = new Object();
		}
		if (window.newUsersObject.newUsers == undefined) {
			window.newUsersObject.newUsers = [];
		}

		execAjax('/get_users/',
				JSON.stringify({}),
				function(p_return) {

					v_usersObject = new Object();
					v_usersObject.v_user_ids = p_return.v_data.v_user_ids;
					v_usersObject.v_cellChanges = [];
					v_usersObject.list = p_return.v_data.v_data;


					var v_users_update_html = '';
					if (p_options) {
						if (p_options.users_update) {
							if (p_options.users_update.edited.length > 0) {
								v_users_update_html +=
								'<div class="card p-4 mx-auto">' +
								'<div><h5>Edited Users:</h5></div>' +
								'<ul class="pl-4">';
								for (let i = 0; i < p_options.users_update.edited.length; i++) {
									v_users_update_html += '<li class="mt-2"> - ' + p_options.users_update.edited[i][0] + '</li>';
								}
								v_users_update_html +=
								'</ul>' +
								'</div>';
							}
							if (p_options.users_update.new.length > 0) {
								v_users_update_html +=
								'<div class="card p-4 mx-auto">' +
								'<div><h5>New Users:</h5></div>' +
								'<ul class="pl-4">';
								for (let i = 0; i < p_options.users_update.new.length; i++) {
									v_users_update_html += '<li class="mt-2"> - ' + p_options.users_update.new[i][0] + '</li>';
								}
								v_users_update_html +=
								'</ul>' +
								'</div>';
							}
						}
					}



					var v_user_list_data = p_return.v_data.v_data;
					var v_user_list_element = document.createElement('div');
					v_user_list_element.classList = ["omnidb__user-list"];
					var v_user_count = 0;
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
							"<select id='omnidb_user_select' onchange='renderSelectedUser(event)' class='form-control'>";
							if (p_options.focus_last)
								v_user_list_html += "<option value=''> </option>";
							else
								v_user_list_html += "<option value='' selected> </option>";
							for (var i = 0; i < v_user_list_data.length; i++) {
								var v_user_item = v_user_list_data[i];
								var v_user_is_superuser = (v_user_item[2] === 1) ? ' (superuser)' : '';
								v_user_list_html +=
								"<option value='" + i + "'>" + v_user_item[0] + v_user_is_superuser + "</option>";
								v_user_count++;
							}
							for (var i = 0; i < window.newUsersObject.newUsers.length; i++) {
								var v_user_item = window.newUsersObject.newUsers[i];
								var v_user_is_superuser = (v_user_item[2] === 1) ? ' (superuser)' : '';
								var v_user_item_index = parseInt(v_user_count) + parseInt(i);
								var v_user_item_name = (v_user_item[0] === "") ? '(pending info)' : v_user_item[0] + v_user_is_superuser + ' (pending save)';
								var v_user_is_selected = (p_options.focus_last && i + 1 == window.newUsersObject.newUsers.length) ? ' selected ' : '';
								v_user_list_html +=
								"<option class='bg-warning' value='" + v_user_item_index + "' " + v_user_is_selected + ">" + v_user_item_name + "</option>";
							}
							v_user_list_html +=
							"</select>" +
							"<button id='omnidb_utilities_menu_btn_new_user' type='button' class='btn omnidb__theme__btn--primary ml-2' onclick='newUser()'><i class='fas fa-user-plus'></i><span class='ml-2'>Add new user</span></button>" +
						"</div>" +
						"<div id='omnidb_user_content' class='row'>" +
							v_users_update_html +
						"</div>" +
						"<div class='text-center'>" +
							"<button type='button' id='div_save_users' class='btn btn-success ml-1' style='visibility: hidden;' onclick='saveUsers()'>Save</button>" +
						"</div>" +
						"<button type='submit' disabled style='display: none' aria-hidden='true'></button>" +
					"</div>";
					v_user_list_element.innerHTML = v_user_list_html;

					$('#div_users').addClass('isActive');

					window.scrollTo(0,0);

					var v_div_result = document.getElementById('div_user_list');
					var container = v_div_result;
					container.appendChild(v_user_list_element);

					if (p_options) {
						if (p_options.focus_last) {
							setTimeout(function(){
								$('#omnidb_user_select option:last-child').trigger('change');
							},300);
						}
					}
					if (v_usersObject.v_cellChanges.length > 0 || window.newUsersObject.newUsers.length > 0)
						document.getElementById('div_save_users').style.visibility = 'visible';
					$('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips
	        endLoading();
				},
				null,
				'box');
	}


}

/// <summary>
/// Retrieving and displaying users.
/// </summary>
function listUsers(p_refresh,p_options = false) {

  startLoading();

  var v_save_button = document.getElementById('div_save_users');
	if (v_save_button !== null) {
		if (v_usersObject.v_cellChanges.length === 0 && window.newUsersObject.newUsers.length === 0) {
			document.getElementById('div_save_users').style.visibility = 'hidden';
		}
	}

  var v_div_result = document.getElementById('div_user_list');

	if (v_div_result.innerHTML!='' && !p_options.adding_user) {
		v_div_result.innerHTML = '';
	}

  if (p_refresh==null) {
		$('#modal_users').modal();
	}
  else {
		getUsers(p_options);
	}
}

/// <summary>
/// Rendering selected user.
/// </summary>
function renderSelectedUser(event) {
	var v_index = event.target.value;
	var v_user_div_content = document.getElementById('omnidb_user_content');
	if (v_index == "") {
		v_user_div_content.innerHTML = "<div class='col-12 text-center'><h5 class='my-4'>No users selected, select an user or click add new user.</h5></div>";
	}
	else {
		var v_user_count = 0;
		for (var i = 0; i < v_usersObject.list.length; i++) {
			var v_user_item = v_usersObject.list[i];
			var v_superuser_checked = (v_user_item[2] === 1) ? 'checked' : '';
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
			v_user_count++;
		}
		for (var i = 0; i < window.newUsersObject.newUsers.length; i++) {
			var v_user_item = window.newUsersObject.newUsers[i];
			var v_superuser_checked = (v_user_item[2] === 1) ? 'checked' : '';
			var v_user_item_index = parseInt(v_user_count) + parseInt(i);
			var v_user_div_content = document.getElementById('omnidb_user_content');
			if (v_user_item_index == v_index) {
				v_user_div_content.innerHTML =
				"<div class='col-12 mb-4'>" +
				"<div id='omnidb_user_item_" + i + "' class='omnidb__user-list__item card'>" +
				"<div class='d-flex align-items-center'>" +
					"<div class='input-group mb-2'>" +
						"<div class='input-group-prepend'>" +
							"<label for='new_user_item_username_" + i  + "' type='button' class='input-group-text'>" +
								"<i class='fas fa-user'></i>" +
							"</label>" +
						"</div>" +
						"<input autofill='false' autocomplete='off' name='off' id='new_user_item_username_" + i  + "' type='text' class='form-control my-0' placeholder='User name' value='" + v_user_item[0] + "' onchange='changeNewUser(event," + i + ",0)'>" +
					"</div>" +
					"<span class='ml-2'>Superuser?</span>" +
					"<div class='ml-2 mb-2'>" +
						"<div class='omnidb__switch mr-2' data-toggle='tooltip' data-placement='bottom' data-html='true' title='<h5>Toggle superuser status. To enable again, simply turn the switch on.</h5>'>" +
							"<input type='checkbox' id='new_user_item_superuser_" + i  + "' class='omnidb__switch--input' " + v_superuser_checked + " onchange='changeNewUser(event," + i + ",2)'>" +
							"<label for='new_user_item_superuser_" + i  + "' class='omnidb__switch--label'><span><i class='fas fa-star'></i></span></label>" +
						"</div>" +
					"</div>" +
				"</div>" +
				"<div class='input-group w-100 mb-2'>" +
				"<div class='input-group-prepend'>" +
				"<label for='new_user_item_password_" + i  + "' type='button' class='input-group-text'>" +
				"<i class='fas fa-key'></i>" +
				"</label>" +
				"</div>" +
				"<input autofill='false' autocomplete='off' name='off' id='new_user_item_password_" + i  + "' type='password' class='form-control my-0' placeholder='New password' value='" + v_user_item[1] + "' onchange='changeNewUser(event," + i + ",1)'>" +
				"</div>" +
				"<span class='mr-2 text-danger omnidb__user-list__close'>" +
					"<i title=\"Remove User\" class='fas fa-times action-grid action-close text-danger' onclick='removeNewUser(\"" + i + "\")'></i>" +
				"</span>" +
				"</div>" +
				"</div>";
			}
		}
	}

}
