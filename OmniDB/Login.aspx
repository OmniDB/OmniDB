<%@ Page Language="C#" Inherits="OmniDB.Login" %>
<!DOCTYPE html>
<html>
<head runat="server">
	<title>OmniDB</title>

	<link rel="shortcut icon" type="image/x-icon" href="images/favicon.ico" />

	<link rel="stylesheet" type="text/css" href="css/style.css?v1.6"/>
		
	<script type="text/javascript" src="js/jquery-1.11.2.min.js?v1.6"   ></script>
	<script type="text/javascript" src="lib/jquery-ui/jquery-ui.js?v1.6"></script>
  	<script type="text/javascript" src="js/NotificationControl.js?v1.6" ></script>
  	<script type="text/javascript" src="js/AjaxControl.js?v1.6"         ></script>
  	<script type="text/javascript" src="js/WebSocketControl.js?v1.6"    ></script>
	<script type="text/javascript">

		$(function () {

			checkSessionMessage();

		});

		function signIn() {

			document.getElementById("txt_user").blur();
			document.getElementById("txt_pwd").blur();

			var v_user_name = document.getElementById('txt_user').value;
			var v_pwd = document.getElementById('txt_pwd').value;

			execAjax('Login.aspx/SignIn',
				JSON.stringify({"p_username": v_user_name, "p_pwd": v_pwd}),
				function(p_return) {

					if (p_return.v_data==true) {
						if (v_user_name=='admin') {
							window.open("Users.aspx",'_self');
						}
						else {
							window.open("Connections.aspx",'_self');
						}
					}
					else
						showAlert('Invalid username or password.');

				},
				null,
				'box'
			);
		}

	</script>
</head>
<body id="grad1">
<div id="div_form">
	<table style="width: 70%; margin-left: auto; margin-right: auto; height: 200px; vertical-align: middle;">
	<tr>
	<td style="width: 20%;">
	<div id="div_time" style="font-size: 50px; color:white; font-weight: bold; text-shadow: 2px 2px rgb(106, 129, 162);"><img src="images/omnidb_big.png"/></div>
	</td>
	<td style="width: 80%;">
		<input id='txt_user' type='text' placeholder='user' onkeydown="if (event.keyCode == 13) signIn();"/>
		<input id='txt_pwd' type='password' placeholder='password' onkeydown="if (event.keyCode == 13) signIn();"/>
		<button onclick='signIn()'>Sign in</button>
	</td>
	</tr>
	</table>
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
				<div class ="white_box" style="width: 30%; height: 20%; left: 35%; top: 40%;">
						<div id="div_alert_content" style="height:100%; width:100%;"></div>
				</div>
		</div>
</div>

	<div class="div_loading">
	</div>

</body>
</html>
