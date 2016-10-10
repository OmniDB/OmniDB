<%@ Page Language="C#" Inherits="OmniDB.Users" %>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
    <title>OmniDB</title>

    <link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico" />

	<link rel="stylesheet" type="text/css" href="css/style.css?v1.6"            />
	<link rel="stylesheet" type="text/css" href="css/handsontable.full.css?v1.6"/>
	<link rel="stylesheet" type="text/css" href="css/msdropdown/dd.css?v1.6"    />

	<script type="text/javascript" src="js/jquery-1.11.2.min.js?v1.6"  ></script>
	<script type="text/javascript" src="js/jquery.dd.min.js?v1.6"      ></script>
	<script type="text/javascript" src="js/handsontable.full.js?v1.6"  ></script>
    <script type="text/javascript" src="js/AjaxControl.js?v1.6"        ></script>
    <script type="text/javascript" src="js/NotificationControl.js?v1.6"></script>
    <script type="text/javascript" src="js/Renderers.js?v1.6"          ></script>
    <script type="text/javascript" src="js/HeaderActions.js?v1.6"      ></script>
    <script type="text/javascript" src="js/Users.js?v1.6"              ></script>

	<script type="text/javascript">

		//Global variables
    	var v_users_data;

    </script>
</head>
<body>

<div class="header">
	<div class="header_menu">
	<img src="images/omnidb.png" />
		<ul>
			<li><a class="header_a_selected" href="Users.aspx">Users</a></li>
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
    <button onclick="newUser()">New User</button>
  </div>
  <div id='div_save' style='visibility: hidden; display:inline-block;'>
    <button class="bt_blue" onclick="saveUsers()">Save Data</button>
  </div>

  <div id='div_user_list' style='width: 80%; margin:20px;'></div>

  <div id="div_config_user" style="display: none;">
        <div class="modal_background_dark">
            <div class ="white_box" style="width: 40%; left: 30%; top: 30%;">
                <img src="images/window_close.png" class="img_close" onclick="hideConfigUser()"/>


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
