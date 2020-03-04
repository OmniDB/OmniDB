function secondqCreateUnitDashboard(p_customer_id, p_host_id, p_su_id) {

  if (!secondqSelectExistingTab('secondq_unit_dashboard',{customer_id: p_customer_id, host_id: p_host_id, su_id: p_su_id})) {

    startLoading();
    setTimeout(function() {

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
      p_name: '<i class="fas fa-eye icon-tab-title"></i>',
      p_selectFunction: function() {
        if(this.tag != null) {
          secondqChangeTabTitle(this.tag);
          secondqAdjustHeights();
          if (this.tag.load_pending) {

            secondqLoadUnitDashboardData(true,'all');
          }
        }
      },
      p_closeFunction: function(e,p_tab) {
        var v_current_tab = p_tab;
        removeTab(v_current_tab);
      },
    });

      v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

      var dashboard_unit_details_info_summary_data = [
        {id: 'dashboard_unit_details_value_' + v_tab.id, label: 'Value'},
        {id: 'dashboard_unit_details_metrics_' + v_tab.id, label: 'Metrics'}
      ];

      var dashboard_unit_details_info_summary_content = '';

      for (var i = 0; i < dashboard_unit_details_info_summary_data.length; i++) {
        dashboard_unit_details_info_summary_content +=
        "<div class='col-12'>" +
          "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
            "<label class='mb-0'>" +
              "<strong>" + dashboard_unit_details_info_summary_data[i].label + "</strong>" +
            "</label>" +
            "<div class='col'>" +
              "<span id='" + dashboard_unit_details_info_summary_data[i].id + "'></span>" +
            "</div>" +
          "</div>" +
        "</div>";
      }

      // if (dashboard_unit_details_info_summary_data.length % 2 !== 0) {
      //   dashboard_unit_details_info_summary_content +=
      //   "<div class='col-6'>" +
      //     "<div class='row my-1 py-1 align-items-center secondq_border-bottom-dashed text-left'>" +
      //       "<div class='col'>&nbsp;</div>" +
      //     "</div>" +
      //   "</div>";
      // }

      dashboard_unit_details_info_summary_html =
      "<div class='container-fluid' style='height: 150px; overflow: auto;'>" +
        "<h6 class='mt-2 text-center'>Info Summary <button onclick='secondqViewJsonData();' class='btn btn-secondary btn-sm ml-1'><i class='fas fa-list mr-1'></i>More Details</button></h6>" +
        "<div class='row'>" +
          dashboard_unit_details_info_summary_content +
        "</div>" +
      "</div>";

      var v_html =
      "<div class='row'>" +
        "<div class='col-md-12 mt-2'>" +
          "<h6 class='text-center'>" +
          " <span id='dashboard_unit_details_customer_" + v_tab.id + "' class='secondq_link' onclick='secondqCreateCustomerDashboard(" + p_customer_id + ");'></span>" +
          " - <span id='dashboard_unit_details_host_" + v_tab.id + "' class='secondq_link' onclick='secondqCreateHostDashboard(" + p_customer_id + "," + p_host_id + ");'></span>" +
          " - <span id='dashboard_unit_details_unit_" + v_tab.id + "'></span>" +
          " <button title='Refresh' class='btn btn-secondary btn-sm' onclick='secondqLoadUnitDashboardData(true,\"all\");'><i class='fas fa-sync'></i></button>" +
          " <button class='btn btn-secondary btn-sm' onclick='secondqUnitActions(event);'>Actions</button>" +
          "</h6>" +
        "</div>" +
      "</div>" +
      "<div class='row'>" +
        "<div class='col-md-6 my-2'>" +
          "<div class='card'>" +
            "<div class='card-body'>" +
              "<div class='container text-center' style='height: 150px; overflow: auto;'>" +
                "<div class='row'>" +
                  "<div class='col-md-4 my-2'>State (Elapsed)</div>" +
                  "<div class='col-md-8 my-2'><span id='dashboard_unit_details_status_" + v_tab.id + "'></span></div>" +
                "</div>" +
                "<div class='row'>" +
                  "<div class='col-md-4 my-2'>Thresholds</div>" +
                  "<div class='col-md-8 my-2'><span id='dashboard_unit_details_thresholds_" + v_tab.id + "'></span></div>" +
                "</div>" +
                "<div class='row'>" +
                  "<div class='col-md-4 my-2'>Actions</div>" +
                  "<div class='col-md-8 my-2'><span id='dashboard_unit_details_actions_" + v_tab.id + "'></span></div>" +
                "</div>" +
              "</div>" +
            "</div>" +
          "</div>" +
        "</div>" +
        "<div class='col-md-6 my-2'>" +
          "<div class='card'>" +
            "<div class='card-body'>" +

              dashboard_unit_details_info_summary_html +

              // "<div class='container' style='height: 150px; overflow: auto;'>" +
              //   "<h6 class='card-title text-center'><button class='btn btn-secondary btn-sm' onclick='secondqViewJsonData();'>Details</button></h6>" +
              //   "<div class='row text-center'>" +
              //     "<div class='col-md-4 my-2'>Value</div>" +
              //     "<div class='col-md-8 my-2'><span id='dashboard_unit_details_value_" + v_tab.id + "'></span></div>" +
              //   "</div>" +
              //   "<div class='row text-center'>" +
              //     "<div class='col-md-4 my-2'>Metrics</div>" +
              //     "<div class='col-md-8 my-2'><span id='dashboard_unit_details_metrics_" + v_tab.id + "'></span></div>" +
              //   "</div>" +
              // "</div>" +


            "</div>" +

            "</div>" +
          "</div>" +
        "</div>" +
      "</div>" +
      "<form autofill='false'>" +
        "<div class='d-flex align-items-center'>" +
          "<div class='my-2 d-flex align-items-center'>" +
            "<span class='mr-1'>Set dates interval by</span>" +
            "<div class='btn-group btn-group-sm btn-group-toggle' data-toggle='buttons'>" +
              "<label class='btn btn-secondary btn-sm' for='secondq_load_dates_interval_day'>" +
                "<input type='radio' name='secondq_load_dates_interval' id='secondq_load_dates_interval_day' value='day' autocomplete='off' onchange='secondqLoadDatesInterval(this, true, \"day\");'> 1 day" +
              "</label>" +
              "<label class='btn btn-secondary btn-sm' for='secondq_load_dates_interval_week'>" +
                "<input type='radio' name='secondq_load_dates_interval' id='secondq_load_dates_interval_week' value='week' autocomplete='off' onchange='secondqLoadDatesInterval(this, true, \"week\");'> 1 week" +
              "</label>" +
              "<label class='btn btn-secondary btn-sm' for='secondq_load_dates_interval_month'>" +
                "<input type='radio' name='secondq_load_dates_interval' id='secondq_load_dates_interval_month' value='month' autocomplete='off' onchange='secondqLoadDatesInterval(this, true, \"month\");'> 1 month" +
              "</label>" +
              "<label class='btn btn-secondary btn-sm d-none' for='secondq_load_dates_interval_none'>" +
                "<input type='radio' name='secondq_load_dates_interval' id='secondq_load_dates_interval_none' value='none' autocomplete='off'> None" +
              "</label>" +
              // "<label class='btn btn-secondary btn-sm' for='secondq_load_dates_interval_clear'>" +
              //   "<input type='radio' name='secondq_load_dates_interval' id='secondq_load_dates_interval_clear' value='clear' autocomplete='off' onchange='secondqUnitDashboardClearFilter();'> Clear Filter" +
              // "</label>" +
              // "<label class='btn btn-secondary btn-sm' for='secondq_load_dates_interval_refresh'>" +
              //   "<input type='radio' name='secondq_load_dates_interval' id='secondq_load_dates_interval_refresh' value='refresh' autocomplete='off' onchange='secondqLoadUnitDashboardData(true,\"chart\");'> Refresh" +
              // "</label>" +
            "</div>" +
          "</div>" +
          "<div class='my-2 d-flex align-items-center'>" +
            "<div class='input-group w-auto ml-1'>" +
              "<div class='input-group-prepend'>" +
                "<span class='input-group-text bg-transparent'>" +
                  "<i class='far fa-calendar-alt'></i>" +
                "</span>" +
              "</div>" +
              "<input type='text' class='form-control form-control-sm d-inline' placeholder='Start Time'id='server_unit_chart_start_time_" + v_tab.id + "' onblur='secondqLoadUnitDashboardData(true,\"chart\");'>" +
              "<input type='text' class='form-control form-control-sm d-inline' placeholder='End Time'id='server_unit_chart_end_time_" + v_tab.id + "' onblur='secondqLoadUnitDashboardData(true,\"chart\");'>" +
            "</div>" +
          "</div>" +
          "<div class='my-2 d-flex align-items-center'>" +
            "<button type='button' class='btn btn-secondary btn-sm ml-1' onclick='secondqLoadUnitDashboardData(true,\"chart\",true);'>Refresh</button>" +
            "<button type='button' class='btn btn-secondary btn-sm ml-1' onclick='secondqUnitDashboardClearFilter();'>Clear Filter</button>" +
          "</div>" +
        "</div>" +
      "</form>" +
      "<div id='div_chart_" + v_tab.id + "' style='height: 200px;'>" +
      "<canvas class='secondq_chart_global_canvas_overlay' id='canvas_server_unit_chart_overlay_" + v_tab.id + "'></canvas>" +
      "<canvas class='secondq_chart_global_canvas' id='canvas_server_unit_chart_" + v_tab.id + "'></canvas>" +
      "</div>";

      var v_div = document.getElementById('div_' + v_tab.id);
      v_div.innerHTML = v_html;

      var v_filter_start_time = document.getElementById('server_unit_chart_start_time_' + v_tab.id);
      var v_filter_end_time = document.getElementById('server_unit_chart_end_time_' + v_tab.id);
      var v_current_date = new Date();
      v_current_date.setHours( v_current_date.getHours() - 5 );

      jQuery(v_filter_start_time).datetimepicker({
        format:'Y-m-d H:i',
        value: v_current_date.toISOString(),
        closeOnDateSelect:true,
        onSelectDate:function(){
          secondqLoadUnitDashboardData(true,"chart");
        }
      });

      jQuery(v_filter_end_time).datetimepicker({
        format:'Y-m-d H:i',
        closeOnDateSelect:true,
        onSelectDate:function(){
          secondqLoadUnitDashboardData(true,"chart");
        }
      });

      //Setting up chart
      var v_canvas_server_unit_chart = document.getElementById('canvas_server_unit_chart_' + v_tab.id);
      var ctx = v_canvas_server_unit_chart.getContext('2d');
      var chart = new Chart(ctx, {
        "type": "line",
        "data": {
          "datasets": [
            {
                "type": 'line',
                "label": 'min',
                "hidden": false,
                "fill": false,
                "borderColor": 'rgba(74, 183, 65,0)',
                "backgroundColor": 'rgba(74, 183, 65,0)',
                "lineTension": 0,
                "pointRadius": 0,
                "borderWidth": 0,
                "data": [],
                "fill": false,
                radius: 0,
            },
            {
                "type": 'line',
                "label": 'average',
                "hidden": false,
                "fill": false,
                "borderColor": "rgba(140, 140, 140, 1.0)",
                "backgroundColor": 'rgba(68, 169, 3, 0.5)',
                "lineTension": 0,
                "pointRadius": 0,
                "borderWidth": 2,
                "data": [],
                "fill": "-1",
            },
            {
                "type": 'line',
                "label": 'max',
                "hidden": false,
                "fill": false,
                "borderColor": 'rgba(232, 79, 79,0)',
                "backgroundColor": 'rgba(74, 134, 232, 0.5)',
                "lineTension": 0,
                "pointRadius": 0,
                "borderWidth": 0,
                "data": [],
                "fill": "-1",
                radius: 0,
            },
            {
                "type": 'line',
                "label": 'unknown',
                "hidden": false,
                "fill": false,
                "borderColor": 'rgba(165, 84, 175,0)',
                "backgroundColor": 'rgba(165, 84, 175)',
                "lineTension": 0,
                "pointRadius": 0,
                "borderWidth": 0,
                "data": []
            }
          ],
          "labels": []
        },
        "options": {
          plugins: {
            datalabels: {
              display: false
            }
          },
          annotation: {
            annotations: [
            ]
          },
            "responsive": true,
            "maintainAspectRatio": false,
            "title":{
                "display":false
            },
            "legend": {
                "display": false
             },
            "tooltips": {
                "mode": "index",
                "intersect": false,
                "displayColors": false,
            },
            "hover": {
                "mode": "nearest",
                "intersect": true
            },
            "scales": {
                "xAxes": [{
                    "display": true,
                    "scaleLabel": {
                        "display": false,
                        "labelString": "Time"
                    }
                }],
                "yAxes": [{
                    "display": true,
                    "scaleLabel": {
                        "display": false,
                        "labelString": "Value"
                    },
                    "ticks": {
                        "beginAtZero": true
                    }
                }]
            }
        }
      }
      );
      adjustChartTheme(chart);

      var canvas = v_canvas_server_unit_chart;
      var overlay = document.getElementById('canvas_server_unit_chart_overlay_' + v_tab.id);
      var startIndex = 0;
      overlay.width = canvas.width;
      overlay.style.width = canvas.width + 'px';
      overlay.height = canvas.height;
      overlay.style.height = canvas.height + 'px';
      var selectionContext = overlay.getContext('2d');
      var selectionRect = {
        w: 0,
        startX: 0,
        startY: 0
      };
      var drag = false;
      canvas.addEventListener('pointerdown', evt => {
        const points = chart.getElementsAtEventForMode(evt, 'index', {
          intersect: false
        });
        startIndex = points[0]._index;
        const rect = canvas.getBoundingClientRect();
        selectionRect.startX = evt.clientX - rect.left;
        selectionRect.startY = chart.chartArea.top;
        drag = true;
        // save points[0]._index for filtering
      });
      canvas.addEventListener('pointermove', evt => {

        const rect = canvas.getBoundingClientRect();
        if (drag) {
          const rect = canvas.getBoundingClientRect();
          selectionRect.w = (evt.clientX - rect.left) - selectionRect.startX;
          selectionContext.globalAlpha = 0.3;
          selectionContext.clearRect(0, 0, canvas.width, canvas.height);
          selectionContext.fillRect(selectionRect.startX,
            selectionRect.startY,
            selectionRect.w,
            chart.chartArea.bottom - chart.chartArea.top);
        } else {
          selectionContext.clearRect(0, 0, canvas.width, canvas.height);
          var x = evt.clientX - rect.left;
          if (x > chart.chartArea.left) {
            selectionContext.fillRect(x,
              chart.chartArea.top,
              1,
              chart.chartArea.bottom - chart.chartArea.top);
          }
        }
      });
      canvas.addEventListener('pointerup', evt => {
        selectionContext.clearRect(0, 0, canvas.width, canvas.height);
        const points = chart.getElementsAtEventForMode(evt, 'index', {
          intersect: false
        });
        drag = false;

        if (startIndex != points[0]._index) {
          var v_first_index = null;
          var v_last_index = null;
          if (startIndex < points[0]._index) {
            v_first_index = startIndex;
            v_last_index = points[0]._index;
          }
          else {
            v_first_index = points[0]._index;
            v_last_index = startIndex;
          }

          v_filter_start_time.value = chart.data.labels[v_first_index];
          v_filter_end_time.value = chart.data.labels[v_last_index];
          secondqLoadUnitDashboardData(true,'chart');
        }
      });

      var v_tag = {
        tab_id: v_tab.id,
        tab_object: v_tab,
        mode: 'secondq_unit_dashboard',
        load_pending: false,
        status_data: null,
        customer: null,
        host: null,
        unit: null,
        customer_id: p_customer_id,
        host_id: p_host_id,
        su_id: p_su_id,
        key: null,
        div_chart: document.getElementById('div_chart_' + v_tab.id),
        chart: chart,
        canvas_chart: v_canvas_server_unit_chart,
        canvas_overlay: overlay,
        details_customer: document.getElementById('dashboard_unit_details_customer_' + v_tab.id),
        details_host: document.getElementById('dashboard_unit_details_host_' + v_tab.id),
        details_unit: document.getElementById('dashboard_unit_details_unit_' + v_tab.id),
        details_value: document.getElementById('dashboard_unit_details_value_' + v_tab.id),
        details_metrics: document.getElementById('dashboard_unit_details_metrics_' + v_tab.id),
        details_status: document.getElementById('dashboard_unit_details_status_' + v_tab.id),
        details_thresholds: document.getElementById('dashboard_unit_details_thresholds_' + v_tab.id),
        details_actions: document.getElementById('dashboard_unit_details_actions_' + v_tab.id),
        div_data: document.getElementById('dashboard_unit_data_' + v_tab.id),
        filter_start_time: v_filter_start_time,
        filter_end_time: v_filter_end_time
      };
      v_tab.tag = v_tag;

      secondqAdjustHeights();
      secondqLoadUnitDashboardData(true,'all');
      endLoading();

    },50);
  }
}

/* p_interval is TRUE only when function is triggered by a date interval input */
function secondqLoadUnitDashboardData(p_loading, p_mode, p_interval = false) {
  try {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.load_pending = false;

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'secondq_load_unit_dashboard_data',
      p_data: {
        'p_mode': p_mode,
        'p_customer_id': v_tab_tag.customer_id,
        'p_host_id': v_tab_tag.host_id,
        'p_su_id': v_tab_tag.su_id,
        'p_start_time': v_tab_tag.filter_start_time.value,
        'p_end_time': v_tab_tag.filter_end_time.value
      },
      p_callback: function(p_data) {

        if (p_data.details!=null) {
          v_tab_tag.dashboard_status_data = p_data.details;

          v_tab_tag.tab_object.renameTab('<i class="fas fa-eye icon-tab-title"></i> ' + p_data.details.server + ' - ' + p_data.details.unit)

          v_tab_tag.details_customer.innerHTML = p_data.details.customer;
          v_tab_tag.customer = p_data.details.customer;
          v_tab_tag.details_host.innerHTML = p_data.details.server;
          v_tab_tag.host = p_data.details.server;
          v_tab_tag.details_unit.innerHTML = p_data.details.unit;
          v_tab_tag.unit = p_data.details.unit;

          v_tab_tag.key = p_data.details.key;

          secondqChangeTabTitle(v_tab_tag);

          v_tab_tag.details_status.innerHTML = p_data.details.status;
          v_tab_tag.details_value.innerHTML = p_data.details.value;
          v_tab_tag.details_metrics.innerHTML = p_data.details.metrics;
          v_tab_tag.details_thresholds.innerHTML =
          "<span class='secondq_notification_severity_text secondq_status_box_ack'>" + p_data.details.threshold_critical_text + "</span> " +
          "<span class='secondq_notification_severity_text secondq_status_box_ack'>" + p_data.details.threshold_high_text + "</span> " +
          "<span class='secondq_notification_severity_text secondq_status_box_ack'>" + p_data.details.threshold_medium_text + "</span> " +
          "<span class='secondq_notification_severity_text secondq_status_box_ack'>" + p_data.details.threshold_low_text + "</span>" +
          "<span> " + p_data.details.unit_text + "</span>";

          v_tab_tag.details_actions.innerHTML = "";

          if (p_data.details.ack) {
            v_tab_tag.details_actions.innerHTML = "<i class='secondq_pointer fas fa-thumbs-up mr-2 secondq_status_icon' onclick='secondqShowAckDetails(\"dashboard\",0,this);'></i>";
            var v_i = document.createElement('i');
          }
          if (p_data.details.downtime) {
            v_tab_tag.details_actions.innerHTML = v_tab_tag.details_actions.innerHTML + "<i class='secondq_pointer fas fa-wrench mr-2 secondq_status_icon' onclick='secondqShowDowntimeDetails(\"dashboard\",0,this);'></i>";
          }
          if (!p_data.details.enabled) {
            v_tab_tag.details_actions.innerHTML = v_tab_tag.details_actions.innerHTML + "<i class='fas fa-power-off mr-2 secondq_status_icon' title='Disabled'></i>";
          }

          v_tab_tag.data_json = p_data.details.data_json;

        }

        if (p_data.chart!=null) {
          v_tab_tag.chart.data.labels = p_data.chart.labels;
          v_tab_tag.chart.data.datasets[0].data = p_data.chart.datasets[0];
          v_tab_tag.chart.data.datasets[1].data = p_data.chart.datasets[1];
          v_tab_tag.chart.data.datasets[2].data = p_data.chart.datasets[2];
          v_tab_tag.chart.data.datasets[3].data = p_data.chart.datasets[3];
          v_tab_tag.chart.options.annotation.annotations = p_data.chart.annotations
          v_tab_tag.chart.update();
        }

        if (p_mode == 'all') {
          secondqSetRefreshCallback(v_tab_tag,
          function() {
            secondqLoadUnitDashboardData(false,'all');
          });
        }

      },
      p_loading: p_loading,
      p_check_database_connection: false
    });

    /* Removes selected interval from inputs */
    if (!p_interval)  {
      $("#secondq_load_dates_interval_none").click();
    }
  }
  // Error, schedule another run
  catch(err) {
    if (p_mode == 'all') {
      secondqSetRefreshCallback(v_tab_tag,
      function() {
        secondqLoadUnitDashboardData(false,'all');
      });
    }
  }
}

function secondqLoadDatesInterval(checkbox, p_load, p_date_interval) {
  if (checkbox.checked === true) {
    let date = new Date();
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.filter_end_time.value = date.toISOString();

    if (p_date_interval === 'day') {
      date.setHours( date.getHours() - 24 );
    }
    else if (p_date_interval === 'week') {
      date.setHours( date.getHours() - 168 );
    }
    else if (p_date_interval === 'month') {
      date.setHours( date.getHours() - 744 );
    }

    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.filter_start_time.value = date.toISOString();

    secondqLoadUnitDashboardData(p_load,'chart',true);
  }
}

function secondqUnitActions(e) {
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
              'server_id': v_tab_tag.host_id,
              'su_id': v_tab_tag.su_id,
            }
          ];
          ackUnitsCall(v_data,'unit_dashboard');
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
              'server_id': v_tab_tag.host_id,
              'su_id': v_tab_tag.su_id,
            }
          ];
          removeAckUnitsCall(v_data,'unit_dashboard');
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
              'server_id': v_tab_tag.host_id,
              'su_id': v_tab_tag.su_id,
            }
          ];
          downtimeUnitsCall(v_data,'unit_dashboard');
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
              'server_id': v_tab_tag.host_id,
              'su_id': v_tab_tag.su_id,
            }
          ];
          removeDowntimeUnitsCall(v_data,'unit_dashboard');
  			}
  		},
      {
  			text: 'Change Thresholds',
  			icon: 'fas cm-all fa-retweet',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_data = [
            {
              'customer_id': v_tab_tag.customer_id,
              'server_id': v_tab_tag.host_id,
              'su_id': v_tab_tag.su_id,
              'thresholds': {
                'critical': v_tab_tag.dashboard_status_data.threshold_critical,
                'high': v_tab_tag.dashboard_status_data.threshold_high,
                'medium': v_tab_tag.dashboard_status_data.threshold_medium,
                'low': v_tab_tag.dashboard_status_data.threshold_low
              }
            }
          ];
          changeThresholdUnitsCall(v_data,'unit_dashboard');
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
              'server_id': v_tab_tag.host_id,
              'su_id': v_tab_tag.su_id,
            }
          ];
          enableUnitsCall(v_data,'unit_dashboard');
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
              'server_id': v_tab_tag.host_id,
              'su_id': v_tab_tag.su_id,
            }
          ];
          disableUnitsCall(v_data,'unit_dashboard');
  			}
  		},
      {
  			text: 'Change Key (superuser)',
  			icon: 'fas cm-all fa-key',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_data = [
            {
              'customer_id': v_tab_tag.customer_id,
              'server_id': v_tab_tag.host_id,
              'su_id': v_tab_tag.su_id,
              'key': v_tab_tag.key
            }
          ];
          changeKeyUnitCall(v_data,'unit_dashboard');
  			}
  		}
    ],
    null);
}

function secondqUnitDashboardClearFilter() {
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.filter_start_time.value = '';
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.filter_end_time.value = '';
  secondqLoadUnitDashboardData(true,'chart');
}
