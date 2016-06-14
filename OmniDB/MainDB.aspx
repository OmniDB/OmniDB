<%@ Page Language="C#" Inherits="OmniDB.MainDB" %>
<!DOCTYPE html>
<html style="height: 100%;">
<head runat="server">
	<title>OmniDB</title>

	<link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico" />

	<link rel="stylesheet" type="text/css" href="css/style.css"                   />
	<link rel="stylesheet" type="text/css" href="css/handsontable.full.css"       />
	<link rel="stylesheet" type="text/css" href="css/msdropdown/dd.css"           />
    <link rel="stylesheet" type="text/css" href="lib/jquery-ui/jquery-ui.css"     />
    <link rel="stylesheet" type="text/css" href="lib/jqplot/jquery.jqplot.min.css"/>
    <link rel="stylesheet" type="text/css" href="lib/aimaraJS/css/Aimara.css"     />
    <link rel="stylesheet" type="text/css" href="lib/tabs/css/tabs.css"           />

	<script type="text/javascript" src="js/jquery-1.11.2.min.js"                                ></script>
	<script type="text/javascript" src="lib/jquery-ui/jquery-ui.js"                             ></script>
	<script type="text/javascript" src="js/jquery.dd.min.js"                                    ></script>
	<script type="text/javascript" src="js/handsontable.full.js"                                ></script>
    <script type="text/javascript" src="lib/cytoscape/cytoscape.min.js"                         ></script>
    <script src="https://cdn.rawgit.com/cytoscape/cytoscape.js-spread/1.0.9/cytoscape-spread.js"></script>
    <script type="text/javascript" src="lib/chart/chart.min.js"                                 ></script>
    <script type="text/javascript" src="js/Tree.js"                                             ></script>
    <script type="text/javascript" src="js/NotificationControl.js"                              ></script>
    <script type="text/javascript" src="js/AjaxControl.js"                                      ></script>
    <script type="text/javascript" src="lib/tabs/lib/tabs.js"                                   ></script>
    <script type="text/javascript" src="lib/aimaraJS/lib/Aimara.js"                             ></script>
    <script type="text/javascript" src="lib/ace/ace.js"                                         ></script>
	<script type="text/javascript" src="lib/ace/mode-sql.js"                                    ></script>
	<script type="text/javascript" src="lib/ace/ext-language_tools.js"                          ></script>
	<script type="text/javascript" src="js/Renderers.js"                                        ></script>
    <script type="text/javascript" src="js/HeaderActions.js"                                    ></script>
    <script type="text/javascript" src="js/MainDB.js"                                           ></script>

	<script type="text/javascript">

		//Global variables
		var ht;
		var network;
		var v_tabControl;
		var v_alterTableObject;
		var v_firstModeTable;
		var v_alterTabControl;
		var v_commandListObject;
		var v_editDataObject;
		var v_canEditContent;
		var v_editContentObject;
		var v_editor_theme = "<%= v_session.v_editor_theme %>";
		var v_editor_font_size = "<%= v_session.v_editor_font_size %>";
		var v_completer_ready = true;
		var v_tree_object;
		var v_keybind_object = { v_execute: "<%= System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Keybind.Execute"].ToString() %>",
								 v_execute_mac: "<%= System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Keybind.ExecuteMac"].ToString() %>",
								 v_replace: "<%= System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Keybind.Replace"].ToString() %>",
								 v_replace_mac: "<%= System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Keybind.ReplaceMac"].ToString() %>" };

	</script>
</head>
<body  style="height: 100%;">

<div class="header">
	<div class="header_menu">
	<img src="images/omnidb.png" />
		<ul>
			<li><a href="Connections.aspx">Connections</a></li>
			<li><a class="header_a_selected" href="MainDB.aspx">Main</a></li>
			<li><a href="Conversions.aspx">Convert</a></li>
		</ul>
		<div style="position: absolute; right: 0px; top: 0px;">
			<ul>
				<li style="padding-right: 10px; color: #F1F7FF;"><img id="ajax_status" style="vertical-align: middle;" src="images/status_green.png"/></li>
				<li style="color: #F1F7FF;"><% Response.Write(v_session.v_user_name); %></li>
				<li style="padding-left: 10px; padding-right: 10px; color: #F1F7FF;"><img style="vertical-align: middle; cursor: pointer;" onclick="showConfigUser();" src="images/gear.png"/></li>
				<li style="padding-right: 10px; color: #F1F7FF;"><img style="vertical-align: middle; cursor: pointer;" onclick="showAbout();" src="images/about.png"/></li>
				<li style="padding-right: 10px; color: #F1F7FF;"><img style="vertical-align: middle; cursor: pointer;" onclick="showCommandList();" src="images/command_list.png"/></li>
				<li><a href="Logout.aspx">Logout</a></li>
			</ul>
		</div>
	</div>
</div>



    <div id="div_left" style="float:left; width:30%; height: 90%;">

    	<div id="div_select_db" style="width: 97%; padding-left: 5px;">
        </div>

        <div id="tree1" style="margin: 10px; overflow: auto; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, freesans;">
        </div>

        <div id="html1">
        </div>

    </div>

    <div id="div_right" style="float:left; width:70%;">

    	<div id="tabs" style="width: 99%;">
  <ul>
  </ul>

</div>
</div>

    <div id="div_graph" style="display:none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 90%; height: 90%; left: 5%; top: 5%;">
                <img src="images/window_close.png" class="img_close" onclick="modalGraph('hide')"/>

                <div id="div_legend">
                <ul style="padding-left: 10px; padding-right: 10px;">
                <li class="li_legend"><div class="div_legend_color" style=" background-color: red;"></div><p id="p_legend_5" class="p_legend_label">Vermelho</p></li>
                <li class="li_legend"><div class="div_legend_color" style=" background-color: orange;"></div><p id="p_legend_4" class="p_legend_label">Vermelho</p></li>
                <li class="li_legend"><div class="div_legend_color" style=" background-color: yellow;"></div><p id="p_legend_3" class="p_legend_label">Vermelho</p></li>
                <li class="li_legend"><div class="div_legend_color" style=" background-color: lightgreen;"></div><p id="p_legend_2" class="p_legend_label">Vermelho</p></li>
                <li class="li_legend"><div class="div_legend_color" style=" background-color: cyan;"></div><p id="p_legend_1" class="p_legend_label">Vermelho</p></li>
                <li class="li_legend"><div class="div_legend_color" style=" background-color: #6E6EFD;"></div><p id="p_legend_0" class="p_legend_label">Vermelho</p></li>
                </ul>

                </div>

                <div id="visualization" style="height:100%; width:100%;">

                	<div id="div_graph_content" style="height:100%; width:100%; z-index: 999"></div>

                </div>
            </div>
        </div>
    </div>

    <div id="div_error" style="display:none;">
        <div class="modal_background_dark" style="z-index: 2000">
            <div class ="white_box" style="width: 90%; height: 90%; left: 5%; top: 5%; z-index: 2000;">
                <img src="images/window_close.png" class="img_close" onclick="hideError()"/>
                <div id="div_error_msg" style="height:100%; width:100%; margin-top:20px; text-align: center;"></div>
            </div>
        </div>
    </div>

    <div id="div_statistics" style="display:none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 90%; height: 90%; left: 5%; top: 5%;">
                <img src="images/window_close.png" class="img_close" onclick="hideStatistics()"/>
                <div id="div_statistics" style="width:100%; overflow: auto;">
                	<div id="tot_records" style="margin: 10px;"></div>
                	<canvas id="stat_chart" width="800px" height="500px"></canvas>
                </div>
            </div>
        </div>
    </div>

    <div id="div_alter_table" style="display:none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 90%; left: 5%; top: 5%; font-size: 11px; font-family: sans-serif;">
                <img src="images/window_close.png" class="img_close" onclick="hideAlterTable()"/>
                <span style="margin-left: 10px;">Table Name: </span><input type="text" id="txt_tableNameAlterTable" onchange='changeTableName()' style="margin: 10px;"/>
                <button id="bt_saveAlterTable" class="bt_blue" onclick="saveAlterTable()" style="visibility: hidden;">Save Changes</button>
                <div id="alter_tabs" style='margin-left: 10px; margin-right: 10px; margin-bottom: 10px;'>
	                <ul>
	                <li id="alter_tabs_tab1">Columns</li>
	                <li id="alter_tabs_tab2">Constraints</li>
	                <li id="alter_tabs_tab3">Indexes</li>
	  				</ul>
	  				<div id="div_alter_tabs_tab1">
	  					<div style="padding: 20px;">
		                	<div id='div_alter_table_data' style='width: 100%; height: 400px; overflow: auto;'></div>
		                </div>
	  				</div>
	  				<div id="div_alter_tabs_tab2">

	  					<button id="bt_newConstraintAlterTable" onclick="newConstraintAlterTable()" style="margin-left: 20px; margin-top: 20px;">New Constraint</button>
	  					<div style="padding: 20px;">
	  						<div id='div_alter_constraint_data' style='width: 100%; height: 400px; overflow: auto;'></div>
	  					</div>
	  				</div>
	  				<div id="div_alter_tabs_tab3">

	  					<button id="bt_newIndexAlterTable" onclick="newIndexAlterTable()" style="margin-left: 20px; margin-top: 20px;">New Index</button>
	  					<div style="padding: 20px;">
	  						<div id='div_alter_index_data' style='width: 100%; height: 400px; overflow: auto;'></div>
	  					</div>
	  				</div>
  				</div>
            </div>
        </div>
    </div>

    <div id="div_edit_data" style="display:none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 90%; left: 5%; top: 5%; font-size: 11px; font-family: sans-serif;">
                <img src="images/window_close.png" class="img_close" onclick="hideAlterData()"/>
                <div id='div_edit_data_select' style='margin: 10px; font-size: 14px;'></div>
                <div id='txt_filter_data' style=' margin-left: 10px; margin-right: 10px; height: 100px;border: 1px solid #c3c3c3;'></div>
                <button title='Run (CTRL + Q)' style='margin-top: 10px; margin-bottom: 10px; margin-left: 10px; margin-right: 5px; display: inline-block;' onclick='queryEditData()'><img src='images/play.png' style='vertical-align: middle;'/></button>
                <select id="sel_filtered_data" onchange='queryEditData()'>
                	<option value="10" >10 rows</option>
                	<option value="100">100 rows</option>
                	<option value="1000">1000 rows</option>
                </select>
                <div id='div_edit_data_query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>
                <button id="bt_saveEditData" class="bt_blue" onclick="saveEditData()" style="visibility: hidden; margin-left: 5px;">Save Changes</button>
                <div style="padding: 10px;">
                	<div id='div_edit_data_data' style='width: 100%; height: 400px; overflow: auto;'></div>
                </div>
            </div>
        </div>
    </div>

    <div id="div_command_list" style="display:none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 90%; left: 5%; top: 5%; font-size: 11px; font-family: sans-serif;">
                <img src="images/window_close.png" class="img_close" onclick="hideCommandList()"/>
             	<div style='margin-left:20px; margin-top: 20px; display:inline-block;'>
			      <button onclick="deleteCommandList()">Clear list</button>
			    </div>
                <div style="padding: 10px;">
                	<div id='div_command_list_data' style='width: 100%; height: 600px; overflow: auto;'></div>
                </div>
            </div>
        </div>
    </div>

    <div id="div_column_selection" style="display: none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 40%; height: 40%; left: 30%; top: 30%;">
                <img src="images/window_close.png" class="img_close" onclick="hideColumnSelection()"/>

                <div style="margin: 30px; position: absolute; height: auto; top: 0px; bottom: 0px; left: 0px; right: 0px;">

                <select id="sel_columns_left" ondblclick="addColumnToList()" style="width: 200px; height: 100%" size="10">
                	<option value="1">Column 1</option>
                	<option value="1">Column 2</option>
                	<option value="1">Column 3</option>
                	<option value="1">Column 4</option>
                </select>

                <div style="display: inline-block; vertical-align: top; width: 80px; position: absolute; left: 50%; margin-left: -40px;">

                	<div><button onclick="addColumnToList()"   style="width: 100%; margin-bottom: 10px;">Add</button></div>
                	<div><button onclick="remColumnFromList()" style="width: 100%;">Remove</button></div>

                </div>

                <select id="sel_columns_right" ondblclick="remColumnFromList()" style="width: 200px; height: 100%; position: absolute; right: 0px;" size="10">
                	<option value="1">Column 5</option>
                	<option value="1">Column 6</option>
                	<option value="1">Column 7</option>
                	<option value="1">Column 8</option>
                </select>

                </div>



            </div>
        </div>
    </div>

    <div id="div_find_replace" style="display: none;">
        <div class="modal_background_dark" style="z-index: 2000">
            <div class ="white_box" style="width: 40%; left: 30%; top: 30%;">
                <img src="images/window_close.png" class="img_close" onclick="hideFindReplace()"/>

                <div id="find_replace" style='margin-top: 10px; margin-left: 10px; margin-right: 10px; margin-bottom: 10px;'>
	                <ul>
	                <li id="find_replace_tab1">Find & Replace</li>
	  				</ul>
	  				<div id="div_find_replace_tab1">

	  					<div style="margin: 30px; height: auto; top: 0px; bottom: 0px; left: 0px; right: 0px;">
		                <div style="text-align: center;">
		                <div style="margin-bottom: 10px;">Text</div>
		                <input id="txt_replacement_text" type="text" style="width: 200px; margin-bottom: 20px;">
		                </div>
		                <div style="text-align: center;">
		                <div style="margin-bottom: 10px;">Replacement</div>
		                <input id="txt_replacement_text_new" type="text" style="width: 200px; margin-bottom: 20px;">
		                </div>
		                <div style="text-align: center;">
		                	<button class="bt_blue" onclick="replaceText();">Replace</button>
		                </div>
		                </div>


	  				</div>
  				</div>


            </div>
        </div>
    </div>

    <div id="div_config_user" style="display: none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 40%; left: 30%; top: 30%;">
                <img src="images/window_close.png" class="img_close" onclick="hideConfigUser()"/>

                <div id="config_tabs" style='margin-top: 10px; margin-left: 10px; margin-right: 10px; margin-bottom: 10px;'>
	                <ul>
	                <li id="config_tabs_tab1">Editor</li>
	                <li id="config_tabs_tab2">User</li>
	  				</ul>
	  				<div id="div_config_tabs_tab1">

	  					<div style="margin: 30px; height: auto; top: 0px; bottom: 0px; left: 0px; right: 0px;">
		                <div style="text-align: center;">
		                <div style="margin-bottom: 10px;">Editor font size</div>
		                <select id="sel_editor_font_size" style="width: 200px; margin-bottom: 20px;">
		                	<option value="10">10</option>
		                	<option value="11">11</option>
		                	<option value="12">12</option>
		                	<option value="13">13</option>
		                	<option value="14">14</option>
		                	<option value="15">15</option>
		                	<option value="16">16</option>
		                	<option value="17">17</option>
		                	<option value="18">18</option>
		                </select>
		                </div>

		                <div style="text-align: center;">
		                <div  style="margin-bottom: 10px;">Editor theme</div>
		                <select id="sel_editor_theme" style="width: 200px; margin-bottom: 20px;">
		                	<option value="omnidb">(Light) OmniDB</option>
		                	<option value="chrome">(Light) Chrome</option>
		                	<option value="clouds">(Light) Clouds</option>
		                	<option value="crimson_editor">(Light) Crimson Editor</option>
		                	<option value="dawn">(Light) Dawn</option>
		                	<option value="dreamweaver">(Light) Dreamweaver</option>
		                	<option value="eclipse">(Light) Eclipse</option>
		                	<option value="github">(Light) Github</option>
		                	<option value="iplastic">(Light) Iplastic</option>
		                	<option value="katzenmilch">(Light) Katzenmilch</option>
		                	<option value="kuroir">(Light) Kuroir</option>
		                	<option value="solarized_light">(Light) Solarized Light</option>
		                	<option value="sqlserver">(Light) SQL Server</option>
		                	<option value="textmate">(Light) Textmate</option>
		                	<option value="tomorrow">(Light) Tomorrow</option>
		                	<option value="xcode">(Light) XCode</option>
		                	<option value="ambiance">(Dark) Ambiance</option>
		                	<option value="chaos">(Dark) Chaos</option>
		                	<option value="clouds_midnight">(Dark) Clouds Midnight</option>
		                	<option value="cobalt">(Dark) Cobalt</option>
		                	<option value="idle_fingers">(Dark) Idle Fingers</option>
		                	<option value="kr_theme">(Dark) KR Theme</option>
		                	<option value="merbivore">(Dark) Merbivore</option>
		                	<option value="merbivore_soft">(Dark) Merbivore Soft</option>
		                	<option value="mono_industrial">(Dark) Mono Industrial</option>
		                	<option value="monokai">(Dark) Monokai</option>
		                	<option value="pastel_on_dark">(Dark) Pastel On Dark</option>
		                	<option value="solarized_dark">(Dark) Solarized Dark</option>
		                	<option value="terminal">(Dark) Terminal</option>
		                	<option value="tomorrow_night">(Dark) Tomorrow Night</option>
		                	<option value="tomorrow_night_blue">(Dark) Tomorrow Night Blue</option>
		                	<option value="tomorrow_night_bright">(Dark) Tomorrow Night Bright</option>
		                	<option value="tomorrow_night_eighties">(Dark) Tomorrow Night 80s</option>
		                	<option value="twilight">(Dark) Twilight</option>
		                	<option value="vibrant_ink">(Dark) Vibrant Ink</option>
		                </select>
		                </div>
		                <div style="text-align: center;">
		                	<button class="bt_blue" onclick="saveConfigUser();">Save Changes</button>
		                </div>
		                </div>


	  				</div>
	  				<div id="div_config_tabs_tab2">

	  					<div style="margin: 30px; height: auto; top: 0px; bottom: 0px; left: 0px; right: 0px;">
		                <div style="text-align: center;">
		                <div style="margin-bottom: 10px;">New Password</div>
		                <input id="txt_new_pwd" type="password" style="width: 200px; margin-bottom: 20px;">
		                </div>
		                <div style="text-align: center;">
		                <div style="margin-bottom: 10px;">Confirm New Password</div>
		                <input id="txt_confirm_new_pwd" type="password" style="width: 200px; margin-bottom: 20px;">
		                </div>
		                <div style="text-align: center;">
		                	<button class="bt_blue" onclick="saveConfigUser();">Save Changes</button>
		                </div>
		                </div>


	  				</div>
  				</div>


            </div>
        </div>
    </div>

    <div id="div_about" style="display: none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 40%; left: 30%; top: 30%;">
                <img src="images/window_close.png" class="img_close" onclick="hideAbout()"/>
                <div style="width: 100%; text-align: center;">
                	<div style="margin: 20px;"><h1><% Response.Write(v_session.v_omnidb_version); %></h1></div>
                	<div style="margin: 20px;">
                		<img src="images/oracle_medium.png" title="Oracle"/>
                		<img src="images/postgresql_medium.png" title="PostgreSQL"/>
                		<img src="images/mysql_medium.png" title="MySQL"/>
                		<img src="images/sqlserver_medium.png" title="SQL Server"/>
                		<img src="images/firebird_medium.png" title="Firebird"/>
                		<img src="images/sqlite_medium.png" title="SQLite"/>
                		<img src="images/access_medium.png" title="Microsoft Access"/>
                	</div>
                	<div style="margin: 20px;">Rafael Thofehrn Castro<br/><b>Creator</b></div>
                	<div style="margin: 20px;">William Ivanski<br/><b>Collaborator</b></div>
                	<div style="margin: 20px;">Luis Felipe Thofehrn Castro<br/><b>Collaborator</b></div>
                	<div style="margin: 20px;"><a href="http://www.omnidb.com.br">www.omnidb.com.br</a></div>
                </div>
            </div>
        </div>
    </div>

    <div id="div_commands_log" style="display: none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 90%; height: 90%; left: 5%; top: 5%;">
                <img src="images/window_close.png" class="img_close" onclick="hideCommandsLog()"/>

                <div style="height: 100%;">
	                <div id="div_commands_log_list" style="margin: 20px; height: 90%; overflow: scroll;">
	                </div>
                </div>
            </div>
        </div>
    </div>

    <div id="div_edit_content" style="display: none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 90%; height: 90%; left: 5%; top: 5%;">
                <img src="images/window_close.png" class="img_close" onclick="hideEditContent()"/>

                <div style="height: 90%; padding: 30px;">
	                <div id="txt_edit_content" style="width: 100%; height: 100%; font-size: 12px; border: 1px solid rgb(195, 195, 195);">
	                </div>
                </div>

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