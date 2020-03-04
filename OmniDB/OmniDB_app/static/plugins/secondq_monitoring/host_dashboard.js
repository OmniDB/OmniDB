function secondqCreateHostDashboard(p_customer_id, p_host_id) {

  if (!secondqSelectExistingTab('secondq_host_dashboard',{customer_id: p_customer_id, host_id: p_host_id})) {
    startLoading();
    setTimeout(function() {

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
      p_name: '<i class="fas fa-server icon-tab-title"></i>',
      p_selectFunction: function() {
        if(this.tag != null) {
          secondqChangeTabTitle(this.tag);
          secondqAdjustHeights();
          if (this.tag.load_pending) {
            secondqLoadHostDashboardData(true,'all');
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
      "<div class='row'>" +
        "<div class='col-md-12 mt-2'>" +
          "<h6 class='text-center'>" +
          "<span id='dashboard_host_details_customer_" + v_tab.id + "' class='secondq_link' onclick='secondqCreateCustomerDashboard(" + p_customer_id + ");'></span>" +
          " - <span id='dashboard_host_details_host_" + v_tab.id + "'></span>" +
          " <button title='Refresh' class='btn btn-secondary btn-sm' onclick='secondqLoadHostDashboardData(true,\"all\");'><i class='fas fa-sync'></i></button>" +
          " <button class='btn btn-secondary btn-sm' onclick='secondqHostActions(event);'>Actions</button></h6>" +
        "</div>" +
      "</div>" +
      "<div class='row mb-2'>" +
        "<div class='col-md-5'>" +
          "<div class='card'>" +
            "<div class='card-body'>" +
              "<div class='container text-center' style='height: 250px; overflow: auto;'>" +
                "<div class='row my-2 d-none'>" +
                  "<div class='col-md-4'>Token</div>" +
                  "<div class='col-md-8'><span id='dashboard_host_details_token_" + v_tab.id + "'></div>" +
                "</div>" +
                "<div class='row my-2'>" +
                  "<div class='col-md-4'>Status (Elapsed)</div>" +
                  "<div class='col-md-8'><span id='dashboard_host_details_status_" + v_tab.id + "'></div>" +
                "</div>" +
                "<div class='row my-2'>" +
                  "<div class='col-md-4'>Max severity</div>" +
                  "<div class='col-md-8'><span id='dashboard_host_details_severity_" + v_tab.id + "'></span></div>" +
                "</div>" +
                "<div class='row my-2'>" +
                  "<div class='col-md-4'>Actions</div>" +
                  "<div class='col-md-8'><span id='dashboard_host_details_actions_" + v_tab.id + "'></span></div>" +
                "</div>" +
                "<h6 class='mt-2'>Units</h6>" +
                "<div class='row mt-6'>" +

                  "<div class='col-md-12'>" +
                    "<canvas id='secondq_tactical_chart_units_pie_" + v_tab.id + "'/>" +
                  "</div>" +
                "</div>" +
              "</div>" +
            "</div>" +
          "</div>" +
        "</div>" +
        "<div class='col-md-7'>" +
              "<div class='text-center' style='height: 280px; overflow: auto;'>" +
                "<div id='secondq_dashboard_service_tab_list_" + v_tab.id + "'></div>" +
              "</div>" +
        "</div>" +
        "</div>" +
      "</div>" +
      "<div id='dashboard_unit_list_" + v_tab.id + "' class='ht_text_ellipsis' style='width: 100%; height: 200px; overflow: hidden;'/></div>";

      var v_div = document.getElementById('div_' + v_tab.id);
      v_div.innerHTML = v_html;
      var v_dashboard_unit_list = document.getElementById('dashboard_unit_list_' + v_tab.id);

      // Creating service tab list
      var v_service_tabs = createTabControl({ p_div: 'secondq_dashboard_service_tab_list_' + v_tab.id });

      var v_system_tab = v_service_tabs.createTab(
        {
          p_name: 'Host',
          p_close: false
        });

      var v_postgresql_tab = v_service_tabs.createTab(
        {
          p_name: 'PostgreSQL',
          p_close: false,
          p_disabled: true
        });

      var v_barman_tab = v_service_tabs.createTab(
        {
          p_name: 'Barman',
          p_close: false,
          p_disabled: true
        });

        var v_system_tab_info_summary_data = [
          {id: 'dashboard_host_details_data_elapsed_' + v_tab.id, label: 'Last Data Received (Elapsed)'},
          {id: 'dashboard_host_details_hostname_' + v_tab.id, label: 'Hostname/IP'},
          {id: 'dashboard_host_details_timezone_' + v_tab.id, label: 'Timezone'},
          {id: 'dashboard_host_details_os_' + v_tab.id, label: 'OS'},
          {id: 'dashboard_host_details_resources_' + v_tab.id, label: 'Resources'},
        ];

        var v_system_tab_info_summary_html = '';

        for (var i = 0; i < v_system_tab_info_summary_data.length; i++) {
          v_system_tab_info_summary_html +=
          "<div class='col-6'>" +
            "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
              "<label class='mb-0'>" +
                "<strong>" + v_system_tab_info_summary_data[i].label + "</strong>" +
              "</label>" +
              "<div class='col'>" +
                "<span id='" + v_system_tab_info_summary_data[i].id + "'></span>" +
              "</div>" +
            "</div>" +
          "</div>";
        }

        if (v_system_tab_info_summary_data.length % 2 !== 0) {
          v_system_tab_info_summary_html +=
          "<div class='col-6'>" +
            "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
              "<div class='col'>&nbsp;</div>" +
            "</div>" +
          "</div>";
        }

        v_system_tab.elementDiv.innerHTML =
        "<div class='container-fluid'>" +
          "<h6 class='mt-2'>Info Summary <button id='dashboard_host_details_button_json_host_" + v_tab.id + "' class='btn btn-secondary btn-sm ml-1'><i class='fas fa-list mr-1'></i>More Details</button></h6>" +
          "<div class='row'>" +
            v_system_tab_info_summary_html +
          "</div>" +
          "<h6 class='mt-2'>Servers</h6>" +
          "<div id='dashboard_host_details_services_" + v_tab.id + "'></div>" +
          "<div id='dashboard_host_data_" + v_tab.id + "'></div>" +
        "</div>";

      v_service_tabs.selectTabIndex(0);

      // Units pie
      var v_2ndq_tactical_chart_units_pie = document.getElementById('secondq_tactical_chart_units_pie_' + v_tab.id);
      v_2ndq_tactical_chart_units_pie.height =80;
      var ctx = v_2ndq_tactical_chart_units_pie.getContext('2d');
      var chart_units_pie = new Chart(ctx, {
  			type: 'doughnut',
  			data: {
  				datasets: [{
  					data: [
  						0,
  						0,
  						0,
  						0,
              0,
  						0,
  					],
  					backgroundColor: [
  					'rgba(255, 0, 0, 0.75)',
  					'rgba(255, 153, 0, 0.75)',
  					'rgba(255, 224, 0, 0.75)',
            'rgba(74, 134, 232, 0.75)',
            'rgba(180, 167, 214, 0.75)',
            'rgba(240, 240, 240,0.75)',
  					'rgba(68, 169, 3, 0.75)'
  					],
  					label: 'Dataset 1'
  				}],
  				labels: [
  					'Critical',
  					'High',
  					'Medium',
            'Low',
            'Unknown',
            'Ack/Downtime',
  					'Ok'
  				]
  			},
  			options: {
          plugins: {
            datalabels: {
              anchor: 'end',
              backgroundColor: 'rgba(255,255,255,0.3)',
              borderRadius: 10,
              align: 'start',
              borderWidth: 0,
              display: function(context) {
          return context.dataset.data[context.dataIndex] !== 0; // or >= 1 or ...
       }
            },
          },
          circumference: Math.PI,
          rotation: -Math.PI,
  				responsive: true,
          maintainAspectRatio: false,
  				legend: {
            display: false,
  					position: 'top',
  				},
  				title: {
  					display: false
  				},
  				animation: {
  					animateScale: true,
  					animateRotate: true
  				}
  			}
  		}
      );
      adjustChartTheme(chart_units_pie);

      //Setting up unit check grid
      var columnProperties = [];

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
        //stretchH: 'last',
        copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
        manualColumnResize: true,
        autoColumnSize : true,
        afterOnCellMouseUp: function(event,coords) {
        },
        cells: function (row, col, prop) {

            var cellProperties = {};

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row].ok==true)
              cellProperties.renderer = secondqGrayRenderer;
            else if (col==1)
              cellProperties.renderer = severityRenderer;
            else
              cellProperties.renderer = centerMiddleRenderer;

            return cellProperties;
        },
        mergeCells: true,
        contextMenu: {
          callback: function (key, options) {
            if (key === 'ack') {
              ackUnits(this,'host_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'remove_ack') {
              removeAckUnits(this,'host_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'downtime') {
              downtimeUnits(this,'host_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'remove_downtime') {
              removeDowntimeUnits(this,'host_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'enable') {
              enableUnits(this,'host_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'disable') {
              disableUnits(this,'host_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'change_thresholds') {
              changeThresholdUnits(this,'host_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data);
            }
            else if (key === 'change_key') {
              changeKeyUnit(this,'host_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data);
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
        tab_object: v_tab,
        mode: 'secondq_host_dashboard',
        div_unit_list: v_dashboard_unit_list,
        ht_units: ht,
        chart_units: chart_units_pie,
        load_pending: false,
        status_data: null,
        customer: null,
        host: null,
        customer_id: p_customer_id,
        host_id: p_host_id,
        button_json_host: document.getElementById('dashboard_host_details_button_json_host_' + v_tab.id),
        details_customer: document.getElementById('dashboard_host_details_customer_' + v_tab.id),
        details_host: document.getElementById('dashboard_host_details_host_' + v_tab.id),
        details_token: document.getElementById('dashboard_host_details_token_' + v_tab.id),
        details_status: document.getElementById('dashboard_host_details_status_' + v_tab.id),
        details_severity: document.getElementById('dashboard_host_details_severity_' + v_tab.id),
        details_actions: document.getElementById('dashboard_host_details_actions_' + v_tab.id),
        details_elapsed: document.getElementById('dashboard_host_details_data_elapsed_' + v_tab.id),
        details_hostname: document.getElementById('dashboard_host_details_hostname_' + v_tab.id),
        details_timezone: document.getElementById('dashboard_host_details_timezone_' + v_tab.id),
        details_os: document.getElementById('dashboard_host_details_os_' + v_tab.id),
        details_resources: document.getElementById('dashboard_host_details_resources_' + v_tab.id),
        details_services: document.getElementById('dashboard_host_details_services_' + v_tab.id),
        div_data: document.getElementById('dashboard_host_data_' + v_tab.id),
        service_tab_list: v_service_tabs,
      };
      v_tab.tag = v_tag;

      secondqAdjustHeights();
      secondqLoadHostDashboardData(true,'all');
      endLoading();

    },50);
  }
}

function secondqLoadHostDashboardData(p_loading, p_mode) {
  try {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.load_pending = false;

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'secondq_load_host_dashboard_data',
      p_data: {
        'p_mode': p_mode,
        'p_customer_id': v_tab_tag.customer_id,
        'p_host_id': v_tab_tag.host_id
      },
      p_callback: function(p_data) {

        if (p_data.units!=null) {
          v_tab_tag.status_data = p_data.units.units_status_data;

          v_tab_tag.ht_units.loadData(p_data.units.units_data);
        }

        if (p_data.details!=null) {

          //Chart data
          v_tab_tag.chart_units.data.datasets[0].data = [
            p_data.details.chart.chart_unit_critical_count,
            p_data.details.chart.chart_unit_high_count,
            p_data.details.chart.chart_unit_medium_count,
            p_data.details.chart.chart_unit_low_count,
            p_data.details.chart.chart_unit_unknown_count,
            p_data.details.chart.chart_unit_problem_ok_count,
            p_data.details.chart.chart_unit_ok_count
          ];

          v_tab_tag.chart_units.update();


          // Details data
          v_tab_tag.dashboard_status_data = p_data.details;

          v_tab_tag.tab_object.renameTab('<i class="fas fa-server icon-tab-title"></i> ' + p_data.details.server)

          v_tab_tag.details_host.innerHTML = p_data.details.server;
          v_tab_tag.host = p_data.details.server;
          v_tab_tag.details_customer.innerHTML = p_data.details.customer;
          v_tab_tag.customer = p_data.details.customer;

          v_tab_tag.details_token.innerHTML = p_data.details.token;

          secondqChangeTabTitle(v_tab_tag);

          v_tab_tag.details_status.innerHTML = p_data.details.status;
          v_tab_tag.details_severity.innerHTML = "<span class='secondq_notification_severity_text secondq_status_box_" + p_data.details.max_severity + "'>" + p_data.details.max_severity + "</span>";
          v_tab_tag.details_actions.innerHTML = "";

          if (p_data.details.ack) {
            v_tab_tag.details_actions.innerHTML = "<i class='secondq_pointer fas fa-thumbs-up mr-2 secondq_status_icon' onclick='secondqShowAckDetails(\"dashboard\",0,this);'></i>";
          }
          if (p_data.details.downtime) {
            v_tab_tag.details_actions.innerHTML = v_tab_tag.details_actions.innerHTML + "<i class='secondq_pointer fas fa-wrench mr-2 secondq_status_icon' onclick='secondqShowDowntimeDetails(\"dashboard\",0,this);'></i>";
          }
          if (!p_data.details.enabled) {
            v_tab_tag.details_actions.innerHTML = v_tab_tag.details_actions.innerHTML + "<i class='fas fa-power-off mr-2 secondq_status_icon' title='Disabled'></i>";
          }

          if (p_data.details.data_json!=null) {
            v_tab_tag.details_elapsed.innerHTML = p_data.details.data_elapsed;
            v_tab_tag.details_hostname.innerHTML = p_data.details.data_json.data.system.hostname;
            v_tab_tag.details_timezone.innerHTML = p_data.details.data_json.data.system.timezone;
            v_tab_tag.details_os.innerHTML = p_data.details.data_json.data.system.version;
            v_tab_tag.details_resources.innerHTML = p_data.details.data_json.data.system.memory + ' RAM / ' + p_data.details.data_json.data.system.cpu_count + ' cores';

            v_tab_tag.button_json_host.onclick = function() {
              secondqViewJsonData(p_data.details.data_json.data.system);
            }

            v_tab_tag.details_services.innerHTML = '';

            v_tab_tag.service_tab_list.disableTabIndex(1);
            v_tab_tag.service_tab_list.disableTabIndex(2);

            for (var i=0; i<p_data.details.data_json.data.services.length; i++) {
              var v_service = p_data.details.data_json.data.services[i];
              var v_row = document.createElement('div');
              v_row.className = 'row';
              var v_col1 = document.createElement('div');
              v_col1.className = 'col col-md-4 my-2';
              var v_span1 = document.createElement('span');
              v_span1.className = 'secondq_link';
              v_span1.innerHTML = v_service;
              var v_col2 = document.createElement('div');
              v_col2.className = 'col col-md-8 my-2';

              if (v_service=='postgresql') {
                v_span1.onclick = function() {
                  v_tab_tag.service_tab_list.selectTabIndex(1);
                }
                v_col2.innerHTML = p_data.details.data_json.data.postgresql.num_version + ', Port ' + p_data.details.data_json.data.postgresql.port;
                v_tab_tag.service_tab_list.enableTabIndex(1);

                var v_work_mem = '';
                if (p_data.details.data_json.data.postgresql.settings['work_mem']!=null)
                  v_work_mem = p_data.details.data_json.data.postgresql.settings['work_mem'].value;

                var v_max_connections = '';
                if (p_data.details.data_json.data.postgresql.settings['max_connections']!=null)
                  v_max_connections = p_data.details.data_json.data.postgresql.settings['max_connections'].value;

                var v_shared_buffers = '';
                if (p_data.details.data_json.data.postgresql.settings['shared_buffers']!=null)
                  v_shared_buffers = p_data.details.data_json.data.postgresql.settings['shared_buffers'].value;

                var v_data_dir = '';
                if (p_data.details.data_json.data.postgresql.settings['data_directory']!=null)
                  v_data_dir = p_data.details.data_json.data.postgresql.settings['data_directory'].value;

                var v_html = '';

                // Filling PostgreSQL's tab
                var postgresql_info_summary_data = [
                  {label: 'Version/Port', text: p_data.details.data_json.data.postgresql.num_version},
                  {label: 'Role', text: p_data.details.data_json.data.postgresql.role},
                  {label: 'Uptime', text: p_data.details.data_json.data.postgresql.uptime},
                  {label: 'max_connections', text: v_max_connections},
                  {label: 'work_mem', text: v_work_mem},
                  {label: 'shared_buffers', text: v_shared_buffers},
                  {label: 'data_directory', text: v_data_dir}
                ];

                var postgresql_info_summary_html = '';

                for (var i = 0; i < postgresql_info_summary_data.length; i++) {
                  postgresql_info_summary_html +=
                  "<div class='col-6'>" +
                    "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
                      "<label class='mb-0'>" +
                        "<strong>" + postgresql_info_summary_data[i].label + "</strong>" +
                      "</label>" +
                      "<div class='col'>" +
                        "<span>" + postgresql_info_summary_data[i].text + "</span>" +
                      "</div>" +
                    "</div>" +
                  "</div>";
                }
                if (postgresql_info_summary_data.length % 2 !== 0) {
                  postgresql_info_summary_html +=
                  "<div class='col-6'>" +
                    "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
                      "<div class='col'>&nbsp;</div>" +
                    "</div>" +
                  "</div>";
                }

                v_html =
                "<div class='container-fluid'>" +
                  "<h6 class='mt-2'>Info Summary <button id='view_json_postgresql_" + v_connTabControl.selectedTab.tag.tabControl.selectedTab.id + "' class='btn btn-secondary btn-sm ml-1'><i class='fas fa-list mr-1'></i>More Details</button></h6>" +
                  "<div class='row'>" +
                    postgresql_info_summary_html +
                  "</div>" +
                "</div>";

                v_tab_tag.service_tab_list.tabList[1].elementDiv.innerHTML = v_html;

                document.getElementById('view_json_postgresql_' + v_connTabControl.selectedTab.tag.tabControl.selectedTab.id).onclick = function() {
                  secondqViewJsonData(p_data.details.data_json.data.postgresql);
                }
              }
              else if (v_service=='barman') {
                v_span1.onclick = function() {
                  v_tab_tag.service_tab_list.selectTabIndex(2);
                }
                v_tab_tag.service_tab_list.enableTabIndex(2);

                var v_diagnose = p_data.details.data_json.data.barman.diagnose;

                if (v_diagnose!=null) {

                  v_col2.innerHTML = v_diagnose.global.system_info.barman_ver;

                  var v_html = '';

                  // Filling Barman's tab
                  var barman_info_summary_data = [
                    {label: 'Version', text: v_diagnose.global.system_info.barman_ver},
                    {label: 'Barman home', text: v_diagnose.global.config.barman_home},
                    {label: 'Log file', text: v_diagnose.global.config.log_file}
                  ];

                  var barman_info_summary_html = '';

                  for (var i = 0; i < barman_info_summary_data.length; i++) {
                    barman_info_summary_html +=
                    "<div class='col-6'>" +
                      "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
                        "<label class='mb-0'>" +
                          "<strong>" + barman_info_summary_data[i].label + "</strong>" +
                        "</label>" +
                        "<div class='col'>" +
                          "<span>" + barman_info_summary_data[i].text + "</span>" +
                        "</div>" +
                      "</div>" +
                    "</div>";
                  }

                  if (barman_info_summary_data.length % 2 !== 0) {
                    barman_info_summary_html +=
                    "<div class='col-6'>" +
                      "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
                        "<div class='col'>&nbsp;</div>" +
                      "</div>" +
                    "</div>";
                  }

                  v_html =
                  "<div class='container-fluid'>" +
                    "<h6 class='mt-2'>Info Summary <button id='view_json_barman_" + v_connTabControl.selectedTab.tag.tabControl.selectedTab.id + "' class='btn btn-secondary btn-sm ml-1'><i class='fas fa-list mr-1'></i>More Details</button></h6>" +
                    "<div class='row'>" +
                      barman_info_summary_html +
                    "</div>" +
                    "<h6 class='mt-2'>Servers</h6>";

                  for (var server in v_diagnose.servers) {
                    if (Object.prototype.hasOwnProperty.call(v_diagnose.servers, server)) {
                      var v_backups = 0;
                      var v_failed_backups = 0;
                      for (var backup in v_diagnose.servers[server].backups) {
                        if (Object.prototype.hasOwnProperty.call(v_diagnose.servers[server].backups, backup)) {
                          v_backups = v_backups + 1;
                          if (v_diagnose.servers[server].backups[backup].status=='FAILED')
                            v_failed_backups = v_failed_backups + 1;
                        }
                      }
                      v_html +=
                      "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
                        "<label class='mb-0'>" +
                          "<strong>" + server + "</strong>" +
                        "</label>" +
                        "<div class='col'>" +
                          "<span>" + v_backups + " backups (" + v_failed_backups + " failed)</span>" +
                        "</div>" +
                      "</div>";
                    }
                  }

                  v_html += "</div>";

                  v_tab_tag.service_tab_list.tabList[2].elementDiv.innerHTML = v_html;

                  document.getElementById('view_json_barman_' + v_connTabControl.selectedTab.tag.tabControl.selectedTab.id).onclick = function() {
                    secondqViewJsonData(p_data.details.data_json.data.barman);
                  }

                }

              }

              v_col1.appendChild(v_span1);
              v_row.appendChild(v_col1);
              v_row.appendChild(v_col2);
              v_tab_tag.details_services.appendChild(v_row);
            }

        }

        if (p_mode == 'all') {
          secondqSetRefreshCallback(v_tab_tag,
          function() {
            secondqLoadHostDashboardData(false,'all');
          });
        }
      }
      },
      p_loading: p_loading,
      p_check_database_connection: false
    });
  }
  // Error, schedule another run
  catch(err) {
    if (p_mode == 'all') {
      secondqSetRefreshCallback(v_tab_tag,
      function() {
        secondqLoadHostDashboardData(false,'all');
      });
    }
  }
}

function secondqHostActions(e) {
  customMenu(
    {
      x:e.clientX+5,
      y:e.clientY+5
    },
    [
      {
  			text: 'Acknowledge',
  			icon: 'fas cm-all fa-check',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_data = [
            {
              'customer_id': v_tab_tag.customer_id,
              'server_id': v_tab_tag.host_id
            }
          ];
          ackUnitsCall(v_data,'host_dashboard');
  			}
  		},
      {
  			text: 'REMOVE Acknowledge',
  			icon: 'fas cm-all fa-check',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_data = [
            {
              'customer_id': v_tab_tag.customer_id,
              'server_id': v_tab_tag.host_id
            }
          ];
          removeAckUnitsCall(v_data,'host_dashboard');
  			}
  		},
      {
  			text: 'Set Downtime',
  			icon: 'fas cm-all fa-wrench',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_data = [
            {
              'customer_id': v_tab_tag.customer_id,
              'server_id': v_tab_tag.host_id
            }
          ];
          downtimeUnitsCall(v_data,'host_dashboard');
  			}
  		},
      {
  			text: 'REMOVE Downtime',
  			icon: 'fas cm-all fa-wrench',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_data = [
            {
              'customer_id': v_tab_tag.customer_id,
              'server_id': v_tab_tag.host_id
            }
          ];
          removeDowntimeUnitsCall(v_data,'host_dashboard');
  			}
  		},
      {
  			text: 'Enable (superuser)',
  			icon: 'fas cm-all fa-power-off',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_data = [
            {
              'customer_id': v_tab_tag.customer_id,
              'server_id': v_tab_tag.host_id
            }
          ];
          enableUnitsCall(v_data,'host_dashboard');
  			}
  		},
      {
  			text: 'Disable (superuser)',
  			icon: 'fas cm-all fa-power-off',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_data = [
            {
              'customer_id': v_tab_tag.customer_id,
              'server_id': v_tab_tag.host_id
            }
          ];
          disableUnitsCall(v_data,'host_dashboard');
  			}
  		},
      {
  			text: 'Change Token (superuser)',
  			icon: 'fas cm-all fa-key',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          secondqChangeHostToken(v_tab_tag.customer_id, v_tab_tag.host_id);
  			}
  		}
    ],
    null);
}

function secondqChangeHostToken(p_customer_id, p_host_id) {
  showConfirm('WARNING, changing the token requires changing the configuration in the host.',
  function() {

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'change_host_token',
      p_data: {
        'customer_id': p_customer_id,
        'host_id': p_host_id
      },
      p_callback: function(p_data) {

        if (p_data.error==true)
          showAlert(p_data.message);
        else
        {
          secondqLoadHostDashboardData(true,'all');
        }

      },
      p_loading: true,
      p_check_database_connection: false
    });

  },
  null,
  null);
}
