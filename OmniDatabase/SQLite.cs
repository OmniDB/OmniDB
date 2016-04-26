/*
Copyright 2016 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

using System;

namespace OmniDatabase
{
	/// <summary>
	/// Class to store information of an SQLite database.
	/// </summary>
	public class SQLite : Generic
	{
		/// <summary>
		/// Initializes a new instance of the <see cref="OmniDB.Database.Oracle"/> class.
		/// </summary>
		/// <param name="p_server">Connection address.</param>
		/// <param name="p_port">Connection port.</param>
		/// <param name="v_database">Database file.</param>
		/// <param name="v_user">Database user.</param>
		/// <param name="v_password">Database password.</param>
		public SQLite (string p_conn_id, string p_database)
			: base ("sqlite",p_conn_id)
		{

			if (p_database.Contains("/")) {

				string []v_strings = p_database.Split ('/');

				v_service = v_strings [v_strings.Length - 1];

			}
			else
				v_service = p_database;

			v_has_schema = false;
			v_schema = "";

			v_has_update_rule = true;
			v_default_string = "varchar(500)";

			v_can_rename_table = true;
			v_rename_table_command = "alter table #p_table_name# rename to #p_new_table_name#";

			v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)";
			v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#";
			v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)";

			v_can_alter_type = false;

			v_can_alter_nullable = false;

			v_can_rename_column = false;

			v_can_add_column = true;
			v_add_column_command = "alter table #p_table_name# add column #p_column_name# #p_data_type# #p_nullable#";

			v_can_drop_column = false;

			v_can_add_constraint = false;

			v_can_drop_constraint = false;

			v_create_index_command = "create index #p_index_name# on #p_table_name# (#p_columns#)";
			v_create_unique_index_command = "create unique index #p_index_name# on #p_table_name# (#p_columns#)";

			v_drop_index_command = "drop index #p_index_name#";

			v_update_rules = new System.Collections.Generic.List<string> ();
			v_delete_rules = new System.Collections.Generic.List<string> ();

			v_delete_rules.Add ("");
			v_delete_rules.Add ("NO ACTION");
			v_delete_rules.Add ("RESTRICT");
			v_delete_rules.Add ("SET NULL");
			v_delete_rules.Add ("SET DEFAULT");
			v_delete_rules.Add ("CASCADE");

			v_update_rules.Add ("");
			v_update_rules.Add ("NO ACTION");
			v_update_rules.Add ("RESTRICT");
			v_update_rules.Add ("SET NULL");
			v_update_rules.Add ("SET DEFAULT");
			v_update_rules.Add ("CASCADE");

			v_trim_function = "trim";

			v_transfer_block_size = new System.Collections.Generic.List<uint> ();
			v_transfer_block_size.Add (50);
			v_transfer_block_size.Add (100);
			v_transfer_block_size.Add (200);
			v_transfer_block_size.Add (400);

			v_connection = new Spartacus.Database.Sqlite (p_database);
			v_connection.v_execute_security = false;

		}

		/// <summary>
		/// Get database name.
		/// </summary>
		public override string GetName() {

			return v_service;

		}

		/// <summary>
		/// Print database info.
		/// </summary>
		public override string PrintDatabaseInfo() {

			return v_service;

		}

		/// <summary>
		/// Print database details.
		/// </summary>
		public override string PrintDatabaseDetails() {

			return "Local File";

		}

		/// <summary>
		/// Create update and delete rules.
		/// </summary>
		/// <param name="p_update_rule">Update Rule.</param>
		/// <param name="p_delete_rule">Delete Rule.</param>
		public override string HandleUpdateDeleteRules(string p_update_rule, string p_delete_rule) {

			string v_rules = "";

			if (p_update_rule.Trim() != "")
				v_rules += " on update " + p_update_rule + " ";
			if (p_delete_rule.Trim() != "")
				v_rules += " on delete " + p_delete_rule + " ";

			return v_rules;

		}

		/// <summary>
		/// Test connection.
		/// </summary>
		public override string TestConnection() {

			string v_return = "";

			try {
				
				if (System.IO.File.Exists(this.v_connection.v_service))
					v_return = "Connection successful.";
				else
					v_return = "File does not exist, if you try to manage this connection a database file will be created.";

			}
			catch (Spartacus.Database.Exception e) {
				
				v_return = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
			
			}

			return v_return;

		}

		/// <summary>
		/// Get a datatable with all tables.
		/// </summary>
		/// <param name="p_all_schemas">If querying all schemas or not.</param>
		public override System.Data.DataTable QueryTables(bool p_all_schemas) {

			return v_connection.Query (
				"select name as table_name " +
				"from sqlite_master        " +
				"where type='table'", "Tables");

		}

		/// <summary>
		/// Get a datatable with all views.
		/// </summary>
		public override System.Data.DataTable QueryViews() {

			//TODO
			return null;

		}

		/// <summary>
		/// Get a datatable with all tables fields.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesFields(string p_table) {

			if (p_table == null) {
				
				System.Data.DataTable v_tables = this.QueryTables (false);

				System.Data.DataTable v_table_columns_all = new System.Data.DataTable ();

				v_table_columns_all.Columns.Add ("column_name");
				v_table_columns_all.Columns.Add ("data_type");
				v_table_columns_all.Columns.Add ("nullable");
				v_table_columns_all.Columns.Add ("data_length");
				v_table_columns_all.Columns.Add ("data_precision");
				v_table_columns_all.Columns.Add ("data_scale");
				v_table_columns_all.Columns.Add ("table_name");

				foreach (System.Data.DataRow v_table in v_tables.Rows) {

					System.Data.DataTable v_table_columns = v_connection.Query ("pragma table_info('" + v_table["table_name"] + "')", "TableFields");

					v_table_columns.Columns ["name"].ColumnName = "column_name";
					v_table_columns.Columns ["type"].ColumnName = "data_type";

					v_table_columns.Columns.Add ("nullable");
					v_table_columns.Columns.Add ("data_length");
					v_table_columns.Columns.Add ("data_precision");
					v_table_columns.Columns.Add ("data_scale");
					v_table_columns.Columns.Add ("table_name");



					foreach (System.Data.DataRow v_column in v_table_columns.Rows) {

						v_column ["table_name"] = v_table ["table_name"];

						if (v_column ["notnull"].ToString () == "1")
							v_column ["nullable"] = "NO";
						else
							v_column ["nullable"] = "YES";

						v_column ["data_type"] = v_column ["data_type"].ToString ().ToLower ();

						string v_type = v_column ["data_type"].ToString();


						if (v_type.Contains ("(")) {

							int v_index = v_type.IndexOf ('(');

							if (v_type.Contains (",")) {

								string v_size = v_type.Substring (v_index + 1, v_type.IndexOf (')') - v_index - 1);

								string[] v_sizes = v_size.Split (',');

								v_column ["data_type"] = v_type.Substring (0, v_index);
								v_column ["data_length"] = "";

								v_column ["data_precision"] = v_sizes [0];
								v_column ["data_scale"] = v_sizes [1];

							} 
							else {

								v_column ["data_type"] = v_type.Substring (0, v_index);
								v_column ["data_length"] = v_type.Substring (v_index + 1, v_type.IndexOf (')') - v_index - 1);

								v_column ["data_precision"] = "";
								v_column ["data_scale"] = "";

							}
						}
						else
							v_column ["data_length"] = "";
						
					}

					v_table_columns.Columns.Remove ("notnull");
					v_table_columns.Columns.Remove ("dflt_value");
					v_table_columns.Columns.Remove ("pk");

					v_table_columns_all.Merge (v_table_columns);

				}

				return v_table_columns_all;

			} 
			else {

				System.Data.DataTable v_table_columns = v_connection.Query ("pragma table_info('" + p_table + "')", "TableFields");

				v_table_columns.Columns ["name"].ColumnName = "column_name";
				v_table_columns.Columns ["type"].ColumnName = "data_type";

				v_table_columns.Columns.Add ("nullable");
				v_table_columns.Columns.Add ("data_length");
				v_table_columns.Columns.Add ("data_precision");
				v_table_columns.Columns.Add ("data_scale");
				v_table_columns.Columns.Add ("table_name");

				foreach (System.Data.DataRow v_column in v_table_columns.Rows) {

					v_column ["table_name"] = p_table;

					if (v_column ["notnull"].ToString () == "1")
						v_column ["nullable"] = "NO";
					else
						v_column ["nullable"] = "YES";

					v_column ["data_type"] = v_column ["data_type"].ToString ().ToLower ();

					string v_type = v_column ["data_type"].ToString();

					if (v_type.Contains ("(")) {

						int v_index = v_type.IndexOf ('(');

						if (v_type.Contains (",")) {

							string v_size = v_type.Substring (v_index + 1, v_type.IndexOf (')') - v_index - 1);

							string[] v_sizes = v_size.Split (',');

							v_column ["data_type"] = v_type.Substring (0, v_index);
							v_column ["data_length"] = "";

							v_column ["data_precision"] = v_sizes [0];
							v_column ["data_scale"] = v_sizes [1];

						} 
						else {

							v_column ["data_type"] = v_type.Substring (0, v_index);
							v_column ["data_length"] = v_type.Substring (v_index + 1, v_type.IndexOf (')') - v_index - 1);

							v_column ["data_precision"] = "";
							v_column ["data_scale"] = "";

						}
					}
					else
						v_column ["data_length"] = "";
					
				}

				v_table_columns.Columns.Remove ("notnull");
				v_table_columns.Columns.Remove ("dflt_value");
				v_table_columns.Columns.Remove ("pk");

				return v_table_columns;

			}

		}

		/// <summary>
		/// Get a datatable with all tables foreign keys.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesForeignKeys(string p_table) {

			if (p_table == null) {

				System.Data.DataTable v_all_fks = new System.Data.DataTable();
				v_all_fks.Columns.Add ("r_table_name");
				v_all_fks.Columns.Add ("table_name");
				v_all_fks.Columns.Add ("r_column_name");
				v_all_fks.Columns.Add ("column_name");
				v_all_fks.Columns.Add ("constraint_name");
				v_all_fks.Columns.Add ("update_rule");
				v_all_fks.Columns.Add ("delete_rule");

				System.Data.DataTable v_tables = v_connection.Query ("select name as table_name " +
					"from sqlite_master " +
					"where type='table'", "Tables");

				foreach (System.Data.DataRow v_table in v_tables.Rows) {
					
					System.Data.DataTable v_fks = v_connection.Query ("PRAGMA foreign_key_list('" + v_table["table_name"].ToString() + "')","ForeignKeys");

					if (v_fks.Rows.Count > 0) {
						
						v_fks.Columns ["table"].ColumnName = "r_table_name";
						v_fks.Columns ["from"].ColumnName = "column_name";
						v_fks.Columns ["to"].ColumnName = "r_column_name";
						v_fks.Columns ["id"].ColumnName = "constraint_name";
						v_fks.Columns ["on_update"].ColumnName = "update_rule";
						v_fks.Columns ["on_delete"].ColumnName = "delete_rule";
						v_fks.Columns.Remove ("seq");
						v_fks.Columns.Remove ("match");
						v_fks.Columns.Add ("table_name");

						foreach (System.Data.DataRow v_fk in v_fks.Rows) {
							
							v_fk ["table_name"] = v_table ["table_name"].ToString ();
							v_fk ["constraint_name"] = v_table ["table_name"].ToString () + "_fk_" + v_fk ["constraint_name"];

						}

						if (v_all_fks.Columns.Count == 0)
							v_all_fks = v_fks;
						else
							v_all_fks.Merge (v_fks);

					}

				}

				return v_all_fks;

			} 
			else {

				System.Data.DataTable v_fks = v_connection.Query ("PRAGMA foreign_key_list('" + p_table + "')","ForeignKeys");

				if (v_fks.Rows.Count > 0) {
					
					v_fks.Columns ["table"].ColumnName = "r_table_name";
					v_fks.Columns ["from"].ColumnName = "column_name";
					v_fks.Columns ["to"].ColumnName = "r_column_name";
					v_fks.Columns ["id"].ColumnName = "constraint_name";
					v_fks.Columns ["on_update"].ColumnName = "update_rule";
					v_fks.Columns ["on_delete"].ColumnName = "delete_rule";
					v_fks.Columns.Remove ("seq");
					v_fks.Columns.Remove ("match");
					v_fks.Columns.Add ("table_name");

					foreach (System.Data.DataRow v_fk in v_fks.Rows) {
						
						v_fk ["table_name"] = p_table;
						v_fk ["constraint_name"] = p_table + "_fk_" + v_fk ["constraint_name"];
					
					}

				}

				return v_fks;

			}

		}

		/// <summary>
		/// Get a datatable with all tables primary keys.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesPrimaryKeys(string p_schema, string p_table) {

			if (p_table == null) {

				System.Data.DataTable v_all_pks = new System.Data.DataTable();
				v_all_pks.Columns.Add ("constraint_name");
				v_all_pks.Columns.Add ("column_name");
				v_all_pks.Columns.Add ("table_name");

				System.Data.DataTable v_tables = v_connection.Query (
					"select name as table_name " +
					"from sqlite_master        " +
					"where type='table'", "Tables");


				foreach (System.Data.DataRow v_table in v_tables.Rows) {
					
					System.Data.DataTable v_cols = v_connection.Query ("PRAGMA table_info('" + v_table["table_name"].ToString() + "')","PrimaryKey");

					foreach (System.Data.DataRow v_col in v_cols.Rows) {

						if (v_col["pk"].ToString()!="0") {
							
							System.Data.DataRow v_row = v_all_pks.NewRow ();
							v_row ["constraint_name"] = "pk_" + v_table["table_name"].ToString();
							v_row ["column_name"] = v_col["name"];
							v_row ["table_name"] = v_table["table_name"].ToString();
							v_all_pks.Rows.Add (v_row);
						
						}
					
					}

				}

				return v_all_pks;

			} 
			else {

				System.Data.DataTable v_cols = v_connection.Query ("PRAGMA table_info('" + p_table + "')","PrimaryKey");

				System.Data.DataTable v_pk = new System.Data.DataTable ();
				v_pk.Columns.Add ("constraint_name");
				v_pk.Columns.Add ("column_name");
				v_pk.Columns.Add ("table_name");

				foreach (System.Data.DataRow v_col in v_cols.Rows) {

					if (v_col["pk"].ToString()!="0") {
						
						System.Data.DataRow v_row = v_pk.NewRow ();
						v_row ["constraint_name"] = "pk_" + p_table;
						v_row ["column_name"] = v_col["name"];
						v_row ["table_name"] = p_table;
						v_pk.Rows.Add (v_row);

					}

				}

				return v_pk;

			}

		}

		/// <summary>
		/// Get a datatable with all tables unique constraints.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesUniques(string p_schema, string p_table) {

            System.Data.DataTable v_ret = null, v_tables = null;
            System.Data.DataRow v_row;

			v_ret = new System.Data.DataTable ("TableIndexes");
			v_ret.Columns.Add ("table_name");
			v_ret.Columns.Add ("constraint_name");
			v_ret.Columns.Add ("column_name");

            if (p_table != null)
                v_tables = this.v_connection.Query("select name,sql from sqlite_master where type = 'table' and name = '" + p_table + "'", "TableIndexesTables");
            else
                v_tables = this.v_connection.Query("select name,sql from sqlite_master where type = 'table'", "TableIndexesTables");

            if (v_tables != null && v_tables.Rows.Count > 0) {
				
                foreach (System.Data.DataRow t in v_tables.Rows) {

					string v_sql = t ["sql"].ToString ().ToLower ().Trim();

					if (v_sql.Contains ("unique")) {

						int v_index = v_sql.IndexOf ("(") + 1;
						string v_filtered_sql = v_sql.Substring (v_index,v_sql.Length-(v_index+1));

						string v_formated = System.Text.RegularExpressions.Regex.Replace (v_filtered_sql, @"\s+", " ");

						// Replacing commands by dots when inside parentesis
						int v_level = 0;

						System.Text.StringBuilder v_sb = new System.Text.StringBuilder(v_formated);

						for (int i = 0; i < v_formated.Length; i++) {

							if (v_formated [i] == '(')
								v_level++;
							else if (v_formated [i] == ')')
								v_level--;
							else if (v_formated [i] == ',' && v_level != 0)
								v_sb [i] = '.';

						}

						v_formated = v_sb.ToString ();

						string[] v_commands = v_formated.Split (',');

						int v_unique_count = 0;

						foreach (string v_command in v_commands) {
							
							if (v_command.Contains("unique")) {

								string v_formatted_command = v_command.Trim ();

								if (v_formatted_command [v_formatted_command.Length - 1] != ')') {

									v_row = v_ret.NewRow ();

									v_row ["table_name"] = t["name"].ToString();
									v_row ["constraint_name"] = "unique_" + v_unique_count;
									v_row ["column_name"] = v_formatted_command.Split (' ') [0];

									v_ret.Rows.Add (v_row);

								} 
								else {
									
									v_index = v_formatted_command.IndexOf ("(") + 1;

									string v_columns_string = v_formatted_command.Substring (v_index,v_formatted_command.Length-(v_index+1));

									string[] v_cols = v_columns_string.Split ('.');

									foreach (string v_col in v_cols) {

										v_row = v_ret.NewRow ();

										v_row ["table_name"] = p_table;
										v_row ["constraint_name"] = "unique_" + v_unique_count;
										v_row ["column_name"] = v_col.Trim();

										v_ret.Rows.Add (v_row);

									}

								}
									
								v_unique_count++;

							}

						}

					}

                }

            }

            return v_ret;

		}

		/// <summary>
		/// Get a datatable with all tables indexes.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesIndexes(string p_table) {

            System.Data.DataTable v_ret = null, v_tables = null, v_indexes = null, v_columns = null;
            System.Data.DataRow v_row;

			v_ret = new System.Data.DataTable("TableIndexes");
			v_ret.Columns.Add("table_name");
			v_ret.Columns.Add("index_name");
			v_ret.Columns.Add("column_name");
			v_ret.Columns.Add("uniqueness");

            if (p_table != null)
                v_tables = this.v_connection.Query("select name from sqlite_master where type = 'table' and name = '" + p_table + "'", "TableIndexesTables");
            else
                v_tables = this.v_connection.Query("select name from sqlite_master where type = 'table'", "TableIndexesTables");

            if (v_tables != null && v_tables.Rows.Count > 0) {
				
                foreach (System.Data.DataRow t in v_tables.Rows) {
					
                    v_indexes = this.v_connection.Query("pragma index_list('" + t["name"].ToString() + "')", "TableIndexesIndexes");

                    if (v_indexes != null && v_indexes.Rows.Count > 0) {
						
                        foreach (System.Data.DataRow i in v_indexes.Rows) {
							
                            v_columns = this.v_connection.Query("pragma index_info('" + i["name"].ToString() +"')", "TableIndexesColumns");

                            if (v_columns != null && v_columns.Rows.Count > 0) {
								
                                foreach (System.Data.DataRow c in v_columns.Rows) {
									
                                    v_row = v_ret.NewRow();

                                    v_row["table_name"] = t["name"];
                                    v_row["index_name"] = i["name"];
                                    v_row["column_name"] = c["name"];
                                    if (i["unique"].ToString() == "1")
                                        v_row["uniqueness"] = "Unique";
                                    else
                                        v_row["uniqueness"] = "Non Unique";

                                    v_ret.Rows.Add(v_row);

                                }

                            }

                        }

                    }

                }

            }

            return v_ret;

		}

		/// <summary>
		/// Query limited number of records.
		/// </summary>
		/// <param name="p_query">Query string.</param>
		/// <param name="p_count">Max number of records.</param>
		public override System.Data.DataTable QueryDataLimited(string p_query, int p_count) {

			string v_filter = "";
			if (p_count != -1)
				v_filter = " limit  " + p_count;

			return v_connection.Query (
				"select *                 " +
				"from ( " + p_query + " ) " +
				v_filter, "Limited Query");

		}

		/// <summary>
		/// Query limited number of records.
		/// </summary>
		/// <param name="p_column_list">List of columns separated by comma.</param> 
		/// <param name="p_table">Table name.</param>
		/// <param name="p_filter">Query filter.</param>
		/// <param name="p_count">Max number of records.</param>
		public override System.Data.DataTable QueryTableRecords(string p_column_list, string p_table, string p_filter, int p_count) {

			string v_limit = "";
			if (p_count != -1)
				v_limit = " limit  " + p_count;

			return v_connection.Query (
				"select " + p_column_list + " " +
				"from " + p_table + "  t      " +
				p_filter + "                  " +
				v_limit, "Limited Query");

		}

	}
}