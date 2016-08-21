<%@ Page Language="C#" Inherits="OmniDB.Connections" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">

    <title>OmniDB</title>

    <link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico"/>

	<link rel="stylesheet" type="text/css" href="css/style.css?v1.6"            />
	<link rel="stylesheet" type="text/css" href="css/handsontable.full.css?v1.6"/>
	<link rel="stylesheet" type="text/css" href="css/msdropdown/dd.css?v1.6"    />
    <link rel="stylesheet" type="text/css" href="lib/tabs/css/tabs.css?v1.6"    />

	<script type="text/javascript" src="js/jquery-1.11.2.min.js?v1.6"  ></script>
	<script type="text/javascript" src="js/jquery.dd.min.js?v1.6"      ></script>
    <script type="text/javascript" src="lib/tabs/lib/tabs.js?v1.6"     ></script>
	<script type="text/javascript" src="js/handsontable.full.js?v1.6"  ></script>
    <script type="text/javascript" src="js/AjaxControl.js?v1.6"        ></script>
    <script type="text/javascript" src="js/NotificationControl.js?v1.6"></script>
    <script type="text/javascript" src="js/Renderers.js?v1.6"          ></script>
    <script type="text/javascript" src="js/HeaderActions.js?v1.6"      ></script>
    <script type="text/javascript" src="js/Connections.js?v1.6"        ></script>

    <script type="text/javascript">

		//Global variables
		var v_connections_data;
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
				<li><a class="header_a_selected" href="Connections.aspx">Connections</a></li>
				<li><a href="MainDB.aspx">Main</a></li>
				<li><a href="Conversions.aspx">Convert</a></li>
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

	<div style='margin-left:20px; margin-top: 20px; display:inline-block;'>
		<button onclick="newConnection()">New Connection</button>
	</div>

	<div id='div_save' style='visibility: hidden; display:inline-block;'>
		<button onclick="saveConnections()">Save Data</button>
	</div>

	<div id='div_conn_list' style='width: 80%; margin:20px;'></div>

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
		                	<option value="1">(Light) OmniDB</option>
		                	<option value="2">(Light) Chrome</option>
		                	<option value="3">(Light) Clouds</option>
		                	<option value="4">(Light) Crimson Editor</option>
		                	<option value="5">(Light) Dawn</option>
		                	<option value="6">(Light) Dreamweaver</option>
		                	<option value="7">(Light) Eclipse</option>
		                	<option value="8">(Light) Github</option>
		                	<option value="9">(Light) Iplastic</option>
		                	<option value="10">(Light) Katzenmilch</option>
		                	<option value="11">(Light) Kuroir</option>
		                	<option value="12">(Light) Solarized Light</option>
		                	<option value="13">(Light) SQL Server</option>
		                	<option value="14">(Light) Textmate</option>
		                	<option value="15">(Light) Tomorrow</option>
		                	<option value="16">(Light) XCode</option>
							<option value="17">(Dark) OmniDB Dark</option>
		                	<option value="18">(Dark) Ambiance</option>
		                	<option value="19">(Dark) Chaos</option>
		                	<option value="20">(Dark) Clouds Midnight</option>
		                	<option value="21">(Dark) Cobalt</option>
		                	<option value="22">(Dark) Idle Fingers</option>
		                	<option value="23">(Dark) KR Theme</option>
		                	<option value="24">(Dark) Merbivore</option>
		                	<option value="25">(Dark) Merbivore Soft</option>
		                	<option value="26">(Dark) Mono Industrial</option>
		                	<option value="27">(Dark) Monokai</option>
		                	<option value="28">(Dark) Pastel On Dark</option>
		                	<option value="29">(Dark) Solarized Dark</option>
		                	<option value="30">(Dark) Terminal</option>
		                	<option value="31">(Dark) Tomorrow Night</option>
		                	<option value="32">(Dark) Tomorrow Night Blue</option>
		                	<option value="33">(Dark) Tomorrow Night Bright</option>
		                	<option value="34">(Dark) Tomorrow Night 80s</option>
		                	<option value="35">(Dark) Twilight</option>
		                	<option value="36">(Dark) Vibrant Ink</option>
		                </select>
		                </div>
		                <div style="text-align: center;">
		                	<button onclick="saveConfigUser();">Save Changes</button>
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
		                	<button onclick="saveConfigUser();">Save Changes</button>
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
                	</div>
                	<div style="margin: 20px;">Rafael Thofehrn Castro<br/><b>Creator</b></div>
                	<div style="margin: 20px;">William Ivanski<br/><b>Collaborator</b></div>
                	<div style="margin: 20px;">Luis Felipe Thofehrn Castro<br/><b>Collaborator</b></div>
                	<div style="margin: 20px;"><a href="http://www.omnidb.com.br">www.omnidb.com.br</a></div>
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
