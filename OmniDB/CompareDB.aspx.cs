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
	public class CompareData {
		public string v_html;
		public string v_log;
		public int v_num_green_tables;
		public int v_num_orange_tables;
		public int v_num_red_tables;
		public int v_num_green_cols;
		public int v_num_orange_cols;
		public int v_num_red_cols;
	}

	public class CompareColumns {
		public int v_green_items;
		public int v_orange_items;
		public string v_html;

	}

	public class CompareColumnsDetails {
		public bool v_different;
		public string v_html;

	}


	/// <summary>
	/// Comparison page.
	/// </summary>
	public partial class CompareDB : System.Web.UI.Page
	{

		public Session v_session;

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


		public static int FindInTable(System.Data.DataTable v_table, String v_value, int index) {

			int v_value_pos = (int)v_value [0];


			for (int i = 0; i < v_table.Rows.Count; i++) {
				//Console.WriteLine("v_value char: " + v_value[0] + " - v_value pos: " + v_value_pos + " v_data_char: " + v_table.Rows [i] [index].ToString () [0] + " - v_data pos: " + (int) v_table.Rows [i] [index].ToString () [0]);

				if ((int)v_table.Rows [i] [index].ToString () [0] > v_value_pos) {
					//Console.WriteLine ("Maior, saiu");
					return -1;
				} else if (v_table.Rows [i] [index].ToString () == v_value) {
					//Console.WriteLine ("Achou");
					return i;
				}

			}
			return -1;
		}


		public static string PrintTable(string v_table_name, string v_color_left, string v_color_right) {

			string v_html = "";

			v_html += "<table id=\"compare_table\"><tr onclick=\"toggleDiv('div_" + v_table_name + "')\"><th class=\"th_" + v_color_left + "\">" + v_table_name + "</th>" +
				"<th class=\"th_" + v_color_right + "\">" + v_table_name + "</th></tr></table>" +
				"<div id=\"div_" + v_table_name + "\" style=\"display:none;\">";

			v_html += "<table id=\"compare_table\">";

			//v_html += "<div style=\"float:left;\" class=\"div_" + v_color_left + " left\"><img style=\"vertical-align: sub;\" src=\"images/table.png\"/> <b>" + v_table_name + "</b></div>";
			//v_html += "<div class=\"div_" + v_color_right + "\"><img style=\"vertical-align: sub;\" src=\"images/table.png\"/> <b>" + v_table_name + "</b></div>";

			return v_html;
		}


		public static string PrintTableColumns(System.Data.DataRow v_row, System.Data.DataTable v_columns, string v_color_left, string v_color_right) {

			int v_lower_index = Convert.ToInt32 (v_row ["position"]);

			int v_upper_index = v_lower_index + Convert.ToInt32 (v_row ["num_rows"]);

			string v_html = "";

			for (int i = v_lower_index; i < v_upper_index; i++) {

				v_html += PrintColumn (v_columns.Rows [i], v_color_left, v_color_right);

			}

			v_html += "</table></div>";

			return v_html;
		}

		public static string PrintColumn(System.Data.DataRow v_row, string v_color_left, string v_color_right) {

			string v_html = "";

			v_html += "<tr><td class=\"td_col_" + v_color_left + "\">" + v_row ["column_name"].ToString () + "</td>" +
				"<td class=\"td_col_" + v_color_right + "\">" + v_row ["column_name"].ToString () + "</td></tr>";

			v_html += "<tr><td class=\"td_attr_" + v_color_left + "\">" + v_row ["data_type"].ToString () + "</td>" +
				"<td class=\"td_attr_" + v_color_right + "\">" + v_row ["data_type"].ToString () + "</td></tr>";

			v_html += "<tr><td class=\"td_attr_" + v_color_left + "\">" + v_row ["data_length"].ToString () + "</td>" +
				"<td class=\"td_attr_" + v_color_right + "\">" + v_row ["data_length"].ToString () + "</td></tr>";

			v_html += "<tr><td class=\"td_attr_" + v_color_left + "\">" + v_row ["nullable"].ToString () + "</td>" +
				"<td class=\"td_attr_" + v_color_right + "\">" + v_row ["nullable"].ToString () + "</td></tr>";

			return v_html;
		}

		public static CompareColumnsDetails CompareColumns(System.Data.DataRow v_row1, System.Data.DataRow v_row2) {

			CompareColumnsDetails v_compare_columns = new CompareColumnsDetails();

			bool different = false;

			string v_html = "";

			v_html += "<tr><td class=\"td_col_green\">" + v_row1["column_name"].ToString() + "</td>" +
				"<td class=\"td_col_green\">" + v_row2["column_name"].ToString() + "</td></tr>";

			if (v_row1["data_type"].ToString()==v_row2["data_type"].ToString()) {

				v_html += "<tr><td class=\"td_attr_green\">" + v_row1["data_type"].ToString() + "</td>" +
					"<td class=\"td_attr_green\">" + v_row2["data_type"].ToString() + "</td></tr>";

			}
			else {
				different = true;
				v_html += "<tr><td class=\"td_attr_blue\">" + v_row1["data_type"].ToString() + "</td>" +
					"<td class=\"td_attr_blue\">" + v_row2["data_type"].ToString() + "</td></tr>";

			}

			if (v_row1["data_length"].ToString()==v_row2["data_length"].ToString()) {

				v_html += "<tr><td class=\"td_attr_green\">" + v_row1["data_length"].ToString() + "</td>" +
					"<td class=\"td_attr_green\">" + v_row2["data_length"].ToString() + "</td></tr>";

			}
			else {
				different = true;
				v_html += "<tr><td class=\"td_attr_blue\">" + v_row1["data_length"].ToString() + "</td>" +
					"<td class=\"td_attr_blue\">" + v_row2["data_length"].ToString() + "</td></tr>";

			}

			if (v_row1["nullable"].ToString()==v_row2["nullable"].ToString()) {
				v_html += "<tr><td class=\"td_attr_green\">" + v_row1["nullable"].ToString() + "</td>" +
					"<td class=\"td_attr_green\">" + v_row2["nullable"].ToString() + "</td></tr>";
			}
			else {
				different = true;
				v_html += "<tr><td class=\"td_attr_blue\">" + v_row1["nullable"].ToString() + "</td>" +
					"<td class=\"td_attr_blue\">" + v_row2["nullable"].ToString() + "</td></tr>";
			}

			v_compare_columns.v_different = different;
			v_compare_columns.v_html = v_html;


			return v_compare_columns;
		}

		public static CompareColumns CompareTablesColumns(System.Data.DataRow v_row1, System.Data.DataTable v_columns1,System.Data.DataRow v_row2, System.Data.DataTable v_columns2) {

			CompareColumns v_compare_columns = new CompareColumns ();

			CompareColumnsDetails v_compare_columns_details;

			int v_green_items = 0;
			int v_orange_items = 0;

			int v_lower_index1 = Convert.ToInt32 (v_row1 ["position"]);
			int v_num_rows1 = Convert.ToInt32 (v_row1 ["num_rows"]);
			int v_upper_index1 = v_lower_index1 + v_num_rows1;

			int v_lower_index2 = Convert.ToInt32 (v_row2 ["position"]);
			int v_num_rows2 = Convert.ToInt32 (v_row2 ["num_rows"]);
			int v_upper_index2 = v_lower_index2 + v_num_rows2;

			string v_html = "";

			int v_counter1 = v_lower_index1;
			int v_counter2 = v_lower_index2;

			while (v_counter1 < v_upper_index1) {

				if (v_counter2 - v_lower_index2 < v_num_rows2) {

					int v_compare = String.Compare (v_columns2.Rows [v_counter2] ["column_name"].ToString (), v_columns1.Rows [v_counter1] ["column_name"].ToString (), true);

					//Console.WriteLine(v_columns1.Rows[v_counter1]["column_name"].ToString() + " " + v_columns2.Rows[v_counter2]["column_name"].ToString());

					//Console.WriteLine("Compare " + v_compare);

					// column1[i] nao esta em column2[i]
					if (v_compare == 1) {
						v_html += PrintColumn (v_columns1.Rows [v_counter1], "green", "red");
						v_counter1++;
					}
					// column2[i] nao esta em column1[i]
					else if (v_compare == -1) {
						v_html += PrintColumn (v_columns2.Rows [v_counter2], "red", "green");
						v_counter2++;
					} 
					else {
						v_compare_columns_details = CompareColumns (v_columns1.Rows [v_counter1], v_columns2.Rows [v_counter2]);
						v_html += v_compare_columns_details.v_html;

						if (!v_compare_columns_details.v_different)
							v_green_items++;
						else
							v_orange_items++;

						v_counter1++;
						v_counter2++;
					}

				} 
				else {
					v_html += PrintColumn (v_columns1.Rows [v_counter1], "green", "red");
					v_counter1++;
				}

			}
			while (v_counter2 < v_upper_index2) {
				v_html += PrintColumn(v_columns2.Rows[v_counter2],"red","green");
				v_counter2++;
			}

			v_html += "</table></div>";

			v_compare_columns.v_html = v_html;
			v_compare_columns.v_green_items = v_green_items;
			v_compare_columns.v_orange_items = v_orange_items;

			return v_compare_columns;
		}


		[System.Web.Services.WebMethod]
		public static AjaxReturn CompareBases(int p_second_db)
		{

			HttpContext.Current.Server.ScriptTimeout = 86400;

			AjaxReturn v_g1 = new AjaxReturn();

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_g1.v_error = true;
				v_g1.v_error_id = 1;
				return v_g1;
			} 

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_list_tables = new System.Collections.Generic.List<System.Collections.Generic.List<string>> ();


			CompareData v_d1 = new CompareData ();

			CompareColumns v_compare_columns;

			int v_num_orange_tables = 0;
			int v_num_green_tables = 0;
			int v_num_red_tables = 0;

			int v_num_orange_cols = 0;
			int v_num_green_cols = 0;
			int v_num_red_cols = 0;


			String v_html = "";	

			String v_log = "";

			System.Data.DataTable v_data1;
			System.Data.DataTable v_data2;

			OmniDatabase.Generic v_database1 = v_session.GetSelectedDatabase();
			OmniDatabase.Generic v_database2 = v_session.v_databases[p_second_db];

			try
			{

				System.Data.DataTable v_orig_data_columns1 = v_database1.QueryTablesFields(null);

				System.Data.DataView v_view = new System.Data.DataView(v_orig_data_columns1);
				v_view.Sort = "table_name asc, column_name asc";
				System.Data.DataTable v_data_columns1 = v_view.ToTable();

				System.Data.DataTable v_orig_data_columns2 = v_database2.QueryTablesFields(null);

				v_view = new System.Data.DataView(v_orig_data_columns2);
				v_view.Sort = "table_name asc, column_name asc";
				System.Data.DataTable v_data_columns2 = v_view.ToTable();


				int v_pos_counter = 0;
				int v_count_cols = 0;

				v_data1 = new System.Data.DataTable ();
				v_data1.Columns.Add ("table_name");
				v_data1.Columns.Add ("num_rows");
				v_data1.Columns.Add ("position");

				string v_curr_table = v_orig_data_columns1.Rows[0]["table_name"].ToString();

				foreach (System.Data.DataRow v_column in v_orig_data_columns1.Rows) {
					if (v_curr_table!=v_column["table_name"].ToString()) {
						System.Data.DataRow v_new_row = v_data1.NewRow ();
						v_new_row ["table_name"] = v_curr_table;
						v_new_row ["num_rows"] = v_count_cols;
						v_new_row ["position"] = v_pos_counter;
						v_data1.Rows.Add (v_new_row);

						v_pos_counter += v_count_cols;
						v_count_cols=0;
						v_curr_table=v_column["table_name"].ToString();
					}
	
					v_count_cols++;
				
				}
					
				System.Data.DataRow v_last_row = v_data1.NewRow ();
				v_last_row ["table_name"] = v_curr_table;
				v_last_row ["num_rows"] = v_count_cols;
				v_last_row ["position"] = v_pos_counter;
				v_data1.Rows.Add (v_last_row);



				//Console.WriteLine("--------------------");

				v_pos_counter = 0;
				v_count_cols = 0;

				v_data2 = new System.Data.DataTable ();
				v_data2.Columns.Add ("table_name");
				v_data2.Columns.Add ("num_rows");
				v_data2.Columns.Add ("position");

				v_curr_table = v_orig_data_columns2.Rows[0]["table_name"].ToString();

				foreach (System.Data.DataRow v_column in v_orig_data_columns2.Rows) {
					if (v_curr_table!=v_column["table_name"].ToString()) {
						System.Data.DataRow v_new_row = v_data2.NewRow ();
						v_new_row ["table_name"] = v_curr_table;
						v_new_row ["num_rows"] = v_count_cols;
						v_new_row ["position"] = v_pos_counter;
						v_data2.Rows.Add (v_new_row);

						v_pos_counter += v_count_cols;
						v_count_cols=0;
						v_curr_table=v_column["table_name"].ToString();
					}
					v_count_cols++;

				}

				v_last_row = v_data2.NewRow ();
				v_last_row ["table_name"] = v_curr_table;
				v_last_row ["num_rows"] = v_count_cols;
				v_last_row ["position"] = v_pos_counter;
				v_data2.Rows.Add (v_last_row);


				int v_counter1 = 0;

				int v_counter2 = 0;

				while (v_counter1 < v_data1.Rows.Count) {
					
					if (v_counter2 < v_data2.Rows.Count) {
						
						int v_compare = String.Compare( v_data2.Rows[v_counter2]["table_name"].ToString(), v_data1.Rows[v_counter1]["table_name"].ToString(), true );
						//Console.WriteLine("Compare " + v_compare);
						// data1[i] nao esta em data2[i]

						System.Collections.Generic.List<string> v_table_info = new System.Collections.Generic.List<string>();


						if (v_compare == 1) {
							v_table_info.Add(v_data1.Rows[v_counter1]["table_name"].ToString());
							v_table_info.Add("-1");

							v_html += PrintTable(v_data1.Rows[v_counter1]["table_name"].ToString(),"green","red");
							v_html += PrintTableColumns(v_data1.Rows[v_counter1],v_data_columns1,"green","red");
							v_num_red_cols += Convert.ToInt32(v_data1.Rows[v_counter1]["num_rows"]);
							v_counter1++;
						}
						// data2[i] nao esta em data1[i]
						else if (v_compare == -1) {
							v_table_info.Add(v_data2.Rows[v_counter2]["table_name"].ToString());
							v_table_info.Add("1");

							v_html += PrintTable(v_data2.Rows[v_counter2]["table_name"].ToString(),"red","green");
							v_html += PrintTableColumns(v_data2.Rows[v_counter2],v_data_columns2,"red","green");
							v_num_red_cols += Convert.ToInt32(v_data2.Rows[v_counter2]["num_rows"]);
							v_counter2++;
						}
						else {
							
							//Console.WriteLine("iguais");
							v_compare_columns = CompareTablesColumns(v_data1.Rows[v_counter1],v_data_columns1,v_data2.Rows[v_counter2],v_data_columns2);

							int v_total_cols = Math.Max(Convert.ToInt32(v_data1.Rows[v_counter1]["num_rows"]),Convert.ToInt32(v_data2.Rows[v_counter2]["num_rows"]));

							//Console.WriteLine(v_total_cols + " " + v_compare_columns.v_green_items + " " + v_compare_columns.v_orange_items);

							v_num_green_cols += v_compare_columns.v_green_items;
							v_num_orange_cols += v_compare_columns.v_orange_items;
							v_num_red_cols += v_total_cols - v_compare_columns.v_green_items - v_compare_columns.v_orange_items;

							if (v_total_cols==v_compare_columns.v_green_items) {
								v_table_info.Add(v_data1.Rows[v_counter1]["table_name"].ToString());
								v_table_info.Add("0");

								v_html += PrintTable(v_data1.Rows[v_counter1]["table_name"].ToString(),"green","green");
								v_num_green_tables++;
							}
							else {
								v_table_info.Add(v_data1.Rows[v_counter1]["table_name"].ToString());
								v_table_info.Add("2");

								v_html += PrintTable(v_data1.Rows[v_counter1]["table_name"].ToString(),"orange","orange");
								v_num_orange_tables++;
							}

							v_html += v_compare_columns.v_html;

							v_counter1++;
							v_counter2++;
						}

						v_list_tables.Add(v_table_info);

					}
					else {
						v_html += PrintTable(v_data1.Rows[v_counter1]["table_name"].ToString(),"green","red");
						v_html += PrintTableColumns(v_data1.Rows[v_counter1],v_data_columns1,"green","red");
						v_counter1++;
					}
				}

				while (v_counter2 < v_data2.Rows.Count) {
					System.Collections.Generic.List<string> v_table_info = new System.Collections.Generic.List<string>();

					v_table_info.Add(v_data2.Rows[v_counter2]["table_name"].ToString());
					v_table_info.Add("0");



					v_list_tables.Add(v_table_info);

					v_html += PrintTable(v_data2.Rows[v_counter2]["table_name"].ToString(),"red","green");
					v_html += PrintTableColumns(v_data2.Rows[v_counter2],v_data_columns2,"red","green");
					v_counter2++;
				}

				int v_total_tables = Math.Max(v_data1.Rows.Count,v_data2.Rows.Count);

				v_num_red_tables = v_total_tables - v_num_green_tables - v_num_orange_tables;

				//Console.WriteLine("TABLES -> Greens: " + v_num_green_tables + " - Oranges: " + v_num_orange_tables + " - Reds: " + v_num_red_tables);
				//Console.WriteLine("COLUMNS -> Greens: " + v_num_green_cols + " - Oranges: " + v_num_orange_cols + " - Reds: " + v_num_red_cols);

			}
			catch (Spartacus.Database.Exception e)
			{
				System.Console.WriteLine(e.v_message);
			}

			v_d1.v_html = v_html;
			v_d1.v_log = v_log;
			v_d1.v_num_green_tables = v_num_green_tables;
			v_d1.v_num_orange_tables = v_num_orange_tables;
			v_d1.v_num_red_tables = v_num_red_tables;
			v_d1.v_num_green_cols = v_num_green_cols;
			v_d1.v_num_orange_cols = v_num_orange_cols;
			v_d1.v_num_red_cols = v_num_red_cols;

			//v_g1.v_data = v_d1;
			v_g1.v_data = v_list_tables;


			return v_g1;

		}


	}
}

