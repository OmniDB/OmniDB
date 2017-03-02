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
	/// Data required to create list of tables.
	/// </summary>
	public class ConversionDataReturn {
		public string v_html;
		public System.Collections.Generic.List<string> v_tables;
	}

	/// <summary>
	/// Table info to create a conversion.
	/// </summary>
	public class ConversionTableData {
		public string v_table;
		public bool v_drop_records;
		public bool v_create_table;
		public bool v_transfer_data;
		public bool v_create_pks;
		public bool v_create_fks;
		public bool v_create_uniques;
		public bool v_create_indexes;
		public string v_transferfilter;
	}

	/// <summary>
	/// Page to create Conversion task.
	/// </summary>
	public partial class CreateConversion : System.Web.UI.Page
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
			else if (v_session.v_databases.Count==0) {
				Session ["OMNIDB_ALERT_MESSAGE"] = "There are no database connections, please add at least one before using the application.";
				this.Response.Redirect("Connections.aspx");

			}

			Session["OMNIDB_SESSION"] = v_session;
		}	


		/// <summary>
		/// Generate Conversion data.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn ConversionData(int p_database_index)
		{
			AjaxReturn v_return = new AjaxReturn ();

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) {
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			ConversionDataReturn v_conversion_data = new ConversionDataReturn ();

			string v_html = "<table class='conversion_table'>" +
				"<tr>" +
				"<th>Drop Existing Records</th>" +
				"<th>Create Table</th>" +
				"<th>Transfer Data</th>" +
				"<th>Create Primary Keys</th>" +
				"<th>Create Foreign Keys</th>" +
				"<th>Create Uniques</th>" +
				"<th>Create Indexes</th>" +
				"<th>Transfer Filter</th>" +
				"<th>Table</th>" +
				"</tr>" +
				"<tr>" +
				"<td><input id='cb_all_drop_records' onchange='changeAllCheckboxes(this,0)' type='checkbox'/></td>" +
				"<td><input id='cb_all_create_tables' onchange='changeAllCheckboxes(this,1)' type='checkbox'/></td>" +
				"<td><input id='cb_all_transfer_data' onchange='changeAllCheckboxes(this,2)' type='checkbox'/></td>" +
				"<td><input id='cb_all_create_pks' onchange='changeAllCheckboxes(this,3)' type='checkbox'/></td>" +
				"<td><input id='cb_all_create_fks' onchange='changeAllCheckboxes(this,4)' type='checkbox'/></td>" +
				"<td><input id='cb_all_create_uniques' onchange='changeAllCheckboxes(this,5)' type='checkbox'/></td>" +
				"<td><input id='cb_all_create_indexes' onchange='changeAllCheckboxes(this,6)' type='checkbox'/></td>" +
				"<td></td>" +
				"<td></td>" +
				"</tr>";

			System.Collections.Generic.List<string> v_tables_list = new System.Collections.Generic.List<string> ();

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			try {
				System.Data.DataTable v_tables = v_database.QueryTables (false);

				int v_counter = 0;

				foreach (System.Data.DataRow v_table in v_tables.Rows) {

					string tname = v_table ["table_name"].ToString ();

					v_tables_list.Add (tname);

					string v_class = "";

					if (v_counter % 2 == 0)
						v_class = "class='even_tr'";

					v_html += "<tr " + v_class + ">" +
						"<td><input id='cb_"  + tname + "_drop_records' type='checkbox'/></td>" +
						"<td><input id='cb_"  + tname + "_create_table' type='checkbox'/></td>" +
						"<td><input id='cb_"  + tname + "_transfer_data' type='checkbox'/></td>" +
						"<td><input id='cb_"  + tname + "_create_pks' type='checkbox'/></td>" +
						"<td><input id='cb_"  + tname + "_create_fks' type='checkbox'/></td>" +
						"<td><input id='cb_"  + tname + "_create_uniques' type='checkbox'/></td>" +
						"<td><input id='cb_"  + tname + "_create_indexes' type='checkbox'/></td>" +
						"<td><input id='txt_" + tname + "_transferfilter' type='text'/></td>" +
						"<td>" + tname + "</td>" +
						"</tr>";

					v_counter++;

				}

				v_html += "</table>";

				v_conversion_data.v_html = v_html;
				v_conversion_data.v_tables = v_tables_list;

				v_return.v_data = v_conversion_data;
			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}


			return v_return;
		}

		/// <summary>
		/// Creates conversion data in OmniDBs database.
		/// </summary>
		/// <param name="p_dst_index">Target connection index in connections list.</param>
		/// <param name="p_tables_data">Object containing info of each table.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn StartConversion(int p_src_index, int p_dst_index, System.Collections.Generic.List<ConversionTableData> p_tables_data)
		{
			AjaxReturn v_return = new AjaxReturn ();

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) {
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			int v_dst_index = p_dst_index;

			System.Data.DataTable v_max_conv_id = v_session.v_omnidb_database.v_connection.Query ("select max(conv_id)+1 as next_id from conversions", "Conversions");

			string v_next_id = "";

			if (v_max_conv_id.Rows [0] ["next_id"].ToString () != "")
				v_next_id = v_max_conv_id.Rows [0] ["next_id"].ToString ();
			else
				v_next_id = "0";

			v_session.v_omnidb_database.v_connection.Execute ("insert into conversions values ( " +
				v_next_id + "," +
				v_session.v_databases[p_src_index].v_conn_id + "," +
				v_session.v_databases[v_dst_index].v_conn_id + "," +
				"'','','0','R','',''," + v_session.v_user_id + ",'')");

			foreach (ConversionTableData v_table_data in p_tables_data) {

				string v_drop_records = "N";
				string v_create_table = "N";
				string v_create_pks = "N";
				string v_create_fks = "N";
				string v_create_uniques = "N";
				string v_create_indexes = "N";
				string v_transfer_data = "N";

				bool v_create_record = false;

				if (v_table_data.v_drop_records) {
					v_drop_records = "R";
					v_create_record = true;
				}
				if (v_table_data.v_create_table) {
					v_create_table = "R";
					v_create_record = true;
				}
				if (v_table_data.v_transfer_data) {
					v_transfer_data = "R";
					v_create_record = true;
				}

				if (v_session.v_databases [v_dst_index].v_can_add_constraint) {
					if (v_table_data.v_create_pks) {
						v_create_pks = "R";
						v_create_record = true;
					}
					if (v_table_data.v_create_fks) {
						v_create_fks = "R";
						v_create_record = true;
					}
					if (v_table_data.v_create_uniques) {
						v_create_uniques = "R";
						v_create_record = true;
					}
					if (v_table_data.v_create_indexes) {
						v_create_indexes = "R";
						v_create_record = true;
					}
				}

				if (v_create_record) 
					v_session.v_omnidb_database.v_connection.Execute ("insert into conv_tables_data values ( " +
						v_next_id + ",'" +
						v_table_data.v_table + "','" +
						v_drop_records + "','" +
						v_create_table + "','" +
						v_create_pks + "','" +
						v_create_fks + "','" +
						v_create_uniques + "','" +
						v_create_indexes + "','" +
						v_transfer_data + "'," +
						"0,0,0,0,'','','','','','','','','','','" +
						v_table_data.v_transferfilter.Replace("'","''") + "')");

			}

			return v_return;
		}

	}
}

