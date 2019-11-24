/*
The MIT License (MIT)

Portions Copyright (c) 2015-2019, The OmniDB Team
Portions Copyright (c) 2017-2019, 2ndQuadrant Limited

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
/// Creates new user.
/// </summary>
function newUserConfirm() {

	execAjax('/new_user/',
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

					if (v_usersObject.v_cellChanges.length>0)
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

	if (v_usersObject.v_cellChanges.length==0)
			return;

	var v_unique_rows_changed = [];
	var v_data_changed = [];
	var v_user_id_list = [];

	$.each(v_usersObject.v_cellChanges, function(i, el){
	    if($.inArray(el['rowIndex'], v_unique_rows_changed) === -1) v_unique_rows_changed.push(el['rowIndex']);
	});

	$.each(v_unique_rows_changed, function(i, el){
	    v_data_changed[i] = v_usersObject.ht.getDataAtRow(el);
	    v_user_id_list[i] = v_usersObject.v_user_ids[el];
	});

	var input = JSON.stringify({"p_data": v_data_changed, "p_user_id_list": v_user_id_list});

	execAjax('/save_users/',
			input,
			function() {

				v_usersObject.v_cellChanges = [];
				document.getElementById('div_save_users').style.visibility = 'hidden';
				listUsers();

			},
			null,
			'box');

}

/// <summary>
/// Hides users window.
/// </summary>
function hideUsers() {

	$('#div_users').removeClass('isActive');

	v_usersObject.ht.destroy();

	document.getElementById('div_user_list').innerHTML = '';

}

/// <summary>
/// Retrieving and displaying users.
/// </summary>
function listUsers() {

	execAjax('/get_users/',
			JSON.stringify({}),
			function(p_return) {

				$('#div_users').addClass('isActive');

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Username';
				col.width = '120';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Password';
				col.type = 'password';
				col.width = '120';
				col.hashLength = 10;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Super User';
				col.type = 'checkbox';
				col.checkedTemplate = 1;
        col.uncheckedTemplate = 0;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.renderer = 'html';
				col.readOnly = true;
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_user_list');

				if (v_div_result.innerHTML!='')
					v_usersObject.ht.destroy();

				v_usersObject = new Object();
				v_usersObject.v_user_ids = p_return.v_data.v_user_ids;
				v_usersObject.v_cellChanges = [];

				var container = v_div_result;
				v_usersObject.ht = new Handsontable(container,
													{
														licenseKey: 'non-commercial-and-evaluation',
														data: p_return.v_data.v_data,
														columns : columnProperties,
														colHeaders : true,
														manualColumnResize: true,
														maxRows: p_return.v_data.v_data.length,
														fillHandle:false,
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

														        	v_usersObject.v_cellChanges.push(cellChange);

														            document.getElementById('div_save_users').style.visibility = 'visible';

														        }
														    });

														},
														afterRender: function () {

														    $.each(v_usersObject.v_cellChanges, function (index, element) {
														        var cellChange = element;
														        var rowIndex = cellChange['rowIndex'];
														        var columnIndex = cellChange['columnIndex'];
														        var cell = v_usersObject.ht.getCell(rowIndex, columnIndex);
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
