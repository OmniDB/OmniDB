function secondqCreateCustomerDashboard(p_customer_id) {

  if (!secondqSelectExistingTab('secondq_customer_dashboard',{customer_id: p_customer_id})) {
    startLoading();
    setTimeout(function() {

    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
      p_name: '<i class="fas fa-user icon-tab-title"></i>',
      p_selectFunction: function() {
        if(this.tag != null) {
          secondqChangeTabTitle(this.tag);
          secondqAdjustHeights();
          if (this.tag.load_pending) {

            secondqLoadCustomerDashboardData(true,'all');
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
          "<h6 class='text-center'><span id='dashboard_customer_details_customer_" + v_tab.id + "'></span>" +
          " <button title='Refresh' class='btn btn-secondary btn-sm' onclick='secondqLoadCustomerDashboardData(true,\"all\");'><i class='fas fa-sync'></i></button>" +
          " <button class='btn btn-secondary btn-sm' onclick='secondqCustomerActions(event);'>Actions</button></h6>" +
        "</div>" +
      "</div>" +
      "<div class='row mb-2'>" +
        "<div class='col-md-5'>" +
          "<div class='card'>" +
            "<div class='card-body'>" +
              "<div class='container text-center' style='height: 250px; overflow: auto;'>" +
                "<div class='row my-2 d-none'>" +
                  "<div class='col-md-4'>Token</div>" +
                  "<div class='col-md-8'><span id='dashboard_customer_details_token_" + v_tab.id + "'></span></div>" +
                "</div>" +
                "<div class='row my-2'>" +
                  "<div class='col-md-4'>Max severity</div>" +
                  "<div class='col-md-8'><span id='dashboard_customer_details_severity_" + v_tab.id + "'></span></div>" +
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
      "<div id='dashboard_host_list_" + v_tab.id + "' class='ht_text_ellipsis' style='width: 100%; height: 200px; overflow: hidden;'/></div>";

      var v_div = document.getElementById('div_' + v_tab.id);
      v_div.innerHTML = v_html;
      var v_dashboard_host_list = document.getElementById('dashboard_host_list_' + v_tab.id);

      // Creating service tab list
      var v_service_tabs = createTabControl({ p_div: 'secondq_dashboard_service_tab_list_' + v_tab.id });

      var v_diagram_tab = v_service_tabs.createTab(
        {
          p_name: 'Diagram',
          p_close: false
        });

      var v_location_tab = v_service_tabs.createTab(
        {
          p_name: 'Location',
          p_close: false,
          p_disabled: true
        });

        v_diagram_tab.elementDiv.innerHTML =
        "<div id='dashboard_customer_graph_" + v_tab.id + "' style='height: 240px;' class='secondq_customer_graph'></div>";

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

      //Setting up customer grid
      var columnProperties = [];

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
        stretchH: 'last',
        copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
        manualColumnResize: true,
        autoColumnSize : true,
        afterOnCellMouseUp: function(event,coords) {
        },
        cells: function (row, col, prop) {

            var cellProperties = {};

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row]!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row].ok==true)
              cellProperties.renderer = secondqGrayRenderer;
            else if (col==4)
              cellProperties.renderer = severityRenderer;
            else if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row]!=null && v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.status_data[row].status=='down')
              cellProperties.renderer = redCellRenderer;
            else
              cellProperties.renderer = centerMiddleRenderer;

            return cellProperties;
        },
        mergeCells: true,
        contextMenu: {
          callback: function (key, options) {
            if (key === 'ack') {
              ackUnits(this,'customer_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'remove_ack') {
              removeAckUnits(this,'customer_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'downtime') {
              downtimeUnits(this,'customer_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'remove_downtime') {
              removeDowntimeUnits(this,'customer_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'enable') {
              enableUnits(this,'customer_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
            }
            else if (key === 'disable') {
              disableUnits(this,'customer_dashboard',v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag);
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

      var v_graph_div = document.getElementById('dashboard_customer_graph_' + v_tab.id);

      // Creating graph
      var v_graph = cytoscape({
        container: v_graph_div,
        boxSelectionEnabled: false,
        autounselectify: true,
        layout: {
          name: 'spread',
          minDist: 60,
          expandingFactor: -1.0
        },
        style: [
          {
            selector: 'node',
            style: {
              'content': 'data(label)',
              'background-color': 'data(color)',
              'shape': 'data(shape)',
              'text-valign': 'bottom',
              'text-wrap': 'wrap',
              'font-size': '10',
              'width': '20',
              'height': '20'
            }
          },
          {
            selector: 'edge',
            style: {
              'curve-style': 'bezier',
              'target-arrow-shape': 'triangle',
              'width': 1,
              'control-point-distances': 30,
              'content': 'data(label)',
              'text-wrap': 'wrap',
              'font-size': '10',
              'target-arrow-color': 'data(color)',
              'line-color': 'data(color)',
              'line-style': 'data(line_style)'
            }
          },
        ],

        elements: {
          nodes: [],
          edges: []
        }
      });
      adjustGraphTheme(v_graph);

      var v_tag = {
        tab_id: v_tab.id,
        tab_object: v_tab,
        mode: 'secondq_customer_dashboard',
        div_host_list: v_dashboard_host_list,
        ht_hosts: ht,
        chart_units: chart_units_pie,
        load_pending: false,
        status_data: null,
        customer: null,
        customer_id: p_customer_id,
        details_token: document.getElementById('dashboard_customer_details_token_' + v_tab.id),
        details_customer: document.getElementById('dashboard_customer_details_customer_' + v_tab.id),
        details_severity: document.getElementById('dashboard_customer_details_severity_' + v_tab.id),
        service_tab_list: v_service_tabs,
        graph: v_graph
      };
      v_tab.tag = v_tag;

      secondqAdjustHeights();
      secondqLoadCustomerDashboardData(true,'all');
      endLoading();

    },50);
  }
}

function secondqLoadCustomerDashboardData(p_loading, p_mode) {
  try {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.load_pending = false;

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'secondq_load_customer_dashboard_data',
      p_data: {
        'p_mode': p_mode,
        'p_customer_id': v_tab_tag.customer_id
      },
      p_callback: function(p_data) {

        if (p_data.hosts!=null) {
          v_tab_tag.status_data = p_data.hosts.hosts_status_data;

          v_tab_tag.ht_hosts.loadData(p_data.hosts.hosts_data);
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

          v_tab_tag.tab_object.renameTab('<i class="fas fa-user icon-tab-title"></i> ' + p_data.details.customer)

          v_tab_tag.details_customer.innerHTML = p_data.details.customer;
          v_tab_tag.customer = p_data.details.customer;

          secondqChangeTabTitle(v_tab_tag);
          v_tab_tag.details_token.innerHTML = p_data.details.token;
          v_tab_tag.details_severity.innerHTML = "<span class='secondq_notification_severity_text secondq_status_box_" + p_data.details.max_severity + "'>" + p_data.details.max_severity + "</span>";

          // Graph update

          var v_existing_nodes = v_tab_tag.graph.nodes()
          var v_existing_edges = v_tab_tag.graph.edges()

          var v_new_objects = []

          //Updating existing nodes and adding new ones
          for (var j=0; j<p_data.details.graph.nodes.length; j++) {
            var v_found_node = false;
            var node = p_data.details.graph.nodes[j];
            for (var k=0; k<v_existing_nodes.length; k++) {
              //New node already exists, update data
              if (v_existing_nodes[k].data('id') == node.data['id']) {
                v_found_node = true;
                for (var property in node.data) {
                    if (node.data.hasOwnProperty(property)) {
                        v_existing_nodes[k].data(property,node.data[property])
                    }
                }
                break;
              }
            }
            if (!v_found_node) {
              node['group'] = 'nodes';
              v_new_objects.push(node);
            }
          }

          //Updating existing edges and adding new ones
          for (var j=0; j<p_data.details.graph.edges.length; j++) {
            var v_found_edge = false;
            var edge = p_data.details.graph.edges[j];
            for (var k=0; k<v_existing_edges.length; k++) {
              //New edge already exists, update data
              if (v_existing_edges[k].data('id') == edge.data['id']) {
                v_found_edge = true;
                for (var property in edge.data) {
                    if (edge.data.hasOwnProperty(property)) {
                        v_existing_edges[k].data(property,edge.data[property])
                    }
                }
                break;
              }
            }
            if (!v_found_edge) {
              edge['group'] = 'edges';
              v_new_objects.push(edge);
            }
          }
          //Removing edges that doesn't exist anymore
          for (var k=0; k<v_existing_edges.length; k++) {
            var v_found_edge = false;
            for (var j=0; j<p_data.details.graph.edges.length; j++) {
              var edge = p_data.details.graph.edges[j];
              if (v_existing_edges[k].data('id') == edge.data['id']) {
                v_found_edge = true;
                break;
              }
            }
            //Not found, remove it
            if (!v_found_edge) {
              v_existing_edges[k].remove();
            }
          }
          //Removing nodes that doesn't exist anymore
          for (var k=0; k<v_existing_nodes.length; k++) {
            var v_found_node = false;
            for (var j=0; j<p_data.details.graph.nodes.length; j++) {
              var node = p_data.details.graph.nodes[j];
              if (v_existing_nodes[k].data('id') == node.data['id']) {
                v_found_node = true;
                break;
              }
            }
            //Not found, remove it
            if (!v_found_node) {
              v_existing_nodes[k].remove();
            }
          }

          //Adding new objects and rendering graph again
          if (v_new_objects.length > 0) {
            v_tab_tag.graph.add(v_new_objects);
            v_tab_tag.graph.layout();
          }

        }

        if (p_mode == 'all') {
          secondqSetRefreshCallback(v_tab_tag,
          function() {
            secondqLoadCustomerDashboardData(false,'all');
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
        secondqLoadCustomerDashboardData(false,'all');
      });
    }
  }
}

function secondqCustomerActions(e) {
  customMenu(
    {
      x:e.clientX+5,
      y:e.clientY+5
    },
    [
      {
  			text: 'Change Token (superuser)',
  			icon: 'fas cm-all fa-key',
  			action: function() {
          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          secondqChangeCustomerToken(v_tab_tag.customer_id);
  			}
  		}
    ],
    null);
}

function secondqChangeCustomerToken(p_customer_id) {
  showConfirm('WARNING, changing the token requires changing the configuration of all hosts belonging to this customer.',
  function() {

    callPluginFunction({
      p_plugin_name: 'secondq_monitoring',
      p_function_name: 'change_customer_token',
      p_data: {
        'customer_id': p_customer_id
      },
      p_callback: function(p_data) {

        if (p_data.error==true)
          showAlert(p_data.message);
        else
        {
          secondqLoadCustomerDashboardData(true,'all');
        }

      },
      p_loading: true,
      p_check_database_connection: false
    });

  },
  null,
  null);
}
