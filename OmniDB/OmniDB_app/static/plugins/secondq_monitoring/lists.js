function secondqCreateCustomerList(p_filter) {

  if (!secondqSelectExistingTab('secondq_customer_list',p_filter)) {
    startLoading();
    setTimeout(function() {

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
      p_name: '<i class="fas fa-user icon-tab-title"></i> Customers',
      p_selectFunction: function() {
        if(this.tag != null) {
          secondqChangeTabTitle(this.tag);
          secondqAdjustHeights();
          if (this.tag.load_pending) {

            secondqLoadCustomerListData(true);
          }
        }
      },
      p_closeFunction: function(e,p_tab) {
        var v_current_tab = p_tab;
        removeTab(v_current_tab);
      },
    });

      v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

      var v_html =
      "<div class='container-fluid'>" +
        "<div class='row'>" +
          "<div class='col-md-12 my-2'>" +
            "<form class='d-flex' autofill='false' onsubmit='(event)=>{event.preventDefault();};'>" +
              "<div class='input-group w-auto'>" +
                "<div class='input-group-prepend'>" +
                  "<span class='input-group-text bg-transparent'>" +
                  "<i class='fas fa-filter'></i>" +
                  "</span>" +
                "</div>" +
                "<input type='text' style='width: 300px;'class='form-control d-inline' placeholder='Filter' id='input_filter_customer_" + v_tab.id + "' onchange='secondqLoadCustomerListData(true, true);'>" +
              "</div>" +
              "<button type='submit' disabled style='display: none' aria-hidden='true'></button>" +
              "<button title='Refresh' type='button' style='vertical-align: baseline' class='btn btn-primary btn-sm ml-1' onclick='(event)=>{event.preventDefault();}; secondqLoadCustomerListData(true);'><i class='fas fa-sync'></i></button>" +
            "</form>" +
          "</div>" +
        "</div>" +
        "<div class='row mb-2'>" +
          "<div class='col-md-12'>" +
            "<div id='dashboard_customer_list_pagination_" + v_tab.id + "'></div>" +
          "</div>" +
        "</div>" +
        "<div class='row mb-2'>" +
          "<div class='col-md-12'>" +
            "<div id='dashboard_customer_list_" + v_tab.id + "' class='' style='width: 100%; height: 730px; overflow: hidden;'/></div>" +
          "</div>" +
        "</div>" +
      "</div>";

      var v_div = document.getElementById('div_' + v_tab.id);
      v_div.innerHTML = v_html;
      var v_dashboard_customer_list = document.getElementById('dashboard_customer_list_' + v_tab.id);
      var v_input_filter_customer = document.getElementById('input_filter_customer_' + v_tab.id);

      if (p_filter!=null) {
        if (p_filter.filter_all!=null)
          v_input_filter_customer.value = p_filter.filter_all;
      }

      //Setting up customer grid
      var columnProperties = [];

      var col = new Object();
      col.readOnly = true;
      col.title =  'Customer';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Server Count';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Max Severity';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Notes';
      columnProperties.push(col);

      var ht = new Handsontable(v_dashboard_customer_list,
      {
        licenseKey: 'non-commercial-and-evaluation',
        data: [],
        columns : columnProperties,
        colHeaders : true,
        rowHeaders : false,
        fillHandle:false,
        stretchH: (window.mediaConfig === "desktop-xl" || window.mediaConfig === "desktop-lg") ? 'last' : undefined,
        copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
        manualColumnResize: true,
        autoColumnSize : true,
        afterOnCellMouseUp: function(event,coords) {
        },
        cells: function (row, col, prop) {

            var cellProperties = {};

            if (col==2)
              cellProperties.renderer = severityRenderer;
            else if (col==3)
              cellProperties.renderer = centerRenderer;
            else
              cellProperties.renderer = centerMiddleRenderer;

            return cellProperties;
        },
        mergeCells: true,
        contextMenu: {
          callback: function (key, options) {
            if (key === 'notes') {
              editCustomerNotes(this,'customer_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
          },
          items: {
            "notes": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-comment-dots cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Edit Notes</div>'}
          }
        }
      });

      var v_input_filter_customer = document.getElementById('input_filter_customer_' + v_tab.id);

      var v_tag = {
        tab_id: v_tab.id,
        mode: 'secondq_customer_list',
        div_customer_list: v_dashboard_customer_list,
        ht_customers: ht,
        load_pending: false,
        status_data: null,
        input_filter: v_input_filter_customer,
        div_pagination: document.getElementById('dashboard_customer_list_pagination_' + v_tab.id),
        current_page: 0
      };
      v_tab.tag = v_tag;

      secondqAdjustHeights();
      secondqChangeTabTitle(v_tab.tag);
      secondqLoadCustomerListData(true);
      endLoading();

    },50);
  }
}

function secondqCreateHostList(p_filter) {

  if (!secondqSelectExistingTab('secondq_host_list',p_filter)) {
    startLoading();
    setTimeout(function() {

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
      p_name: '<i class="fas fa-server icon-tab-title"></i> Hosts',
      p_selectFunction: function() {
        if(this.tag != null) {
          secondqChangeTabTitle(this.tag);
          secondqAdjustHeights();
          if (this.tag.load_pending) {

            secondqLoadHostListData(true);
          }
        }
      },
      p_closeFunction: function(e,p_tab) {
        var v_current_tab = p_tab;
        removeTab(v_current_tab);
      },
    });

      v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

      var v_html =
      "<div class='container-fluid'>" +
        "<div class='row'>" +
          "<div class='col-md-12 my-2'>" +
            "<form class='d-flex' autofill='false' onsubmit='(event)=>{event.preventDefault();};'>" +
              "<div class='input-group w-auto'>" +
                "<div class='input-group-prepend'>" +
                  "<span class='input-group-text bg-transparent'>" +
                  "<i class='fas fa-filter'></i>" +
                  "</span>" +
                "</div>" +
                "<input type='text' name='input_filter_customer' style='width: 300px;'class='form-control d-inline' placeholder='Filter' id='input_filter_customer_" + v_tab.id + "' onchange='secondqLoadHostListData(true, true);'>" +
              "</div>" +
              "<div class='input-group w-auto ml-1'>" +
                "<div class='input-group-prepend'>" +
                  "<span class='input-group-text bg-transparent'>" +
                  "<i class='fas fa-heartbeat'></i>" +
                  "</span>" +
                "</div>" +
                "<select class='form-control d-inline' style='width: 300px;' id='sel_filter_customer_" + v_tab.id + "' onchange='secondqLoadHostListData(true, true);'>" +
                  "<option selected='selected' value=0 >ALL</option>" +
                  "<option value=1 >UP</option>" +
                  "<option value=2 >DOWN</option>" +
                  "<option value=3 >DOWN (OK)</option>" +
                  "<option value=4 >ENABLED</option>" +
                  "<option value=5 >DISABLED</option>" +
                "</select>" +
              "</div>" +
              "<button type='submit' disabled style='display: none' aria-hidden='true'></button>" +
              "<button title='Refresh' type='button' style='vertical-align: baseline' class='btn btn-primary btn-sm ml-1' onclick='(event)=>{event.preventDefault();}; secondqLoadHostListData(true);'><i class='fas fa-sync'></i></button>" +
            "</form>" +
          "</div>" +
        "</div>" +
        "<div class='row mb-2'>" +
          "<div class='col-md-12'>" +
            "<div id='dashboard_host_list_pagination_" + v_tab.id + "'></div>" +
          "</div>" +
        "</div>" +
        "<div class='row mb-2'>" +
          "<div class='col-md-12'>" +
            "<div id='dashboard_host_list_" + v_tab.id + "' class='' style='width: 100%; height: 730px; overflow: hidden;'/></div>" +
          "</div>" +
        "</div>" +
      "</div>" ;

      var v_div = document.getElementById('div_' + v_tab.id);
      v_div.innerHTML = v_html;
      var v_dashboard_host_list = document.getElementById('dashboard_host_list_' + v_tab.id);
      var v_sel_filter_customer = document.getElementById('sel_filter_customer_' + v_tab.id);
      var v_input_filter_customer = document.getElementById('input_filter_customer_' + v_tab.id);

      if (p_filter!=null) {
        if (p_filter.filter_all!=null)
          v_input_filter_customer.value = p_filter.filter_all;
        if (p_filter.filter_severity!=null)
          v_sel_filter_customer.value = p_filter.filter_severity;
      }

      //Setting up customer grid
      var columnProperties = [];

      var col = new Object();
      col.readOnly = true;
      col.title =  'Customer';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Host';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Status';
      col.width = '80px';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Time Elapsed';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Actions';
      col.width = '80px';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Max Severity';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Hostname';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'IPs';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Role';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Services';
      columnProperties.push(col);


      var ht = new Handsontable(v_dashboard_host_list,
      {
        licenseKey: 'non-commercial-and-evaluation',
        data: [],
        columns : columnProperties,
        colHeaders : true,
        rowHeaders : false,
        fillHandle:false,
        stretchH: (window.mediaConfig === "desktop-xl" || window.mediaConfig === "desktop-lg") ? 'last' : undefined,
        copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
        manualColumnResize: true,
        autoColumnSize : true,
        afterOnCellMouseUp: function(event,coords) {
        },
        cells: function (row, col, prop) {

            var cellProperties = {};

            if (col!= 0 && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row]!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row].ok==true)
              cellProperties.renderer = secondqGrayRenderer;
            else if (col==5)
              cellProperties.renderer = severityRenderer;
            else if (col!= 0 && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row]!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row].status=='down')
              cellProperties.renderer = redCellRenderer;
            else
              cellProperties.renderer = centerMiddleRenderer;

            return cellProperties;
        },
        mergeCells: true,
        contextMenu: {
          callback: function (key, options) {
            if (key === 'ack') {
              ackUnits(this,'host_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'remove_ack') {
              removeAckUnits(this,'host_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'downtime') {
              downtimeUnits(this,'host_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'remove_downtime') {
              removeDowntimeUnits(this,'host_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'enable') {
              enableUnits(this,'host_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'disable') {
              disableUnits(this,'host_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
          },
          items: {
            "ack": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-check cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Acknowledge</div>'},
            "remove_ack": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-check cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">REMOVE Acknowledge</div>'},
            "downtime": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-wrench cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Set Downtime</div>'},
            "remove_downtime": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-wrench cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">REMOVE Downtime</div>'},
            "enable": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-power-off cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Enable (superuser)</div>'},
            "disable": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-power-off cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Disable (superuser)</div>'}
          }
        }
      });

      var v_sel_filter_customer = document.getElementById('sel_filter_customer_' + v_tab.id);
      var v_input_filter_customer = document.getElementById('input_filter_customer_' + v_tab.id);

      var v_tag = {
        tab_id: v_tab.id,
        mode: 'secondq_host_list',
        div_host_list: v_dashboard_host_list,
        ht_hosts: ht,
        load_pending: false,
        status_data: null,
        sel_filter: v_sel_filter_customer,
        input_filter: v_input_filter_customer,
        div_pagination: document.getElementById('dashboard_host_list_pagination_' + v_tab.id),
        current_page: 0
      };
      v_tab.tag = v_tag;

      secondqAdjustHeights();
      secondqChangeTabTitle(v_tab.tag);
      secondqLoadHostListData(true);
      endLoading();

    },50);
  }
}

function secondqCreateUnitList(p_filter) {

  if (!secondqSelectExistingTab('secondq_unit_list',p_filter)) {
    startLoading();
    setTimeout(function() {

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
      p_name: '<i class="fas fa-eye icon-tab-title"></i> Unit Checks',
      p_selectFunction: function() {
        if(this.tag != null) {
          secondqChangeTabTitle(this.tag);
          secondqAdjustHeights();
          if (this.tag.load_pending) {

            secondqLoadUnitListData(true);
          }
        }
      },
      p_closeFunction: function(e,p_tab) {
        var v_current_tab = p_tab;
        p_tab.removeTab();
      },
    });

      v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

      var v_html =
      "<div class='container-fluid'>" +
        "<div class='row'>" +
          "<div class='col-md-12 my-2'>" +
            "<form class='d-flex' autofill='false' onsubmit='(event)=>{event.preventDefault();};'>" +
              "<div class='input-group w-auto'>" +
                "<div class='input-group-prepend'>" +
                  "<span class='input-group-text bg-transparent'>" +
                  "<i class='fas fa-filter'></i>" +
                  "</span>" +
                "</div>" +
                "<input type='text' style='width: 300px;'class='form-control d-inline' placeholder='Filter' id='input_filter_unit_" + v_tab.id + "' onchange='secondqLoadUnitListData(true, true);'>" +
              "</div>" +
              "<div class='input-group w-auto ml-1'>" +
                "<div class='input-group-prepend'>" +
                  "<span class='input-group-text bg-transparent'>" +
                  "<i class='fas fa-heartbeat'></i>" +
                  "</span>" +
                "</div>" +
                "<select class='form-control d-inline' style='width: 300px;' id='sel_filter_unit_" + v_tab.id + "' onchange='secondqLoadUnitListData(true, true);'>" +
                  "<option selected='selected' value=0 >ALL</option>" +
                  "<option value=1 >OK</option>" +
                  "<option value=2 >CRITICAL</option>" +
                  "<option value=3 >CRITICAL (OK)</option>" +
                  "<option value=4 >HIGH</option>" +
                  "<option value=5 >HIGH (OK)</option>" +
                  "<option value=6 >MEDIUM</option>" +
                  "<option value=7 >MEDIUM (OK)</option>" +
                  "<option value=8 >LOW</option>" +
                  "<option value=9 >LOW (OK)</option>" +
                  "<option value=10 >UNKNOWN</option>" +
                  "<option value=11 >UNKNOWN (OK)</option>" +
                  "<option value=12 >ENABLED</option>" +
                  "<option value=13 >DISABLED</option>" +
                "</select>" +
              "</div>" +
              "<button type='submit' disabled style='display: none' aria-hidden='true'></button>" +
              "<button title='Refresh' type='button' style='vertical-align: baseline' class='btn btn-primary btn-sm ml-1' onclick='(event)=>{event.preventDefault();}; secondqLoadUnitListData(true);'><i class='fas fa-sync'></i></button>" +
            "</form>" +
          "</div>" +
        "</div>" +
        "<div class='row mb-2'>" +
          "<div class='col-md-12'>" +
            "<div id='dashboard_unit_list_pagination_" + v_tab.id + "'></div>" +
          "</div>" +
        "</div>" +
        "<div class='row mb-2'>" +
          "<div class='col-md-12'>" +
            "<div id='dashboard_unit_list_" + v_tab.id + "' class='ht_text_ellipsis' style='width: 100%; height: 730px; overflow: hidden;'/></div>" +
          "</div>" +
        "</div>" +
      "</div>";

      var v_div = document.getElementById('div_' + v_tab.id);
      v_div.innerHTML = v_html;
      var v_dashboard_unit_list = document.getElementById('dashboard_unit_list_' + v_tab.id);
      var v_sel_filter_unit = document.getElementById('sel_filter_unit_' + v_tab.id);
      var v_input_filter_unit = document.getElementById('input_filter_unit_' + v_tab.id);

      if (p_filter!=null) {
        if (p_filter.filter_all!=null)
          v_input_filter_unit.value = p_filter.filter_all;
        if (p_filter.filter_severity!=null)
          v_sel_filter_unit.value = p_filter.filter_severity;
      }

      //Setting up unit check grid
      var columnProperties = [];

      var col = new Object();
      col.readOnly = true;
      col.title =  'Customer';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Host';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Unit Check';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'State';
      col.width = '80px';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Time Elapsed';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Actions';
      columnProperties.push(col);


      var col = new Object();
      col.readOnly = true;
      col.title =  'Thresholds (C / H / M / L)';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Value';
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Metrics';
      columnProperties.push(col);

      var ht = new Handsontable(v_dashboard_unit_list,
      {
        licenseKey: 'non-commercial-and-evaluation',
        data: [],
        columns : columnProperties,
        colHeaders : true,
        rowHeaders : false,
        fillHandle:false,
        stretchH: (window.mediaConfig === "desktop-xl" || window.mediaConfig === "desktop-lg") ? 'last' : undefined,
        copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
        manualColumnResize: true,
        autoColumnSize : true,
        afterOnCellMouseUp: function(event,coords) {
        },
        cells: function (row, col, prop) {

            var cellProperties = {};

            if (col!= 0 && col!=1 && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row]!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row].ok==true)
              cellProperties.renderer = secondqGrayRenderer;
            else if (col==3)
              cellProperties.renderer = severityRenderer;
            else
              cellProperties.renderer = centerMiddleRenderer;

            return cellProperties;
        },
        mergeCells: true,
        contextMenu: {
          callback: function (key, options) {
            if (key === 'ack') {
              ackUnits(this,'unit_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'remove_ack') {
              removeAckUnits(this,'unit_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'downtime') {
              downtimeUnits(this,'unit_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'remove_downtime') {
              removeDowntimeUnits(this,'unit_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'enable') {
              enableUnits(this,'unit_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'disable') {
              disableUnits(this,'unit_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'change_thresholds') {
              changeThresholdUnits(this,'unit_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data);
            }
            else if (key === 'change_key') {
              changeKeyUnit(this,'unit_list',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data);
            }
          },
          items: {
            "ack": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-check cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Acknowledge</div>'},
            "remove_ack": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-check cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">REMOVE Acknowledge</div>'},
            "downtime": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-wrench cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Set Downtime</div>'},
            "remove_downtime": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-wrench cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">REMOVE Downtime</div>'},
            "change_thresholds": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-retweet cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Change Thresholds</div>'},
            "enable": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-power-off cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Enable (superuser)</div>'},
            "disable": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-power-off cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Disable (superuser)</div>'},
            "change_key": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-key cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Change Key (superuser)</div>'}
          }
        }
      });

      var v_tag = {
        tab_id: v_tab.id,
        mode: 'secondq_unit_list',
        div_unit_list: v_dashboard_unit_list,
        ht_units: ht,
        load_pending: false,
        status_data: null,
        sel_filter: v_sel_filter_unit,
        input_filter: v_input_filter_unit,
        div_pagination: document.getElementById('dashboard_unit_list_pagination_' + v_tab.id),
        current_page: 0
      };
      v_tab.tag = v_tag;

      secondqAdjustHeights();
      secondqChangeTabTitle(v_tab.tag);
      secondqLoadUnitListData(true);
      endLoading();

    },50);
  }
}

function secondqLoadCustomerListData(p_loading, p_reset_page) {
  try {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.load_pending = false;

    if (p_reset_page) {
      v_tab_tag.current_page = 0;
    }

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'secondq_load_customer_list_data',
      p_data: {
        'input_filter': v_tab_tag.input_filter.value,
        'page': v_tab_tag.current_page
      },
      p_callback: function(p_data) {

        secondqBuildPagination(v_tab_tag.div_pagination,v_tab_tag.current_page,p_data.num_pages,secondqCustomerListSelectPage);

        v_tab_tag.status_data = p_data.customers_status_data;

        var hotOptions = {}
        hotOptions.mergeCells = [];
        v_tab_tag.ht_customers.updateSettings(hotOptions);

        v_tab_tag.ht_customers.loadData(p_data.customers_data);

        secondqSetRefreshCallback(v_tab_tag,
        function() {
          secondqLoadCustomerListData(false);
        });

      },
      p_loading: p_loading,
      p_check_database_connection: false
    });
  }
  // Error, schedule another run
  catch(err) {
    secondqSetRefreshCallback(v_tab_tag,
    function() {
      secondqLoadCustomerListData(false);
    });
  }
}

function secondqLoadHostListData(p_loading, p_reset_page) {
  try {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.load_pending = false;

    if (p_reset_page) {
      v_tab_tag.current_page = 0;
    }

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'secondq_load_host_list_data',
      p_data: {
        'sel_filter': v_tab_tag.sel_filter.value,
        'input_filter': v_tab_tag.input_filter.value,
        'page': v_tab_tag.current_page
      },
      p_callback: function(p_data) {

        secondqBuildPagination(v_tab_tag.div_pagination,v_tab_tag.current_page,p_data.num_pages,secondqHostListSelectPage);

        v_tab_tag.status_data = p_data.hosts_status_data;

        var hotOptions = {}
        hotOptions.mergeCells = [];
        v_tab_tag.ht_hosts.updateSettings(hotOptions);

        v_tab_tag.ht_hosts.loadData(p_data.hosts_data);

        var hotOptions = {}
        hotOptions.mergeCells = p_data.aggregation_data;
        v_tab_tag.ht_hosts.updateSettings(hotOptions);

        secondqSetRefreshCallback(v_tab_tag,
        function() {
          secondqLoadHostListData(false);
        });

      },
      p_loading: p_loading,
      p_check_database_connection: false
    });
  }
  // Error, schedule another run
  catch(err) {
    secondqSetRefreshCallback(v_tab_tag,
    function() {
      secondqLoadHostListData(false);
    });
  }
}

function secondqLoadUnitListData(p_loading, p_reset_page) {
  try {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.load_pending = false;

    if (p_reset_page) {
      v_tab_tag.current_page = 0;
    }

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'secondq_load_unit_list_data',
      p_data: {
        'sel_filter': v_tab_tag.sel_filter.value,
        'input_filter': v_tab_tag.input_filter.value,
        'page': v_tab_tag.current_page
      },
      p_callback: function(p_data) {

        secondqBuildPagination(v_tab_tag.div_pagination,v_tab_tag.current_page,p_data.num_pages,secondqUnitListSelectPage);

        v_tab_tag.status_data = p_data.units_status_data;

        var hotOptions = {}
        hotOptions.mergeCells = [];
        v_tab_tag.ht_units.updateSettings(hotOptions);

        v_tab_tag.ht_units.loadData(p_data.units_data);

        var hotOptions = {}
        hotOptions.mergeCells = p_data.aggregation_data;
        v_tab_tag.ht_units.updateSettings(hotOptions);

        secondqSetRefreshCallback(v_tab_tag,
        function() {
          secondqLoadUnitListData(false);
        });

      },
      p_loading: p_loading,
      p_check_database_connection: false
    });
  }
  // Error, schedule another run
  catch(err) {
    secondqSetRefreshCallback(v_tab_tag,
    function() {
      secondqLoadUnitListData(false);
    });
  }
}

function secondqBuildPagination(p_div, p_current_page, p_num_pages, p_callback) {

    var v_nav = document.createElement('nav');
    var v_ul = document.createElement('ul');
    v_ul.className = 'pagination m-0';

    for (var i=0; i<p_num_pages; i++) {
      var v_li = document.createElement('li');
      if (p_current_page==i)
        v_li.className = 'page-item active';
      else {
        v_li.className = 'page-item';
        if (p_callback!=null)
          v_li.onclick = (function(current_page) {
            return function() {
              p_callback(current_page);
            }
          })(i);
      }
      var v_a = document.createElement('a');
      v_a.className = 'page-link';
      v_a.innerHTML = i;
      v_a.href = '#';
      v_li.appendChild(v_a);
      v_ul.appendChild(v_li);
    }
    v_nav.appendChild(v_ul);

    p_div.innerHTML = '';
    p_div.appendChild(v_nav);
    secondqAdjustHeights();
}

function secondqUnitListSelectPage(p_page) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  v_tab_tag.current_page = p_page;
  secondqLoadUnitListData(true);
}

function secondqHostListSelectPage(p_page) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  v_tab_tag.current_page = p_page;
  secondqLoadHostListData(true);
}

function secondqCustomerListSelectPage(p_page) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  v_tab_tag.current_page = p_page;
  secondqLoadCustomerListData(true);
}
