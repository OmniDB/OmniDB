<%@ Page Language="C#" Inherits="OmniDB.CompareDB" %>
<!DOCTYPE html>
<html>
<head runat="server">
	<title>OmniDB</title>
	<link rel="stylesheet" type="text/css" href="css/style.css">
	<link rel="stylesheet" media="screen" href="css/handsontable.full.css">
	<link rel="stylesheet" media="screen" href="css/msdropdown/dd.css">
    <link rel="stylesheet" href="js/themes/default/style.min.css" />
    <link rel="stylesheet" href="lib/vis/vis.min.css" />
    <link rel="stylesheet" href="lib/jquery-ui/jquery-ui.css">
    <link rel="stylesheet" href="lib/jqplot/jquery.jqplot.min.css">

    <link rel="stylesheet" href="lib/aimaraJS/css/Aimara.css" />
    <link rel="stylesheet" href="lib/tabs/css/tabs.css" />

	<script src="js/jquery-1.11.2.min.js" type="text/javascript"></script>
	<script src="lib/jquery-ui/jquery-ui.js"></script>
	<script src="js/jquery.dd.min.js" type="text/javascript"></script>
    <script src="js/jstree.min.js" type="text/javascript"></script>
	<script src="js/handsontable.full.js"></script>
    <script src="lib/vis/vis.min.js"></script>
    <script src="lib/cytoscape/build/cytoscape.min.js"></script>
    <script src="lib/chart/chart.min.js"></script>

    <script type="text/javascript" src="js/NotificationControl.js"></script>
    <script type="text/javascript" src="js/AjaxControl.js"></script>
    <script type="text/javascript" src="lib/tabs/lib/tabs.js"></script>

    <script type="text/javascript" src="lib/aimaraJS/lib/Aimara.js"></script>

    <script src="lib/ace/ace.js" type="text/javascript" charset="utf-8"></script>
	<script src="lib/ace/mode-sql.js" type="text/javascript" charset="utf-8"></script>
	<script src="lib/ace/ext-language_tools.js" type="text/javascript" charset="utf-8"></script>

	<script type="text/javascript">

		var v_barchart1 = '';
		var v_barchart2 = '';

		$(function () {

			getDatabaseList1('sl_database1');

		});

		function getDatabaseList1(p_sel_id, p_filter) {

			execAjax('MainDB.aspx/GetDatabaseList',
					JSON.stringify({"p_sel_id": p_sel_id, "p_filter": p_filter}),
					function(p_return) {

						document.getElementById('div_select_db1').innerHTML = p_return.v_data.v_select_html;

						$('#' + p_sel_id).msDropDown();

						getDatabaseList2('sl_database2',p_return.v_data.v_db_type);

					},
					null,
					'box');
		}

		function getDatabaseList2(p_sel_id, p_filter) {

			execAjax('MainDB.aspx/GetDatabaseList',
					JSON.stringify({"p_sel_id": p_sel_id, "p_filter": null}),
					function(p_return) {

						document.getElementById('div_select_db2').innerHTML = p_return.v_data.v_select_html;

						$('#' + p_sel_id).msDropDown();

					},
					null,
					'box');
		}

		function changeDatabase(p_sel_id,p_value) {

			if (p_sel_id == 'sl_database1') {

				execAjax('MainDB.aspx/ChangeDatabase',
					JSON.stringify({"p_value": p_value}),
					function(p_return) {

						getDatabaseList1('sl_database1');

					},
					null,
					'box');


			}
		}

		function compareBases(p_mode) {

			var start_time = new Date().getTime();

			execAjax('CompareDB.aspx/CompareBases',
					JSON.stringify({"p_second_db": document.getElementById('sl_database2').value}),
					function(p_return) {

						console.log(p_return.v_data);


						var tree1 = createTree('tree1','white',null);
						var tree2 = createTree('tree2','white',null);

						for (var i=0; i<p_return.v_data.length;i++) {

							if (p_return.v_data[i][1]=='-1') {
								var node1 = tree1.createNode(p_return.v_data[i][0],true,'images/db.png',null,null,null,'#5FBD5F');
								var node1 = tree2.createNode(p_return.v_data[i][0],true,'images/db.png',null,null,null,'red');
							}
							else if (p_return.v_data[i][1]=='1') {
								var node1 = tree1.createNode(p_return.v_data[i][0],true,'images/db.png',null,null,null,'red');
								var node1 = tree2.createNode(p_return.v_data[i][0],true,'images/db.png',null,null,null,'#5FBD5F');
							}
							else if (p_return.v_data[i][1]=='0') {
								var node1 = tree1.createNode(p_return.v_data[i][0],true,'images/db.png',null,null,null,'#5FBD5F');
								var node1 = tree2.createNode(p_return.v_data[i][0],true,'images/db.png',null,null,null,'#5FBD5F');
							}
							else {
								var node1 = tree1.createNode(p_return.v_data[i][0],true,'images/db.png',null,null,null,'orange');
								var node1 = tree2.createNode(p_return.v_data[i][0],true,'images/db.png',null,null,null,'orange');
							}

						}

						tree1.drawTree();
						tree2.drawTree();


						/*var request_time = new Date().getTime() - start_time;

						document.getElementById('div_comparison_time').innerHTML = '<h2>Comparison Statistics</h2>Execution Time: ' + request_time/1000 + ' seconds.';

						var data1 = [
						    {
						        value: p_return.v_data.v_num_green_tables,
						        color:"greenyellow",
						        highlight: "greenyellow",
						        label: "Equal Tables"
						    },
						    {
						        value: p_return.v_data.v_num_orange_tables,
						        color: "rgb(255, 204, 110)",
						        highlight: "rgb(255, 204, 110)",
						        label: "Different Table Details"
						    },
						    {
						        value: p_return.v_data.v_num_red_tables,
						        color: "lightsalmon",
						        highlight: "lightsalmon",
						        label: "Different Tables"
						    }
						];

						var data2 = [
						    {
						        value: p_return.v_data.v_num_green_cols,
						        color:"greenyellow",
						        highlight: "greenyellow",
						        label: "Equal Columns"
						    },
						    {
						        value: p_return.v_data.v_num_orange_cols,
						        color: "rgb(255, 204, 110)",
						        highlight: "rgb(255, 204, 110)",
						        label: "Different Column Details"
						    },
						    {
						        value: p_return.v_data.v_num_red_cols,
						        color: "lightsalmon",
						        highlight: "lightsalmon",
						        label: "Different Columns"
						    }
						];

						$('#div_chart').show();

						if (v_barchart1!='')
							v_barchart1.destroy();
						if (v_barchart2!='')
							v_barchart2.destroy();

						var ctx = document.getElementById("stat_chart1").getContext("2d");
						v_barchart1 = new Chart(ctx).Pie(data1);

						document.getElementById('legend_chart1').innerHTML = v_barchart1.generateLegend();

						var ctx = document.getElementById("stat_chart2").getContext("2d");
						v_barchart2 = new Chart(ctx).Pie(data2);

						document.getElementById('legend_chart2').innerHTML = v_barchart2.generateLegend();

						document.getElementById('div_compare').innerHTML = p_return.v_data.v_html;
						document.getElementById('div_compare_log').innerHTML = p_return.v_data.v_log;*/

					},
					null,
					'box');

		}

		function toggleDiv(p_div) {
			$('#' + p_div).toggle();
		}

	</script>
</head>
<body>

<div class="header">
	<div class="header_menu">
	<img src="images/omnidb.png" />
		<ul>
			<li><a href="Connections.aspx">Connections</a></li>
			<li><a href="MainDB.aspx">Main</a></li>
			<li><a class="header_a_selected" href="CompareDB.aspx">Compare</a></li>
			<li><a href="MigrateDB.aspx">Migrate</a></li>
			<li><a href="Migrations.aspx">Migrations</a></li>
			<li><a>Erase</a></li>
		</ul>
		<div style="position: absolute; right: 0px; top: 0px;"><ul><li style="margin-right: 20px; color: #F1F7FF;"><% Response.Write(v_session.v_user_name); %></li><li><a href="Logout.aspx">Logout</a></li></ul></div>
	</div>
</div>


<table style="margin: 0px auto;">
		<tr>
			<td>
				<div id="div_select_db1" style="width: 250px;">
				</div>
			</td>
			<td>
				<button onclick="compareBases(2)">Compare Bases</button>
			</td>
			<td>
				<div id="div_select_db2" style="width: 250px;">
				</div>
			</td>
		</tr>
		<tr>
			<td>
				<div id="tree1" style="margin: 10px; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, freesans; display: inline-block;"></div>
			</td>
			<td>
			</td>
			<td>
				<div id="tree2" style="margin: 10px; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, freesans; display: inline-block;"></div>
			</td>
		</tr>
	</table>
	<div id="div_comparison_time" style="text-align: center; margin-left: auto; margin-right: auto; width: 90%; margin-bottom: 10px;">
	</div>

	<div id="div_chart" style="display: none; margin-left: auto; margin-right: auto; width: 90%; margin-bottom: 10px;">

		<table style="width:100%">
			<tr>
				<th>
					<p class="chart_title">Tables</p>
				</th>
				<th>
					<p class="chart_title">Columns</p>
				</th>
			</tr>
			<tr>
				<td style="text-align: center; position: relative;">
					<canvas id="stat_chart1" width="250px" height="250px"></canvas>
					<div id="legend_chart1" class="legend_chart"></div>
				</td>
				<td style="text-align: center; position: relative;">
					<canvas id="stat_chart2" width="250px" height="250px"></canvas>
					<div id="legend_chart2" class="legend_chart"></div>
				</td>
			</tr>
		</table>

	</div>

	<div id="div_compare_log" style="margin-left: auto; margin-right: auto; width: 500px; heigth: 200px;">
	</div>
	<div id="div_compare" style="margin-left: auto; margin-right: auto; width: 500px;">
	</div>

    <div id="div_error" style="display:none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 90%; height: 90%; left: 5%; top: 5%;">
                <a class="bt_close" onclick="hideError()">x</a>
                <div id="div_error_msg" style="height:100%; width:100%; margin-top:20px; text-align: center;"></div>
            </div>
        </div>
    </div>


		<div id="div_alert" style="display:none;">
	      <div class="modal_background_dark">
	          <div class ="white_box" style="width: 40%; height: 20%; left: 30%; top: 40%;">
	              <div id="div_alert_content" style="height:100%; width:100%;"></div>
	          </div>
	      </div>
	  </div>

    <div class="div_loading">
    </div>

</body>
</html>
