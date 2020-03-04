/// <summary>
/// Startup function.
/// </summary>
$(function () {

  window.addEventListener("beforeunload", function (event) {
    event.returnValue = "Your work will be lost.";
  });

  secondqMediaQuery();

  activateHook('windowResize',
  function() {
    secondqMediaQuery();
    secondqAdjustHeights();
  });


  //Loading sound
  //secondq_sound = document.createElement('audio');
  //var secondq_sound_source = document.createElement('source');
  //secondq_sound_source.type = 'audio/mpeg';
  //secondq_sound_source.src = getPluginPath('secondq_monitoring') + 'paranoid.mp3';

  //secondq_sound.appendChild(secondq_sound_source);
  //document.body.appendChild(secondq_sound);

  let tempVersioning = Date.now();

  //Loading leaflet
  var importedjs = document.createElement('script');
  importedjs.src = getPluginPath('secondq_monitoring') + 'leaflet.js';
  document.head.appendChild(importedjs);

  //Loading helper
  var importedjs = document.createElement('script');
  importedjs.src = getPluginPath('secondq_monitoring') + 'helper.js?v' + tempVersioning;
  document.head.appendChild(importedjs);

  //Loading customer file
  var importedjs = document.createElement('script');
  importedjs.src = getPluginPath('secondq_monitoring') + 'customer_dashboard.js?v' + tempVersioning;
  document.head.appendChild(importedjs);

  //Loading host file
  var importedjs = document.createElement('script');
  importedjs.src = getPluginPath('secondq_monitoring') + 'host_dashboard.js?v' + tempVersioning;
  document.head.appendChild(importedjs);

  //Loading unit file
  var importedjs = document.createElement('script');
  importedjs.src = getPluginPath('secondq_monitoring') + 'unit_dashboard.js?v' + tempVersioning;
  document.head.appendChild(importedjs);

  //Loading lists file
  var importedjs = document.createElement('script');
  importedjs.src = getPluginPath('secondq_monitoring') + 'lists.js?v' + tempVersioning;
  document.head.appendChild(importedjs);

  var importedcss = document.createElement('link');
  importedcss.rel = 'stylesheet';
  importedcss.href = getPluginPath('secondq_monitoring') + 'leaflet.css';
  document.head.appendChild(importedcss);

  secondqCreateMonitoringTab();
  secondqCreateDashboardTab();

});

function secondqCreateMonitoringTab() {

  var v_tab_tag = createOuterTab({
    p_name: '2ndq Monitoring',
    p_image: 'fas cm-all fa-chart-line',
    p_select_function: function() {

      if (v_connTabControl.selectedTab.tag != null
       && v_connTabControl.selectedTab.tag.tabControl != null
       && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag != null) {
         var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
         secondqAdjustHeights();
         secondqChangeTabTitle(v_tab_tag);
         if (v_tab_tag.mode=='secondq_monitoring_dashboard') {
           if (v_tab_tag.load_pending) {
             secondqLoadDashboardData(true,'all');
           }
         }
         else if (v_tab_tag.mode=='secondq_customer_list') {
           if (v_tab_tag.load_pending) {
             secondqLoadCustomerListData(true);
           }
         }
         else if (v_tab_tag.mode=='secondq_host_list') {
           if (v_tab_tag.load_pending) {
             secondqLoadHostListData(true);
           }
         }
         else if (v_tab_tag.mode=='secondq_unit_list') {
           if (v_tab_tag.load_pending) {
             secondqLoadUnitListData(true);
           }
         }
         else if (v_tab_tag.mode=='secondq_host_dashboard') {
           if (v_tab_tag.load_pending) {
             secondqLoadHostDashboardData(true,'all');
           }
         }
         else if (v_tab_tag.mode=='secondq_customer_dashboard') {
           if (v_tab_tag.load_pending) {
             secondqLoadCustomerDashboardData(true,'all');
           }
         }
         else if (v_tab_tag.mode=='secondq_unit_dashboard') {
           if (v_tab_tag.load_pending) {
             secondqLoadUnitDashboardData(true,'all');
           }
         }
      }

      if(this.tag != null && this.tag.select_notification_type!=null) {

        secondqAdjustHeights();

        if (this.tag.load_pending) {

          secondqLoadDashboardData(true,'all');
        }
      }

    },
    p_before_close_function: null
  });

  var v_html =
  "<div class='container-fluid'>" +
    "<div class='row'>" +
      "<div class='col-12 d-flex'>" +

        "<div id='" + v_tab_tag.tab_id + "_div_left' class='secondq_menu_toggler bg-light'>" +
          // "<form autofill='false'>" +
          // "<input type='text' class='form-control mt-2 mb-2' id='2ndq_input_search' placeholder='Search'>" +
          // "</form>" +
          "<ul class='nav flex-column'>" +
          "  <li class='nav-item'>" +
          "    <a class='nav-link' href='#' onclick='secondqCreateDashboardTab()'><i class='fas fa-columns'></i> <span>Tactical Board</span></a>" +
          "  </li>" +
          "  <li class='nav-item'>" +
          "    <a class='nav-link' href='#' onclick='secondqCreateCustomerList()'><i class='fas fa-users'></i> <span>Customers</span></a>" +
          "  </li>" +
          "  <li class='nav-item'>" +
          "    <a class='nav-link' href='#' onclick='secondqCreateHostList()'><i class='fas fa-server'></i> <span>Hosts</span></a>" +
          "  </li>" +
          "  <li class='nav-item'>" +
          "    <a class='nav-link' href='#' onclick='secondqCreateUnitList()'><i class='fas fa-eye'></i> <span>Unit Checks</span></a>" +
          "  </li>" +
          "  <li class='nav-item'>" +
          "    <a class='nav-link'><i class='fas fa-bell'></i> <span>Notifications</span></a>" +
          "  </li>" +
          "</ul>" +
        "</div>" +
        "<div id='" + v_tab_tag.tab_id + "_div_right' style='flex-grow: 1; max-width: calc(100% - 48px); margin-left: auto;'>" +
          "<div id='" + v_tab_tag.tab_id + "_tabs' class='mt-2'></div>" +
        "</div>" +

      "</div>" +
    "</div>" +
  "</div>";

  v_tab_tag.div.innerHTML = v_html;


  var v_currTabControl = createTabControl({'p_div': v_tab_tag.tab_id + '_tabs' });

  v_tab_tag.tabControl = v_currTabControl;
  v_tab_tag.divTree = document.getElementById(v_tab_tag.tab_id + '_tree');
  v_tab_tag.connTabControl = v_connTabControl,
  v_tab_tag.mode = 'secondq_monitoring_tab';

}

function secondqCreateDashboardTab() {

  if (!secondqSelectExistingTab('secondq_monitoring_dashboard')) {

    var p_tag = v_connTabControl.selectedTab.tag;
    startLoading();
    setTimeout(function() {

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
      p_name: '<i class="fas fa-columns icon-tab-title"></i> Tactical Board',
      p_selectFunction: function() {
        if(this.tag != null && this.tag.select_notification_type!=null) {
          secondqChangeTabTitle(this.tag);
          secondqAdjustHeights();
          if (this.tag.load_pending) {
            secondqLoadDashboardData(true,'all');
          }
        }
      },
      p_close: false
    });
      p_tag.tabControl.selectTab(v_tab);

      var v_html =
      "<div class='container-fluid mt-2'>" +
        "<div class='row'>" +
          "<div class='col d-flex flex-column'>" +
            "<div class='row text-center flex-grow-1 h-50 pb-2'>" +
              "<div class='col-md-5 h-100 d-flex flex-column'>" +
                // "<div class='h-100 d-flex flex-column'>" +

                  "<div class='row' style='height: calc(100% - 172px);'>" +
                    "<div class='col-md-4 mt-2'>" +
                      "<h5>Hosts</h5>" +
                    "</div>" +
                    "<div class='col-md-8 d-flex h-100'>" +
                      "<div class='mb-auto ml-auto mr-auto mt-0' style='height: 100%; max-width: 257px; position: relative; width: 100%;'>" +
                        "<canvas id='secondq_tactical_chart_hosts_pie_" + v_tab.id + "'/>" +
                      "</div>" +
                    "</div>" +
                  "</div>" +

                  "<div class='row my-auto py-2 flex-shrink-0'>" +
                    "<div class='col-md-12'>" +
                      // "<div class='container-fluid'>" +

                        "<div class='row'>" +
                          "<div class='col-md-4'>" +
                          "</div>" +
                          "<div class='col-md-8'>" +
                            "Down" +
                          "</div>" +
                        "</div>" +

                        "<div class='row secondq_border-bottom-dashed'>" +
                          "<div class='col-md-4'>" +
                          "</div>" +
                          "<div class='col-md-8'>" +
                            "<div id='secondq_server_status_box_critical_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                          "</div>" +
                        "</div>" +

                        "<div class='row secondq_border-bottom-dashed'>" +
                          "<div class='col-md-4 my-auto'>" +
                          "Ack" +
                          "</div>" +
                          "<div class='col-md-8'>" +
                            "<div id='secondq_server_status_box_critical_ack_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                          "</div>" +
                        "</div>" +

                        "<div class='row'>" +
                          "<div class='col-md-4 my-auto'>" +
                          "Downtime" +
                          "</div>" +
                          "<div class='col-md-8'>" +
                            "<div id='secondq_server_status_box_critical_downtime_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                          "</div>" +
                        "</div>" +

                      // "</div>" +
                    "</div>" +
                  "</div>" +

                // "</div>" +
              "</div>" +
              "<div class='col-md-7 h-100 d-flex flex-column'>" +
                // "<div class='h-100 d-flex flex-column'>" +

                  "<div class='row' style='height: calc(100% - 172px);'>" +
                    "<div class='col-md-4 mt-2'>" +
                    "<h5>Units</h5>" +
                    "</div>" +
                    "<div class='col-md-8 d-flex h-100'>" +
                      "<div class=' mb-auto ml-auto mr-auto mt-0' style='height: 100%; max-width: 257px; position: relative; width: 100%;'>" +
                        "<canvas id='secondq_tactical_chart_units_pie_" + v_tab.id + "'/>" +
                      "</div>" +
                    "</div>" +
                  "</div>" +

                  "<div class='row my-auto py-2 flex-shrink-0 secondq_border-left-dashed'>" +
                    "<div class='col-md-12'>" +
                      // "<div class='container-fluid'>" +

                          "<div class='row'>" +
                            "<div class='secondq_w20'>" +
                              "Critical" +
                            "</div>" +
                            "<div class='secondq_w20'>" +
                              "High" +
                            "</div>" +
                            "<div class='secondq_w20'>" +
                              "Medium" +
                            "</div>" +
                            "<div class='secondq_w20'>" +
                              "Low" +
                            "</div>" +
                            "<div class='secondq_w20'>" +
                              "Unknown" +
                            "</div>" +
                          "</div>" +

                          "<div class='row justify-content-center secondq_border-bottom-dashed'>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_critical_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_high_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_medium_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_low_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_unknown_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                          "</div>" +

                          "<div class='row justify-content-center secondq_border-bottom-dashed'>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_critical_ack_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_high_ack_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_medium_ack_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_low_ack_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_unknown_ack_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                          "</div>" +

                          "<div class='row justify-content-center'>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_critical_downtime_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_high_downtime_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_medium_downtime_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_low_downtime_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                            "<div class='col'>" +
                              "<div id='secondq_unit_status_box_unknown_downtime_" + v_tab.id + "' class='mx-auto my-2 secondq_status_box'></div>" +
                            "</div>" +
                          "</div>" +

                      // "</div>" +
                    "</div>" +
                  "</div>" +

                // "</div>" +
              "</div>" +
            "</div>" +

            "<div class='row pb-1 pt-2 flex-grow-1 h-25'>" +
              "<div class='col-md-6'>" +
                "<div class='card h-100'>" +
                "  <div class='card-body d-flex flex-column'>" +
                "    <div class='text-center'><span class='secondq_notification_severity_text secondq_status_box_ack'>Critical</span> - Act NOW</div>" +
                "    <div id='secondq_dashboard_summary_critical_" + v_tab.id + "' class='secondq_dashboard_summary_box flex-grow-1 py-2 px-4'></div>" +
                "  </div>" +
                "</div>" +
              "</div>" +
              "<div class='col-md-6'>" +
                "<div class='card h-100'>" +
                "  <div class='card-body d-flex flex-column'>" +
                "    <div class='text-center'><span class='secondq_notification_severity_text secondq_status_box_ack'>High</span> - Act Soon</div>" +
                "    <div id='secondq_dashboard_summary_high_" + v_tab.id + "' class='secondq_dashboard_summary_box flex-grow-1 py-2 px-4'></div>" +
                "  </div>" +
                "</div>" +
              "</div>" +
            "</div>" +

            "<div class='row pt-3 flex-grow-1 h-25'>" +
              "<div class='col-md-6'>" +
                "<div class='card h-100'>" +
                "  <div class='card-body d-flex flex-column'>" +
                "    <div class='text-center'><span class='secondq_notification_severity_text secondq_status_box_ack'>Medium</span></div>" +
                "    <div id='secondq_dashboard_summary_medium_" + v_tab.id + "' class='secondq_dashboard_summary_box flex-grow-1 py-2 px-4'></div>" +
                "  </div>" +
                "</div>" +
              "</div>" +
              "<div class='col-md-6'>" +
                "<div class='card h-100'>" +
                "  <div class='card-body d-flex flex-column'>" +
                "    <div class='text-center'><span class='secondq_notification_severity_text secondq_status_box_ack'>Low</span></div>" +
                "    <div id='secondq_dashboard_summary_low_" + v_tab.id + "' class='secondq_dashboard_summary_box flex-grow-1 py-2 px-4'></div>" +
                "  </div>" +
                "</div>" +
              "</div>" +
            "</div>" +

          "</div>" +
          "<div class='omnidb__2ndq-tactical__notifications-container col'>" +
            "<div class='d-flex mb-2'>" +
              "<div class='text-center flex-grow-1 mr-1'>" +
                "    <select id='secondq_tactical_board_select_not_type_" + v_tab.id + "' onchange='secondqChangeNotificationType(this.value)' class='form-control form-control-sm'>" +
                "      <option value='events' selected>Notifications</option>" +
                "      <option value='problems'>Problems</option>" +
                "    </select>" +
              "</div>" +
              "<form style='width:200px;' autofill='false' onsubmit='(event)=>{event.preventDefault();};'>" +
                "<div class='input-group input-group-sm w-100'>" +
                  "<input type='text' class='form-control my-0' id='secondq_notifications-input_search' placeholder='Search' onchange='secondqLoadNotifications()'>" +
                  "<div class='input-group-append'>" +
                    "<button type='button' class='input-group-text btn btn-sm rounded-right bg-secondary border-secondary text-white'>" +
                      "<i class='fas fa-filter'></i>" +
                    "</button>" +
                  "</div>" +
                  "<button type='submit' disabled style='display: none' aria-hidden='true'></button>" +
                "</div>" +
              "</form>" +
            "</div>" +
            "<div id='secondq_tactical_board_notification_group_events_" + v_tab.id + "' class='secondq_notifications_checkbox_group'>" +
              "<div class='form-check d-inline-flex'>" +
              "  <input type='checkbox' onchange='secondqLoadNotifications()' checked class='form-check-input' id='secondq_tactical_board_checkbox_events_severity_" + v_tab.id + "'>" +
              "  <label class='form-check-label mt-1' for='secondq_tactical_board_checkbox_events_severity_" + v_tab.id + "'>Unit Checks</label>" +
              "</div>" +
              "<div class='form-check d-inline-flex ml-2'>" +
              "  <input type='checkbox' onchange='secondqLoadNotifications()' checked class='form-check-input' id='secondq_tactical_board_checkbox_events_user_" + v_tab.id + "'>" +
              "  <label class='form-check-label mt-1' for='secondq_tactical_board_checkbox_events_user_" + v_tab.id + "'>Administrative</label>" +
              "</div>" +
            "</div>" +
            "<div id='secondq_tactical_board_notification_group_problems_" + v_tab.id + "' class='secondq_notifications_checkbox_group' style='display: none;'>" +
              "<div class='form-check d-inline-flex'>" +
              "  <input type='checkbox' onchange='secondqLoadNotifications()' class='form-check-input' id='secondq_tactical_board_checkbox_problems_criticalhigh_" + v_tab.id + "'>" +
              "  <label class='form-check-label mt-1' for='secondq_tactical_board_checkbox_problems_criticalhigh_" + v_tab.id + "'>Critical + High</label>" +
              "</div>" +
            "</div>" +
            "<div id='dashboard_notification_box_" + v_tab.id + "' class='secondq_ht_invisible' style='width: 100%; height: 500px; overflow: hidden;'/></div>" +
          "</div>" +
        "</div>" +
      "</div>";

      var v_div = document.getElementById('div_' + v_tab.id);
      v_div.innerHTML = v_html;
      var v_dashboard_notification_box = document.getElementById('dashboard_notification_box_' + v_tab.id);

      //Setting up notification grid
      var columnProperties = [];

      var col = new Object();
      col.readOnly = true;
      col.title =  'Time';
      col.width = ()=>{return (window.mediaConfig === "desktop-xl" ) ? '170px' : (window.mediaConfig === "desktop-lg" ) ? '155px' : ( window.mediaConfig === "desktop-md") ? '145px' : undefined;}
      columnProperties.push(col);

      var col = new Object();
      col.readOnly = true;
      col.title =  'Data';
      col.width = ()=>{return (window.mediaConfig === "desktop-xl" ) ? '576px' : (window.mediaConfig === "desktop-lg" ) ? '360px' : ( window.mediaConfig === "desktop-md") ? '350px' : undefined;}
      columnProperties.push(col);


      var ht = new Handsontable(v_dashboard_notification_box,
      {
        licenseKey: 'non-commercial-and-evaluation',
        data: [],
        columns : columnProperties,
        colHeaders : false,
        rowHeaders : false,
        fillHandle:false,
        stretchH: ()=>{return (window.mediaConfig === "desktop-xl" || window.mediaConfig === "desktop-lg" || window.mediaConfig === "desktop-md") ? 'all' : undefined;},
        disableVisualSelection: true,
        copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
        manualColumnResize: true,
        autoColumnSize : true,
        afterOnCellMouseUp: function(event,coords) {
        },
        cells: function (row, col, prop) {
            var cellProperties = {};

            if (col==0)
              cellProperties.renderer = centerMiddleRenderer;
            else
              cellProperties.renderer = centerRenderer;

            return cellProperties;
        }
      });

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

      var v_2ndq_tactical_chart_hosts_pie = document.getElementById('secondq_tactical_chart_hosts_pie_' + v_tab.id);
      v_2ndq_tactical_chart_hosts_pie.height =80;
      var ctx = v_2ndq_tactical_chart_hosts_pie.getContext('2d');
      var chart_hosts_pie = new Chart(ctx, {
  			type: 'doughnut',
  			data: {
  				datasets: [{
  					data: [
  						0,
  						0,
  					],
  					backgroundColor: [
  					'rgba(255, 0, 0, 0.75)',
            'rgba(240, 240, 240,0.75)',
  					'rgba(68, 169, 3, 0.75)'
  					],
  					label: 'Dataset 1'
  				}],
  				labels: [
  					'Down',
            'Ack/Downtime',
  					'Up'
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
            }
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
      adjustChartTheme(chart_hosts_pie);



      var v_tag = {
        tab_id: v_tab.id,
        mode: 'secondq_monitoring_dashboard',
        //canvas_alert_chart: v_canvas_alert_chart,
        chart_units: chart_units_pie,
        chart_hosts: chart_hosts_pie,

        server_status_box_critical: document.getElementById('secondq_server_status_box_critical_' + v_tab.id),
        server_status_box_critical_ack: document.getElementById('secondq_server_status_box_critical_ack_' + v_tab.id),
        server_status_box_critical_downtime: document.getElementById('secondq_server_status_box_critical_downtime_' + v_tab.id),

        unit_status_box_critical: document.getElementById('secondq_unit_status_box_critical_' + v_tab.id),
        unit_status_box_critical_ack: document.getElementById('secondq_unit_status_box_critical_ack_' + v_tab.id),
        unit_status_box_critical_downtime: document.getElementById('secondq_unit_status_box_critical_downtime_' + v_tab.id),

        unit_status_box_high: document.getElementById('secondq_unit_status_box_high_' + v_tab.id),
        unit_status_box_high_ack: document.getElementById('secondq_unit_status_box_high_ack_' + v_tab.id),
        unit_status_box_high_downtime: document.getElementById('secondq_unit_status_box_high_downtime_' + v_tab.id),

        unit_status_box_medium: document.getElementById('secondq_unit_status_box_medium_' + v_tab.id),
        unit_status_box_medium_ack: document.getElementById('secondq_unit_status_box_medium_ack_' + v_tab.id),
        unit_status_box_medium_downtime: document.getElementById('secondq_unit_status_box_medium_downtime_' + v_tab.id),

        unit_status_box_low: document.getElementById('secondq_unit_status_box_low_' + v_tab.id),
        unit_status_box_low_ack: document.getElementById('secondq_unit_status_box_low_ack_' + v_tab.id),
        unit_status_box_low_downtime: document.getElementById('secondq_unit_status_box_low_downtime_' + v_tab.id),

        unit_status_box_unknown: document.getElementById('secondq_unit_status_box_unknown_' + v_tab.id),
        unit_status_box_unknown_ack: document.getElementById('secondq_unit_status_box_unknown_ack_' + v_tab.id),
        unit_status_box_unknown_downtime: document.getElementById('secondq_unit_status_box_unknown_downtime_' + v_tab.id),
        select_notification_type: document.getElementById('secondq_tactical_board_select_not_type_' + v_tab.id),

        summary_critical: document.getElementById('secondq_dashboard_summary_critical_' + v_tab.id),
        summary_high: document.getElementById('secondq_dashboard_summary_high_' + v_tab.id),
        summary_medium: document.getElementById('secondq_dashboard_summary_medium_' + v_tab.id),
        summary_low: document.getElementById('secondq_dashboard_summary_low_' + v_tab.id),

        div_group_events: document.getElementById('secondq_tactical_board_notification_group_events_' + v_tab.id),
        div_group_problems: document.getElementById('secondq_tactical_board_notification_group_problems_' + v_tab.id),

        checkbox_events_severity: document.getElementById('secondq_tactical_board_checkbox_events_severity_' + v_tab.id),
        checkbox_events_user: document.getElementById('secondq_tactical_board_checkbox_events_user_' + v_tab.id),
        checkbox_problems_criticalhigh: document.getElementById('secondq_tactical_board_checkbox_problems_criticalhigh_' + v_tab.id),

        div_notifications: v_dashboard_notification_box,
        ht_notifications: ht,
        load_pending: false
      };

      //Box click functions

      v_tag.server_status_box_critical.onclick = function () {
        secondqCreateHostList({
          'filter_all': '',
          'filter_severity': 2
        })
      };
      v_tag.server_status_box_critical_ack.onclick = function () {
        secondqCreateHostList({
          'filter_all': '',
          'filter_severity': 3
        })
      };
      v_tag.server_status_box_critical_downtime.onclick = function () {
        secondqCreateHostList({
          'filter_all': '',
          'filter_severity': 3
        })
      };

      v_tag.unit_status_box_critical.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 2
        })
      };
      v_tag.unit_status_box_critical_ack.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 3
        })
      };
      v_tag.unit_status_box_critical_downtime.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 3
        })
      };
      v_tag.unit_status_box_high.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 4
        })
      };
      v_tag.unit_status_box_high_ack.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 5
        })
      };
      v_tag.unit_status_box_high_downtime.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 5
        })
      };
      v_tag.unit_status_box_medium.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 6
        })
      };
      v_tag.unit_status_box_medium_ack.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 7
        })
      };
      v_tag.unit_status_box_medium_downtime.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 7
        })
      };
      v_tag.unit_status_box_low.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 8
        })
      };
      v_tag.unit_status_box_low_ack.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 9
        })
      };
      v_tag.unit_status_box_low_downtime.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 9
        })
      };
      v_tag.unit_status_box_unknown.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 10
        })
      };
      v_tag.unit_status_box_unknown_ack.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 11
        })
      };
      v_tag.unit_status_box_unknown_downtime.onclick = function () {
        secondqCreateUnitList({
          'filter_all': '',
          'filter_severity': 11
        })
      };

      v_tab.tag = v_tag;

      secondqAdjustHeights();
      secondqChangeTabTitle(v_tab.tag);
      secondqLoadDashboardData(true,'all');
      endLoading();

    },50);
  }
}

function processStatusBox(p_tag,p_data,p_type,p_severity) {
  if (p_data[p_type + '_' + p_severity + '_count'] == 0) {
    p_tag[p_type + '_status_box_' + p_severity].classList.remove('secondq_status_box_' + p_severity)
    p_tag[p_type + '_status_box_' + p_severity].classList.remove('secondq_pointer')
    p_tag[p_type + '_status_box_' + p_severity].classList.add('secondq_status_box_blank');
    p_tag[p_type + '_status_box_' + p_severity].innerHTML = '';
  }
  else {
    p_tag[p_type + '_status_box_' + p_severity].classList.add('secondq_status_box_' + p_severity)
    p_tag[p_type + '_status_box_' + p_severity].classList.add('secondq_pointer')
    p_tag[p_type + '_status_box_' + p_severity].classList.remove('secondq_status_box_blank');
    p_tag[p_type + '_status_box_' + p_severity].innerHTML = p_data[p_type + '_' + p_severity + '_count'];
  }

  if (p_data[p_type + '_' + p_severity + '_ack_count'] == 0) {
    p_tag[p_type + '_status_box_' + p_severity + '_ack'].classList.remove('secondq_status_box_ack')
    p_tag[p_type + '_status_box_' + p_severity + '_ack'].classList.remove('secondq_pointer')
    p_tag[p_type + '_status_box_' + p_severity + '_ack'].classList.add('secondq_status_box_blank');
    p_tag[p_type + '_status_box_' + p_severity + '_ack'].innerHTML = '';
  }
  else {
    p_tag[p_type + '_status_box_' + p_severity + '_ack'].classList.add('secondq_status_box_ack')
    p_tag[p_type + '_status_box_' + p_severity + '_ack'].classList.add('secondq_pointer')
    p_tag[p_type + '_status_box_' + p_severity + '_ack'].classList.remove('secondq_status_box_blank');
    p_tag[p_type + '_status_box_' + p_severity + '_ack'].innerHTML = p_data[p_type + '_' + p_severity + '_ack_count'];
  }

  if (p_data[p_type + '_' + p_severity + '_downtime_count'] == 0) {
    p_tag[p_type + '_status_box_' + p_severity + '_downtime'].classList.remove('secondq_status_box_ack')
    p_tag[p_type + '_status_box_' + p_severity + '_downtime'].classList.remove('secondq_pointer')
    p_tag[p_type + '_status_box_' + p_severity + '_downtime'].classList.add('secondq_status_box_blank');
    p_tag[p_type + '_status_box_' + p_severity + '_downtime'].innerHTML = '';
  }
  else {
    p_tag[p_type + '_status_box_' + p_severity + '_downtime'].classList.add('secondq_status_box_ack')
    p_tag[p_type + '_status_box_' + p_severity + '_downtime'].classList.add('secondq_pointer')
    p_tag[p_type + '_status_box_' + p_severity + '_downtime'].classList.remove('secondq_status_box_blank');
    p_tag[p_type + '_status_box_' + p_severity + '_downtime'].innerHTML = p_data[p_type + '_' + p_severity + '_downtime_count'];
  }

}

function secondqRenderNotifications(p_data) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

  //events
  if (v_tab_tag.select_notification_type.value=='events') {
    var v_grid_data = []

    for (var i=0; i<p_data.length; i++) {
      var v_not_row = p_data[i];
      var v_data_cell = '';

      var v_customer_text = "<span class='secondq_link' onclick='secondqCreateCustomerDashboard(" + v_not_row.customer_id + ");'>" + v_not_row.customer_name + "</span>";
      var v_server_text = "<span class='secondq_link' onclick='secondqCreateHostDashboard(" + v_not_row.customer_id + "," + v_not_row.server_id + ");'>" + v_not_row.server_name + "</span>";
      var v_unit_text = "<span class='omnidb__2ndq-tactical__notifications-unit-text badge badge-info'>All units</span>";
      if (v_not_row.su_id!=null)
        v_unit_text = "<span class='secondq_link' onclick='secondqCreateUnitDashboard(" + v_not_row.customer_id + "," + v_not_row.server_id + "," + v_not_row.su_id + ");'>" + v_not_row.unit_name + "</span>";

      if (v_not_row.type == 'severity_up' || v_not_row.type == 'severity_down' || v_not_row.type == 'no_data' || v_not_row.type == 'recovery') {
        v_data_cell = "<div class='secondq_notification_data_cell'>" + v_customer_text + " | " + v_server_text + " | " + v_unit_text + " | " + v_not_row.data.previous_state + " > <span class='secondq_notification_severity_text secondq_status_box_" + v_not_row.data.new_state + "'>" + v_not_row.data.new_state + "</span></div>";
      }
      else if (v_not_row.type == 'ack' || v_not_row.type == 'downtime' || v_not_row.type == 'remove_ack' || v_not_row.type == 'remove_downtime') {
        v_data_cell = "<div class='secondq_notification_data_cell'>" + v_customer_text + " | " + v_server_text + " | " + v_unit_text + " | " + v_not_row.data.user + "</div>";
      }
      else if (v_not_row.type == 'downtime_end' || v_not_row.type == 'enable_unit' || v_not_row.type == 'disable_unit') {
        v_data_cell = "<div class='secondq_notification_data_cell'>" + v_customer_text + " | " + v_server_text + " | " + v_unit_text + "</div>";
      }
      else if (v_not_row.type == 'customer_token_change') {
        v_data_cell = "<div class='secondq_notification_data_cell'>" + v_customer_text + "</div>";
      }
      else if (v_not_row.type == 'host_token_change') {
        v_data_cell = "<div class='secondq_notification_data_cell'>" + v_customer_text + " | " + v_server_text + "</div>";
      }
      else if (v_not_row.type == 'threshold_change') {
        v_data_cell = "<div class='secondq_notification_data_cell'>" + v_customer_text + " | " + v_server_text + " | " +
        v_unit_text + " | " + v_not_row.data.severity + " | <span class='secondq_notification_severity_text secondq_status_box_ack'>" + v_not_row.data.old + "</span> > <span class='secondq_notification_severity_text secondq_status_box_ack'>" + v_not_row.data.new + "</span>" +
        "</div>";
      }
      else if (v_not_row.type == 'unit_key_change') {
        v_data_cell = "<div class='secondq_notification_data_cell'>" + v_customer_text + " | " + v_server_text + " | " +
        v_unit_text + " | <span class='secondq_notification_severity_text secondq_status_box_ack'>" + v_not_row.data.old_key + "</span> > <span class='secondq_notification_severity_text secondq_status_box_ack'>" + v_not_row.data.new_key + "</span>" +
        "</div>";
      }

      var gridBreak = "<br />";
      v_grid_data.push(["<div class='secondq__notification_date-container'>" + p_data[i].time + gridBreak + "<span class='secondq_notification_severity_text secondq_status_box_ack'>" + v_not_row.type_name + "</span></div>",v_data_cell])
    }
    v_tab_tag.ht_notifications.loadData(v_grid_data);
  }
  //problems
  else {
    var v_grid_data = []

    for (var i=0; i<p_data.length; i++) {
      var v_not_row = p_data[i];
      var v_data_cell = '';

      var v_customer_text = "<span class='secondq_link' onclick='secondqCreateCustomerDashboard(" + v_not_row.customer_id + ");'>" + v_not_row.customer_name + "</span>";
      var v_server_text = "<span class='secondq_link' onclick='secondqCreateHostDashboard(" + v_not_row.customer_id + "," + v_not_row.server_id + ");'>" + v_not_row.server_name + "</span>";
      var v_unit_text = "<span class='secondq_link' onclick='secondqCreateUnitDashboard(" + v_not_row.customer_id + "," + v_not_row.server_id + "," + v_not_row.su_id + ");'>" + v_not_row.unit_name + "</span>";

      v_data_cell = "<div class='secondq_notification_data_cell'>" + v_customer_text + " | " + v_server_text + " | " + v_unit_text + "</div>";

      var gridBreak = "<br />";
      var v_time_cell = v_not_row.time + gridBreak;
      v_time_cell = "<div class='secondq__notification_date-container'>" + v_time_cell + "<span class='secondq_notification_severity_text secondq_status_box_" + v_not_row.state + "'>" + v_not_row.state + "</span></div>";


      v_grid_data.push([v_time_cell,v_data_cell])
    }
    v_tab_tag.ht_notifications.loadData(v_grid_data);
  }
}

function secondqChangeNotificationType(p_value) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

  if (p_value=='events') {
    v_tab_tag.div_group_events.style.display = '';
    v_tab_tag.div_group_problems.style.display = 'none';
  }
  else {
    v_tab_tag.div_group_events.style.display = 'none';
    v_tab_tag.div_group_problems.style.display = '';
  }

  secondqLoadNotifications();
}

function secondqLoadNotifications() {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  var input_filter = document.getElementById('secondq_notifications-input_search');

  callPluginFunction({
    p_plugin_name: 'secondq_monitoring',
    p_function_name: 'secondq_get_notifications',
    p_data: {
      'p_notification_type': v_tab_tag.select_notification_type.value,
      'p_check_events_severity': v_tab_tag.checkbox_events_severity.checked,
      'p_check_events_user': v_tab_tag.checkbox_events_user.checked,
      'p_check_problems_criticalhigh': v_tab_tag.checkbox_problems_criticalhigh.checked,
      'input_filter': input_filter.value,
    },
    p_callback: function(p_data) {

      secondqRenderNotifications(p_data);

    },
    p_loading: true,
    p_check_database_connection: false
  });
}

function secondqLoadDashboardData(p_loading, p_mode) {
  try {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.load_pending = false;
    var input_filter = document.getElementById('secondq_notifications-input_search');

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'secondq_load_dashboard_data',
      p_data: {
        'p_mode': p_mode,
        'p_notification_type': v_tab_tag.select_notification_type.value,
        'p_check_events_severity': v_tab_tag.checkbox_events_severity.checked,
        'p_check_events_user': v_tab_tag.checkbox_events_user.checked,
        'p_check_problems_criticalhigh': v_tab_tag.checkbox_problems_criticalhigh.checked,
	'input_filter': input_filter.value,
      },
      p_callback: function(p_data) {

        if (p_data.state_counts!=null) {
          processStatusBox(v_tab_tag,p_data.state_counts,'server','critical');
          processStatusBox(v_tab_tag,p_data.state_counts,'unit','critical');
          processStatusBox(v_tab_tag,p_data.state_counts,'unit','high');
          processStatusBox(v_tab_tag,p_data.state_counts,'unit','medium');
          processStatusBox(v_tab_tag,p_data.state_counts,'unit','low');
          processStatusBox(v_tab_tag,p_data.state_counts,'unit','unknown');

          v_tab_tag.chart_hosts.data.datasets[0].data = [
            p_data.state_counts.chart_server_critical_count,
            p_data.state_counts.chart_server_problem_ok_count,
            p_data.state_counts.chart_server_ok_count
          ];
          v_tab_tag.chart_units.data.datasets[0].data = [
            p_data.state_counts.chart_unit_critical_count,
            p_data.state_counts.chart_unit_high_count,
            p_data.state_counts.chart_unit_medium_count,
            p_data.state_counts.chart_unit_low_count,
            p_data.state_counts.chart_unit_unknown_count,
            p_data.state_counts.chart_unit_problem_ok_count,
            p_data.state_counts.chart_unit_ok_count
          ];
          v_tab_tag.chart_hosts.update();
          v_tab_tag.chart_units.update();


          //groups
          secondqBuildSummaryBox(v_tab_tag.summary_critical,p_data.state_counts.groups.critical,2);
          secondqBuildSummaryBox(v_tab_tag.summary_high,p_data.state_counts.groups.high,4);
          secondqBuildSummaryBox(v_tab_tag.summary_medium,p_data.state_counts.groups.medium,6);
          secondqBuildSummaryBox(v_tab_tag.summary_low,p_data.state_counts.groups.low,8);

        }

        if (p_data.notifications!=null) {

          secondqRenderNotifications(p_data.notifications);
        }

        if (p_mode == 'all') {
          secondqSetRefreshCallback(v_tab_tag,
          function() {
            secondqLoadDashboardData(false,'all');
          });
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
        secondqLoadDashboardData(false,'all');
      });
    }
  }
}

function secondqBuildSummaryBox(p_div,p_list,p_severity_filter) {

  var v_div_global = document.createElement('div');
  for (var i=0; i<p_list.length; i++) {
    var v_item = p_list[i];
    var v_div = document.createElement('div');
    v_div.className = 'secondq_notification_data_cell';
    var v_span1 = document.createElement('span');
    v_span1.className = 'secondq_link';
    v_span1.innerHTML = v_item.unit;

    v_span1.onclick = (function (unit) {
      return function() {
        secondqCreateUnitList({
          'filter_all': unit,
          'filter_severity': p_severity_filter
        })
      }

    })(v_item.unit);

    var v_span2 = document.createElement('span');
    v_span2.innerHTML = ': ' + v_item.count;

    v_div.appendChild(v_span1);
    v_div.appendChild(v_span2);
    v_div_global.appendChild(v_div);
  }
  p_div.innerHTML = '';
  p_div.appendChild(v_div_global);

}

function secondqChangeTabTitle(p_tag) {

  if (p_tag.mode=='secondq_monitoring_dashboard') {
    document.title = 'Tactical Board';
  }
  else if (p_tag.mode=='secondq_customer_list') {
    document.title = 'Customers';
  }
  else if (p_tag.mode=='secondq_host_list') {
    document.title = 'Hosts';
  }
  else if (p_tag.mode=='secondq_unit_list') {
    document.title = 'Unit Checks';
  }
  else if (p_tag.mode=='secondq_host_dashboard') {
    document.title = p_tag.host;
  }
  else if (p_tag.mode=='secondq_customer_dashboard') {
    document.title = p_tag.customer;
  }
  else if (p_tag.mode=='secondq_unit_dashboard') {
    document.title = p_tag.host + ' - ' + p_tag.unit;
  }
}

function secondqSelectExistingTab(p_type, p_params) {
  for (var i=0; i < v_connTabControl.selectedTab.tag.tabControl.tabList.length; i++) {
    var v_tab = v_connTabControl.selectedTab.tag.tabControl.tabList[i];
    if (v_tab.tag!=null) {
      if (p_type=='secondq_customer_dashboard') {

        if (p_type==v_tab.tag.mode && p_params.customer_id == v_tab.tag.customer_id) {
          v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);
          return true;
        }
      }
      else if (p_type=='secondq_host_dashboard') {
        if (p_type==v_tab.tag.mode && p_params.customer_id == v_tab.tag.customer_id && p_params.host_id == v_tab.tag.host_id) {
          v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);
          return true;
        }
      }
      else if (p_type=='secondq_unit_dashboard') {
        if (p_type==v_tab.tag.mode && p_params.customer_id == v_tab.tag.customer_id && p_params.host_id == v_tab.tag.host_id && p_params.su_id == v_tab.tag.su_id) {
          v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);
          return true;
        }
      }
      else if (p_type=='secondq_unit_list') {
        if (p_type==v_tab.tag.mode) {

          if (p_params!=null) {
            if (p_params.filter_all!=null)
              v_tab.tag.input_filter.value = p_params.filter_all;
            if (p_params.filter_severity!=null)
              v_tab.tag.sel_filter.value = p_params.filter_severity;
          }
          else {
            v_tab.tag.sel_filter.value = 0;
            v_tab.tag.input_filter.value = '';
          }

          if (v_tab.tag.timeout!=null) {
            clearTimeout(v_tab.tag.timeout)
          }

          v_tab.tag.load_pending = false;
          v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);
          secondqLoadUnitListData(true, true);

          return true;
        }
      }
      else if (p_type=='secondq_host_list') {
        if (p_type==v_tab.tag.mode) {

          if (p_params!=null) {
            if (p_params.filter_all!=null)
              v_tab.tag.input_filter.value = p_params.filter_all;
            if (p_params.filter_severity!=null)
              v_tab.tag.sel_filter.value = p_params.filter_severity;
          }
          else {
            v_tab.tag.sel_filter.value = 0;
            v_tab.tag.input_filter.value = '';
          }

          if (v_tab.tag.timeout!=null) {
            clearTimeout(v_tab.tag.timeout)
          }
          v_tab.tag.load_pending = false;
          v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);
          secondqLoadHostListData(true, true);

          return true;
        }
      }
      else if (p_type=='secondq_customer_list') {
        if (p_type==v_tab.tag.mode) {

          if (p_params!=null) {
            if (p_params.filter_all!=null)
              v_tab.tag.input_filter.value = p_params.filter_all;
          }
          else {
            v_tab.tag.input_filter.value = '';
          }

          if (v_tab.tag.timeout!=null) {
            clearTimeout(v_tab.tag.timeout)
          }
          v_tab.tag.load_pending = false;
          v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);
          secondqLoadCustomerListData(true, true);

          return true;
        }
      }
      else if (p_type=='secondq_monitoring_dashboard') {
        if (p_type==v_tab.tag.mode) {
          if (v_tab.tag.timeout!=null) {
            clearTimeout(v_tab.tag.timeout)
          }
          v_tab.tag.load_pending = false;
          v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);
          secondqLoadDashboardData(true,'all');

          return true;
        }
      }
    }
  }
  return false;
}

function secondqAdjustHeights() {

  setTimeout(function() {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

    if (v_tab_tag.mode=='secondq_monitoring_dashboard') {
      var v_height = (window.innerHeight - $(v_tab_tag.summary_critical).offset().top - 140)/2;
      // v_tab_tag.summary_critical.style.height = v_height + 'px';
      // v_tab_tag.summary_high.style.height = v_height + 'px';
      // v_tab_tag.summary_medium.style.height = v_height + 'px';
      // v_tab_tag.summary_low.style.height = v_height + 'px';

      v_tab_tag.div_notifications.style.height = window.innerHeight - $(v_tab_tag.div_notifications).offset().top - 20 + 'px';
      v_tab_tag.ht_notifications.render();
    }
    else if (v_tab_tag.mode=='secondq_customer_list') {
      v_tab_tag.div_customer_list.style.height = window.innerHeight - $(v_tab_tag.div_customer_list).offset().top - 20 + 'px';
      v_tab_tag.ht_customers.render();
    }
    else if (v_tab_tag.mode=='secondq_host_list') {
      v_tab_tag.div_host_list.style.height = window.innerHeight - $(v_tab_tag.div_host_list).offset().top - 20 + 'px';
      v_tab_tag.ht_hosts.render();
    }
    else if (v_tab_tag.mode=='secondq_unit_list') {
      v_tab_tag.div_unit_list.style.height = window.innerHeight - $(v_tab_tag.div_unit_list).offset().top - 20 + 'px';
      v_tab_tag.ht_units.render();
    }
    else if (v_tab_tag.mode=='secondq_customer_dashboard') {
      v_tab_tag.div_host_list.style.height = window.innerHeight - $(v_tab_tag.div_host_list).offset().top - 20 + 'px';
      v_tab_tag.ht_hosts.render();
    }
    else if (v_tab_tag.mode=='secondq_host_dashboard') {
      v_tab_tag.div_unit_list.style.height = window.innerHeight - $(v_tab_tag.div_unit_list).offset().top - 20 + 'px';
      v_tab_tag.ht_units.render();
    }
    else if (v_tab_tag.mode=='secondq_unit_dashboard') {
      var v_height = window.innerHeight - $(v_tab_tag.div_chart).offset().top - 10;
      v_tab_tag.div_chart.style.height = v_height + 'px';
      v_tab_tag.canvas_overlay.width = v_tab_tag.canvas_chart.width;
      v_tab_tag.canvas_overlay.style.width = v_tab_tag.canvas_chart.width + 'px';
      v_tab_tag.canvas_overlay.height = v_height;
      v_tab_tag.canvas_overlay.style.height = v_height + 'px';
      v_tab_tag.chart.update();
    }
  },50);
}

function secondqMediaQuery() {
  let config = [
    ["(min-width: 2048px)", 'desktop-xl'],
    ["(min-width: 1440px) and (max-width: 2047px)", 'desktop-lg'],
    ["(min-width: 1280px) and (max-width: 1439px)", 'desktop-md'],
    ["(min-width: 1140px) and (max-width: 1279px)", 'xl'],
    ["(min-width: 960px) and (max-width: 1139px)", 'lg'],
    ["(min-width: 720px) and (max-width: 959px)", 'md'],
    ["(min-width: 540px) and (max-width: 719px)", 'sm'],
    ["(max-width: 539px)", 'xs']
  ];
  for (let i = 0; i < config.length; i++) {
    if (window.matchMedia(config[i][0]).matches)
      window.mediaConfig = config[i][1];
  }
}

function secondqSetRefreshCallback(p_tab_tag, p_callback_function) {
  clearTimeout(p_tab_tag.timeout);
  p_tab_tag.timeout = setTimeout(function() {
    //timeout refers to the currently active tab, refresh
    if (v_connTabControl.selectedTab.tag.tabControl != null
     && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag != null
     && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id == p_tab_tag.tab_id) {
       p_callback_function();
     }
     // Mark for refresh
     else {
       p_tab_tag.load_pending = true;
     }

  },60000);
}

function pointerRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
	td.style['cursor'] = 'pointer';
  td.style['text-align'] = 'center';
}

function centerRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
  td.style['vertical-align'] = 'middle';

  td.className ='';
}

function centerMiddleRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
	td.style['text-align'] = 'center';
  td.style['vertical-align'] = 'middle';

  td.className ='';
}

function secondqGrayRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
	td.style['text-align'] = 'center';
  td.style['vertical-align'] = 'middle';

  td.className ='secondq_status_box_ack_text';
}

function redCellRenderer(instance, td, row, col, prop, value, cellProperties) {
  Handsontable.renderers.HtmlRenderer.apply(this, arguments);
	td.style['text-align'] = 'center';
  td.style['vertical-align'] = 'middle';

  td.className ='secondq_status_box_critical_text';
}

function severityRenderer(instance, td, row, col, prop, value, cellProperties) {

	Handsontable.renderers.HtmlRenderer.apply(this, arguments);
	if (value == 'unknown')
		td.className = 'secondq_status_box_unknown';
	else if (value == 'ok')
		td.className = 'secondq_status_box_ok';
  else if (value == 'low')
		td.className = 'secondq_status_box_low';
  else if (value == 'medium')
		td.className = 'secondq_status_box_medium';
	else if (value == 'high')
		td.className = 'secondq_status_box_high';
	else if (value == 'critical')
		td.className = 'secondq_status_box_critical';

		td.style['text-align'] = 'center';
    td.style['vertical-align'] = 'middle';
}
