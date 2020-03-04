function secondqGetUniqueSelectedRows(p_grid, p_mode, p_tag) {
  var v_selected = p_grid.getSelected();
  //Building data list
  var v_data = [];
  for (var i=0; i<v_selected.length; i++) {
    var v_lower_index = 0;
    var v_uper_index = 0;
    if (v_selected[i][0] < v_selected[i][2]) {
      v_lower_index = v_selected[i][0];
      v_uper_index = v_selected[i][2];
    }
    else {
      v_lower_index = v_selected[i][2];
      v_uper_index = v_selected[i][0];
    }
    for (var j=v_lower_index; j<=v_uper_index; j++) {
      // check if line wasn't added already
      var v_found = false;
      for (var k=0; k<v_data.length; k++) {
        if (v_data[k] == j) {
          v_found = true;
          break;
        }
      }
      if (v_found==true)
        continue;

      v_data.push(j);
    }
  }

  var v_final_data = [];

  for (var i=0; i<v_data.length; i++) {
    var v_row = p_grid.getDataAtRow(v_data[i]);

    if (p_mode=='host_list' || p_mode=='customer_dashboard') {
      v_final_data.push({
        'line_number': v_data[i],
        'customer_id': p_tag.status_data[v_data[i]].customer_id,
        'server_id': p_tag.status_data[v_data[i]].host_id
      });
    }
    else if (p_mode=='unit_list') {
      v_final_data.push({
        'line_number': v_data[i],
        'customer_id': p_tag.status_data[v_data[i]].customer_id,
        'server_id': p_tag.status_data[v_data[i]].host_id,
        'su_id': p_tag.status_data[v_data[i]].su_id,
        'key': p_tag.status_data[v_data[i]].key
      });
    }
    else if (p_mode=='customer_list') {
      v_final_data.push({
        'line_number': v_data[i],
        'customer_id': p_tag.status_data[v_data[i]].customer_id,
        'notes': p_tag.status_data[v_data[i]].notes
      });
    }
    // Host dashboard
    else {
      v_final_data.push({
        'line_number': v_data[i],
        'customer_id': p_tag.customer_id,
        'server_id': p_tag.host_id,
        'su_id': p_tag.status_data[v_data[i]].su_id,
        'key': p_tag.status_data[v_data[i]].key
      });
    }
  }

  return v_final_data;
}

function editCustomerNotes(p_ht, p_mode, p_tag) {
  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);
  editCustomerNotesCall(v_data, p_mode, p_tag);
}

function editCustomerNotesCall(p_data, p_mode, p_tag) {
  if (p_data.length>1) {
    showAlert('Please select a single customer.')
  }
  else {

    var v_old_notes = p_data[0]['notes'];

    showConfirm('<textarea class="form-control" style="height: 300px;" id="secondq_customer_nodes_textarea" placeholder="Customer notes"></textarea>',
    function() {

      var v_new_notes = document.getElementById('secondq_customer_nodes_textarea').value;

      if (v_old_notes != v_new_notes) {
        callPluginFunction({
          p_plugin_name: 'secondq_monitoring',
          p_function_name: 'change_notes_customer',
          p_data: {
            'rows': p_data,
            'notes': v_new_notes
          },
          p_callback: function(p_data) {

            if (p_data.error==true)
              showAlert(p_data.message);
            else
            {
              secondqLoadCustomerListData(true);
            }

          },
          p_loading: true,
          p_check_database_connection: false
        });
      }
    },
    null,
    function() {
      document.getElementById('secondq_customer_nodes_textarea').focus()
    },
    true);

    var v_input1 = document.getElementById('secondq_customer_nodes_textarea');
    v_input1.value = v_old_notes

  }
}

function changeKeyUnit(p_ht, p_mode, p_tag) {

  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);
  changeKeyUnitCall(v_data, p_mode, p_tag);
}

function changeKeyUnitCall(p_data, p_mode, p_tag) {
  if (p_data.length>1) {
    showAlert('Please select a single unit.')
  }
  else {

    var v_old_key = p_data[0]['key'];

    showConfirm('WARNING, changing the key requires changing the configuration of this unit check in the host.<br/><br/><input type="text" class="form-control" id="secondq_unit_key_input" placeholder="Key"/>',
    function() {

      var v_new_key = document.getElementById('secondq_unit_key_input').value.trim();
      if (v_new_key == '')
        v_new_key = null;

      if (v_old_key != v_new_key) {
        callPluginFunction({
          p_plugin_name: 'secondq_monitoring',
          p_function_name: 'change_key_unit',
          p_data: {
            'rows': p_data,
            'type': p_mode,
            'new_key': v_new_key,
            'old_key': v_old_key
          },
          p_callback: function(p_data) {

            if (p_data.error==true)
              showAlert(p_data.message);
            else
            {
              if (p_mode=='host_list')
                secondqLoadHostListData(true);
              else if (p_mode=='unit_list')
                secondqLoadUnitListData(true);
              else if (p_mode=='customer_dashboard')
                secondqLoadCustomerDashboardData(true,'all');
              else if (p_mode=='host_dashboard')
                secondqLoadHostDashboardData(true,'all');
              else if (p_mode=='unit_dashboard')
                secondqLoadUnitDashboardData(true,'details');
            }

          },
          p_loading: true,
          p_check_database_connection: false
        });
      }
    },
    null,
    function() {
      document.getElementById('secondq_unit_key_input').focus()
    });

    var v_input1 = document.getElementById('secondq_unit_key_input');
    v_input1.value = v_old_key

    v_input1.onkeydown = function() {
      if (event.keyCode == 13)
        document.getElementById('modal_message_ok').click();
      else if (event.keyCode == 27)
        document.getElementById('modal_message_cancel').click();
    }
  }
}

function enableUnits(p_ht, p_mode, p_tag) {

  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);
  enableUnitsCall(v_data, p_mode, p_tag);
}

function enableUnitsCall(p_data, p_mode, p_tag) {

  showConfirm('Are you sure you want to ENABLE the selected item(s)?',
  function() {
    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'enable_units',
      p_data: {
        'rows': p_data,
        'type': p_mode
      },
      p_callback: function(p_data) {

        if (p_data.error==true)
          showAlert(p_data.message);
        else
        {
          if (p_mode=='host_list')
            secondqLoadHostListData(true);
          else if (p_mode=='unit_list')
            secondqLoadUnitListData(true);
          else if (p_mode=='customer_dashboard')
            secondqLoadCustomerDashboardData(true,'all');
          else if (p_mode=='host_dashboard')
            secondqLoadHostDashboardData(true,'all');
          else if (p_mode=='unit_dashboard')
            secondqLoadUnitDashboardData(true,'details');
        }

      },
      p_loading: true,
      p_check_database_connection: false
    });
  },
  null,
  null);
}

function disableUnits(p_ht, p_mode, p_tag) {

  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);
  disableUnitsCall(v_data, p_mode, p_tag);
}

function disableUnitsCall(p_data, p_mode, p_tag) {

  showConfirm('Are you sure you want to DISABLE the selected item(s)?',
  function() {
    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'disable_units',
      p_data: {
        'rows': p_data,
        'type': p_mode
      },
      p_callback: function(p_data) {

        if (p_data.error==true)
          showAlert(p_data.message);
        else
        {
          if (p_mode=='host_list')
            secondqLoadHostListData(true);
          else if (p_mode=='unit_list')
            secondqLoadUnitListData(true);
          else if (p_mode=='customer_dashboard')
            secondqLoadCustomerDashboardData(true,'all');
          else if (p_mode=='host_dashboard')
            secondqLoadHostDashboardData(true,'all');
          else if (p_mode=='unit_dashboard')
            secondqLoadUnitDashboardData(true,'details');
        }

      },
      p_loading: true,
      p_check_database_connection: false
    });
  },
  null,
  null);
}

function ackUnits(p_ht, p_mode, p_tag) {

  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);
  ackUnitsCall(v_data, p_mode, p_tag);
}

function ackUnitsCall(p_data, p_mode, p_tag) {

  showConfirm('<input type="text" class="form-control mb-2" id="secondq_datetime_picker1" placeholder="End time"/><input type="text" class="form-control" id="secondq_ack_message" placeholder="Message"/>',
  function() {
    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'acknowledge_units',
      p_data: {
        'time': document.getElementById('secondq_datetime_picker1').value,
        'message': document.getElementById('secondq_ack_message').value,
        'rows': p_data,
        'type': p_mode
      },
      p_callback: function(p_data) {

        if (p_mode=='host_list')
          secondqLoadHostListData(true);
        else if (p_mode=='unit_list')
          secondqLoadUnitListData(true);
        else if (p_mode=='customer_dashboard')
          secondqLoadCustomerDashboardData(true,'all');
        else if (p_mode=='host_dashboard')
          secondqLoadHostDashboardData(true,'all');
        else if (p_mode=='unit_dashboard')
          secondqLoadUnitDashboardData(true,'details');

      },
      p_loading: true,
      p_check_database_connection: false
    });
  },
  null,
  function() {
    var v_input = document.getElementById('secondq_datetime_picker1');
    v_input.focus();
  });
  jQuery('#secondq_datetime_picker1').datetimepicker({format:'Y-m-d H:i'});
  var v_input1 = document.getElementById('secondq_datetime_picker1');
  var v_input2 = document.getElementById('secondq_ack_message');
  v_input1.onkeydown = function() {
    if (event.keyCode == 13)
      document.getElementById('modal_message_ok').click();
    else if (event.keyCode == 27)
      document.getElementById('modal_message_cancel').click();
  }
  v_input2.onkeydown = function() {
    if (event.keyCode == 13)
      document.getElementById('modal_message_ok').click();
    else if (event.keyCode == 27)
      document.getElementById('modal_message_cancel').click();
  }
}

function removeAckUnits(p_ht, p_mode, p_tag) {
  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);
  removeAckUnitsCall(v_data, p_mode, p_tag);
}

function removeAckUnitsCall(p_data, p_mode, p_tag) {

  showConfirm('Are you sure you want to remove ACK from the selected hosts?',
  function() {
    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'remove_acknowledge_units',
      p_data: {
        'rows': p_data,
        'type': p_mode
      },
      p_callback: function(p_data) {

        if (p_mode=='host_list')
          secondqLoadHostListData(true);
        else if (p_mode=='unit_list')
          secondqLoadUnitListData(true);
        else if (p_mode=='customer_dashboard')
          secondqLoadCustomerDashboardData(true,'all');
        else if (p_mode=='host_dashboard')
          secondqLoadHostDashboardData(true,'all');
        else if (p_mode=='unit_dashboard')
          secondqLoadUnitDashboardData(true,'details');

      },
      p_loading: true,
      p_check_database_connection: false
    });
  });
}

function downtimeUnits(p_ht, p_mode, p_tag) {
  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);
  downtimeUnitsCall(v_data, p_mode, p_tag);
}

function downtimeUnitsCall(p_data, p_mode, p_tag) {

  showConfirm('<input type="text" class="form-control mb-2" id="secondq_datetime_picker1" placeholder="Start time"/><input type="text" class="form-control" id="secondq_datetime_picker2" placeholder="End time"/>',
  function() {
    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'downtime_units',
      p_data: {
        'start_time': document.getElementById('secondq_datetime_picker1').value,
        'end_time': document.getElementById('secondq_datetime_picker2').value,
        'rows': p_data,
        'type': p_mode
      },
      p_callback: function(p_data) {

        if (p_mode=='host_list')
          secondqLoadHostListData(true);
        else if (p_mode=='unit_list')
          secondqLoadUnitListData(true);
        else if (p_mode=='customer_dashboard')
          secondqLoadCustomerDashboardData(true,'all');
        else if (p_mode=='host_dashboard')
          secondqLoadHostDashboardData(true,'all');
        else if (p_mode=='unit_dashboard')
          secondqLoadUnitDashboardData(true,'details');

      },
      p_loading: true,
      p_check_database_connection: false
    });
  },
  null,
  function() {
    var v_input = document.getElementById('secondq_datetime_picker1');
    v_input.focus();
  });
  jQuery('#secondq_datetime_picker1').datetimepicker({format:'Y-m-d H:i'});
  jQuery('#secondq_datetime_picker2').datetimepicker({format:'Y-m-d H:i'});
  var v_input1 = document.getElementById('secondq_datetime_picker1');
  var v_input2 = document.getElementById('secondq_datetime_picker2');
  v_input1.onkeydown = function() {
    if (event.keyCode == 13)
      document.getElementById('modal_message_ok').click();
    else if (event.keyCode == 27)
      document.getElementById('modal_message_cancel').click();
  }
  v_input2.onkeydown = function() {
    if (event.keyCode == 13)
      document.getElementById('modal_message_ok').click();
    else if (event.keyCode == 27)
      document.getElementById('modal_message_cancel').click();
  }
}

function removeDowntimeUnits(p_ht, p_mode, p_tag) {
  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);
  removeDowntimeUnitsCall(v_data, p_mode, p_tag);
}

function removeDowntimeUnitsCall(p_data, p_mode, p_tag) {

  showConfirm('Are you sure you want to remove DOWNTIME from the selected hosts?',
  function() {
    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'remove_downtime_units',
      p_data: {
        'rows': p_data,
        'type': p_mode
      },
      p_callback: function(p_data) {

        if (p_mode=='host_list')
          secondqLoadHostListData(true);
        else if (p_mode=='unit_list')
          secondqLoadUnitListData(true);
        else if (p_mode=='customer_dashboard')
          secondqLoadCustomerDashboardData(true,'all');
        else if (p_mode=='host_dashboard')
          secondqLoadHostDashboardData(true,'all');
        else if (p_mode=='unit_dashboard')
          secondqLoadUnitDashboardData(true,'details');

      },
      p_loading: true,
      p_check_database_connection: false
    });
  });
}

function changeThresholdUnits(p_ht,p_mode, p_tag, p_row_status) {

  var v_data = secondqGetUniqueSelectedRows(p_ht, p_mode, p_tag);

  var v_selected = p_ht.getSelected();

  for (var i=0; i<v_data.length; i++) {
    v_data[i]['thresholds'] = {
      'critical': p_row_status[v_data[i]['line_number']].threshold_critical,
      'high': p_row_status[v_data[i]['line_number']].threshold_high,
      'medium': p_row_status[v_data[i]['line_number']].threshold_medium,
      'low': p_row_status[v_data[i]['line_number']].threshold_low
    }
  }

  changeThresholdUnitsCall(v_data, p_mode);
}

function changeThresholdUnitsCall(p_data, p_mode) {


  var v_threshold_critical = '';
  var v_threshold_high = '';
  var v_threshold_medium = '';
  var v_threshold_low = '';

  v_threshold_critical = p_data[0]['thresholds']['critical'];
  v_threshold_high = p_data[0]['thresholds']['high'];
  v_threshold_medium = p_data[0]['thresholds']['medium'];
  v_threshold_low = p_data[0]['thresholds']['low'];

  showConfirm(
  '<div class="form-group"><label>Critical (leave blank to disable)</label>' +
  '<input type="text" class="form-control mb-2" id="secondq_threshold_critical" placeholder="Critical"/>' +
  '</div>' +
  '<div class="form-group"><label>High (leave blank to disable)</label>' +
  '<input type="text" class="form-control mb-2" id="secondq_threshold_high" placeholder="High"/>' +
  '</div>' +
  '<div class="form-group"><label>Medium (leave blank to disable)</label>' +
  '<input type="text" class="form-control mb-2" id="secondq_threshold_medium" placeholder="Medium"/>' +
  '</div>' +
  '<div class="form-group"><label>Low (leave blank to disable)</label>' +
  '<input type="text" class="form-control mb-2" id="secondq_threshold_low" placeholder="Low"/>',
  function() {

    var v_threshold_critical_new = document.getElementById('secondq_threshold_critical').value.trim();
    var v_threshold_high_new = document.getElementById('secondq_threshold_high').value.trim();
    var v_threshold_medium_new = document.getElementById('secondq_threshold_medium').value.trim();
    var v_threshold_low_new = document.getElementById('secondq_threshold_low').value.trim();

    var v_problem = false;
    var v_problematic_field = '';
    if (isNaN(v_threshold_critical_new)) {
      v_problem = true;
      v_problematic_field = v_threshold_critical_new;
    }
    if (isNaN(v_threshold_high_new)) {
      v_problem = true;
      v_problematic_field = v_threshold_high_new;
    }
    if (isNaN(v_threshold_medium_new)) {
      v_problem = true;
      v_problematic_field = v_threshold_medium_new;
    }
    if (isNaN(v_threshold_low_new)) {
      v_problem = true;
      v_problematic_field = v_threshold_low_new;
    }

    if (v_problem)
    {
      setTimeout( function() {
        showAlert(v_problematic_field + ' is an invalid number.');
        return;
      },200);
    }
    else {
      var v_has_new_threshold = false;

      for (var i=p_data.length-1; i>=0; i--) {
        var v_row_changed = false;

        var v_float_old = null;
        var v_float_new = null;
        if (p_data[i]['thresholds']['critical']==null)
          v_float_old = null;
        else
          v_float_old = parseFloat(p_data[i]['thresholds']['critical']);
        if (v_threshold_critical_new=='')
          v_float_new = null;
        else
          v_float_new = parseFloat(v_threshold_critical_new);

        if (v_float_old != v_float_new) {
          p_data[i]['thresholds']['critical'] = {
            'old': p_data[i]['thresholds']['critical'],
            'new': v_threshold_critical_new
          }
          v_has_new_threshold = true;
          v_row_changed = true;
        }
        else {
          p_data[i]['thresholds']['critical'] = null;
        }

        if (p_data[i]['thresholds']['high']==null)
          v_float_old = null;
        else
          v_float_old = parseFloat(p_data[i]['thresholds']['high']);
        if (v_threshold_high_new=='')
          v_float_new = null;
        else
          v_float_new = parseFloat(v_threshold_high_new);

        if (v_float_old != v_float_new) {
          p_data[i]['thresholds']['high'] = {
            'old': p_data[i]['thresholds']['high'],
            'new': v_threshold_high_new
          }
          v_has_new_threshold = true;
          v_row_changed = true;
        }
        else {
          p_data[i]['thresholds']['high'] = null;
        }

        if (p_data[i]['thresholds']['medium']==null)
          v_float_old = null;
        else
          v_float_old = parseFloat(p_data[i]['thresholds']['medium']);
        if (v_threshold_medium_new=='')
          v_float_new = null;
        else
          v_float_new = parseFloat(v_threshold_medium_new);

        if (v_float_old != v_float_new) {
          p_data[i]['thresholds']['medium'] = {
            'old': p_data[i]['thresholds']['medium'],
            'new': v_threshold_medium_new
          }
          v_has_new_threshold = true;
          v_row_changed = true;
        }
        else {
          p_data[i]['thresholds']['medium'] = null;
        }

        if (p_data[i]['thresholds']['low']==null)
          v_float_old = null;
        else
          v_float_old = parseFloat(p_data[i]['thresholds']['low']);
        if (v_threshold_low_new=='')
          v_float_new = null;
        else
          v_float_new = parseFloat(v_threshold_low_new);

        if (v_float_old != v_float_new) {
          p_data[i]['thresholds']['low'] = {
            'old': p_data[i]['thresholds']['low'],
            'new': v_threshold_low_new
          }
          v_has_new_threshold = true;
          v_row_changed = true;
        }
        else {
          p_data[i]['thresholds']['low'] = null;
        }

        if (!v_row_changed) {
          p_data.splice(i, 1);
        }
      }

      if (v_has_new_threshold) {
        callPluginFunction({
          p_plugin_name: 'secondq_monitoring',
          p_function_name: 'threshold_units',
          p_data: { 'rows': p_data },
          p_callback: function(p_data) {

            if (p_data.error==true)
              showAlert(p_data.message);
            else {
              if (p_mode=='unit_list')
                secondqLoadUnitListData(true);
              else if (p_mode=='host_dashboard')
                secondqLoadHostDashboardData(true,'all');
              else if (p_mode=='unit_dashboard')
                secondqLoadUnitDashboardData(true,'all');
            }

          },
          p_loading: true,
          p_check_database_connection: false
        });
      }
    }
  },
  null,
  function() {
    var v_input = document.getElementById('secondq_threshold_critical');
    v_input.focus();
  });

  var v_input1 = document.getElementById('secondq_threshold_critical');
  var v_input2 = document.getElementById('secondq_threshold_high');
  var v_input3 = document.getElementById('secondq_threshold_medium');
  var v_input4 = document.getElementById('secondq_threshold_low');
  v_input1.value = v_threshold_critical;
  v_input2.value = v_threshold_high;
  v_input3.value = v_threshold_medium;
  v_input4.value = v_threshold_low;

  v_input1.onkeydown = function() {
    if (event.keyCode == 13)
      document.getElementById('modal_message_ok').click();
    else if (event.keyCode == 27)
      document.getElementById('modal_message_cancel').click();
  }
  v_input2.onkeydown = function() {
    if (event.keyCode == 13)
      document.getElementById('modal_message_ok').click();
    else if (event.keyCode == 27)
      document.getElementById('modal_message_cancel').click();
  }
  v_input3.onkeydown = function() {
    if (event.keyCode == 13)
      document.getElementById('modal_message_ok').click();
    else if (event.keyCode == 27)
      document.getElementById('modal_message_cancel').click();
  }
  v_input4.onkeydown = function() {
    if (event.keyCode == 13)
      document.getElementById('modal_message_ok').click();
    else if (event.keyCode == 27)
      document.getElementById('modal_message_cancel').click();
  }

}

function secondqViewJsonData(p_json) {
  var v_json = null;
  // No json passed as argument, use JSON from current tab
  if (p_json==null) {
    v_json = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.data_json;
  }
  else
    v_json = p_json;

  var v_div = document.createElement('div');

  var json_object = {
    target: v_div,
    data: v_json,
    template: 'template-2',
  }

  var json_component = new BsJsonComponent(json_object);
  json_component.render();
  showAlert(v_div.innerHTML,null,true);
}

function secondqShowAckDetails(p_mode,p_line,p_element) {

  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  var v_content = '';

  if (p_mode=='grid') {
    v_content = 'End Time: ' + v_tab_tag.status_data[p_line].ack_endtime + '<br/>' +
             'User: ' + v_tab_tag.status_data[p_line].ack_user + '<br/>' +
             'Message: ' + v_tab_tag.status_data[p_line].ack_message;
  }
  else {
    v_content = 'End Time: ' + v_tab_tag.dashboard_status_data.ack_endtime + '<br/>' +
             'User: ' + v_tab_tag.dashboard_status_data.ack_user + '<br/>' +
             'Message: ' + v_tab_tag.dashboard_status_data.ack_message;
  }

  $(p_element).popover(
  {
    title: 'Ack',
    content: v_content,
    placement: 'bottom',
    html: true
  });
  $(p_element).popover('show');

  var v_close_function = function() {
    $(p_element).popover('hide');
  }

  $(p_element).on('hidden.bs.popover', function () {
    $(p_element).popover('dispose');
    window.removeEventListener("click",v_close_function);
  })

  $(p_element).on('shown.bs.popover', function () {
    window.addEventListener("click",v_close_function,false);
  })
}

function secondqShowDowntimeDetails(p_mode,p_line,p_element) {

  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  var v_content = '';

  if (p_mode=='grid') {
    v_content = 'Start Time: ' + v_tab_tag.status_data[p_line].downtime_starttime + '<br/>' +
             'End Time: ' + v_tab_tag.status_data[p_line].downtime_endtime + '<br/>' +
             'User: ' + v_tab_tag.status_data[p_line].downtime_user;
  }
  else {
    v_content = 'Start Time: ' + v_tab_tag.dashboard_status_data.downtime_starttime + '<br/>' +
             'End Time: ' + v_tab_tag.dashboard_status_data.downtime_endtime + '<br/>' +
             'User: ' + v_tab_tag.dashboard_status_data.downtime_user;
  }

  $(p_element).popover(
  {
    title: 'Downtime',
    content: v_content,
    placement: 'bottom',
    html: true
  });
  $(p_element).popover('show');

  var v_close_function = function() {
    $(p_element).popover('hide');
  }

  $(p_element).on('hidden.bs.popover', function () {
    $(p_element).popover('dispose');
    window.removeEventListener("click",v_close_function);
  })

  $(p_element).on('shown.bs.popover', function () {
    window.addEventListener("click",v_close_function,false);
  })
}
