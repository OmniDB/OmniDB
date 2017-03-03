<%@ Page Language="C#" Inherits="OmniDB.CreateConversion" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>OmniDB</title>

    <link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico" />

	<link rel="stylesheet" type="text/css" href="css/style.css?v1.6"            />
	<link rel="stylesheet" type="text/css" href="css/handsontable.full.css?v1.6"/>
	<link rel="stylesheet" type="text/css" href="css/msdropdown/dd.css?v1.6"    />
    <link rel="stylesheet" type="text/css" href="lib/tabs/css/tabs.css?v1.6"    />

    <script type="text/javascript" src="lib/tabs/lib/tabs.js?v1.6"     ></script>
	<script type="text/javascript" src="js/jquery-1.11.2.min.js?v1.6"  ></script>
	<script type="text/javascript" src="js/jquery.dd.min.js?v1.6"      ></script>
	<script type="text/javascript" src="js/handsontable.full.js?v1.6"  ></script>
    <script type="text/javascript" src="js/AjaxControl.js?v1.6"        ></script>
    <script type="text/javascript" src="js/NotificationControl.js?v1.6"></script>
    <script type="text/javascript" src="js/HeaderActions.js?v1.6"      ></script>
    <script type="text/javascript" src="js/CreateConversion.js?v1.6"   ></script>

	<script type="text/javascript">

		//Global variables
		var v_tables = [];
		var v_editor_theme = "<%= v_session.v_editor_theme %>";
		var	v_theme_type = "<%= v_session.v_theme_type %>";
		var	v_theme_id = "<%= v_session.v_theme_id %>";
		var v_editor_font_size = "<%= v_session.v_editor_font_size %>";

    </script>
</head>
<body>

<div class="header">
	<div class="header_menu">
	<img src="images/omnidb.png" />
		<ul>
			<li><a href="Connections.aspx">Connections</a></li>
			<li><a href="MainDB.aspx">Main</a></li>
			<li><a class="header_a_selected" href="Conversions.aspx">Convert</a></li>
		</ul>
		<div style="position: absolute; right: 0px; top: 0px;">
			<ul>
				<li style="padding-right: 10px; color: #F1F7FF;"><img id="ajax_status" style="vertical-align: middle;" src="images/status_green.png"/></li>
				<li style="color: #F1F7FF;"><% Response.Write(v_session.v_user_name); %></li>
				<li style="padding-left: 10px; padding-right: 10px; color: #F1F7FF;"><img style="vertical-align: middle; cursor: pointer;" onclick="showConfigUser();" src="images/gear.png"/></li>
				<li style="padding-right: 10px; color: #F1F7FF;"><img style="vertical-align: middle; cursor: pointer;" onclick="showAbout();" src="images/about.png"/></li>
				<li><a href="Logout.aspx">Logout</a></li>
			</ul>
		</div>
	</div>
</div>
<div class="div_left">
<h2 style="text-align: center;">Source Database</h2>
<div id="div_select_db1" style="width: 350px; margin: 10px auto;">

</div>

<div style="width: 250px; margin: 10px auto; text-align: center;">
	<button onclick="conversionData()">Generate Conversion Data</button>
</div>

<div id="div_conversion_data" style="margin-left: auto; margin-right: auto; width: 90%; margin-bottom: 10px;">
	</div>

<div id="div_execute" style="display: none; width: 250px; margin: 10px auto; text-align: center;">
	<h2>Target Database</h2>
	<div id="div_select_db2" style="width: 350px; margin: 10px auto; text-align: left;">
	</div>
	<button id="bt_execute" onclick="startConversion()">Create Conversion</button>
</div>
</div>

<div id="div_config_user" style="display: none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 40%; left: 30%; top: 30%;">
				<a class="modal-closer" onclick="hideConfigUser()">x</a>

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
				<a class="modal-closer" onclick="hideAbout()">x</a>
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
                		<img src="images/mariadb_medium.png" title="MariaDB"/>
						<img src="images/filedb_medium.png" title="Spartacus FileDB"/>
                	</div>
                	<div style="margin: 20px;">Rafael Thofehrn Castro<br/><b>Creator</b></div>
                	<div style="margin: 20px;">William Ivanski<br/><b>Collaborator</b></div>
                	<div style="margin: 20px;">Luis Felipe Thofehrn Castro<br/><b>Collaborator</b></div>
					<div style="margin: 20px;">Israel Barth Rubio<br/><b>Collaborator</b></div>
                	<div style="margin: 20px;"><a href="http://www.omnidb.com.br">www.omnidb.com.br</a></div>
                </div>
            </div>
        </div>
    </div>


  <div id="div_error" style="display:none;">
      <div class="modal_background_dark">
          <div class ="white_box" style="width: 90%; height: 90%; left: 5%; top: 5%;">
              <img src="images/window_close.png" class="img_close" onclick="hideError()"/>
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

  <div class="div_loading"></div>


</body>
</html>
