/*
Copyright 2015-2019 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Startup function.
/// </summary>
$(function () {
	v_connections_data = new Object();
  v_connections_data.technologies = null;
  v_connections_data.card_list = [];
  v_connections_data.current_id = -1;
});

function startConnectionManagement() {
  getGroups();
  showConnectionList(true,true);
}


function showConnectionList(p_open_modal, p_change_group) {

	var v_conn_id_list = [];

	for (var i=0; i < v_connTabControl.tabList.length; i++) {
		var v_tab = v_connTabControl.tabList[i];
		if (v_tab.tag && v_tab.tag.mode=='connection')
			v_conn_id_list.push(v_tab.tag.selectedDatabaseIndex);
		else if (v_tab.tag && v_tab.tag.mode=='outer_terminal' && v_tab.tag.connId!=null)
			v_conn_id_list.push( v_tab.tag.connId);
	}

	var input = JSON.stringify({"p_conn_id_list": v_conn_id_list});

	execAjax('/get_connections_new/',
			input,
			function(p_return) {

        v_connections_data.card_list = [];
        v_connections_data.technologies = p_return.v_data.v_technologies;

        //Building connection cards
				var v_container = null;
        var v_container = document.createElement('div');
        v_container.className = 'container-fluid';

        var v_row = null;

        var v_target_div = document.getElementById('connection_card_list');

        var v_row = document.createElement('div');
        v_row.className = 'row';


        for (var i=0; i<p_return.v_data.v_conn_list.length; i++) {
          var v_conn_obj = p_return.v_data.v_conn_list[i];

          var v_col_div = document.createElement('div');
          v_col_div.className = 'omnidb__connections__cols';
          v_row.appendChild(v_col_div);

          var v_card_div = document.createElement('div');
          v_card_div.className = 'card omnidb__connections__card';
          v_col_div.appendChild(v_card_div);

          var v_cover_div = document.createElement('div');
          v_cover_div.className = 'connection-card-cover';
          v_cover_div.style.display = 'none';
          v_card_div.appendChild(v_cover_div);

          var v_checkbox = document.createElement('input');
          v_checkbox.className = 'connection-card-checkbox';
          v_checkbox.type="checkbox";
          v_cover_div.appendChild(v_checkbox);

          v_cover_div.onclick = (function(checkbox) {
              return function() {
                if(checkbox.checked == false)
                  checkbox.checked = true;
                else
                  checkbox.checked = false;
              };
          }(v_checkbox));



          var v_card_body_div = document.createElement('div');
          v_card_body_div.className = 'card-body';
          v_card_div.appendChild(v_card_body_div);

          if (v_conn_obj.technology=='terminal')
            v_card_body_div.innerHTML +=
            '<h5 class="card-title"><i class="fas fa-terminal"></i> ' + v_conn_obj.alias + '</h5>' +
            '<h6 class="card-subtitle mb-2 text-muted"><i title="Tunnel" class="fas fa-archway"></i> ' + v_conn_obj.tunnel.user + '@' + v_conn_obj.tunnel.server + ':' + v_conn_obj.tunnel.port + '</h6>';
          else {
            var v_tunnel = '';
            var v_details = '';
            if (v_conn_obj.conn_string!='')
              v_details = '<h6 class="card-subtitle mb-2 text-muted"><i title="Connection String" class="fas fa-quote-left"></i> ' + v_conn_obj.conn_string + '</h6>';
            else
              v_details =
              '      <h6 class="card-subtitle mb-2 text-muted">' + v_conn_obj.server + ':' + v_conn_obj.port + '</h6>' +
              '      <p class="card-text">' + v_conn_obj.user + '@' + v_conn_obj.service + '</p>';
            if (v_conn_obj.tunnel.enabled==true)
              v_tunnel = '<h6 class="card-subtitle mb-2 text-muted"><i title="Tunnel" class="fas fa-archway"></i> ' + v_conn_obj.tunnel.user + '@' + v_conn_obj.tunnel.server + ':' + v_conn_obj.tunnel.port + '</h6>';

            v_card_body_div.innerHTML +=
            '<h5 class="card-title"><i class="icon_tree node-' + v_conn_obj.technology + '"></i>' + v_conn_obj.alias + '</h5>' +
            v_tunnel +
            v_details;
          }

					var v_button_select = document.createElement('button');
					v_button_select.className = 'btn btn-success btn-sm omnidb__connections__btn--select';
					v_button_select.title = "Select";
					if (v_conn_obj.locked==true)
						v_button_select.setAttribute("disabled",true);
					v_button_select.innerHTML = '<svg width="15px" height="160px" viewBox="0 0 15 160" style="width: auto;height: 100%;stroke: none;stroke-width: 0;"><path stroke-width="0" stroke="none" d="M 0 0 L 15 80 L 0 160 Z"></path></svg><i class="fas fa-plug"></i>';
					v_card_body_div.appendChild(v_button_select);

          var v_button_edit = document.createElement('button');
          v_button_edit.className = 'btn btn-sm mx-1 omnidb__theme__btn--primary';
          v_button_edit.title = "Edit";
          if (v_conn_obj.locked==true)
            v_button_edit.setAttribute("disabled",true);
          v_button_edit.innerHTML = '<i class="fas fa-pen"</i>'
          v_card_body_div.appendChild(v_button_edit);

          var v_button_delete = document.createElement('button');
          v_button_delete.className = 'btn btn-danger btn-sm mx-1';
          v_button_delete.title = "Delete";
          if (v_conn_obj.locked==true)
            v_button_delete.setAttribute("disabled",true);
          v_button_delete.innerHTML = '<i class="fas fa-trash-alt"></i>'
          v_card_body_div.appendChild(v_button_delete);

					v_button_select.onclick = (function(conn_obj) {
						return function() {
							selectConnection(conn_obj);
						};
					}(v_conn_obj));

          v_button_edit.onclick = (function(conn_obj) {
              return function() {
                editConnection(conn_obj);
              };
          }(v_conn_obj));

          v_button_delete.onclick = (function(conn_obj) {
              return function() {
                deleteConnection(conn_obj);
              };
          }(v_conn_obj));

          v_connections_data.card_list.push(
            {
              'data': v_conn_obj,
              'card_div': v_col_div,
              'cover_div': v_cover_div,
              'checkbox': v_checkbox
            }
          );
        }

				v_container.appendChild(v_row);

        v_target_div.innerHTML = '';
        v_target_div.appendChild(v_container);


        if (p_open_modal)
          $('#modal_connections').modal();

        if (p_change_group)
          groupChange(document.getElementById('group_selector').value);
			},
			null,
			'box',
			true);
}

function groupChange(p_value) {

  if (p_value!=-1) {
    document.getElementById('button_group_actions').style.display = '';

    // Filtering group cards
    var v_group_obj = null;

    // Finding the selected group object
    for (var i=0; i<v_connections_data.v_group_list.length; i++) {
      if (p_value == v_connections_data.v_group_list[i].id) {
        v_group_obj = v_connections_data.v_group_list[i];
        break;
      }
    }

    // Going over the cards and adjusting cover div and checkbox
    for (var i=0; i<v_connections_data.card_list.length; i++) {
      var v_conn_obj = v_connections_data.card_list[i];

      // Check the div if it belongs to the currently selected group
      if (v_group_obj.conn_list.includes(v_conn_obj.data.id))
        $(v_conn_obj.card_div).fadeIn(400);
      else
        $(v_conn_obj.card_div).fadeOut(400);
    }


  }
  else {
    document.getElementById('button_group_actions').style.display = 'none';
    document.getElementById('group_selector').value = -1;

    // Going over the cards and adjusting cover div and checkbox
    for (var i=0; i<v_connections_data.card_list.length; i++) {
      var v_conn_obj = v_connections_data.card_list[i];
      $(v_conn_obj.card_div).fadeIn(400);
    }
  }
}

function manageGroup() {

  document.getElementById('group_actions_1').style.display = 'none';
  document.getElementById('group_actions_2').style.display = '';


  var v_current_group_id = document.getElementById('group_selector').value;
  var v_group_obj = null;

  // Finding the selected group object
  for (var i=0; i<v_connections_data.v_group_list.length; i++) {
    if (v_current_group_id == v_connections_data.v_group_list[i].id) {
      v_group_obj = v_connections_data.v_group_list[i];
      break;
    }
  }

  // Going over the cards and adjusting cover div and checkbox
  for (var i=0; i<v_connections_data.card_list.length; i++) {
    var v_conn_obj = v_connections_data.card_list[i];
    v_conn_obj.cover_div.style.display = '';
    $(v_conn_obj.card_div).fadeIn(400);

    // Check the div if it belongs to the currently selected group
    if (v_group_obj.conn_list.includes(v_conn_obj.data.id)) {
      v_conn_obj.checkbox.checked = true;
    }
  }
}

function manageGroupSave() {

  document.getElementById('group_actions_1').style.display = '';
  document.getElementById('group_actions_2').style.display = 'none';

  // Going over the cards and adjusting cover div and checkbox
  for (var i=0; i<v_connections_data.card_list.length; i++) {
    var v_conn_obj = v_connections_data.card_list[i];
    v_conn_obj.cover_div.style.display = 'none';
    v_conn_obj.checkbox.checked = false;
  }

  groupChange(document.getElementById('group_selector').value);

}

function newGroupConfirm(p_name) {
	execAjax('/new_group/',
			JSON.stringify({"p_name": p_name}),
			function(p_return) {
				getGroups();
			},
			null,
			'box');
}

function renameGroupConfirm(p_id, p_name) {
	execAjax('/edit_group/',
			JSON.stringify({"p_id": p_id,"p_name": p_name}),
			function(p_return) {
				getGroups();
			},
			null,
			'box');
}

function deleteGroup() {

	var v_group_id = document.getElementById('group_selector').value;

	showConfirm('Are you sure you want to delete the current group?',
							function() {
								deleteGroupConfirm(v_group_id);
							});
}

function deleteGroupConfirm(p_group_id) {
	execAjax('/delete_group/',
			JSON.stringify({"p_id": p_group_id}),
			function(p_return) {
				getGroups();
			},
			null,
			'box');
}

function newGroup() {
	showConfirm('<input id="group_name_input"/ class="form-control" placeholder="Group Name" style="width: 100%;">',
							function() {
								newGroupConfirm(document.getElementById('group_name_input').value);
							});

  var v_input = document.getElementById('group_name_input');

	v_input.onkeydown = function() {
		if (event.keyCode == 13)
			document.getElementById('modal_message_ok').click();
		else if (event.keyCode == 27)
			document.getElementById('modal_message_cancel').click();
	}
  setTimeout(function () {
  	v_input.focus();
  },500);
}

function renameGroup() {
	var v_select = document.getElementById('group_selector');
	showConfirm('<input id="group_name_input"/ class="form-control" placeholder="Group Name" value="' + v_select.options[v_select.selectedIndex].text + '" style="width: 100%;">',
							function() {
								renameGroupConfirm(
									document.getElementById('group_selector').value,
									document.getElementById('group_name_input').value);
							});
	var v_input = document.getElementById('group_name_input');
	v_input.onkeydown = function() {
		if (event.keyCode == 13)
			document.getElementById('modal_message_ok').click();
		else if (event.keyCode == 27)
			document.getElementById('modal_message_cancel').click();
	}
  setTimeout(function () {
  	v_input.focus();
    v_input.selectionStart = v_input.selectionEnd = 10000;
  },500);
}

function getGroups() {
	execAjax('/get_groups/',
			JSON.stringify({}),
			function(p_return) {
				v_connections_data.v_group_list = p_return.v_data;
				var select = document.getElementById('group_selector');
				var current_value = select.value;
				select.innerHTML = '';
				var option = document.createElement('option');
				option.value = -1;
				option.textContent = 'Select group';
				select.appendChild(option);
				var found = false;
				for (var i=0; i<p_return.v_data.length; i++) {
					option = document.createElement('option');
					option.value = p_return.v_data[i].id;
					option.textContent = p_return.v_data[i].name;
					if (option.value == current_value) {
						option.selected = true;
						found = true;
					}
					select.appendChild(option);
				}
				if (!found==true && current_value!=-1) {
					groupChange(-1);
				}
        else {
          groupChange(document.getElementById('group_selector').value);
        }

			},
			null,
			'box');

}

/// <summary>
/// Tests specific connection.
/// </summary>
function testConnection(p_password = null) {

	var input = JSON.stringify({
    "type": document.getElementById('conn_form_type').value,
    "connstring": document.getElementById('conn_form_connstring').value,
    "server": document.getElementById('conn_form_server').value,
    "port": document.getElementById('conn_form_port').value,
    "database": document.getElementById('conn_form_database').value,
    "user": document.getElementById('conn_form_user').value,
    "tunnel": {
      "enabled": document.getElementById('conn_form_use_tunnel').checked,
      "server": document.getElementById('conn_form_ssh_server').value,
      "port": document.getElementById('conn_form_ssh_port').value,
      "user": document.getElementById('conn_form_ssh_user').value,
      "password": document.getElementById('conn_form_ssh_password').value,
      "key": document.getElementById('conn_form_ssh_key').value
    }
  });

	execAjax('/test_connection_new/',
			input,
			function(p_return) {
				if (p_return.v_data=="Connection successful.")
					showAlert(p_return.v_data);
				else
          showError(p_return.v_data);
			},
			function(p_return) {
        showConfirm(
          p_return.v_data +
          '<input id="txt_test_password_prompt" class="form-control" type="password" placeholder="Password" style="margin-bottom:20px; margin-top: 20px; text-align: center;"/>',
        function() {
          testConnection(document.getElementById('txt_test_password_prompt').value);
        },
        null,
        function() {
          var v_input = document.getElementById('txt_test_password_prompt');
          v_input.focus();
        });

        var v_input = document.getElementById('txt_test_password_prompt');
      	v_input.onkeydown = function() {
      		if (event.keyCode == 13)
      			document.getElementById('modal_message_ok').click();
      		else if (event.keyCode == 27)
      			document.getElementById('modal_message_cancel').click();
      	}

      },
			'box',
			true,
			true);

}

function saveConnection() {

	var input = JSON.stringify({
    "id": v_connections_data.current_id,
    "type": document.getElementById('conn_form_type').value,
    "connstring": document.getElementById('conn_form_connstring').value,
    "server": document.getElementById('conn_form_server').value,
    "port": document.getElementById('conn_form_port').value,
    "database": document.getElementById('conn_form_database').value,
    "user": document.getElementById('conn_form_user').value,
    "title": document.getElementById('conn_form_title').value,
    "tunnel": {
      "enabled": document.getElementById('conn_form_use_tunnel').checked,
      "server": document.getElementById('conn_form_ssh_server').value,
      "port": document.getElementById('conn_form_ssh_port').value,
      "user": document.getElementById('conn_form_ssh_user').value,
      "password": document.getElementById('conn_form_ssh_password').value,
      "key": document.getElementById('conn_form_ssh_key').value
    }
  });

	execAjax('/save_connection_new/',
			input,
			function(p_return) {
				console.log('foi');
        $('#modal_edit_connection').modal('hide');
        showConnectionList(false,true);

			},
			null,
			'box');

}

function deleteConnection(p_conn_obj) {

  showConfirm("Are you sure you want to delete this connection?",
  function() {

    var input = JSON.stringify({
      "id": p_conn_obj.id
    });

  	execAjax('/delete_connection_new/',
  			input,
  			function(p_return) {
  				console.log('foi');
          showConnectionList(false,true);

  			},
  			null,
  			'box');

  })

}

function adjustTechSelector() {
  var select = document.getElementById('conn_form_type');
  select.innerHTML = '';
  var option = document.createElement('option');
  option.value = -1;
  option.textContent = 'Select Type';
  select.appendChild(option);
  for (var i=0; i<v_connections_data.technologies.length; i++) {
    option = document.createElement('option');
    option.value = v_connections_data.technologies[i];
    option.textContent = v_connections_data.technologies[i];
    select.appendChild(option);
  }
}

function editConnection(p_conn_obj) {

  v_connections_data.current_id = p_conn_obj.id;
  adjustTechSelector();

  document.getElementById('conn_form_type').value = p_conn_obj.technology;
  document.getElementById('conn_form_title').value = p_conn_obj.alias;
  document.getElementById('conn_form_connstring').value = p_conn_obj.conn_string;
  document.getElementById('conn_form_server').value = p_conn_obj.server;
  document.getElementById('conn_form_port').value = p_conn_obj.port;
  document.getElementById('conn_form_database').value = p_conn_obj.service;
  document.getElementById('conn_form_user').value = p_conn_obj.user;
  document.getElementById('conn_form_use_tunnel').checked = p_conn_obj.tunnel.enabled;
  document.getElementById('conn_form_ssh_server').value = p_conn_obj.tunnel.server;
  document.getElementById('conn_form_ssh_port').value = p_conn_obj.tunnel.port;
  document.getElementById('conn_form_ssh_user').value = p_conn_obj.tunnel.user;
  document.getElementById('conn_form_ssh_password').value = p_conn_obj.tunnel.password;
  document.getElementById('conn_form_ssh_key').value = p_conn_obj.tunnel.key;

  $('#modal_edit_connection').modal();

}

function newConnection() {

  v_connections_data.current_id = -1;
  adjustTechSelector();

  document.getElementById('conn_form_type').value = -1;
  document.getElementById('conn_form_connstring').value = '';
  document.getElementById('conn_form_server').value = '';
  document.getElementById('conn_form_port').value = '';
  document.getElementById('conn_form_database').value = '';
  document.getElementById('conn_form_user').value = '';
  document.getElementById('conn_form_use_tunnel').checked = false;
  document.getElementById('conn_form_ssh_server').value = '';
  document.getElementById('conn_form_ssh_port').value = '22';
  document.getElementById('conn_form_ssh_user').value = '';
  document.getElementById('conn_form_ssh_password').value = '';
  document.getElementById('conn_form_ssh_key').value = '';

  $('#modal_edit_connection').modal();
}

function selectConnection(p_tech,p_index) {

	alert('TODO: Try connection');

}

function toggleConnectionsLayout(l_type) {
	if (l_type === 'cards') {
		$('.omnidb__connections__card-list').removeClass('omnidb__connections__card-list--rows');
		$('.omnidb__connections__card-list').addClass('omnidb__connections__card-list--cards');
	}
	else if (l_type === 'rows') {
		$('.omnidb__connections__card-list').removeClass('omnidb__connections__card-list--cards');
		$('.omnidb__connections__card-list').addClass('omnidb__connections__card-list--rows');
	}
}
