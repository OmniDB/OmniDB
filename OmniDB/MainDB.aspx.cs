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
	/// Query data.
	/// </summary>
	public class QueryReturn
	{
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> v_data;
		public System.Collections.Generic.List<string> v_col_names;

		public int v_error;
		public string v_error_desc;

		public string v_query_info;
	}

	/// <summary>
	/// Alter Table Data Return.
	/// </summary>
	public class AlterTableDataReturn
	{
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> v_data_columns;
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> v_data_constraints;
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> v_data_indexes;
		public System.Collections.Generic.List<string> v_update_rules;
		public System.Collections.Generic.List<string> v_delete_rules;
		public System.Collections.Generic.List<string> v_data_types;
		public System.Collections.Generic.List<string> v_tables;
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> table_ref_columns;
		public bool v_can_rename_table;
		public bool v_can_rename_column;
		public bool v_can_alter_type;
		public bool v_can_alter_nullable;
		public bool v_can_drop_column;
		public bool v_can_add_constraint;
		public bool v_can_drop_constraint;
		public bool v_has_update_rule;
	}

	/// <summary>
	/// Data sent from client with column changes.
	/// </summary>
	public class AlterTableColumnInfo
	{
		public bool canAlter;
		public int mode;
		public int old_mode;
		public int index;
		public string originalColName;
		public string originalDataType;
		public string originalNullable;
	}

	/// <summary>
	/// Data sent from client with constraint changes.
	/// </summary>
	public class AlterTableConstraintInfo
	{
		public bool canAlter;
		public int mode;
		public int old_mode;
		public int index;
	}

	/// <summary>
	/// Data sent from client with index changes.
	/// </summary>
	public class AlterTableIndexInfo
	{
		public int mode;
		public int old_mode;
		public int index;
	}

	public class Completion
	{
		public string value;
		public int score;
		public string meta;

		public Completion(string p_value, int p_score, string p_meta)
		{
			this.value = p_value;
			this.score = p_score;
			this.meta = p_meta;
		}

	}

	/// <summary>
	/// Connection info.
	/// </summary>
	public class ConnectionInfo
	{
		public string v_db_type;
		public string v_alias;
	}

	/// <summary>
	/// Database selection combobox.
	/// </summary>
	public class SelectDatabase
	{
		public int v_id;
		public string v_db_type;
		public System.Collections.Generic.List<ConnectionInfo> v_connections;
		public string v_select_html;
	}

	/// <summary>
	/// Bar chart data.
	/// </summary>
	public class BarChartData
	{
		public System.Collections.Generic.List<string> texts;
		public System.Collections.Generic.List<int> values;
		public int total;
	}

	/// <summary>
	/// Graph node.
	/// </summary>
	public class GraphNode
	{
		public string id;
		public string label;
		public int group;
	}

	/// <summary>
	/// Graph edge.
	/// </summary>
	public class GraphEdge
	{
		public string from;
		public string to;
		public string label;
		public string arrows;
	}

	/// <summary>
	/// Graph data.
	/// </summary>
	public class Graph
	{
		public System.Collections.Generic.List<GraphNode> v_nodes;
		public System.Collections.Generic.List<GraphEdge> v_edges;
		public string[] v_legends;
	}

	/// <summary>
	/// Primary Key.
	/// </summary>
	public class PrimaryKeyColumn
	{
		public string v_column;
		public string v_value;
	}

	/// <summary>
	/// Primary Key.
	/// </summary>
	public class PrimaryKeyInfo
	{
		public string v_column;
		public string v_class;
		public string v_compareformat;
		public int v_index;
	}


	/// <summary>
	/// Column Info.
	/// </summary>
	public class ColumnInfo
	{
		public string v_column;
		public string v_type;
		public string v_class;
		public string v_readformat;
		public string v_writeformat;
		public string v_compareformat;
		public bool v_is_pk;
	}

	/// <summary>
	/// Data sent from client with column changes.
	/// </summary>
	public class EditDataRowInfo
	{
		public int mode;
		public int old_mode;
		public int index;
		public System.Collections.Generic.List<PrimaryKeyColumn> pk;
		public System.Collections.Generic.List<int> changed_cols;
	}

	/// <summary>
	/// Edit data initial info.
	/// </summary>
	public class StartEditDataReturn
	{
		public System.Collections.Generic.List<PrimaryKeyInfo> v_pk;
		public System.Collections.Generic.List<ColumnInfo> v_cols;
		public string v_ini_orderby;
	}

	/// <summary>
	/// Edit data initial info.
	/// </summary>
	public class EditDataReturn
	{
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> v_data;
		public System.Collections.Generic.List<System.Collections.Generic.List<PrimaryKeyColumn>> v_row_pk;

		public string v_query_info;
	}

	public class CommandInfoReturn
	{
		public bool error;
		public string v_command;
		public string v_message;
		public int mode;
		public int index;
	}

	public class CommandColumnInfoReturn
	{
		public int mode;
		public int index;
		public CommandInfoReturn alter_datatype;
		public CommandInfoReturn alter_nullable;
		public CommandInfoReturn alter_colname;
	}

	public class SaveAlterTableReturn {
		public System.Collections.Generic.List<CommandInfoReturn> v_columns_simple_commands_return;
		public System.Collections.Generic.List<CommandColumnInfoReturn> v_columns_group_commands_return;
		public System.Collections.Generic.List<CommandInfoReturn> v_constraints_commands_return;
		public System.Collections.Generic.List<CommandInfoReturn> v_indexes_commands_return;
		public CommandInfoReturn v_create_table_command;
		public CommandInfoReturn v_rename_table_command;
	}

	/// <summary>
	/// Theme details.
	/// </summary>
	public class ThemeDetails
	{
		public string v_theme_name;
		public string v_theme_type;
	}

	/// <summary>
	/// Chat message.
	/// </summary>
	public class ChatMessage
	{
		public int v_message_id;
		public string v_user_name;
		public string v_text;
		public string v_timestamp;
	}

	/// <summary>
	/// Main page. Contains the treeview of database components and query area.
	/// </summary>
	public partial class MainDB : System.Web.UI.Page
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
			else if (v_session.v_user_name=="admin") {
				Session ["OMNIDB_ALERT_MESSAGE"] = "Admin can only manage users.";
				this.Response.Redirect("Users.aspx");

			}
			else if (v_session.v_databases.Count==0) {
				Session ["OMNIDB_ALERT_MESSAGE"] = "There are no database connections, please add at least one before using the application.";
				this.Response.Redirect("Connections.aspx");

			}

			Session["OMNIDB_SESSION"] = v_session;

		}

		public System.Collections.Generic.List<string> GetDatabases() {
			System.Collections.Generic.List<string> v_list = new System.Collections.Generic.List<string>();
			v_list.Add("opa");
			v_list.Add("ae");

			return v_list;

		}

		/// <summary>
		/// Changes user options.
		/// </summary>
		/// <param name="p_font_size">Font size.</param>
		/// <param name="p_theme">Theme name.</param>
		/// <param name="p_pwd">New password.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SaveConfigUser(string p_font_size, string p_theme, string p_pwd)
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

			v_session.v_theme_id = p_theme;
			v_session.v_editor_font_size = p_font_size;

			string v_enc_pwd = v_cryptor.Encrypt (p_pwd);

			string v_update_command = "";
			string v_query_theme_name = "select theme_name, theme_type from themes where theme_id = " + p_theme;

			if (p_pwd!="")
				v_update_command = "update users                            " +
					"set theme_id = " + p_theme + ",               " +
					"    editor_font_size = '" + p_font_size + "', " +
					"    password = '" + v_enc_pwd + "'            " +
					"where user_id = " + v_session.v_user_id;
			else
				v_update_command = "update users                           " +
					"set theme_id = " + p_theme + ",              " +
					"    editor_font_size = '" + p_font_size + "' " +
					"where user_id = " + v_session.v_user_id;

			try {

				v_session.v_omnidb_database.v_connection.Execute(v_update_command);
				System.Data.DataTable v_theme_details = v_session.v_omnidb_database.v_connection.Query(v_query_theme_name,"ThemeDetails");

				v_session.v_editor_theme = v_theme_details.Rows[0]["theme_name"].ToString();
				v_session.v_theme_type = v_theme_details.Rows[0]["theme_type"].ToString();

				ThemeDetails v_details = new ThemeDetails();
				v_details.v_theme_name = v_theme_details.Rows[0]["theme_name"].ToString();
				v_details.v_theme_type = v_theme_details.Rows[0]["theme_type"].ToString();

				v_return.v_data = v_details;

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
		/// Returns an object with the list of databases.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetDatabaseList()
		{
			AjaxReturn v_return = new AjaxReturn();
			SelectDatabase v_select_database = new SelectDatabase ();

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			}

			System.Collections.Generic.List<ConnectionInfo> v_connections = new System.Collections.Generic.List<ConnectionInfo>();

			string v_html = "";

			string v_atu_options = "";

			for (int i=0; i<v_session.v_databases.Count; i++) {

				ConnectionInfo v_conn = new ConnectionInfo();
				v_conn.v_db_type = v_session.v_databases[i].v_db_type;
				v_conn.v_alias = v_session.v_databases[i].v_alias;

				v_connections.Add(v_conn);

				string v_alias = "";

					if (v_session.v_databases [i].v_alias != "")
						v_alias = "(" + v_session.v_databases [i].v_alias + ") ";

					//if (i == v_session.v_database_index)	
					//	v_atu_options += "<option selected=\"selected\" data-image=\"images/" + v_session.v_databases [i].v_db_type + "_medium.png\" value=\"" + i + "\" data-description=\"" + v_session.v_databases [i].PrintDatabaseDetails() + "\">" + v_alias + v_session.v_databases [i].PrintDatabaseInfo() + "</option>";
					//else	
						v_atu_options += "<option data-image=\"images/" + v_session.v_databases [i].v_db_type + "_medium.png\" value=\"" + i + "\" data-description=\"" + v_session.v_databases [i].PrintDatabaseDetails() + "\">" + v_alias + v_session.v_databases [i].PrintDatabaseInfo() + "</option>";

				
			}

			v_html = "<select style=\"width: 100%; font-weight: bold;\" onchange=\"changeDatabase(this.value);\">" +
				v_atu_options +
				"</select>";

			v_select_database.v_select_html = v_html;
			v_select_database.v_connections = v_connections;
			v_select_database.v_id = v_session.v_database_index;


			v_return.v_data = v_select_database;

			return v_return;

		}

		/// <summary>
		/// Changes selected database.
		/// </summary>
		/// <param name="p_value">Database ID.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn ChangeDatabase(int p_value)
		{
			AjaxReturn v_return = new AjaxReturn();

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 
				
			v_session.v_database_index = p_value;

			System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"] = v_session;

			return v_return;
		}

		/// <summary>
		/// Builds a graph with tables and relationships.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn DrawGraphSimple(int p_database_index)
		{
			AjaxReturn v_return = new AjaxReturn();

			System.Collections.Generic.List<GraphNode> v_nodes = new System.Collections.Generic.List<GraphNode>();
			System.Collections.Generic.List<GraphEdge> v_edges = new System.Collections.Generic.List<GraphEdge>();

			GraphNode v_node;
			GraphEdge v_edge;

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			try {

				System.Data.DataTable v_data = v_database.QueryTables(false);

				for (int j = 0; j < v_data.Rows.Count; j++)
				{
					v_node = new GraphNode();

					v_node.id = v_data.Rows [j] ["table_name"].ToString ();
					v_node.label = v_data.Rows [j] ["table_name"].ToString (); 

					v_nodes.Add(v_node);
				}

				v_data = v_database.QueryTablesForeignKeys(null);

				string v_curr_constraint = "";
				string v_curr_from = "";
				string v_curr_to = "";

				for (int j = 0; j < v_data.Rows.Count; j++) {
					if (v_curr_constraint!="" && v_curr_constraint!=v_data.Rows [j] ["constraint_name"].ToString () && (!v_database.v_has_schema || (v_database.v_schema==v_data.Rows [j] ["r_table_schema"].ToString () && v_database.v_has_schema))) {

						v_edge = new GraphEdge ();
						v_edge.from = v_curr_from;
						v_edge.to = v_curr_to;
						v_edge.label = "";
						v_edge.arrows = "to";

						v_edges.Add (v_edge);
						v_curr_constraint = "";
					}

					v_curr_from = v_data.Rows [j] ["table_name"].ToString ();
					v_curr_to = v_data.Rows [j] ["r_table_name"].ToString ();
					v_curr_constraint = v_data.Rows [j] ["constraint_name"].ToString ();

				}

				if (v_curr_constraint!="") {

					v_edge = new GraphEdge ();
					v_edge.from = v_curr_from;
					v_edge.to = v_curr_to;
					v_edge.label = "";
					v_edge.arrows = "to";

					v_edges.Add (v_edge);

				}



			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			Graph v_graph1 = new Graph();
			v_graph1.v_edges = v_edges;
			v_graph1.v_nodes = v_nodes;

			v_return.v_data = v_graph1;

			return v_return;

		}

		/// <summary>
		/// Builds a graph with tables and relationships.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn DrawGraphComplete(int p_database_index)
		{
			AjaxReturn v_return = new AjaxReturn();

			System.Collections.Generic.List<GraphNode> v_nodes = new System.Collections.Generic.List<GraphNode>();
			System.Collections.Generic.List<GraphEdge> v_edges = new System.Collections.Generic.List<GraphEdge>();

			GraphNode v_node;
			GraphEdge v_edge;

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			try {

				System.Data.DataTable v_data = v_database.QueryTables(false);

				for (int j = 0; j < v_data.Rows.Count; j++)
				{
					System.Data.DataTable v_columns = v_database.QueryTablesFields(v_data.Rows [j] ["table_name"].ToString ());

					v_node = new GraphNode();

					v_node.id = v_data.Rows [j] ["table_name"].ToString ();
					v_node.label = v_data.Rows [j] ["table_name"].ToString () + "\n"; 

					foreach (System.Data.DataRow v_column in v_columns.Rows)
						v_node.label += "\n" + v_column["column_name"].ToString() + ": " + v_column["data_type"].ToString();

					v_nodes.Add(v_node);
				}


				v_data = v_database.QueryTablesForeignKeys(null);

				string v_curr_constraint = "";
				string v_curr_label = "";
				string v_curr_from = "";
				string v_curr_to = "";
				bool v_first = true;

				for (int j = 0; j < v_data.Rows.Count; j++) {
					if (v_curr_constraint!="" && v_curr_constraint!=v_data.Rows [j] ["constraint_name"].ToString ()) {

						v_edge = new GraphEdge ();
						v_edge.from = v_curr_from;
						v_edge.to = v_curr_to;
						v_edge.label = v_curr_label;
						v_edge.arrows = "to";

						v_edges.Add (v_edge);

						v_first = true;
						v_curr_label = "";

					}

					if (!v_first)
						v_curr_label += "\n";

					v_first = false;

					v_curr_label += v_data.Rows [j] ["column_name"].ToString () + " - " + v_data.Rows [j] ["r_column_name"].ToString ();
					v_curr_from = v_data.Rows [j] ["table_name"].ToString ();
					v_curr_to = v_data.Rows [j] ["r_table_name"].ToString ();
					v_curr_constraint = v_data.Rows [j] ["constraint_name"].ToString ();

				}

				if (v_curr_label!="") {

					v_edge = new GraphEdge ();
					v_edge.from = v_curr_from;
					v_edge.to = v_curr_to;
					v_edge.label = v_curr_label;
					v_edge.arrows = "to";

					v_edges.Add (v_edge);

					v_first = true;
					v_curr_label = "";

				}



			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			Graph v_graph1 = new Graph();
			v_graph1.v_edges = v_edges;
			v_graph1.v_nodes = v_nodes;

			v_return.v_data = v_graph1;

			return v_return;

		}

		/// <summary>
		/// Builds a graph with tables, number of records, relationships and a color scale.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn DrawGraph(int p_database_index)
		{
			AjaxReturn v_return = new AjaxReturn();

			System.Collections.Generic.List<GraphNode> v_nodes = new System.Collections.Generic.List<GraphNode>();
			System.Collections.Generic.List<GraphEdge> v_edges = new System.Collections.Generic.List<GraphEdge>();
			string [] v_legends = new string[6];

			GraphNode v_node;
			GraphEdge v_edge;

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			try {
				
				System.Data.DataTable v_count_total_table = v_database.CountTablesRecords();

				// Calculating Groups

				int v_max_count = Convert.ToInt32(v_count_total_table.Rows[0]["total"]);

				int v_inc_group =  Convert.ToInt32(v_max_count/6);

				int[] v_groups = new int[7];



				v_groups[0] = 0;
				v_groups[6] = v_max_count;

				for (int i=1; i<6; i++)
					v_groups[i] = v_inc_group*i;

				for (int i=0; i<6; i++)
					v_legends[i] = v_groups[i] + " - " + v_groups[i+1] + " records"; 

				for (int j = 0; j < v_count_total_table.Rows.Count; j++)
				{
					v_node = new GraphNode();

					v_node.id = v_count_total_table.Rows [j] ["table_name"].ToString ();
					v_node.label = v_count_total_table.Rows [j] ["table_name"].ToString () + "\nRows: " + v_count_total_table.Rows [j] ["total"].ToString ();


					int v_curr_count = Convert.ToInt32(v_count_total_table.Rows [j] ["total"]);

					for (int i=1; i<7; i++) {
						if (v_curr_count <= v_groups[i]) {
							v_node.group = i;
							break;
						}

					}

					v_nodes.Add(v_node);

				}

				System.Data.DataTable v_foreign_keys = v_database.QueryTablesForeignKeys(null);

				v_foreign_keys = v_database.QueryTablesForeignKeys(null);

				string v_curr_constraint = "";
				string v_curr_from = "";
				string v_curr_to = "";

				for (int j = 0; j < v_foreign_keys.Rows.Count; j++) {
					if (v_curr_constraint!="" && v_curr_constraint!=v_foreign_keys.Rows [j] ["constraint_name"].ToString ()) {

						v_edge = new GraphEdge ();
						v_edge.from = v_curr_from;
						v_edge.to = v_curr_to;
						v_edge.label = "";
						v_edge.arrows = "to";

						v_edges.Add (v_edge);
						v_curr_constraint = "";
					}

					v_curr_from = v_foreign_keys.Rows [j] ["table_name"].ToString ();
					v_curr_to = v_foreign_keys.Rows [j] ["r_table_name"].ToString ();
					v_curr_constraint = v_foreign_keys.Rows [j] ["constraint_name"].ToString ();

				}

				if (v_curr_constraint!="") {

					v_edge = new GraphEdge ();
					v_edge.from = v_curr_from;
					v_edge.to = v_curr_to;
					v_edge.label = "";
					v_edge.arrows = "to";

					v_edges.Add (v_edge);

				}

			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			Graph v_graph1 = new Graph();
			v_graph1.v_edges = v_edges;
			v_graph1.v_nodes = v_nodes;
			v_graph1.v_legends = v_legends;

			v_return.v_data = v_graph1;

			return v_return;

		}

		/// <summary>
		/// Builds a bar chart with information about tables and number of records.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetStatistics(int p_database_index)
		{
			AjaxReturn v_return = new AjaxReturn();

			BarChartData v_b1 = new BarChartData ();

			v_b1.texts = new System.Collections.Generic.List<string>();
			v_b1.values = new System.Collections.Generic.List<int>();

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			try {
				
				System.Data.DataTable v_tablelist_counts = v_database.CountTablesRecords();


				int v_tot = 0;
				for (int j = 0; j < v_tablelist_counts.Rows.Count; j++)
				{
					v_tot += Convert.ToInt32(v_tablelist_counts.Rows [j] ["total"].ToString ());

				}

				v_b1.total = v_tot;


				for (int j = 0; j < v_tablelist_counts.Rows.Count; j++)
				{
					if (j>=50)
						break;

					v_b1.values.Add(Convert.ToInt32(v_tablelist_counts.Rows [j] ["total"].ToString ()));
					v_b1.texts.Add(v_tablelist_counts.Rows [j] ["table_name"].ToString ());

				}


			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			v_return.v_data = v_b1;

			return v_return;

		}

		/// <summary>
		/// Clears command history.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn ClearCommandList()
		{

			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			try
			{
				v_session.v_omnidb_database.v_connection.Execute ("delete from command_list where user_id=" + v_session.v_user_id);
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
		/// Queries on selected database.
		/// </summary>
		/// <param name="p_sql">SQL string.</param>
		/// <param name="p_select_value">Command type.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn QuerySQL(int p_database_index, string p_sql, int p_select_value)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			System.Data.DataTable v_data1;

			QueryReturn v_g1 = new QueryReturn();

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_table = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			System.Collections.Generic.List<string> v_col_names = new System.Collections.Generic.List<string>();


			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			if (p_select_value == -2) {
                
				try {
                    v_session.Execute(p_database_index, p_sql, true, true);
				} catch (Spartacus.Database.Exception e) {

					v_return.v_error = true;
					v_return.v_data = e.v_message.Replace ("<", "&lt;").Replace (">", "&gt;").Replace (System.Environment.NewLine, "<br/>");

					return v_return;

				} catch (System.InvalidOperationException e) {
					v_return.v_error = true;
					v_return.v_data = e.Message.Replace ("<", "&lt;").Replace (">", "&gt;").Replace (System.Environment.NewLine, "<br/>");

					return v_return;
				}
			} else if (p_select_value == -3) {
			
				string[] v_commands = p_sql.Split (';');

				string v_return_html = "";

				int v_num_success_commands = 0;
				int v_num_error_commands = 0;

				v_database.v_connection.Open ();

				foreach (string v_command in v_commands) {

					if (v_command.Trim () != "") {
					
						try {
                            v_session.Execute(p_database_index, v_command, true, true);
							v_num_success_commands++;

						} catch (Spartacus.Database.Exception e) {
							v_num_error_commands++;
							v_return_html += "<b>Command:</b> " + v_command + "<br/><br/><b>Message:</b> " + e.v_message.Replace ("<", "&lt;").Replace (">", "&gt;").Replace (System.Environment.NewLine, "<br/>") + "<br/><br/>";
						}

					}
				}


				v_return.v_data = "<b>Successful commands:</b> " + v_num_success_commands + "<br/>";
				v_return.v_data += "<b>Errors: </b> " + v_num_error_commands + "<br/><br/>";

				if (v_num_error_commands > 0) {
					v_return.v_data += "<b>Errors details:</b><br/><br/>" + v_return_html;
				}

				v_database.v_connection.Close ();

				return v_return;

			} else {
				try {
					if (p_select_value == -1)
                        v_data1 = v_session.Query(p_database_index, p_sql, true, true);
					else
                        v_data1 = v_session.QueryDataLimited(p_database_index, p_sql, p_select_value, true, false);

					for (int j = 0; j < v_data1.Columns.Count; j++) {
						v_col_names.Add (v_data1.Columns [j].ColumnName);
					}

					System.Collections.Generic.List<string> v_row_data;

					v_g1.v_query_info = "Number of records: " + v_data1.Rows.Count.ToString ();

					for (int i = 0; i < v_data1.Rows.Count; i++) {
						v_row_data = new System.Collections.Generic.List<string> ();

						for (int j = 0; j < v_data1.Columns.Count; j++) {

							v_row_data.Add (v_data1.Rows [i] [j].ToString ());

						}

						v_table.Add (v_row_data);

					}

					v_g1.v_data = v_table;
					v_g1.v_col_names = v_col_names;

					v_return.v_data = v_g1;

				} catch (Spartacus.Database.Exception e) {

					v_return.v_error = true;
					v_return.v_data = e.v_message.Replace ("<", "&lt;").Replace (">", "&gt;").Replace (System.Environment.NewLine, "<br/>");

					return v_return;
				} catch (System.InvalidOperationException e) {
					v_return.v_error = true;
					v_return.v_data = e.Message.Replace ("<", "&lt;").Replace (">", "&gt;").Replace (System.Environment.NewLine, "<br/>");

					return v_return;
				} catch (System.Data.DuplicateNameException e) {
					v_return.v_error = true;
					v_return.v_data = e.Message.Replace ("<", "&lt;").Replace (">", "&gt;").Replace (System.Environment.NewLine, "<br/>");

					return v_return;
				}

			}

			return v_return;

		}

		/// <summary>
		/// Exports data from query.
		/// </summary>
		/// <param name="p_sql">SQL string.</param>
		/// <param name="p_select_value">Command type.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn ExportData(int p_database_index, string p_sql, string p_select_value, string p_tab_name)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			Spartacus.Utils.Cryptor v_cryptor = new Spartacus.Utils.Cryptor ("OmniDB");

			string v_filename = v_cryptor.RandomString () +  "." + p_select_value;

			System.Web.HttpContext.Current.Session ["OMNIDB_EXPORTED_FILE"] = v_filename;
			System.Web.HttpContext.Current.Session ["OMNIDB_EXPORTED_TYPE"] = p_select_value;
			System.Web.HttpContext.Current.Session ["OMNIDB_EXPORTED_NAME"] = p_tab_name;

			try
			{
				
				if (p_select_value == "csv")
					v_database.v_connection.TransferToCSV(p_sql,
						System.Web.Configuration.WebConfigurationManager.AppSettings["OmniDB.ExportedFilesFolder"] + "/" + v_filename,
						System.Web.Configuration.WebConfigurationManager.AppSettings["OmniDB.ExportedCSVSeparator"].ToString(),
						System.Web.Configuration.WebConfigurationManager.AppSettings["OmniDB.ExportedCSVDelimiter"],
						true,
						System.Text.Encoding.UTF8);
				else
					v_database.v_connection.TransferToFile(p_sql, System.Web.Configuration.WebConfigurationManager.AppSettings["OmniDB.ExportedFilesFolder"] + "/" + v_filename);
			
			} 
			catch (Spartacus.Database.Exception e) {

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace ("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			} catch (System.InvalidOperationException e) {
				v_return.v_error = true;
				v_return.v_data = e.Message.Replace ("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			} catch (System.Data.DuplicateNameException e) {
				v_return.v_error = true;
				v_return.v_data = e.Message.Replace ("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			return v_return;

		}

		/// <summary>
		/// Retrieves command history.
		/// </summary>
		/// <returns>The connections.</returns>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetCommandList()
		{

			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			System.Data.DataTable v_commands = v_session.v_omnidb_database.v_connection.Query ("select * from command_list where user_id = " + v_session.v_user_id + " order by cl_in_codigo desc", "Command List");

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_command_list = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();


			int v_index = 0;

			foreach (System.Data.DataRow v_command in v_commands.Rows) 
			{

				System.Collections.Generic.List<string> v_command_data = new System.Collections.Generic.List<string>();

				v_command_data.Add(v_command["cl_st_data"].ToString());
				v_command_data.Add(v_command["cl_st_command"].ToString());

				v_index++;

				v_command_list.Add(v_command_data);		


			}

			v_return.v_data = v_command_list;
			return v_return;

		}

		/// <summary>
		/// Drops a table
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn DropTable(int p_database_index, string p_table)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			string v_table_name = "";

			if (v_database.v_has_schema)
				v_table_name = v_database.v_schema + "." + p_table;
			else
				v_table_name = p_table;

			try
			{
                v_session.Execute(p_database_index, "drop table " + v_table_name, false, true);
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
        /// Drops a function
        /// </summary>
        [System.Web.Services.WebMethod]
        public static AjaxReturn DropFunction(int p_database_index, string p_function)
        {
            Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

            AjaxReturn v_return = new AjaxReturn ();

            if (v_session == null) 
            {
                v_return.v_error = true;
                v_return.v_error_id = 1;
                return v_return;
            } 

            OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

            try
            {
                v_session.Execute(p_database_index, "drop function " + p_function, false, true);
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
        /// Drops a procedure
        /// </summary>
        [System.Web.Services.WebMethod]
        public static AjaxReturn DropProcedure(int p_database_index, string p_procedure)
        {
            Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

            AjaxReturn v_return = new AjaxReturn ();

            if (v_session == null) 
            {
                v_return.v_error = true;
                v_return.v_error_id = 1;
                return v_return;
            } 

            OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

            try
            {
                v_session.Execute(p_database_index, "drop procedure " + p_procedure, false, true);
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
		/// Wipes table records.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn DeleteData(int p_database_index, string p_table)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			string v_table_name = "";

			if (v_database.v_has_schema)
				v_table_name = v_database.v_schema + "." + p_table;
			else
				v_table_name = p_table;

			try
			{
                v_session.Execute(p_database_index, "delete from " + v_table_name, false, false);
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
		/// Retrieves edit data initial information.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn StartEditData(int p_database_index, string p_table)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			StartEditDataReturn v_data = new StartEditDataReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			}

			string v_ini_orderby = "";

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			System.Collections.Generic.List<PrimaryKeyInfo> v_pk_list = new System.Collections.Generic.List<PrimaryKeyInfo>();

			System.Collections.Generic.List<ColumnInfo> v_col_list = new System.Collections.Generic.List<ColumnInfo>();

			try
			{
				System.Data.DataTable v_pk = v_database.QueryTablesPrimaryKeys ("", p_table);

				string v_table_name = "";

				if (v_database.v_has_schema)
					v_table_name = v_database.v_schema + "." + p_table;
				else
					v_table_name = p_table;

				System.Data.DataTable v_columns = v_database.QueryTablesFields(p_table);

				System.Data.DataTable v_data1 = v_database.QueryDataLimited("select * from " + v_table_name,0);

				string v_query_column_classes = "";

				bool v_first = true;

				foreach (System.Data.DataRow v_column in v_columns.Rows) {
					

					if (!v_first)
						v_query_column_classes += "union ";

					v_first = false;

					v_query_column_classes += "select '" + v_column["column_name"].ToString() + "' as column, dc.cat_st_class as cat_st_class, dt.dt_type as dt_type, dt.dt_st_readformat as dt_st_readformat, dt.dt_st_compareformat as dt_st_compareformat, dt.dt_st_writeformat as dt_st_writeformat " +
						"from data_types dt, data_categories dc " +
					"where dt.dbt_st_name='" + v_database.v_db_type + "' and dt.dt_type='" + v_column["data_type"].ToString().ToLower() +
						"' and dt.cat_st_name=dc.cat_st_name " +
						" union " +
						"select '" + v_column["column_name"].ToString() + "' as column, 'text' as cat_st_class, '" + v_column["data_type"].ToString().ToLower() + "' as dt_type, '#' as dt_st_readformat, '#' as dt_st_compareformat, '''#''' as dt_st_writeformat where '" + v_column["data_type"].ToString().ToLower() + "' not in (select dt_type from data_types where dbt_st_name='" + v_database.v_db_type + "') ";
				
				}

				System.Data.DataTable v_column_classes = v_session.v_omnidb_database.v_connection.Query(v_query_column_classes,"ColumnClasses");

				foreach (System.Data.DataColumn v_column in v_data1.Columns) {

					ColumnInfo v_col = new ColumnInfo();

					foreach (System.Data.DataRow v_column_class in v_column_classes.Rows) {

						if (v_column.ColumnName.ToLower()==v_column_class["column"].ToString().ToLower()) {
							v_col.v_class = v_column_class["cat_st_class"].ToString();
							v_col.v_type = v_column_class["dt_type"].ToString();
							v_col.v_column = v_column_class["column"].ToString();
							v_col.v_readformat = v_column_class["dt_st_readformat"].ToString();
							v_col.v_writeformat = v_column_class["dt_st_writeformat"].ToString();
							v_col.v_compareformat = v_column_class["dt_st_compareformat"].ToString();
							v_col.v_is_pk = false;
							break;
						}

					}


					v_col_list.Add(v_col);

				}
			
				if (v_pk.Rows.Count > 0)
					v_ini_orderby = "order by ";

				v_first = true;

				int v_index = 0;
				foreach (ColumnInfo v_column in v_col_list) {

					foreach (System.Data.DataRow v_pk_col in v_pk.Rows) {
						if (v_pk_col ["column_name"].ToString ().ToLower() == v_column.v_column.ToLower()) {

							v_column.v_is_pk = true;

							if (!v_first)
								v_ini_orderby += ", ";

							v_first = false;

							v_ini_orderby += "t." + v_pk_col ["column_name"].ToString ();

							PrimaryKeyInfo v_pk_info = new PrimaryKeyInfo();

							v_pk_info.v_column = v_pk_col ["column_name"].ToString ();
							v_pk_info.v_index = v_index;
							v_pk_info.v_class = v_column.v_class;
							v_pk_info.v_compareformat = v_column.v_compareformat;

							v_pk_list.Add (v_pk_info);
							break;
						}

					}

					v_index++;

				}


			}
			catch (Spartacus.Database.Exception e)
			{
				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}
			catch (System.InvalidOperationException e) 
			{
				v_return.v_error = true;
				v_return.v_data = e.Message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			v_data.v_cols = v_col_list;
			v_data.v_pk = v_pk_list;
			v_data.v_ini_orderby = v_ini_orderby;

			v_return.v_data = v_data;

			return v_return;
		}

		/// <summary>
		/// Queries records for the edit data window.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		/// <param name="p_filter">Filter.</param>
		/// <param name="p_count">Number of records.</param>
		/// <param name="p_pk_list">List of primary keys.</param>
		/// <param name="p_columns">List of columns.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn QueryEditData(int p_database_index, string p_table, string p_filter, int p_count, System.Collections.Generic.List<PrimaryKeyInfo> p_pk_list, System.Collections.Generic.List<ColumnInfo> p_columns)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			EditDataReturn v_data = new EditDataReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			}

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_table = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			System.Collections.Generic.List<System.Collections.Generic.List<PrimaryKeyColumn>> v_row_pk_list = new System.Collections.Generic.List<System.Collections.Generic.List<PrimaryKeyColumn>>();

			try
			{
				string v_table_name = "";

				if (v_database.v_has_schema)
					v_table_name = v_database.v_schema + "." + p_table;
				else
					v_table_name = p_table;

				string v_column_list = "";
				bool v_first = true;
				foreach (ColumnInfo v_column in p_columns) {
					if (!v_first)
						v_column_list += ",";

					v_first = false;

					v_column_list += v_column.v_readformat.Replace("#",v_column.v_column);

				}

				System.Data.DataTable v_data1 = v_database.QueryTableRecords(v_column_list,v_table_name,p_filter,p_count);

				v_data.v_query_info = "Number of records: " + v_data1.Rows.Count.ToString();

				System.Collections.Generic.List<string> v_row_data;
				System.Collections.Generic.List<PrimaryKeyColumn> v_row_pk;

				for (int i = 0; i < v_data1.Rows.Count; i++)
				{
					v_row_data = new System.Collections.Generic.List<string>();

					v_row_pk = new System.Collections.Generic.List<PrimaryKeyColumn>();

					for (int j = 0; j < p_pk_list.Count; j++) {

						PrimaryKeyColumn v_pk_col = new PrimaryKeyColumn();
						v_pk_col.v_column = p_pk_list[j].v_column;
						v_pk_col.v_value = v_data1.Rows[i][p_pk_list[j].v_column].ToString();

						v_row_pk.Add(v_pk_col);
					}

					v_row_pk_list.Add(v_row_pk);

					v_row_data.Add("");

					for (int j = 0; j < v_data1.Columns.Count; j++)
					{

						v_row_data.Add(v_data1.Rows[i][j].ToString());

					}

					v_table.Add(v_row_data);

				}

			}
			catch (Spartacus.Database.Exception e)
			{
				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}
			catch (System.InvalidOperationException e) 
			{
				v_return.v_error = true;
				v_return.v_data = e.Message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			v_data.v_data = v_table;
			v_data.v_row_pk = v_row_pk_list;

			v_return.v_data = v_data;

			return v_return;
		}



		/// <summary>
		/// Retrieves alter table table data.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn AlterTableData(int p_database_index, string p_table)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			AlterTableDataReturn v_alter_data = new AlterTableDataReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_table_columns = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_table_constraints = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_table_indexes = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_table_ref_columns = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			System.Collections.Generic.List<string> v_data_types = new System.Collections.Generic.List<string> ();

			System.Collections.Generic.List<string> v_tables = new System.Collections.Generic.List<string> ();

			try
			{
				System.Data.DataTable v_data_types_table = v_session.v_omnidb_database.v_connection.Query("select dt_type, dt_in_sufix " +
					" from data_types " +
					" where dbt_st_name = '" + v_database.v_db_type + "' ","data_types");

				foreach (System.Data.DataRow v_data_type in v_data_types_table.Rows) {
					if (v_data_type["dt_in_sufix"].ToString()=="0")
						v_data_types.Add(v_data_type["dt_type"].ToString());
					else if (v_data_type["dt_in_sufix"].ToString()=="1")
						v_data_types.Add(v_data_type["dt_type"].ToString() + "(#)");
					else if (v_data_type["dt_in_sufix"].ToString()=="2")
						v_data_types.Add(v_data_type["dt_type"].ToString() + "(#,#)");
				}

				System.Data.DataTable v_tables_table = v_database.QueryTables(true);

				if (v_database.v_has_schema)
					foreach (System.Data.DataRow v_table in v_tables_table.Rows) {
						v_tables.Add(v_table["table_schema"].ToString() + "." + v_table["table_name"].ToString());
					}
				else
					foreach (System.Data.DataRow v_table in v_tables_table.Rows) {
						v_tables.Add(v_table["table_name"].ToString());
					}


				if (p_table!=null) {
					
					//Table Columns

					System.Data.DataTable v_columns_table = v_database.QueryTablesFields(p_table);

					System.Collections.Generic.List<string> v_row_data;

					int v_index = 0;

					foreach (System.Data.DataRow v_column in v_columns_table.Rows) {

						string v_data_sufix = v_session.v_omnidb_database.v_connection.ExecuteScalar("select dt_in_sufix " +
							" from data_types " +
							" where dbt_st_name = '" + v_database.v_db_type + "' " +
							"   and dt_type = '" + v_column["data_type"].ToString().ToLower() + "'");
						
						v_row_data = new System.Collections.Generic.List<string>();

						v_row_data.Add(v_column["column_name"].ToString());

						if (v_data_sufix=="2") {
							if (v_column["data_precision"].ToString()!="" && v_column["data_scale"].ToString()!="")
								v_row_data.Add(v_column["data_type"].ToString()+"("+v_column["data_precision"].ToString()+","+v_column["data_scale"].ToString()+")");
							else if (v_column["data_scale"].ToString()!="")
								v_row_data.Add(v_column["data_type"].ToString()+"("+v_column["data_scale"].ToString()+")");
							else
								v_row_data.Add(v_column["data_type"].ToString());
						}
						else if (v_data_sufix=="1") {
							if (v_column["data_length"].ToString()!="")
								v_row_data.Add(v_column["data_type"].ToString()+"("+v_column["data_length"].ToString()+")");
							else
								v_row_data.Add(v_column["data_type"].ToString());
						}
						else
							v_row_data.Add(v_column["data_type"].ToString());
					
			
						v_row_data.Add(v_column["nullable"].ToString());

						v_row_data.Add("");

						v_index++;
						
						v_table_columns.Add(v_row_data);

					}

					//Table Primary Keys
					System.Data.DataTable v_pk_table = v_database.QueryTablesPrimaryKeys("", p_table);

					if (v_pk_table.Rows.Count>0) {

						v_table_ref_columns.Add(new System.Collections.Generic.List<string>());

						string v_column_list = "";
						bool v_first = true;

						foreach (System.Data.DataRow v_column in v_pk_table.Rows) {


							if (!v_first)
								v_column_list += ", ";

							v_column_list += v_column["column_name"].ToString();
							v_first = false;

						}

						v_row_data = new System.Collections.Generic.List<string>();

						v_row_data.Add(v_pk_table.Rows[0]["constraint_name"].ToString());
						v_row_data.Add("Primary Key");
						v_row_data.Add("<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list);
						v_row_data.Add("");
						v_row_data.Add("");
						v_row_data.Add("");
						v_row_data.Add("");

						if (v_database.v_can_drop_constraint)
							v_row_data.Add("<img src='images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>");
						else
							v_row_data.Add("");

						v_table_constraints.Add(v_row_data);

					}


					//Table Foreign Keys
					System.Data.DataTable v_fks_table = v_database.QueryTablesForeignKeys(p_table);

					if (v_fks_table.Rows.Count>0) {
						
						string v_column_list = "";
						string v_referenced_column_list = "";
						string v_constraint_name = v_fks_table.Rows[0]["constraint_name"].ToString();
						string v_update_rule = v_fks_table.Rows[0]["update_rule"].ToString();
						string v_delete_rule = v_fks_table.Rows[0]["delete_rule"].ToString();
						string v_r_table_name = "";

						if (v_database.v_has_schema)
							v_r_table_name = v_fks_table.Rows[0]["r_table_schema"].ToString() + "." + v_fks_table.Rows[0]["r_table_name"].ToString();
						else
							v_r_table_name = v_fks_table.Rows[0]["r_table_name"].ToString();

						bool v_first = true;

						foreach (System.Data.DataRow v_column in v_fks_table.Rows) {

							if (v_column["constraint_name"].ToString()!=v_constraint_name) {
								v_row_data = new System.Collections.Generic.List<string>();

								v_row_data.Add(v_constraint_name);
								v_row_data.Add("Foreign Key");
								v_row_data.Add("<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list);
								v_row_data.Add(v_r_table_name);
								v_row_data.Add(v_referenced_column_list);
								v_row_data.Add(v_delete_rule);
								v_row_data.Add(v_update_rule);

								if (v_database.v_can_drop_constraint)
									v_row_data.Add("<img src='images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>");
								else
									v_row_data.Add("");

								v_table_constraints.Add(v_row_data);

								v_constraint_name = v_column["constraint_name"].ToString();
								v_update_rule = v_column["update_rule"].ToString();
								v_delete_rule = v_column["delete_rule"].ToString();

								v_column_list = "";
								v_referenced_column_list = "";
								v_first = true;
							}

							if (v_database.v_has_schema)
								v_r_table_name = v_column["r_table_schema"].ToString() + "." + v_column["r_table_name"].ToString();
							else
								v_r_table_name = v_column["r_table_name"].ToString();


							if (!v_first) {
								v_column_list += ", ";
								v_referenced_column_list += ", ";
							}

							v_column_list += v_column["column_name"].ToString();
							v_referenced_column_list += v_column["r_column_name"].ToString();
							v_first = false;

						}

						if (v_column_list!="") {
							v_row_data = new System.Collections.Generic.List<string>();

							v_row_data.Add(v_constraint_name);
							v_row_data.Add("Foreign Key");
							v_row_data.Add("<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list);
							v_row_data.Add(v_r_table_name);
							v_row_data.Add(v_referenced_column_list);
							v_row_data.Add(v_delete_rule);
							v_row_data.Add(v_update_rule);

							if (v_database.v_can_drop_constraint)
								v_row_data.Add("<img src='images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>");
							else
								v_row_data.Add("");
							
							v_table_constraints.Add(v_row_data);
						}

					}

					//Table Uniques
					System.Data.DataTable v_uniques_table = v_database.QueryTablesUniques("",p_table);

					if (v_uniques_table.Rows.Count>0) {

						string v_column_list = "";
						string v_constraint_name = v_uniques_table.Rows[0]["constraint_name"].ToString();
						bool v_first = true;

						foreach (System.Data.DataRow v_column in v_uniques_table.Rows) {

							if (v_column["constraint_name"].ToString()!=v_constraint_name) {
								v_row_data = new System.Collections.Generic.List<string>();

								v_row_data.Add(v_constraint_name);
								v_row_data.Add("Unique");
								v_row_data.Add("<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list);
								v_row_data.Add("");
								v_row_data.Add("");
								v_row_data.Add("");
								v_row_data.Add("");

								if (v_database.v_can_drop_constraint)
									v_row_data.Add("<img src='images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>");
								else
									v_row_data.Add("");

								v_table_constraints.Add(v_row_data);



								v_constraint_name = v_column["constraint_name"].ToString();
								v_column_list = "";
								v_first = true;
							}


							if (!v_first) {
								v_column_list += ", ";
							}

							v_column_list += v_column["column_name"].ToString();
							v_first = false;

						}

						if (v_column_list!="") {
							v_row_data = new System.Collections.Generic.List<string>();

							v_row_data.Add(v_constraint_name);
							v_row_data.Add("Unique");
							v_row_data.Add("<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_list);
							v_row_data.Add("");
							v_row_data.Add("");
							v_row_data.Add("");
							v_row_data.Add("");

							if (v_database.v_can_drop_constraint)
								v_row_data.Add("<img src='images/tab_close.png' class='img_ht' onclick='dropConstraintAlterTable()'/>");
							else
								v_row_data.Add("");
							
							v_table_constraints.Add(v_row_data);
						}

					}

					//Table Indexes
					System.Data.DataTable v_indexes_table = v_database.QueryTablesIndexes(p_table);

					if (v_indexes_table.Rows.Count>0) {

						string v_column_list = "";
						string v_index_name = v_indexes_table.Rows[0]["index_name"].ToString();
						string v_uniqueness = v_indexes_table.Rows[0]["uniqueness"].ToString();
						bool v_first = true;

						foreach (System.Data.DataRow v_column in v_indexes_table.Rows) {

							if (v_column["index_name"].ToString()!=v_index_name) {
								v_row_data = new System.Collections.Generic.List<string>();

								v_row_data.Add(v_index_name);
								v_row_data.Add(v_uniqueness);
								v_row_data.Add("<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionIndexes()'/> " + v_column_list);
								v_row_data.Add("<img src='images/tab_close.png' class='img_ht' onclick='dropIndexAlterTable()'/>");
			

								v_table_indexes.Add(v_row_data);



								v_index_name = v_column["index_name"].ToString();
								v_uniqueness = v_column["uniqueness"].ToString();
								v_column_list = "";
								v_first = true;
							}


							if (!v_first) {
								v_column_list += ", ";
							}

							v_column_list += v_column["column_name"].ToString();
							v_first = false;

						}

						if (v_column_list!="") {
							v_row_data = new System.Collections.Generic.List<string>();

							v_row_data.Add(v_index_name);
							v_row_data.Add(v_uniqueness);
							v_row_data.Add("<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionIndexes()'/> " + v_column_list);
							v_row_data.Add("<img src='images/tab_close.png' class='img_ht' onclick='dropIndexAlterTable()'/>");
						
							v_table_indexes.Add(v_row_data);
						}

					}

				}


			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}
			catch (System.InvalidOperationException e) 
			{
				v_return.v_error = true;
				v_return.v_data = e.Message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			v_alter_data.v_can_rename_table = v_database.v_can_rename_table;
			v_alter_data.v_data_columns = v_table_columns;
			v_alter_data.v_data_constraints = v_table_constraints;
			v_alter_data.v_data_indexes = v_table_indexes;
			v_alter_data.v_data_types = v_data_types;
			v_alter_data.v_tables = v_tables;
			v_alter_data.table_ref_columns = v_table_ref_columns;
			v_alter_data.v_can_rename_column = v_database.v_can_rename_column;
			v_alter_data.v_can_alter_type = v_database.v_can_alter_type;
			v_alter_data.v_can_alter_nullable = v_database.v_can_alter_nullable;
			v_alter_data.v_can_drop_column = v_database.v_can_drop_column;
			v_alter_data.v_can_add_constraint = v_database.v_can_add_constraint;
			v_alter_data.v_can_drop_constraint = v_database.v_can_drop_constraint;
			v_alter_data.v_has_update_rule = v_database.v_has_update_rule;
			v_alter_data.v_update_rules = v_database.v_update_rules;
			v_alter_data.v_delete_rules = v_database.v_delete_rules;

			v_return.v_data = v_alter_data;

			return v_return;

		}

		/// <summary>
		/// Retrieves list of strings containing columns list separated by comma.
		/// </summary>
		/// <param name="p_table_name">Table name.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn RefreshRefColumnsList(int p_database_index, string p_table_name)
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			try {
				System.Collections.Generic.List<string> v_list_columns = GetRefColumnsList (v_database, p_table_name);

				v_return.v_data = v_list_columns;

				return v_return;

			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

		}

		/// <summary>
		/// Helper to retrieve list of strings containing columns list separated by comma.
		/// </summary>
		/// <param name="p_database">Connection info.</param>
		/// <param name="p_table">Table name.</param>
		public static System.Collections.Generic.List<string> GetRefColumnsList(OmniDatabase.Generic p_database, string p_table) {

			string v_table = "";
			string v_schema = "";

			if (p_database.v_has_schema) {
				string[] v_strings = p_table.Split ('.');
				v_schema = v_strings [0];
				v_table = v_strings [1];
			} 
			else
				v_table = p_table;

			System.Data.DataTable v_pk_table = p_database.QueryTablesPrimaryKeys(v_schema, v_table);

			System.Collections.Generic.List<string> v_ref_columns = new System.Collections.Generic.List<string>();

			if (v_pk_table.Rows.Count>0) {

				string v_column_list = "";
				bool v_first = true;

				foreach (System.Data.DataRow v_pk_column in v_pk_table.Rows) {

					if (!v_first)
						v_column_list += ", ";

					v_column_list += v_pk_column["column_name"].ToString();
					v_first = false;

				}

				v_ref_columns.Add(v_column_list);


			}

			//Table Uniques
			System.Data.DataTable v_uniques_table = p_database.QueryTablesUniques(v_schema, v_table);

			if (v_uniques_table.Rows.Count>0) {

				string v_column_list = "";
				string v_constraint_name = v_uniques_table.Rows[0]["constraint_name"].ToString();
				bool v_first = true;

				foreach (System.Data.DataRow v_column in v_uniques_table.Rows) {

					if (v_column["constraint_name"].ToString()!=v_constraint_name) {
						v_ref_columns.Add(v_column_list);

						v_constraint_name = v_column["constraint_name"].ToString();
						v_column_list = "";
						v_first = true;
					}


					if (!v_first) {
						v_column_list += ", ";
					}

					v_column_list += v_column["column_name"].ToString();
					v_first = false;

				}

				if (v_column_list!="") {
					v_ref_columns.Add(v_column_list);
				}

			}

			return v_ref_columns;

		}

		/// <summary>
		/// Saves edit data window changes.
		/// </summary>
		/// <param name="p_table_name">Table name.</param>
		/// <param name="p_data_rows">Records data.</param>
		/// <param name="p_rows_info">Records info.</param>
		/// <param name="p_columns">Column list.</param>
		/// <param name="p_pk_info">Primary keys list.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SaveEditData(int p_database_index, 
		                                      string p_table_name,
			System.Collections.Generic.List<System.Collections.Generic.List<string>> p_data_rows, 
			System.Collections.Generic.List<EditDataRowInfo> p_rows_info,
			System.Collections.Generic.List<ColumnInfo> p_columns,
			System.Collections.Generic.List<PrimaryKeyInfo> p_pk_info)
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			System.Collections.Generic.List<CommandInfoReturn> v_row_info_return_list = new System.Collections.Generic.List<CommandInfoReturn>();



			string v_table_name = "";

			if (v_database.v_has_schema)
				v_table_name = v_database.v_schema + "." + p_table_name;
			else
				v_table_name = p_table_name;

			int i = 0;

			foreach (EditDataRowInfo v_row_info in p_rows_info) {

				string v_command = "";

				//Deleting row
				if (v_row_info.mode == -1) {
					v_command = "delete from " + v_table_name + " where ";

					bool v_first = true;

					int v_pk_index = 0;



					foreach (PrimaryKeyColumn v_pk in v_row_info.pk) {

						if (!v_first)
							v_command += " and ";

						v_first = false;

						for (int j=0; j < p_pk_info.Count; j++) {
							if (v_pk.v_column == p_pk_info [j].v_column) {
								v_pk_index = j;
								break;
							}
						}

						if (p_pk_info[v_pk_index].v_class=="numeric")
							v_command += p_pk_info[v_pk_index].v_compareformat.Replace("#",v_pk.v_column) + " = " + v_pk.v_value;
						else
							v_command += p_pk_info[v_pk_index].v_compareformat.Replace("#",v_pk.v_column) + " = '" + v_pk.v_value + "'";

					}

					CommandInfoReturn v_row_info_return = new CommandInfoReturn ();
					v_row_info_return.mode = -1;
					v_row_info_return.index = v_row_info.index;
					v_row_info_return.v_command = v_command;

					try {
                        v_session.Execute(p_database_index, v_command, false, false);
						v_row_info_return.error = false;
						v_row_info_return.v_message = "Success.";

					} catch (Spartacus.Database.Exception e) {
						v_row_info_return.error = true;
						v_row_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
					}

					v_row_info_return_list.Add (v_row_info_return);
				}
				//Inserting New Row
				else if (v_row_info.mode == 2) {
					v_command = "insert into " + v_table_name + " ( ";

					bool v_first = true;

					foreach (ColumnInfo v_col in p_columns) {

						if (!v_first)
							v_command += ", ";

						v_first = false;

						v_command += v_col.v_column;
					}

					v_command += " ) values ( ";

					v_first = true;

					for (int j = 1; j < p_data_rows[i].Count; j++) {

						if (!v_first)
							v_command += ", ";

						v_first = false;

						string v_value = "";

						if (p_data_rows [i] [j] != null)
							v_value = p_data_rows [i] [j];

						if (p_columns [j - 1].v_class == "numeric" || p_columns [j - 1].v_class == "other") {
							if (v_value == "")
								v_command += "null";
							else
								v_command += p_columns [j - 1].v_writeformat.Replace ("#", v_value);
						} 
						else {
							v_command += p_columns [j - 1].v_writeformat.Replace ("#", v_value.Replace("'","''")); ;
						}
						

					}

					v_command += " ) ";

					CommandInfoReturn v_row_info_return = new CommandInfoReturn ();
					v_row_info_return.mode = 2;
					v_row_info_return.index = v_row_info.index;
					v_row_info_return.v_command = v_command;

					try {
                        v_session.Execute(p_database_index, v_command, false, false);
						v_row_info_return.error = false;
						v_row_info_return.v_message = "Success.";

					} catch (Spartacus.Database.Exception e) {
						v_row_info_return.error = true;
						v_row_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
					}

					v_row_info_return_list.Add (v_row_info_return);
				}
				//Updating Existing Row
				else if (v_row_info.mode == 1) {
					v_command = "update " + v_table_name + " set ";

					bool v_first = true;

					foreach (int v_col_index in p_rows_info[i].changed_cols) {
						
						if (!v_first)
							v_command += ", ";
						
						v_first = false;

						string v_value = "";

						if (p_data_rows [i] [v_col_index+1] != null)
							v_value = p_data_rows [i] [v_col_index+1];

						v_command += p_columns [v_col_index].v_column + " = ";

						if (p_columns [v_col_index].v_class == "numeric" || p_columns [v_col_index].v_class == "other") {
							if (v_value == "")
								v_command += "null";
							else
								v_command += p_columns [v_col_index].v_writeformat.Replace ("#", v_value);
						} 
						else {
							v_command += p_columns [v_col_index].v_writeformat.Replace ("#", v_value.Replace("'","''"));
						}


					}

					v_command += " where ";

					v_first = true;

					int v_pk_index = 0;

					foreach (PrimaryKeyColumn v_pk in v_row_info.pk) {

						if (!v_first)
							v_command += " and ";

						for (int j=0; j < p_pk_info.Count; j++) {
							if (v_pk.v_column == p_pk_info [j].v_column) {
								v_pk_index = j;
								break;
							}
						}

						v_first = false;

						if (p_pk_info[v_pk_index].v_class=="numeric")
							v_command += p_pk_info[v_pk_index].v_compareformat.Replace("#",v_pk.v_column) + " = " + v_pk.v_value;
						else
							v_command += p_pk_info[v_pk_index].v_compareformat.Replace("#",v_pk.v_column) + " = '" + v_pk.v_value + "'";

					}

					CommandInfoReturn v_row_info_return = new CommandInfoReturn ();
					v_row_info_return.mode = 1;
					v_row_info_return.index = v_row_info.index;
					v_row_info_return.v_command = v_command;

					try {
                        v_session.Execute(p_database_index, v_command, false, false);
						v_row_info_return.error = false;
						v_row_info_return.v_message = "Success.";

					} catch (Spartacus.Database.Exception e) {
						v_row_info_return.error = true;
						v_row_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
					}

					v_row_info_return_list.Add (v_row_info_return);
				}

				i++;
			}

			v_return.v_data = v_row_info_return_list;

			return v_return;
		}

		/// <summary>
		/// Saves alter table window changes.
		/// </summary>
		/// <param name="p_mode">Mode.</param>
		/// <param name="p_new_table_name">New table name.</param>
		/// <param name="p_original_table_name">Original table name.</param>
		/// <param name="p_data_columns">Columns data.</param>
		/// <param name="p_row_columns_info">Columns info.</param>
		/// <param name="p_data_constraints">Constraints data.</param>
		/// <param name="p_row_constraints_info">Constraints info.</param>
		/// <param name="p_data_indexes">Indexes data.</param>
		/// <param name="p_row_indexes_info">Indexes info.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SaveAlterTable(int p_database_index, 
		                                        string p_mode, 
												string p_new_table_name, 
												string p_original_table_name, 
												System.Collections.Generic.List<System.Collections.Generic.List<string>> p_data_columns, 
												System.Collections.Generic.List<AlterTableColumnInfo> p_row_columns_info,
												System.Collections.Generic.List<System.Collections.Generic.List<string>> p_data_constraints, 
												System.Collections.Generic.List<AlterTableConstraintInfo> p_row_constraints_info,
												System.Collections.Generic.List<System.Collections.Generic.List<string>> p_data_indexes, 
												System.Collections.Generic.List<AlterTableIndexInfo> p_row_indexes_info)
		{
			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			SaveAlterTableReturn v_alter_return = new SaveAlterTableReturn ();


			v_alter_return.v_columns_simple_commands_return = new System.Collections.Generic.List<CommandInfoReturn>();
			v_alter_return.v_columns_group_commands_return = new System.Collections.Generic.List<CommandColumnInfoReturn>();
			v_alter_return.v_constraints_commands_return = new System.Collections.Generic.List<CommandInfoReturn>();
			v_alter_return.v_indexes_commands_return = new System.Collections.Generic.List<CommandInfoReturn>();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];


			int i = 0;

			// Changing existing table
			if (p_mode == "alter") {

				string v_table_name = "";

				if (v_database.v_has_schema)
					v_table_name = v_database.v_schema + "." + p_original_table_name;
				else
					v_table_name = p_original_table_name;

				//Columns
				foreach (AlterTableColumnInfo v_row in p_row_columns_info) {
					//Adding new column
					if (v_row.mode == 2) {
						string v_command = v_database.v_add_column_command;
						v_command = v_command.Replace ("#p_table_name#", v_table_name);
						v_command = v_command.Replace ("#p_column_name#", p_data_columns [i] [0]);
						v_command = v_command.Replace ("#p_data_type#", p_data_columns [i] [1]);

						if (p_data_columns [i] [2] == "YES")
							v_command = v_command.Replace ("#p_nullable#", "");
						else
							v_command = v_command.Replace ("#p_nullable#", "not null");

						CommandInfoReturn v_info_return = new CommandInfoReturn ();
						v_info_return.mode = 2;
						v_info_return.index = p_row_columns_info[i].index;
						v_info_return.v_command = v_command;

						try {
                            v_session.Execute(p_database_index, v_command, false, true);
							v_info_return.error = false;
							v_info_return.v_message = "Success.";

						} catch (Spartacus.Database.Exception e) {
							v_info_return.error = true;
							v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
						}

						v_alter_return.v_columns_simple_commands_return.Add (v_info_return);
					
					}
					//Dropping existing column
					else if (v_row.mode == -1) {
						string v_command = v_database.v_drop_column_command;
						v_command = v_command.Replace ("#p_table_name#", v_table_name);
						v_command = v_command.Replace ("#p_column_name#", v_row.originalColName);

						CommandInfoReturn v_info_return = new CommandInfoReturn ();
						v_info_return.mode = -1;
						v_info_return.index = p_row_columns_info[i].index;
						v_info_return.v_command = v_command;

						try {
                            v_session.Execute(p_database_index, v_command, false, true);
							v_info_return.error = false;
							v_info_return.v_message = "Success.";

						} catch (Spartacus.Database.Exception e) {
							v_info_return.error = true;
							v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
						}

						v_alter_return.v_columns_simple_commands_return.Add (v_info_return);



					}
					//Changing existing column
					else if (v_row.mode == 1) {

						CommandColumnInfoReturn v_info_return = new CommandColumnInfoReturn ();
						v_info_return.mode = 1;
						v_info_return.index = p_row_columns_info[i].index;

						// Changing column type

						CommandInfoReturn v_info_return1 = new CommandInfoReturn ();
						v_info_return1.mode = 1;
						v_info_return1.index = p_row_columns_info[i].index;
						v_info_return1.error = false;
						v_info_return1.v_message = "Success.";

						if (v_row.originalDataType != p_data_columns [i] [1]) {

							string v_command = v_database.v_alter_type_command;
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_column_name#", v_row.originalColName);
							v_command = v_command.Replace ("#p_new_data_type#", p_data_columns [i] [1]);

							v_info_return1.v_command = v_command;

							try {
                                v_session.Execute(p_database_index, v_command, false, true);
							} catch (Spartacus.Database.Exception e) {
								v_info_return1.error = true;
								v_info_return1.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

						}

						v_info_return.alter_datatype = v_info_return1;

						// Changing column nullable

						v_info_return1 = new CommandInfoReturn ();
						v_info_return1.mode = 1;
						v_info_return1.index = p_row_columns_info[i].index;
						v_info_return1.error = false;
						v_info_return1.v_message = "Success.";

						if (v_row.originalNullable != p_data_columns [i] [2]) {

							string v_command;

							if (p_data_columns [i] [2] == "YES")
								v_command = v_database.v_set_nullable_command;
							else
								v_command = v_database.v_drop_nullable_command;
							
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_column_name#", v_row.originalColName);
							v_command = v_command.Replace ("#p_new_data_type#", p_data_columns [i] [1]);

							v_info_return1.v_command = v_command;

							try {
                                v_session.Execute(p_database_index, v_command, false, true);

							} catch (Spartacus.Database.Exception e) {
								v_info_return1.error = true;
								v_info_return1.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

						}

						v_info_return.alter_nullable = v_info_return1;

						// Changing column name

						v_info_return1 = new CommandInfoReturn ();
						v_info_return1.mode = 1;
						v_info_return1.index = p_row_columns_info[i].index;
						v_info_return1.error = false;
						v_info_return1.v_message = "Success.";

						if (v_row.originalColName != p_data_columns [i] [0]) {
							
							string v_command = v_database.v_rename_column_command;
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_column_name#", v_row.originalColName);
							v_command = v_command.Replace ("#p_new_column_name#", p_data_columns [i] [0]);
							v_command = v_command.Replace ("#p_new_data_type#", p_data_columns [i] [1]);
							if (p_data_columns [i] [2]=="YES")
								v_command = v_command.Replace ("#p_new_nullable#", "");
							else
								v_command = v_command.Replace ("#p_new_nullable#", "not null");

							v_info_return1.v_command = v_command;

							try {
                                v_session.Execute(p_database_index, v_command, false, true);

							} catch (Spartacus.Database.Exception e) {
								v_info_return1.error = true;
								v_info_return1.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

						}

						v_info_return.alter_colname = v_info_return1;

						v_alter_return.v_columns_group_commands_return.Add (v_info_return);


					}
					i++;
				}

				i = 0;

				//Constraints
				foreach (AlterTableConstraintInfo v_row in p_row_constraints_info) {

					//Adding new constraint
					if (v_row.mode == 2) {
						
						// Adding PK
						if (p_data_constraints [i] [1].ToString () == "Primary Key") {
							
							string v_command = v_database.v_add_pk_command;
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);
							v_command = v_command.Replace ("#p_columns#", p_data_constraints [i] [2]);

							CommandInfoReturn v_info_return = new CommandInfoReturn ();
							v_info_return.mode = 2;
							v_info_return.index = p_row_constraints_info[i].index;
							v_info_return.v_command = v_command;

							try {
                                v_session.Execute(p_database_index, v_command, false, true);
								v_info_return.error = false;
								v_info_return.v_message = "Success.";

							} catch (Spartacus.Database.Exception e) {
								v_info_return.error = true;
								v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

							v_alter_return.v_constraints_commands_return.Add (v_info_return);

						}
						// Adding FK
						else if (p_data_constraints [i] [1].ToString () == "Foreign Key") {

							string v_command = v_database.v_add_fk_command;
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);
							v_command = v_command.Replace ("#p_columns#", p_data_constraints [i] [2]);
							v_command = v_command.Replace ("#p_r_table_name#", p_data_constraints [i] [3]);
							v_command = v_command.Replace ("#p_r_columns#", p_data_constraints [i] [4]);
							v_command = v_command.Replace ("#p_delete_update_rules#", v_database.HandleUpdateDeleteRules(p_data_constraints [i] [6], p_data_constraints [i] [5]));

							CommandInfoReturn v_info_return = new CommandInfoReturn ();
							v_info_return.mode = 2;
							v_info_return.index = p_row_constraints_info[i].index;
							v_info_return.v_command = v_command;

							try {

                                v_session.Execute(p_database_index, v_command, false, true);
								v_info_return.error = false;
								v_info_return.v_message = "Success.";

							} catch (Spartacus.Database.Exception e) {
								v_info_return.error = true;
								v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

							v_alter_return.v_constraints_commands_return.Add (v_info_return);

						}
						// Adding Unique
						if (p_data_constraints [i] [1].ToString () == "Unique") {

							string v_command = v_database.v_add_unique_command;
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);
							v_command = v_command.Replace ("#p_columns#", p_data_constraints [i] [2]);

							CommandInfoReturn v_info_return = new CommandInfoReturn ();
							v_info_return.mode = 2;
							v_info_return.index = p_row_constraints_info[i].index;
							v_info_return.v_command = v_command;

							try {
                                v_session.Execute(p_database_index, v_command, false, true);
								v_info_return.error = false;
								v_info_return.v_message = "Success.";

							} catch (Spartacus.Database.Exception e) {
								v_info_return.error = true;
								v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

							v_alter_return.v_constraints_commands_return.Add (v_info_return);

						}

					}
					//Dropping existing constraint
					else if (v_row.mode == -1) {

						// Dropping PK
						if (p_data_constraints [i] [1].ToString () == "Primary Key") {

							string v_command = v_database.v_drop_pk_command;
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);

							CommandInfoReturn v_info_return = new CommandInfoReturn ();
							v_info_return.mode = -1;
							v_info_return.index = p_row_constraints_info[i].index;
							v_info_return.v_command = v_command;

							try {
                                v_session.Execute(p_database_index, v_command, false, true);
								v_info_return.error = false;
								v_info_return.v_message = "Success.";

							} catch (Spartacus.Database.Exception e) {
								v_info_return.error = true;
								v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

							v_alter_return.v_constraints_commands_return.Add (v_info_return);

						}
						// Dropping FK
						else if (p_data_constraints [i] [1].ToString () == "Foreign Key") {

							string v_command = v_database.v_drop_fk_command;
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);

							CommandInfoReturn v_info_return = new CommandInfoReturn ();
							v_info_return.mode = -1;
							v_info_return.index = p_row_constraints_info[i].index;
							v_info_return.v_command = v_command;

							try {
                                v_session.Execute(p_database_index, v_command, false, true);
								v_info_return.error = false;
								v_info_return.v_message = "Success.";

							} catch (Spartacus.Database.Exception e) {
								v_info_return.error = true;
								v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

							v_alter_return.v_constraints_commands_return.Add (v_info_return);

						}
						// Dropping Unique
						else if (p_data_constraints [i] [1].ToString () == "Unique") {

							string v_command = v_database.v_drop_unique_command;
							v_command = v_command.Replace ("#p_table_name#", v_table_name);
							v_command = v_command.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);

							CommandInfoReturn v_info_return = new CommandInfoReturn ();
							v_info_return.mode = -1;
							v_info_return.index = p_row_constraints_info[i].index;
							v_info_return.v_command = v_command;

							try {
                                v_session.Execute(p_database_index, v_command, false, true);
								v_info_return.error = false;
								v_info_return.v_message = "Success.";

							} catch (Spartacus.Database.Exception e) {
								v_info_return.error = true;
								v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
							}

							v_alter_return.v_constraints_commands_return.Add (v_info_return);

						}

					}
					i++;

				}

				i = 0;

				//Indexes
				foreach (AlterTableIndexInfo v_row in p_row_indexes_info) {

					//Adding new index
					if (v_row.mode == 2) {
						
						string v_command = "";

						if (p_data_indexes [i] [1] == "Unique")
							v_command = v_database.v_create_unique_index_command;
						else
							v_command = v_database.v_create_index_command;
						
						v_command = v_command.Replace ("#p_table_name#", v_table_name);
						v_command = v_command.Replace ("#p_index_name#", p_data_indexes [i] [0]);
						v_command = v_command.Replace ("#p_columns#", p_data_indexes [i] [2]);

						CommandInfoReturn v_info_return = new CommandInfoReturn ();
						v_info_return.mode = 2;
						v_info_return.index = p_row_indexes_info[i].index;
						v_info_return.v_command = v_command;

						try {
                            v_session.Execute(p_database_index, v_command, false, true);
							v_info_return.error = false;
							v_info_return.v_message = "Success.";

						} catch (Spartacus.Database.Exception e) {
							v_info_return.error = true;
							v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
						}

						v_alter_return.v_indexes_commands_return.Add (v_info_return);


					}
					//Dropping existing index
					else if (v_row.mode == -1) {
						
						string v_command = v_database.v_drop_index_command;
						v_command = v_command.Replace ("#p_table_name#", v_table_name);
						v_command = v_command.Replace ("#p_index_name#", p_data_indexes [i] [0]);
						v_command = v_command.Replace ("#p_schema_name#", v_database.v_schema);

						CommandInfoReturn v_info_return = new CommandInfoReturn ();
						v_info_return.mode = -1;
						v_info_return.index = p_row_indexes_info[i].index;
						v_info_return.v_command = v_command;

						try {
                            v_session.Execute(p_database_index, v_command, false, true);
							v_info_return.error = false;
							v_info_return.v_message = "Success.";

						} catch (Spartacus.Database.Exception e) {
							v_info_return.error = true;
							v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
						}

						v_alter_return.v_indexes_commands_return.Add (v_info_return);

					}
					i++;

				}

				if (p_original_table_name != p_new_table_name) {

					CommandInfoReturn v_info_return = new CommandInfoReturn ();

					string v_command = v_database.v_rename_table_command;
					v_command = v_command.Replace ("#p_table_name#", v_table_name);
					v_command = v_command.Replace ("#p_new_table_name#", p_new_table_name);

					v_info_return.v_command = v_command;

					try {
                        v_session.Execute(p_database_index, v_command, false, true);
						v_info_return.error = false;
						v_info_return.v_message = "Success.";
					} catch (Spartacus.Database.Exception e) {

						v_info_return.error = true;
						v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
					}

					v_alter_return.v_rename_table_command = v_info_return;


				}

				v_return.v_data = v_alter_return;
				return v_return;

			} 
			// Creating new table
			else {

				string v_table_name = "";

				if (v_database.v_has_schema)
					v_table_name = v_database.v_schema + "." + p_new_table_name;
				else
					v_table_name = p_new_table_name;

				string v_command = "create table " + v_table_name + " (";

				bool v_first = true;

				foreach (AlterTableColumnInfo v_row in p_row_columns_info) {

					if (!v_first)
						v_command += ",";

					v_command += p_data_columns [i] [0] + " " + p_data_columns [i] [1];
					if (p_data_columns [i] [2] == "NO")
						v_command += " not null";
					
					i++;

					v_first = false;

				}

				i = 0;

				foreach (AlterTableConstraintInfo v_row in p_row_constraints_info) {

					if (!v_first)
						v_command += ",";

					v_first = false;

					if (p_data_constraints [i] [1].ToString () == "Primary Key") {

						string v_command_constraint = v_database.v_create_pk_command;
						v_command_constraint = v_command_constraint.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);
						v_command_constraint = v_command_constraint.Replace ("#p_columns#", p_data_constraints [i] [2]);

						v_command += v_command_constraint;

					}
					else if (p_data_constraints [i] [1].ToString () == "Foreign Key") {

						string v_command_constraint = v_database.v_create_fk_command;
						v_command_constraint = v_command_constraint.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);
						v_command_constraint = v_command_constraint.Replace ("#p_columns#", p_data_constraints [i] [2]);
						v_command_constraint = v_command_constraint.Replace ("#p_r_table_name#", p_data_constraints [i] [3]);
						v_command_constraint = v_command_constraint.Replace ("#p_r_columns#", p_data_constraints [i] [4]);
						v_command_constraint = v_command_constraint.Replace ("#p_delete_update_rules#", v_database.HandleUpdateDeleteRules(p_data_constraints [i] [6], p_data_constraints [i] [5]));

						v_command += v_command_constraint;

					}
					else if (p_data_constraints [i] [1].ToString () == "Unique") {

						string v_command_constraint = v_database.v_create_unique_command;
						v_command_constraint = v_command_constraint.Replace ("#p_constraint_name#", p_data_constraints [i] [0]);
						v_command_constraint = v_command_constraint.Replace ("#p_columns#", p_data_constraints [i] [2]);

						v_command += v_command_constraint;

					}

					i++;


				}


				v_command += ")";


				CommandInfoReturn v_info_return = new CommandInfoReturn ();
				v_info_return.v_command = v_command;

				try {
                    v_session.Execute(p_database_index, v_command, false, true);
					v_info_return.error = false;
					v_info_return.v_message = "Success.";
				} catch (Spartacus.Database.Exception e) {

					v_info_return.error = true;
					v_info_return.v_message = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
				}

				v_alter_return.v_create_table_command = v_info_return;

				v_return.v_data = v_alter_return;
				return v_return;
			}

		}

		/// <summary>
		/// Helper function. Retrieves list of positions where string appears in text.
		/// </summary>
		/// <param name="p_source">String that contains searchString.</param>
		/// <param name="p_searchString">String to be found in source.</param>
		public static System.Collections.Generic.List<int> GetPositions(string p_source, string p_searchString)
		{
			System.Collections.Generic.List<int> ret = new System.Collections.Generic.List<int>();
			int len = p_searchString.Length;
			int start = -len;
			while (true)
			{
				start = p_source.IndexOf(p_searchString, start + len);
				if (start == -1)
				{
					break;
				}
				else
				{
					ret.Add(start);
				}
			}
			return ret;
		}

		/// <summary>
		/// Helper function.
		/// </summary>
		/// <param name="p_sql">SQL command.</param>
		/// <param name="p_prefix">Prefix.</param>
		/// <param name="p_occurence_index">Prefix position in SQL command.</param>
		/// <param name="p_cursor_index">Cursor position.</param>
		public static bool IsReference(string p_sql, string p_prefix, int p_occurence_index, int p_cursor_index) {
			
			
			int v_length = p_prefix.Length;

			int v_next_index = p_occurence_index + v_length;

			//If prefix and occurence are the same
			if (v_next_index == p_cursor_index)
				return false;

			//prefix is at the end of the string
			if (p_occurence_index + v_length >= p_sql.Length) {
				if (p_occurence_index == 0)
					return false;
				else if (p_sql [p_occurence_index - 1] == ' ')
					return true;
				else
					return false;
			}

			char next_char = p_sql [v_next_index];

			if (next_char=='.')
				return false;

			if (next_char == ',' || next_char == '\n' || next_char == ' ' || next_char == ')') {
				if (p_occurence_index == 0)
					return false;
				else if (p_sql [p_occurence_index - 1] == ' ')
					return true;
				else
					return false;
			}

			return false;

		}

		/// <summary>
		/// Gets column auto completion list.
		/// </summary>
		/// <param name="p_prefix">Prefix.</param>
		/// <param name="p_sql">SQL command.</param>
		/// <param name="p_prefix_pos">Prefix position.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetCompletions(int p_database_index, string p_prefix, string p_sql, int p_prefix_pos)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			System.Collections.Generic.List<Completion> v_list = new System.Collections.Generic.List<Completion> ();

			if (v_session.v_database_index != -1) {

				string v_prefix = p_prefix;

				OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];



				bool v_found = false;

				System.Collections.Generic.List<int> inst = GetPositions (p_sql, v_prefix);

				int index = 0;

				foreach (int v_index in inst) {
					v_found = IsReference (p_sql, v_prefix, v_index, p_prefix_pos);
					if (v_found) {
						index = v_index;
						break;
					}
				}

				if (!v_found) {
					v_return.v_data = v_list;
					return v_return;
				}

				string v_table = "";

				while (index > 0 && p_sql [index - 1] == ' ')
					index--;

				int v_last_pos = index;

				if (p_sql [v_last_pos - 1] == ')') {

					int v_level = 0;

					while (index > 0) {
					

						if (p_sql [index - 1] == ')')
							v_level--;
						else if (p_sql [index - 1] == '(')
							v_level++;

						if (p_sql [index - 1] == '(' && v_level == 0)
							break;

						index--;
					}

					v_table = p_sql.Substring (index - 1, v_last_pos - index + 1);


				} else {

					while (index > 0 && p_sql [index - 1] != ' ' && p_sql [index - 1] != ',')
						index--;

					int v_first_pos = index;

					v_table = p_sql.Substring (v_first_pos, v_last_pos - v_first_pos);

				}

				string[,] v_data1;

				try {
					v_data1 = v_database.v_connection.GetColumnNamesAndTypes ("select x.* from " + v_table + " x where 1 = 0");
				} catch (Spartacus.Database.Exception e) {

					v_return.v_error = true;
					v_return.v_data = e.v_message.Replace ("<", "&lt;").Replace (">", "&gt;").Replace (System.Environment.NewLine, "<br/>");

					return v_return;
				}

				int v_score = (v_data1.Length / 2 * 100) + 100;

				v_list.Add (new Completion (v_prefix + ".", v_score, ""));

				v_score -= 100;

				for (int k = 0; k < v_data1.Length / 2; k++) {
					v_list.Add (new Completion (v_prefix + "." + v_data1 [k, 0].ToLower (), v_score, v_data1 [k, 1]));
					v_score -= 100;
				}
            
			}

			v_return.v_data = v_list;

			return v_return;
		}

		/// <summary>
		/// Gets column auto completion list for specific table.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetCompletionsTable(int p_database_index, string p_table)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_databases[p_database_index];

			string v_table_name = "";

			if (v_database.v_has_schema)
				v_table_name = v_database.v_schema + "." + p_table;
			else
				v_table_name = p_table;

			System.Collections.Generic.List<Completion> v_list = new System.Collections.Generic.List<Completion>();

			string[,] v_data1;

			try {
				v_data1 = v_database.v_connection.GetColumnNamesAndTypes("select x.* from " + v_table_name + " x where 1 = 0");
			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			int v_score = (v_data1.Length / 2 * 100) + 100;

			v_list.Add(new Completion("t.", v_score, ""));

			v_score -= 100;

			for (int k = 0; k < v_data1.Length / 2; k++)
			{
				v_list.Add(new Completion("t." + v_data1[k, 0].ToLower(), v_score, v_data1[k, 1]));
				v_score -= 100;
			}

			v_return.v_data = v_list;

			return v_return;
		}

		/// <summary>
		/// Get messages to be viewed in OmniChat.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetChatMessages()
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn();

			if (v_session == null)
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			}

			OmniDatabase.Generic v_database = v_session.v_omnidb_database;
			System.Collections.Generic.List<ChatMessage> v_messageList = new System.Collections.Generic.List<ChatMessage>();

			try
			{
				string v_sql =
					"select mes.mes_in_code, " +
					"    use.user_name, " +
					"    mes.mes_st_text, " +
					"    mes.mes_dt_timestamp " +
					"from messages mes " +
					"inner join messages_users meu " +
					"           on mes.mes_in_code = meu.mes_in_code " +
					"inner join users use " +
					"           on mes.user_id = use.user_id " +
					"where meu.user_id = " + v_session.v_user_id + " " +
					"  and meu.meu_bo_viewed = 'N';";

				System.Data.DataTable v_table = v_database.v_connection.Query(v_sql, "chat_messages");

				if (v_table != null && v_table.Rows.Count > 0)
				{
					for (int i = 0; i < v_table.Rows.Count; i++)
					{
						ChatMessage v_message = new ChatMessage();
						v_message.v_message_id = int.Parse(v_table.Rows[i]["mes_in_code"].ToString());
						v_message.v_user_name = v_table.Rows[i]["user_name"].ToString();
						v_message.v_text = v_table.Rows[i]["mes_st_text"].ToString();
						v_message.v_timestamp = v_table.Rows[i]["mes_dt_timestamp"].ToString();

						v_messageList.Add(v_message);
					}
				}
			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			try
			{
				if(v_messageList.Count > 0)
				{
					string v_sql =
						"update messages_users " +
						"set meu_bo_viewed = 'Y' " +
						"where user_id = " + v_session.v_user_id + " " +
						"  and mes_in_code in (";

					for(int i = 0; i < v_messageList.Count; i++)
					{
						v_sql += v_messageList[i].v_message_id + ", ";
					}

					v_sql = v_sql.Remove(v_sql.Length - 2);
					v_sql += ");";

					v_database.v_connection.Execute(v_sql);
				}
			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			v_return.v_data = v_messageList;
			return v_return;
		}

		/// <summary>
		/// Set messages as viewed by OmniChat.
		/// </summary>
		/// <param name="p_message_list">List of messages that were viewed by OmniChat.</param>
		/*[System.Web.Services.WebMethod]
		public static AjaxReturn ViewChatMessages(System.Collections.Generic.List<ChatMessage> p_message_list)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn();

			if (v_session == null)
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			}

			OmniDatabase.Generic v_database = v_session.v_omnidb_database;

			try
			{
				if(p_message_list.Count > 0)
				{
					string v_sql =
						"update messages_users " +
						"set meu_bo_viewed = 'Y' " +
						"where user_id = " + v_session.v_user_id + " " +
						"  and mes_in_code in (";

					for(int i = 0; i < p_message_list.Count; i++)
					{
						v_sql += p_message_list[i].v_message_id + ", ";
					}

					v_sql = v_sql.Remove(v_sql.Length - 2);
					v_sql += ");";

					v_database.v_connection.Execute(v_sql);
				}
			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}
			
			return v_return;
		}*/

		/// <summary>
		/// Sends a message through OmniChat.
		/// </summary>
		/// <param name="p_text">Message text.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SendChatMessage(string p_text)
		{
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["DB_SESSION"];

			AjaxReturn v_return = new AjaxReturn ();

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			OmniDatabase.Generic v_database = v_session.v_omnidb_database;
			ChatMessage v_message;

			try {
				string v_sql = 
					"insert into messages (" +
					"    mes_st_text, " +
					"    mes_dt_timestamp, " +
					"    user_id " +
					") values ( " +
					"  '" + p_text + "', " +
					"    datetime('now', 'localtime'), " +
					"  " + v_session.v_user_id +
					");" +
					"select max(mes_in_code) " +
					"from messages;";

				int v_messsageCode = int.Parse(v_database.v_connection.ExecuteScalar(v_sql));

				v_sql =
					"insert into messages_users (" +
					"    mes_in_code, " +
					"    meu_bo_viewed, " +
					"    user_id " +
					")" +
					"select " + v_messsageCode + ", " +
					"    'N', " +
					"    use.user_id " +
					"from users use " +
					"where use.user_id <> " + v_session.v_user_id + ";";

				v_database.v_connection.Execute(v_sql);

				v_sql = 
					"select mes_dt_timestamp " +
					"from messages " +
					"where mes_in_code = " + v_messsageCode;

				v_message = new ChatMessage();
				v_message.v_message_id = v_messsageCode;
				v_message.v_user_name = v_session.v_user_name;
				v_message.v_text = p_text;
				v_message.v_timestamp = v_database.v_connection.ExecuteScalar(v_sql);

			}
			catch (Spartacus.Database.Exception e)
			{

				v_return.v_error = true;
				v_return.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

				return v_return;
			}

			v_return.v_data = v_message;
			return v_return;
		}
	}
}