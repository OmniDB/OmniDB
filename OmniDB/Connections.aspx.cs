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
	/// Connections Data.
	/// </summary>
	public class ConnectionsData
	{
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> v_data;
		public System.Collections.Generic.List<string> v_technologies;
		public System.Collections.Generic.List<string> v_conn_ids;
	}

	/// <summary>
	/// Session State.
	/// </summary>
	public class SessionState
	{
		public bool v_active;
		public bool v_has_connections;
	}

	/// <summary>
	/// Page to list and add new database connections.
	/// </summary>
	public partial class Connections : System.Web.UI.Page
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

				this.Response.Redirect("Login.aspx");

			}
			else if (v_session.v_user_name=="admin") {
				Session ["OMNIDB_ALERT_MESSAGE"] = "Admin can only manage users.";
				this.Response.Redirect("Users.aspx");

			}

			Session["DB_SESSION"] = v_session;

		}

		/// <summary>
		/// Checks session message to display alert.
		/// </summary>
		/// <returns>Session state.</returns>
		[System.Web.Services.WebMethod]
		public static AjaxReturn CheckSessionMessage()
		{

			AjaxReturn v_return = new AjaxReturn();

			string v_message;

			if (System.Web.HttpContext.Current.Session ["OMNIDB_ALERT_MESSAGE"] != null)
				v_message = System.Web.HttpContext.Current.Session ["OMNIDB_ALERT_MESSAGE"].ToString ();
			else
				v_message = "";

			System.Web.HttpContext.Current.Session ["OMNIDB_ALERT_MESSAGE"] = "";

			v_return.v_data = v_message;
			return v_return;

		}

		/// <summary>
		/// Checks session variable.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn CheckSession()
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			SessionState v_ses_state = new SessionState ();


			v_ses_state.v_has_connections = true;

			if (v_session.v_databases.Count > 0)
				v_ses_state.v_has_connections = true;
			else
				v_ses_state.v_has_connections = false;
		

			v_return.v_data = v_ses_state;
			return v_return;

		}

		/// <summary>
		/// Creates new connection in omnidb database.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn NewConnection()
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

            v_numconnections = int.Parse(v_session.v_omnidb_database.v_connection.ExecuteScalar("select count(*) from connections"));
            if (v_numconnections > 0)
			    v_connections = v_session.v_omnidb_database.v_connection.Query ("select max(conn_id)+1 as next_id from connections", "Connections");
            else
                v_connections = v_session.v_omnidb_database.v_connection.Query ("select 1 as next_id", "Connections");

			v_session.v_omnidb_database.v_connection.Execute ("insert into connections values ( " +
															  v_connections.Rows [0] ["next_id"].ToString () + "," +
															  v_session.v_user_id + "," +
															  "'sqlite','','','','','','','')");

			v_session.RefreshDatabaseList ();

			return v_return;

		}

		/// <summary>
		/// Removes the connection.
		/// </summary>
		/// <param name="p_id">Connection ID.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn RemoveConnection(int p_id)
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			v_session.v_omnidb_database.v_connection.Execute ("delete from connections " +
				"where conn_id=" + p_id);

			v_session.RefreshDatabaseList ();

			return v_return;

		}

		/// <summary>
		/// Tests the connection.
		/// </summary>
		/// <returns>The connection.</returns>
		/// <param name="p_index">List index.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn TestConnection(int p_index)
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			v_return.v_data = v_session.v_databases [p_index].TestConnection ();



			return v_return;

		}

		/// <summary>
		/// Saves the connections.
		/// </summary>
		/// <param name="p_data">Connections data.</param>
		/// <param name="p_conn_id_list">List of connections ids.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SaveConnections(System.Collections.Generic.List<System.Collections.Generic.List<string>> p_data, System.Collections.Generic.List<string> p_conn_id_list)
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

			string v_update_format = "update connections " +
				"set dbt_st_name = '#p_dbt_st_name#', " +
				"server          = '#p_server#', " +
				"port            = '#p_port#', " +
				"service         = '#p_service#', " +
				"schema          = '#p_schema#', " +
				"user            = '#p_user#', " +
				"password        = '#p_password#', " +
				"alias           = '#p_alias#' " +
			    "where conn_id   = #p_conn_id#";

			for (int i=0; i < p_data.Count; i++)
			{

                string v_update = v_update_format;
                v_update = v_update.Replace ("#p_conn_id#", p_conn_id_list[i]);
                v_update = v_update.Replace ("#p_dbt_st_name#", p_data [i][0]);
                try
                {
                    v_update = v_update.Replace ("#p_server#", v_cryptor.Encrypt(p_data [i][1]));
                    v_update = v_update.Replace ("#p_port#", v_cryptor.Encrypt(p_data [i][2]));
                    v_update = v_update.Replace ("#p_service#", v_cryptor.Encrypt(p_data [i][3]));
                    v_update = v_update.Replace ("#p_schema#", v_cryptor.Encrypt(p_data [i][4]));
                    v_update = v_update.Replace ("#p_user#", v_cryptor.Encrypt(p_data [i][5]));
					v_update = v_update.Replace ("#p_password#", v_cryptor.Encrypt(p_data [i][6]));
					v_update = v_update.Replace ("#p_alias#", v_cryptor.Encrypt(p_data [i][7]));
                }
                catch (Spartacus.Utils.Exception)
                {
                    v_update = v_update.Replace ("#p_server#", p_data [i][1]);
                    v_update = v_update.Replace ("#p_port#", p_data [i][2]);
                    v_update = v_update.Replace ("#p_service#", p_data [i][3]);
                    v_update = v_update.Replace ("#p_schema#", p_data [i][4]);
                    v_update = v_update.Replace ("#p_user#", p_data [i][5]);
					v_update = v_update.Replace ("#p_password#", p_data [i][6]);
					v_update = v_update.Replace ("#p_alias#", p_data [i][7]);
                }

				v_session.v_omnidb_database.v_connection.Execute (v_update);

			}

			v_session.RefreshDatabaseList ();

			return v_return;

		}

		/// <summary>
		/// Retrieving all database connections.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetConnections()
		{

			AjaxReturn v_return = new AjaxReturn();
			ConnectionsData v_return_data = new ConnectionsData ();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];
            Spartacus.Utils.Cryptor v_cryptor = new Spartacus.Utils.Cryptor("omnidb_spartacus");

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

            System.Data.DataTable v_connections = v_session.v_omnidb_database.v_connection.Query ("select * from connections where user_id = " + v_session.v_user_id + " order by dbt_st_name, conn_id", "Connections");
			System.Data.DataTable v_techs = v_session.v_omnidb_database.v_connection.Query ("select dbt_st_name from db_type", "Technologies");

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_connection_list = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();
			System.Collections.Generic.List<string> v_tech_list = new System.Collections.Generic.List<string>();
			System.Collections.Generic.List<string> v_conn_id_list = new System.Collections.Generic.List<string>();

			foreach (System.Data.DataRow v_tech in v_techs.Rows) 
			{
				v_tech_list.Add(v_tech["dbt_st_name"].ToString());
			}

			int v_index = 0;

			foreach (System.Data.DataRow v_connection in v_connections.Rows) 
			{

				System.Collections.Generic.List<string> v_connection_data_list = new System.Collections.Generic.List<string>();

				v_connection_data_list.Add(v_connection["dbt_st_name"].ToString());

                try
                {
                    v_connection_data_list.Add(v_cryptor.Decrypt(v_connection["server"].ToString()));
                    v_connection_data_list.Add(v_cryptor.Decrypt(v_connection["port"].ToString()));
                    v_connection_data_list.Add(v_cryptor.Decrypt(v_connection["service"].ToString()));
                    v_connection_data_list.Add(v_cryptor.Decrypt(v_connection["schema"].ToString()));
                    v_connection_data_list.Add(v_cryptor.Decrypt(v_connection["user"].ToString()));
					v_connection_data_list.Add(v_cryptor.Decrypt(v_connection["password"].ToString()));
					v_connection_data_list.Add(v_cryptor.Decrypt(v_connection["alias"].ToString()));
                }
                catch (Spartacus.Utils.Exception)
                {
                    v_connection_data_list.Add(v_connection["server"].ToString());
                    v_connection_data_list.Add(v_connection["port"].ToString());
                    v_connection_data_list.Add(v_connection["service"].ToString());
                    v_connection_data_list.Add(v_connection["schema"].ToString());
                    v_connection_data_list.Add(v_connection["user"].ToString());
					v_connection_data_list.Add(v_connection["password"].ToString());
					v_connection_data_list.Add(v_connection["alias"].ToString());
                }

				v_connection_data_list.Add("<img src='images/tab_close.png' class='img_ht' onclick='removeConnection(" + v_connection["conn_id"].ToString() + ")'/>" +
					"<img src='images/test.png' class='img_ht' onclick='testConnection(" + v_index + ")'/>");

				v_index++;

				v_connection_list.Add(v_connection_data_list);		

				v_conn_id_list.Add(v_connection["conn_id"].ToString());
			
			}

			v_return_data.v_data = v_connection_list;
			v_return_data.v_technologies = v_tech_list;
			v_return_data.v_conn_ids = v_conn_id_list;

			v_return.v_data = v_return_data;
			return v_return;

		}

	}
}
