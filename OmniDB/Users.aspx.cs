/*
Copyright 2015-2017 The OmniDB Team

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
	/// Connections Return Data.
	/// </summary>
	public class UsersData
	{
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> v_data;
		public System.Collections.Generic.List<string> v_user_ids;
	}

	/// <summary>
	/// Page to manage users.
	/// </summary>
	public partial class Users : System.Web.UI.Page
	{
		/// <summary>
		/// Session variable
		/// </summary>
		public Session v_session;

		/// <summary>
		/// Page load function.
		/// </summary>
		protected void Page_Load(object sender, EventArgs e)
		{
			v_session = (Session)Session ["OMNIDB_SESSION"];

			if (v_session == null) {
				Session ["OMNIDB_ALERT_MESSAGE"] = "Session object was destroyed, please sign in again.";
				this.Response.Redirect("Login.aspx");

			}
			else if (v_session.v_user_name!="admin") {
				Session ["OMNIDB_ALERT_MESSAGE"] = "Only admin can manage users.";
				this.Response.Redirect("Connections.aspx");

			}

			Session["DB_SESSION"] = v_session;

		}

		/// <summary>
		/// Creates a new user.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn NewUser()
		{
			AjaxReturn v_return = new AjaxReturn();
			System.Data.DataTable v_connections;
			int v_numconnections;

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			v_numconnections = int.Parse(v_session.v_omnidb_database.v_connection.ExecuteScalar("select count(*) from users"));
			if (v_numconnections > 0)
				v_connections = v_session.v_omnidb_database.v_connection.Query ("select max(user_id)+1 as next_id from users", "Users");
			else
				v_connections = v_session.v_omnidb_database.v_connection.Query ("select 1 as next_id", "Users");

			v_session.v_omnidb_database.v_connection.Execute ("insert into users values ( " +
				v_connections.Rows [0] ["next_id"].ToString () + "," +
				"'user" + v_connections.Rows [0] ["next_id"].ToString () + "','',1,'14')");

			return v_return;

		}

		/// <summary>
		/// Saves admin password.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SaveConfigUser(string p_pwd)
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			Spartacus.Utils.Cryptor v_cryptor = new Spartacus.Utils.Cryptor("omnidb_spartacus");

			System.IO.File.WriteAllText("config/admin.txt",v_cryptor.Encrypt(p_pwd));

			return v_return;

		}

		/// <summary>
		/// Removes the user.
		/// </summary>
		/// <param name="p_id">User id.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn RemoveUser(int p_id)
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			v_session.v_omnidb_database.v_connection.Execute ("delete from users " +
				"where user_id=" + p_id);

			v_session.v_omnidb_database.v_connection.Execute ("delete from connections " +
				"where user_id=" + p_id);

			return v_return;

		}

		/// <summary>
		/// Saves the users.
		/// </summary>
		/// <param name="p_data">Users data.</param>
		/// <param name="p_user_id_list">List with users ids.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SaveUsers(System.Collections.Generic.List<System.Collections.Generic.List<string>> p_data, System.Collections.Generic.List<string> p_user_id_list)
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];
			Spartacus.Utils.Cryptor v_cryptor = new Spartacus.Utils.Cryptor("omnidb_spartacus");

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			string v_update_format = "update users  " +
				"set user_name   = '#p_user_name#', " +
				"password        = '#p_password#'   " +
				"where user_id   = #p_user_id#";

			for (int i=0; i < p_data.Count; i++)
			{

				string v_update = v_update_format;
				v_update = v_update.Replace ("#p_user_id#", p_user_id_list[i]);
				v_update = v_update.Replace ("#p_user_name#", p_data [i][0]);
				try
				{
					v_update = v_update.Replace ("#p_password#", v_cryptor.Encrypt(p_data [i][1]));
				}
				catch (Spartacus.Utils.Exception)
				{
					v_update = v_update.Replace ("#p_password#", p_data [i][1]);
				}

				v_session.v_omnidb_database.v_connection.Execute (v_update);

			}


			return v_return;

		}

		/// <summary>
		/// Gets the users.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetUsers()
		{
			AjaxReturn v_return = new AjaxReturn();
			UsersData v_return_data = new UsersData ();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];
			Spartacus.Utils.Cryptor v_cryptor = new Spartacus.Utils.Cryptor("omnidb_spartacus");

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			System.Data.DataTable v_users = v_session.v_omnidb_database.v_connection.Query ("select * from users order by user_id", "Users");

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_user_list = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();
			System.Collections.Generic.List<string> v_user_id_list = new System.Collections.Generic.List<string>();

			int v_index = 0;

			foreach (System.Data.DataRow v_user in v_users.Rows) 
			{

				System.Collections.Generic.List<string> v_user_data_list = new System.Collections.Generic.List<string>();

				v_user_data_list.Add(v_user["user_name"].ToString());

				try
				{
					v_user_data_list.Add(v_cryptor.Decrypt(v_user["password"].ToString()));
				}
				catch (Spartacus.Utils.Exception)
				{
					v_user_data_list.Add(v_user["password"].ToString());
				}

				if (v_user["user_name"].ToString()=="admin")
					v_user_data_list.Add("");
				else
					v_user_data_list.Add("<img src='images/tab_close.png' class='img_ht' onclick='removeUser(" + v_user["user_id"].ToString() + ")'/>");

				v_index++;

				v_user_list.Add(v_user_data_list);		

				v_user_id_list.Add(v_user["user_id"].ToString());

			}

			v_return_data.v_data = v_user_list;
			v_return_data.v_user_ids = v_user_id_list;

			v_return.v_data = v_return_data;
			return v_return;

		}
	}
}
