/*
Copyright 2016 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

using System;
using System.Web;
using System.Web.UI;

namespace OmniDB
{
	/// <summary>
	/// Data structure used to store return data from AJAX calls.
	/// </summary>
	public class AjaxReturn
	{
		public Object v_data;
		public bool v_error;
		public int v_error_id; // 0: Session object is null; 1: Other
	}

	/// <summary>
	/// Data structure used to store data of WebSocket messages.
	/// </summary>
	public class WebSocketMessage
	{
		public int v_user_id;
		public int v_code;
		public bool v_error;
		public Object v_data;

		public WebSocketMessage()
		{
			this.v_user_id = 0;
			this.v_code = 0;
			this.v_error = false;
		}
	}

	/// <summary>
	/// Page to log into the application.
	/// </summary>
	public partial class Login : System.Web.UI.Page
	{

		/// <summary>
		/// Logging into the application.
		/// </summary>
		/// <returns>The in.</returns>
		/// <param name="p_username">Username.</param>
		/// <param name="p_pwd">Password.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SignIn(string p_username, string p_pwd)
		{
			AjaxReturn v_return = new AjaxReturn ();
            Spartacus.Utils.Cryptor v_cryptor = new Spartacus.Utils.Cryptor("omnidb_spartacus");

			// Instantiating tool management database.
			OmniDatabase.Generic v_omnidb_database = OmniDatabase.Generic.InstantiateDatabase ("","0",
				"sqlite",
				"",
				"",
				System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Database"].ToString (),
				"",
				"",
				"");


			if (p_username == "admin") {
				string v_encrypted_pwd = System.IO.File.ReadAllText("config/admin.txt");

				string v_pwd;
				try {
					v_pwd = v_cryptor.Decrypt (v_encrypted_pwd);

					if (v_pwd == p_pwd) {
						Session v_session = new Session("-1", p_username, v_omnidb_database, "", "", "", "");
						v_session.v_omnidb_version = System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Version"].ToString ();
						System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"] = v_session;
						v_return.v_data = true;

					}
					else {
						System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"] = null;
						v_return.v_data = false;
					}

				} catch (Spartacus.Utils.Exception) {
					System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"] = null;
					v_return.v_data = false;
				}

				return v_return;

			} else {
				
				try {
					// Querying user information.
					System.Data.DataTable v_user_data = v_omnidb_database.v_connection.Query (
						                                               "select u.user_id,              " +
						                                               "       u.password,             " +
																	   "       t.theme_id,             " +
						                                               "       t.theme_name,           " +
																	   "       t.theme_type,           " +
						                                               "       u.editor_font_size      " +
						                                               "from users u,                  " +
																	   "     themes t                  " +
																	   " where u.theme_id = t.theme_id " +
						                                               "and u.user_name = '" + p_username + "' ", "db_data");

					// If username exists, decrypt password.
					if (v_user_data.Rows.Count > 0) {
						string v_pwd;
						try {
							v_pwd = v_cryptor.Decrypt (v_user_data.Rows [0] ["password"].ToString ());
						} catch (Spartacus.Utils.Exception) {
							v_pwd = v_user_data.Rows [0] ["password"].ToString ();
						}

						// If password is correct, set user as logged in, instantiate Session and return true.
						if (v_pwd == p_pwd) {

							Session v_session = new Session (v_user_data.Rows [0] ["user_id"].ToString (), p_username, v_omnidb_database, v_user_data.Rows[0]["theme_name"].ToString(), v_user_data.Rows[0]["theme_type"].ToString(), v_user_data.Rows[0]["theme_id"].ToString(), v_user_data.Rows [0] ["editor_font_size"].ToString ());
							v_session.v_omnidb_version = System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Version"].ToString ();
							System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"] = v_session;

							v_omnidb_database.v_connection.Execute (
											"update users " +
											"set online = 1 " +
											"where user_id = " + v_user_data.Rows [0] ["user_id"]);

							v_return.v_data = true;

						} else {

							System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"] = null;
							v_return.v_data = false;

						}
					} else {
						System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"] = null;
						v_return.v_data = false;
					}

				} catch (Spartacus.Database.Exception e) {
					v_return.v_error = true;
					v_return.v_data = e.v_message;
				}

				return v_return;
			}

		}
	}
}

