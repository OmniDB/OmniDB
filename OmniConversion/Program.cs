/*
Copyright 2016 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

using System;
using Spartacus;
using System.Data;

namespace TaskConversion
{
	/// <summary>
	/// Strucute to keep track of conversion progress.
	/// </summary>
	public class ConversionProgress {
		public double v_total_progress;
		public double v_table_progress;
		public uint v_total_records;
		public uint v_transf_records;
		public uint v_curr_transf_records;
		public string v_curr_table;
		public int v_mode;
		public DateTime v_old_time;
		public DateTime v_new_time;
	}

	/// <summary>
	/// Structure to store command data.
	/// </summary>
	public class Command {
		public string v_table_name;
		public string v_command;
	}

	/// <summary>
	/// Structure to store transfer data info.
	/// </summary>
	public class TransferCommand {
		public string v_table_name;
		public string v_full_table_name;
		public string v_select;
		public string v_total_records;
		public Spartacus.Database.Command v_insert;
	}

	class MainClass
	{
		public static void Main (string[] args)
		{

			System.Threading.Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo ("pt-BR");

			if (System.IO.File.Exists ("log/conv_" + args[0] + ".txt"))
				System.IO.File.Delete ("log/conv_" + args[0] + ".txt");

			// Log file
			System.IO.TextWriter v_tw;
			string v_path = "log/conv_" + args[0] + ".txt";
			if (!System.IO.File.Exists(v_path))
			{
				v_tw = new System.IO.StreamWriter(v_path);
			}
			else
			{
				v_tw = new System.IO.StreamWriter(v_path,true);
			}

			// Instantiating tool management database.
			OmniDatabase.Generic v_omnidb_database = OmniDatabase.Generic.InstantiateDatabase ("","0",
				"sqlite",
				"",
				"",
				"databases/tool_database",
				"",
				"",
				"");

			v_omnidb_database.v_connection.SetTimeout (10);

			DateTime v_start = DateTime.Now;
			DateTime v_begin = DateTime.Now;
			v_tw.WriteLine(v_begin + " - Starting conversion.\n");
			v_tw.Flush ();

			ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_ch_status = 'E', conv_st_start = '" + v_begin.ToString() + "' where conv_id = " + args[0]);

			DataTable v_conversion           = v_omnidb_database.v_connection.Query ("select * from conversions where conv_id = " + args[0], "Conversion Tables");
			DataTable v_src_db_data         = v_omnidb_database.v_connection.Query ("select * from connections where conn_id = " + v_conversion.Rows[0]["conn_id_src"].ToString(), "Source Connection");
			DataTable v_dst_db_data         = v_omnidb_database.v_connection.Query ("select * from connections where conn_id = " + v_conversion.Rows[0]["conn_id_dst"].ToString(), "Target Connection");

			Spartacus.Utils.Cryptor v_cryptor = new Spartacus.Utils.Cryptor ("omnidb_spartacus");

			// Instantiating source database
			OmniDatabase.Generic v_src_database = OmniDatabase.Generic.InstantiateDatabase ("",v_src_db_data.Rows[0] ["conn_id"].ToString (),
				v_src_db_data.Rows[0] ["dbt_st_name"].ToString (),
				v_cryptor.Decrypt(v_src_db_data.Rows[0] ["server"].ToString ()),
				v_cryptor.Decrypt(v_src_db_data.Rows[0] ["port"].ToString ()),
				v_cryptor.Decrypt(v_src_db_data.Rows[0] ["service"].ToString ()),
				v_cryptor.Decrypt(v_src_db_data.Rows[0] ["user"].ToString ()),
				v_cryptor.Decrypt(v_src_db_data.Rows[0] ["password"].ToString ()),
				v_cryptor.Decrypt(v_src_db_data.Rows[0] ["schema"].ToString ()));


			v_src_database.v_connection.SetTimeout (0);
			v_src_database.v_connection.SetExecuteSecurity(false);

			// Instantiating target database
			OmniDatabase.Generic v_dst_database = OmniDatabase.Generic.InstantiateDatabase ("",v_dst_db_data.Rows[0] ["conn_id"].ToString (),
				v_dst_db_data.Rows[0] ["dbt_st_name"].ToString (),
				v_cryptor.Decrypt(v_dst_db_data.Rows[0] ["server"].ToString ()),
				v_cryptor.Decrypt(v_dst_db_data.Rows[0] ["port"].ToString ()),
				v_cryptor.Decrypt(v_dst_db_data.Rows[0] ["service"].ToString ()),
				v_cryptor.Decrypt(v_dst_db_data.Rows[0] ["user"].ToString ()),
				v_cryptor.Decrypt(v_dst_db_data.Rows[0] ["password"].ToString ()),
				v_cryptor.Decrypt(v_dst_db_data.Rows[0] ["schema"].ToString ()));

			v_dst_database.v_connection.SetExecuteSecurity(false);

			// Querying conversion data for current conversion
			DataTable v_conv_pk = null, v_conv_fk = null, v_conv_uq = null, v_conv_idx = null, v_conv_tables = null;
			string v_tables_filter = null, v_pk_filter = null, v_fk_filter = null, v_uq_filter = null, v_idx_filter = null;

			if (v_dst_database.v_can_add_constraint) {

				v_conv_pk = v_omnidb_database.v_connection.Query ("select * from conv_tables_data where conv_id = " + args [0] + " and (ctd_ch_createpk<>'N') order by ctd_st_table asc", "Conversion Tables");
				v_conv_fk = v_omnidb_database.v_connection.Query ("select * from conv_tables_data where conv_id = " + args [0] + " and (ctd_ch_createfk<>'N') order by ctd_st_table asc", "Conversion Tables");
				v_conv_uq = v_omnidb_database.v_connection.Query ("select * from conv_tables_data where conv_id = " + args [0] + " and (ctd_ch_createuq<>'N') order by ctd_st_table asc", "Conversion Tables");
				v_conv_idx = v_omnidb_database.v_connection.Query ("select * from conv_tables_data where conv_id = " + args [0] + " and (ctd_ch_createidx<>'N') order by ctd_st_table asc", "Conversion Tables");

				// Creating desired tables filter
				v_pk_filter = CreateFilter(v_conv_pk);

				// Creating desired tables filter
				v_fk_filter = CreateFilter(v_conv_fk);

				// Creating desired tables filter
				v_uq_filter = CreateFilter(v_conv_uq);

				// Creating desired tables filter
				v_idx_filter = CreateFilter(v_conv_idx);

			}


			v_conv_tables = v_omnidb_database.v_connection.Query ("select * from conv_tables_data where conv_id = " + args[0] + " and (ctd_ch_createtable<>'N' or ctd_ch_transferdata<>'N') order by ctd_st_table asc", "Conversion Tables");

			// Creating desired tables filter
			v_tables_filter = CreateFilter(v_conv_tables);



			v_dst_database.v_connection.SetTimeout (0);


			DataTable v_columns = null, v_table_counts = null, v_primary_keys = null, v_foreign_keys = null, v_uniques = null, v_indexes = null, v_unique_types = null, v_representatives = null;

			try {

				if (v_conv_tables.Rows.Count > 0) {

					// Retrieving columns for desired tables
					v_columns = v_src_database.QueryTablesFields (null);

					RemoveUnwantedRows (v_columns, v_tables_filter);

					v_columns = SortByTableName (v_columns);

					System.Collections.Generic.List<string> v_table_list  = new System.Collections.Generic.List<string>();
					System.Collections.Generic.List<string> v_filter_list = new System.Collections.Generic.List<string>();

					for (int i =0; i < v_conv_tables.Rows.Count; i++) {
						v_table_list.Add(v_conv_tables.Rows[i]["ctd_st_table"].ToString());
						v_filter_list.Add(v_conv_tables.Rows[i]["ctd_st_transferfilter"].ToString());
					}

					// Retrieving tables register count
					v_table_counts = v_src_database.CountTablesRecords (v_table_list,v_filter_list);
					v_table_counts.Columns.Add ("drop_records");
					v_table_counts.Columns.Add ("create_table");
					v_table_counts.Columns.Add ("transfer_data");
					v_table_counts.Columns.Add ("transfer_filter");
					RemoveUnwantedRows (v_table_counts, v_tables_filter);
					AssingConversionTables (v_table_counts, v_conv_tables);
					v_table_counts = SortByTableName (v_table_counts);

					// Creating indexes to columns datatable at tables datatable
					v_table_counts.Columns.Add ("position");
					v_table_counts.Columns.Add ("num_columns");
					SetupTablesDatatable (v_columns, v_table_counts);
					v_tw.WriteLine("Column Indexing Done.");
					v_tw.Flush ();

					// Retrieving unique data types from source database
					v_unique_types = GetUniqueDataTypes (v_columns);

					// Retrieving representatives
					v_representatives = GetRepresentatives (v_omnidb_database, v_unique_types, v_src_database.v_db_type, v_dst_database.v_db_type);

					// Printing data type mapping
					v_tw.WriteLine("*** DATA TYPE MAPPING ***\n");

					v_tw.Flush ();

					System.Data.DataTable v_rep_clone = v_representatives.Copy ();

					int v_max_dt_length = 16;
					int v_max_cat_length = 8;
					int v_max_tdt_length = 15;

					foreach (DataRow v_rep in v_rep_clone.Rows) {
						string v_src_type = v_rep ["src_dt_type"].ToString ();

						if (v_rep ["cat_st_name"].ToString () == "")
							v_rep ["cat_st_name"] = "NO CATEGORY";

						if (v_rep ["dst_dt_type"].ToString () == "")
							v_rep ["dst_dt_type"] = "DEFAULT";

						if (v_src_type.Length > v_max_dt_length)
							v_max_dt_length = v_src_type.Length;

						if (v_rep ["cat_st_name"].ToString().Length > v_max_cat_length)
							v_max_cat_length = v_rep ["cat_st_name"].ToString().Length;

						if (v_rep ["dst_dt_type"].ToString ().Length > v_max_tdt_length)
							v_max_tdt_length = v_rep ["dst_dt_type"].ToString ().Length;

					}

					v_tw.WriteLine("{0," + v_max_dt_length + "} - {1," + v_max_cat_length + "} - {2," + v_max_tdt_length + "}","SOURCE DATA TYPE","CATEGORY","TARGET DATATYPE\n");

					foreach (DataRow v_rep in v_rep_clone.Rows) {
						v_tw.WriteLine("{0," + v_max_dt_length + "} - {1," + v_max_cat_length + "} - {2," + v_max_tdt_length + "}",v_rep ["src_dt_type"].ToString (),v_rep ["cat_st_name"].ToString(),v_rep ["dst_dt_type"].ToString ());
					}

					v_tw.WriteLine("\n");
					v_tw.Flush ();

					// Assigning each column to the correct representative
					v_columns.Columns.Add ("rep_index");
					AssignRepresentatives (v_columns, v_representatives);
				}

				if (v_conv_pk!=null && v_conv_pk.Rows.Count > 0) {

					// Retrieving desired primary keys
					v_primary_keys = v_src_database.QueryTablesPrimaryKeys ("", null);
					RemoveUnwantedRows (v_primary_keys, v_pk_filter);
					v_primary_keys = SortByTableName (v_primary_keys);

				}

				if (v_conv_fk!=null && v_conv_fk.Rows.Count > 0) {

					// Retrieving desired primary keys
					v_foreign_keys = v_src_database.QueryTablesForeignKeys (null);
					RemoveUnwantedRows (v_foreign_keys, v_fk_filter);
					v_foreign_keys = SortByTableName (v_foreign_keys);

				}

				if (v_conv_uq!=null && v_conv_uq.Rows.Count > 0) {

					// Retrieving desired primary keys
					v_uniques = v_src_database.QueryTablesUniques ("", null);
					RemoveUnwantedRows (v_uniques, v_uq_filter);
					v_uniques = SortByTableName (v_uniques);

				}

				if (v_conv_idx!=null && v_conv_idx.Rows.Count > 0) {

					// Retrieving desired primary keys
					v_indexes = v_src_database.QueryTablesIndexes (null);
					RemoveUnwantedRows (v_indexes, v_idx_filter);
					v_indexes = SortByTableName (v_indexes);

				}

			}
			catch (Spartacus.Database.Exception e) {
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_ch_status='X' where conv_id = " + args[0]);
				v_tw.WriteLine("*** SOURCE DATABASE DATA RETRIEVAL ERROR ***");
				v_tw.WriteLine("Error:\n");
				v_tw.WriteLine(e.v_message + "\n");
				v_tw.Flush ();
				return;
			}
			catch (System.InvalidOperationException e) {
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_ch_status='X' where conv_id = " + args[0]);
				v_tw.WriteLine("*** SOURCE DATABASE DATA RETRIEVAL ERROR ***");
				v_tw.WriteLine("Error:\n");
				v_tw.WriteLine(e.Message + "\n");
				v_tw.Flush ();
				return;
			}

			v_begin = DateTime.Now;
			v_tw.WriteLine(v_begin + " - Initial Setup Done.");
			v_tw.WriteLine(v_begin + " - Creating Conversion Commands...");
			v_tw.Flush ();

			System.Collections.Generic.List<Command> v_delete_commands = new System.Collections.Generic.List<Command> ();
			System.Collections.Generic.List<Command> v_create_commands = new System.Collections.Generic.List<Command> ();
			System.Collections.Generic.List<TransferCommand> v_transfer_commands = new System.Collections.Generic.List<TransferCommand> ();
			System.Collections.Generic.List<Command> v_pk_commands = new System.Collections.Generic.List<Command> ();
			System.Collections.Generic.List<Command> v_fk_commands = new System.Collections.Generic.List<Command> ();
			System.Collections.Generic.List<Command> v_uq_commands = new System.Collections.Generic.List<Command> ();
			System.Collections.Generic.List<Command> v_idx_commands = new System.Collections.Generic.List<Command> ();

			if (v_table_counts != null) {
				// Iterate through all tables
				foreach (DataRow v_table in v_table_counts.Rows) {

					int v_first_col_index = Convert.ToInt32 (v_table ["position"]);
					int v_last_col_index = v_first_col_index + Convert.ToInt32 (v_table ["num_columns"]);

					bool v_first_column = true;
					string v_select_command = "select ";

					string v_full_table_name_dst = "";

					if (v_dst_database.v_has_schema)
						v_full_table_name_dst = v_dst_database.v_schema + "." + v_table ["table_name"];
					else
						v_full_table_name_dst = v_table ["table_name"].ToString ();

					string v_full_table_name_src = "";

					if (v_src_database.v_has_schema)
						v_full_table_name_src = v_src_database.v_schema + "." + v_table ["table_name"];
					else
						v_full_table_name_src = v_table ["table_name"].ToString ();

					string v_table_name = v_table ["table_name"].ToString ();

					string v_delete_command = "delete from " + v_full_table_name_dst;
					string v_create_command = "create table " + v_full_table_name_dst + " ( ";
					Spartacus.Database.Command v_insert_command = new Spartacus.Database.Command ();
					v_insert_command.v_text = "( ";

					// Iterate through all columns from current table
					for (int i = v_first_col_index; i < v_last_col_index; i++) {

						int v_rep_index = Convert.ToInt32 (v_columns.Rows [i] ["rep_index"]);

						if (!v_first_column) {
							v_create_command += ", ";
							v_insert_command.v_text += ", ";
							v_select_command += ", ";
						}
						v_first_column = false;

						string v_precision = v_columns.Rows [i] ["data_precision"].ToString ();
						string v_scale = v_columns.Rows [i] ["data_scale"].ToString ();
						string v_length = v_columns.Rows [i] ["data_length"].ToString ();
						string v_null;
						if (v_columns.Rows [i] ["nullable"].ToString () == "YES")
							v_null = "";
						else
							v_null = " not null";

						string v_new_type = "";

						string v_category = v_representatives.Rows [v_rep_index] ["cat_st_name"].ToString ();

						if (v_category != "") {

							if (v_representatives.Rows [v_rep_index] ["dst_dt_in_sufix"].ToString () == "2") {
								if (v_precision == "" || v_scale == "")
									v_new_type = v_representatives.Rows [v_rep_index] ["rep_st_default"].ToString ();
								else
									v_new_type = v_representatives.Rows [v_rep_index] ["dst_dt_type"].ToString () + "(" + v_precision + "," + v_scale + ")";

							} 
							else if (v_representatives.Rows [v_rep_index] ["dst_dt_in_sufix"].ToString () == "1") {
								if (v_length == "")
									v_new_type = v_representatives.Rows [v_rep_index] ["rep_st_default"].ToString ();
								else
									v_new_type = v_representatives.Rows [v_rep_index] ["dst_dt_type"].ToString () + "(" + v_length + ")";

							} 
							else {
								v_new_type = v_representatives.Rows [v_rep_index] ["dst_dt_type"].ToString ();

							}

						}
						else
							v_new_type = v_dst_database.v_default_string;


						v_create_command += v_columns.Rows [i] ["column_name"] + " " + v_new_type + v_null;

						// Add column using the readformat from specific datatype
						v_select_command += v_representatives.Rows [v_rep_index] ["dt_st_readformat"].ToString ().Replace ("#", v_columns.Rows [i] ["column_name"].ToString ());

						// Add column using the writeformat from specific datatype
						v_insert_command.v_text += "#" + v_columns.Rows [i] ["column_name"].ToString ().ToLower() + "#";

						if (v_category == "integer" || v_category == "smallint" || v_category == "bigint")
							v_insert_command.AddParameter (v_columns.Rows [i] ["column_name"].ToString ().ToLower (), Spartacus.Database.Type.INTEGER);
						else if (v_category == "fp" || v_category == "decimal")
							v_insert_command.AddParameter (v_columns.Rows [i] ["column_name"].ToString ().ToLower (), Spartacus.Database.Type.REAL);
						else if (v_category == "datetime" || v_category == "time" || v_category == "date")
							v_insert_command.AddParameter (v_columns.Rows [i] ["column_name"].ToString ().ToLower (), Spartacus.Database.Type.DATE,v_representatives.Rows [v_rep_index] ["dt_st_writeformat"].ToString ());
						else
							v_insert_command.AddParameter (v_columns.Rows [i] ["column_name"].ToString ().ToLower (), Spartacus.Database.Type.QUOTEDSTRING);

						v_insert_command.v_parameters [v_insert_command.v_parameters.Count - 1].v_locale = Spartacus.Database.Locale.EUROPEAN;

					}

					v_create_command += " ) ";
					v_select_command += " from " + v_full_table_name_src + " " + v_table["transfer_filter"].ToString();
					v_insert_command.v_text += " ) ";

					// If table is set to be created, create command
					if (v_table ["drop_records"].ToString () != "N") {
						Command v_command = new Command ();
						v_command.v_command = v_delete_command;
						v_command.v_table_name = v_table_name;

						v_delete_commands.Add (v_command);
					}

					// If table is set to be created, create command
					if (v_table ["create_table"].ToString () != "N") {
						Command v_command = new Command ();
						v_command.v_command = v_create_command;
						v_command.v_table_name = v_table_name;

						v_create_commands.Add (v_command);
					}

					// If table is set to transfer data, create command
					if (v_table ["transfer_data"].ToString () != "N") {


						TransferCommand v_command = new TransferCommand ();
						v_command.v_select = v_select_command;
						v_command.v_insert = v_insert_command;
						v_command.v_table_name = v_table_name;
						v_command.v_full_table_name = v_full_table_name_dst;
						v_command.v_total_records = v_table ["total"].ToString ();

						v_transfer_commands.Add (v_command);
					}
				}
			}



			if (v_primary_keys != null) {

				string v_curr_table = "";
				string v_curr_constraint = "";
				string v_pk_columns = "";

				bool v_first_column = true;

				foreach (DataRow v_constraint in v_primary_keys.Rows) {

					if (v_curr_table != "" && v_curr_table != v_constraint ["table_name"].ToString()) {

						string v_full_table_name = "";
						if (v_dst_database.v_has_schema)
							v_full_table_name = v_dst_database.v_schema + "." + v_curr_table;
						else
							v_full_table_name = v_curr_table;

						Command v_command = new Command ();
						v_command.v_command = v_dst_database.v_add_pk_command.Replace("#p_table_name#",v_full_table_name).Replace("#p_constraint_name#",v_curr_constraint).Replace("#p_columns#",v_pk_columns);
						v_command.v_table_name = v_curr_table;
						v_pk_columns = "";
						v_first_column = true;

						v_pk_commands.Add (v_command);
					}

					if (!v_first_column)
						v_pk_columns += ", ";

					v_pk_columns += v_constraint ["column_name"];

					v_first_column = false;

					v_curr_constraint = v_constraint ["constraint_name"].ToString ();
					v_curr_table 	  = v_constraint ["table_name"].ToString ();

				}

				if (v_pk_columns != "") {

					string v_full_table_name = "";
					if (v_dst_database.v_has_schema)
						v_full_table_name = v_dst_database.v_schema + "." + v_curr_table;
					else
						v_full_table_name = v_curr_table;

					Command v_command = new Command ();
					v_command.v_command = v_dst_database.v_add_pk_command.Replace("#p_table_name#",v_full_table_name).Replace("#p_constraint_name#",v_curr_constraint).Replace("#p_columns#",v_pk_columns);
					v_command.v_table_name = v_curr_table;
					v_pk_columns = "";
					v_first_column = true;

					v_pk_commands.Add (v_command);
				}
			}

			if (v_uniques != null) {

				string v_curr_table = "";
				string v_curr_unique = "";
				string v_unique_columns = "";

				bool v_first_column = true;

				int v_count = 0;

				foreach (DataRow v_constraint in v_uniques.Rows) {

					if ((v_curr_table != "" && v_curr_table != v_constraint ["table_name"].ToString()) || (v_curr_unique != "" && v_curr_unique != v_constraint ["constraint_name"].ToString())) {

						string v_full_table_name = "";
						if (v_dst_database.v_has_schema)
							v_full_table_name = v_dst_database.v_schema + "." + v_curr_table;
						else
							v_full_table_name = v_curr_table;

						Command v_command = new Command ();
						v_command.v_command = v_dst_database.v_add_unique_command.Replace("#p_table_name#",v_full_table_name).Replace("#p_constraint_name#",v_curr_unique).Replace("#p_columns#",v_unique_columns);
						v_command.v_table_name = v_curr_table;
						v_unique_columns = "";
						v_first_column = true;

						v_count++;

						v_uq_commands.Add (v_command);
					}

					if (!v_first_column)
						v_unique_columns += ", ";

					v_unique_columns += v_constraint ["column_name"];

					v_first_column = false;

					v_curr_unique	  = v_constraint ["constraint_name"].ToString ();
					v_curr_table 	  = v_constraint ["table_name"].ToString ();

				}

				if (v_unique_columns != "") {

					string v_full_table_name = "";
					if (v_dst_database.v_has_schema)
						v_full_table_name = v_dst_database.v_schema + "." + v_curr_table;
					else
						v_full_table_name = v_curr_table;

					Command v_command = new Command ();
					v_command.v_command = v_dst_database.v_add_unique_command.Replace("#p_table_name#",v_full_table_name).Replace("#p_constraint_name#",v_curr_unique).Replace("#p_columns#",v_unique_columns);
					v_command.v_table_name = v_curr_table;
					v_unique_columns = "";
					v_first_column = true;

					v_uq_commands.Add (v_command);
				}
			}

			if (v_foreign_keys != null) {

				string v_curr_table = "";
				string v_curr_r_table = "";
				string v_curr_update_rule = "";
				string v_curr_delete_rule = "";
				string v_curr_fk = "";
				string v_fk_columns = "";
				string v_fk_r_columns = "";

				bool v_first_column = true;

				int v_count = 0;

				foreach (DataRow v_constraint in v_foreign_keys.Rows) {

					if ((v_curr_table != "" && v_curr_table != v_constraint ["table_name"].ToString()) || (v_curr_fk != "" && v_curr_fk != v_constraint ["constraint_name"].ToString())) {

						string v_full_table_name = "";
						string v_full_r_table_name = "";
						if (v_dst_database.v_has_schema) {
							v_full_table_name = v_dst_database.v_schema + "." + v_curr_table;
							v_full_r_table_name = v_dst_database.v_schema + "." + v_curr_r_table;
						}  
						else {
							v_full_table_name = v_curr_table;
							v_full_r_table_name = v_curr_r_table;
						}

						Command v_command = new Command ();
						v_command.v_command = v_dst_database.v_add_fk_command.Replace("#p_table_name#",v_full_table_name).Replace("#p_r_table_name#",v_full_r_table_name).Replace("#p_constraint_name#",v_curr_fk).Replace("#p_columns#",v_fk_columns).Replace("#p_r_columns#",v_fk_r_columns).Replace ("#p_delete_update_rules#", v_dst_database.HandleUpdateDeleteRules(v_curr_update_rule,v_curr_delete_rule));
						v_command.v_table_name = v_curr_table;
						v_fk_columns = "";
						v_fk_r_columns = "";
						v_first_column = true;

						v_count++;

						v_fk_commands.Add (v_command);
					}

					if (!v_first_column) {
						v_fk_columns   += ", ";
						v_fk_r_columns += ", ";
					}

					v_fk_columns   += v_constraint ["column_name"];
					v_fk_r_columns += v_constraint ["r_column_name"];

					v_first_column = false;

					v_curr_fk	       = v_constraint ["constraint_name"].ToString ();
					v_curr_table 	   = v_constraint ["table_name"].ToString ();
					v_curr_r_table     = v_constraint ["r_table_name"].ToString ();
					v_curr_update_rule = v_constraint ["update_rule"].ToString ();
					v_curr_delete_rule = v_constraint ["delete_rule"].ToString ();

				}

				if (v_fk_columns != "") {

					string v_full_table_name = "";
					string v_full_r_table_name = "";
					if (v_dst_database.v_has_schema) {
						v_full_table_name = v_dst_database.v_schema + "." + v_curr_table;
						v_full_r_table_name = v_dst_database.v_schema + "." + v_curr_r_table;
					}  
					else {
						v_full_table_name = v_curr_table;
						v_full_r_table_name = v_curr_r_table;
					}

					Command v_command = new Command ();
					v_command.v_command = v_dst_database.v_add_fk_command.Replace("#p_table_name#",v_full_table_name).Replace("#p_r_table_name#",v_full_r_table_name).Replace("#p_constraint_name#",v_curr_fk).Replace("#p_columns#",v_fk_columns).Replace("#p_r_columns#",v_fk_r_columns).Replace ("#p_delete_update_rules#", v_dst_database.HandleUpdateDeleteRules(v_curr_update_rule,v_curr_delete_rule));
					v_command.v_table_name = v_curr_table;
					v_fk_columns = "";
					v_first_column = true;

					v_fk_commands.Add (v_command);
				}
			}

			if (v_indexes != null) {

				string v_curr_table = "";
				string v_curr_index = "";
				string v_curr_uniqueness = "";
				string v_index_columns = "";

				bool v_first_column = true;

				int v_count = 0;

				foreach (DataRow v_constraint in v_indexes.Rows) {

					if ((v_curr_table != "" && v_curr_table != v_constraint ["table_name"].ToString()) || (v_curr_index != "" && v_curr_index != v_constraint ["index_name"].ToString())) {

						string v_full_table_name = "";
						if (v_dst_database.v_has_schema)
							v_full_table_name = v_dst_database.v_schema + "." + v_curr_table;
						else
							v_full_table_name = v_curr_table;

						Command v_command = new Command ();
						v_command.v_command = v_dst_database.v_create_index_command.Replace("#p_table_name#",v_full_table_name).Replace("#p_index_name#","idx_" + v_count + "_" + v_curr_table).Replace("#p_columns#",v_index_columns).Replace("#p_uniqueness#",v_curr_uniqueness);
						v_command.v_table_name = v_curr_table;
						v_index_columns = "";
						v_first_column = true;

						v_count++;

						v_idx_commands.Add (v_command);
					}

					if (!v_first_column)
						v_index_columns += ", ";

					v_index_columns += v_constraint ["column_name"];

					v_first_column = false;

					v_curr_index	  = v_constraint ["index_name"].ToString ();
					v_curr_table 	  = v_constraint ["table_name"].ToString ();
					v_curr_uniqueness = v_constraint ["uniqueness"].ToString ();

				}

				if (v_index_columns != "") {

					string v_full_table_name = "";
					if (v_dst_database.v_has_schema)
						v_full_table_name = v_dst_database.v_schema + "." + v_curr_table;
					else
						v_full_table_name = v_curr_table;

					Command v_command = new Command ();
					v_command.v_command = v_dst_database.v_create_index_command.Replace("#p_table_name#",v_full_table_name).Replace("#p_index_name#","idx_" + v_count + "_" + v_curr_table).Replace("#p_columns#",v_index_columns).Replace("#p_uniqueness#",v_curr_uniqueness);
					v_command.v_table_name = v_curr_table;
					v_index_columns = "";
					v_first_column = true;

					v_idx_commands.Add (v_command);
				}
			}

			v_begin = DateTime.Now;
			v_tw.WriteLine(v_begin + " - Conversion commands successfully created.\n");
			v_tw.WriteLine (v_delete_commands.Count + " delete commands");
			v_tw.WriteLine (v_create_commands.Count + " table creation commands");
			v_tw.WriteLine (v_transfer_commands.Count + " table data transfer commands");
			v_tw.WriteLine (v_pk_commands.Count + " primary key creation commands");
			v_tw.WriteLine (v_fk_commands.Count + " foreign key creation commands");
			v_tw.WriteLine (v_uq_commands.Count + " unique creation commands");
			v_tw.WriteLine (v_idx_commands.Count + " index creation commands\n");
			v_tw.Flush ();

			int v_total_steps = v_delete_commands.Count + 
				v_create_commands.Count + 
				v_transfer_commands.Count + 
				v_pk_commands.Count + 
				v_fk_commands.Count +
				v_uq_commands.Count +
				v_idx_commands.Count;
			double v_inc_perc = 100.0 / v_total_steps;
			double v_total_perc = 0;

			ConversionProgress v_conversion_progress;

			v_conversion_progress = new ConversionProgress ();
			v_conversion_progress.v_mode = 0;

			foreach (Command v_command in v_delete_commands) {

				try {

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_droprecords = 'E' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

					v_dst_database.v_connection.Execute(v_command.v_command);

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_droprecords = 'F' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}
				catch (Spartacus.Database.Exception e) {

					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** DELETE RECORD ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.v_message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_droprecords = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}
				catch (System.InvalidOperationException e) {
					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** DELETE RECORD ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.Message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_droprecords = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}

				v_total_perc += v_inc_perc;
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_re_perc = " + Math.Round(v_total_perc,2).ToString().Replace(",",".") + " where conv_id = " + args[0]);

				v_conversion_progress.v_total_progress = v_total_perc;
				v_conversion_progress.v_curr_table = v_command.v_table_name;

			}


			foreach (Command v_command in v_create_commands) {

				try {

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createtable = 'E' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

					v_dst_database.v_connection.Execute(v_command.v_command);

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createtable = 'F' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}
				catch (Spartacus.Database.Exception e) {

					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** CREATE TABLE ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.v_message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createtable = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}
				catch (System.InvalidOperationException e) {
					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** CREATE TABLE ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.Message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createtable = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}

				v_total_perc += v_inc_perc;
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_re_perc = " + Math.Round(v_total_perc,2).ToString().Replace(",",".") + " where conv_id = " + args[0]);

				v_conversion_progress.v_total_progress = v_total_perc;
				v_conversion_progress.v_curr_table = v_command.v_table_name;

			}

			v_conversion_progress.v_mode = 1;


			foreach (TransferCommand v_command in v_transfer_commands) {

				uint v_total_records = Convert.ToUInt32(v_command.v_total_records);

				v_conversion_progress.v_table_progress = 0;
				v_conversion_progress.v_total_records = v_total_records;
				v_conversion_progress.v_transf_records = 0;
				v_conversion_progress.v_curr_transf_records = 0;
				v_conversion_progress.v_curr_table = v_command.v_table_name;

				//Updating start time for current table
				DateTime v_begintable = DateTime.Now;

				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_transferdata='E', ctd_st_starttransfer = '" + v_begintable.ToString() + "', ctd_in_totalrecords = " + v_command.v_total_records + " where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				bool v_hasmoredata = true;

				string v_insert_log = "";

				try {
					v_src_database.v_connection.Open ();
					v_dst_database.v_connection.Open ();
				}  
				catch (Spartacus.Database.Exception) {
				}
				catch (System.InvalidOperationException) {
				}


				uint v_block_size = v_dst_database.v_transfer_block_size[0];
				int v_curr_block_index = 0;
				double v_curr_avg_transfer = 0;
				bool v_is_tuning = true;

				uint v_transfered = 0;
				uint v_curr_transfered = 0;

				v_conversion_progress.v_old_time = DateTime.Now;

				int v_num_blocks_transfered = 0;

				bool v_error = false;

				while (v_hasmoredata) {
					try {

						v_insert_log = "";
						v_curr_transfered = v_src_database.v_connection.Transfer(v_command.v_select,v_command.v_full_table_name.ToLower(), v_command.v_insert, v_dst_database.v_connection, ref v_insert_log, v_transfered, v_transfered + v_block_size - 1, out v_hasmoredata);
						v_transfered += v_curr_transfered;

						if (v_insert_log!="") {
							v_tw.WriteLine("*** DATA TRANSFER ERROR ***");
							v_tw.WriteLine("Table: " + v_command.v_table_name);
							v_tw.WriteLine("Error:\n");
							v_tw.WriteLine(v_insert_log + "\n");
							v_tw.Flush ();
							v_error = true;
							ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_transferdata = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");
							break;
						}


						v_conversion_progress.v_transf_records = v_transfered;
						v_conversion_progress.v_curr_transf_records += v_curr_transfered;

						if (v_num_blocks_transfered==5) {

							v_conversion_progress.v_new_time = DateTime.Now;

							TimeSpan v_span_curr_block = v_conversion_progress.v_new_time.Subtract (v_conversion_progress.v_old_time);

							v_conversion_progress.v_old_time = DateTime.Now;

							double v_avg_transfer = Math.Round(v_conversion_progress.v_curr_transf_records/v_span_curr_block.TotalSeconds,2);

							v_conversion_progress.v_curr_transf_records = 0;

							double v_perc_transfer = Math.Round(Convert.ToDouble(v_conversion_progress.v_transf_records*100/v_conversion_progress.v_total_records),2);

							ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_re_transfperc = " + v_perc_transfer.ToString().Replace(",",".") + ", ctd_in_transfrecords = " + v_conversion_progress.v_transf_records + ", ctd_re_transferrate=" + v_avg_transfer.ToString().Replace(",",".") + " where conv_id = " + args[0] + " and ctd_st_table='" + v_conversion_progress.v_curr_table + "'");

							v_num_blocks_transfered = 0;


							if (v_is_tuning) {
								if (v_avg_transfer > v_curr_avg_transfer) {
									if (v_curr_block_index < 3) {
										v_curr_avg_transfer = v_avg_transfer;
										v_curr_block_index++;
									}
									else {
										v_is_tuning = false;
									}

								}
								else {
									v_is_tuning = false;
								}

								v_block_size = v_dst_database.v_transfer_block_size[v_curr_block_index];

							}

						}

						v_num_blocks_transfered++;

					}  
					catch (Spartacus.Database.Exception e) {

						v_tw.WriteLine("*** DATA TRANSFER ERROR ***");
						v_tw.WriteLine("Table: " + v_command.v_table_name);
						v_tw.WriteLine("Error:\n");
						v_tw.WriteLine(e.v_message + "\n");
						v_tw.Flush ();
						v_error = true;
						ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_transferdata = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");
						break;
					}
					catch (System.InvalidOperationException e) {

						v_tw.WriteLine("*** DATA TRANSFER ERROR ***");
						v_tw.WriteLine("Table: " + v_command.v_table_name);
						v_tw.WriteLine("Error:\n");
						v_tw.WriteLine(e.Message + "\n");
						v_tw.Flush ();
						v_error = true;
						ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_transferdata = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");
						break;
					}
				}

				try {
					v_dst_database.v_connection.Close ();
					v_src_database.v_connection.Close ();
				}  
				catch (Spartacus.Database.Exception) {
				}
				catch (System.InvalidOperationException) {

				}

				//Updating end time and duration for current table
				DateTime v_endtable = DateTime.Now;
				TimeSpan v_spantable = v_endtable.Subtract (v_begintable);

				if (!v_error)
					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_transferdata = 'F', ctd_re_transfperc = 100, ctd_in_transfrecords = " + v_conversion_progress.v_transf_records + ", ctd_st_endtransfer = '" + v_endtable.ToString() + "', ctd_st_duration = '" + new DateTime(v_spantable.Ticks).ToString("HH:mm:ss") + "', ctd_re_transfperc = " + 100 + ", ctd_in_transfrecords = " + v_conversion_progress.v_transf_records + " where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				v_total_perc += v_inc_perc;
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_re_perc = " + Math.Round(v_total_perc,2).ToString().Replace(",",".") + " where conv_id = " + args[0]);

				v_conversion_progress.v_total_progress = v_total_perc;
			}

			// Primary Keys
			foreach (Command v_command in v_pk_commands) {

				try {

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createpk = 'E' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

					v_dst_database.v_connection.Execute(v_command.v_command);

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createpk = 'F' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}
				catch (Spartacus.Database.Exception e) {

					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** CREATE PRIMARY KEY ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.v_message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createpk = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");


				}
				catch (System.InvalidOperationException e) {
					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** CREATE PRIMARY KEY ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.Message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createpk = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}

				v_total_perc += v_inc_perc;
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_re_perc = " + Math.Round(v_total_perc,2).ToString().Replace(",",".") + " where conv_id = " + args[0]);

				v_conversion_progress.v_total_progress = v_total_perc;
				v_conversion_progress.v_curr_table = v_command.v_table_name;

			}

			// Foreign Keys
			foreach (Command v_command in v_fk_commands) {

				try {

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createfk = 'E' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

					v_dst_database.v_connection.Execute(v_command.v_command);


					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createfk = 'F' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}
				catch (Spartacus.Database.Exception e) {

					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** FOREIGN KEY ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.v_message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createfk = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");


				}
				catch (System.InvalidOperationException e) {
					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** FOREIGN KEY ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.Message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createfk = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}

				v_total_perc += v_inc_perc;
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_re_perc = " + Math.Round(v_total_perc,2).ToString().Replace(",",".") + " where conv_id = " + args[0]);

				v_conversion_progress.v_total_progress = v_total_perc;
				v_conversion_progress.v_curr_table = v_command.v_table_name;

			}

			// Uniques
			foreach (Command v_command in v_uq_commands) {

				try {

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createuq = 'E' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

					v_dst_database.v_connection.Execute(v_command.v_command);

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createuq = 'F' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}
				catch (Spartacus.Database.Exception e) {

					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** CREATE UNIQUE ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.v_message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createuq = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");


				}
				catch (System.InvalidOperationException e) {
					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** CREATE UNIQUE ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.Message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createuq = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}

				v_total_perc += v_inc_perc;
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_re_perc = " + Math.Round(v_total_perc,2).ToString().Replace(",",".") + " where conv_id = " + args[0]);

				v_conversion_progress.v_total_progress = v_total_perc;
				v_conversion_progress.v_curr_table = v_command.v_table_name;

			}

			// Indexes
			foreach (Command v_command in v_idx_commands) {

				try {

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createidx = 'E' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

					v_dst_database.v_connection.Execute(v_command.v_command);

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createidx = 'F' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}
				catch (Spartacus.Database.Exception e) {

					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** CREATE INDEX ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.v_message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createidx = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");


				}
				catch (System.InvalidOperationException e) {
					v_begin = DateTime.Now;
					v_tw.WriteLine(v_begin + " - *** CREATE INDEX ERROR ***");
					v_tw.WriteLine("Command:\n");
					v_tw.WriteLine(v_command.v_command + "\n");
					v_tw.WriteLine("Error:\n");
					v_tw.WriteLine(e.Message + "\n");
					v_tw.Flush ();

					ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conv_tables_data set ctd_ch_createidx = 'X' where conv_id = " + args[0] + " and ctd_st_table='" + v_command.v_table_name + "'");

				}

				v_total_perc += v_inc_perc;
				ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_re_perc = " + Math.Round(v_total_perc,2).ToString().Replace(",",".") + " where conv_id = " + args[0]);

				v_conversion_progress.v_total_progress = v_total_perc;
				v_conversion_progress.v_curr_table = v_command.v_table_name;

			}


			DateTime v_end = DateTime.Now;
			v_tw.WriteLine(v_end + " - Conversion Completed.");
			v_tw.Flush();
			v_tw.Close ();

			TimeSpan v_span = v_end.Subtract (v_start);

			ExecuteOmniDBCommand (v_omnidb_database,v_tw,"update conversions set conv_ch_status='F', conv_st_end = '" + v_end.ToString() + "', conv_st_duration=' " + new DateTime(v_span.Ticks).ToString("HH:mm:ss") + "' where conv_id = " + args[0]);

		}

		/// <summary>
		/// Executes SQL command in OmniDBs command.
		/// </summary>
		/// <param name="p_database">Database object</param>.</param>
		/// <param name="p_logfile">Log file object.</param>
		/// <param name="p_sql">SQL command.</param>
		public static void ExecuteOmniDBCommand(OmniDatabase.Generic p_database, System.IO.TextWriter p_logfile, string p_sql) {

			try {
				p_database.v_connection.Execute (p_sql);
			}
			catch (Spartacus.Database.Exception e) {

				System.DateTime v_begin = DateTime.Now;
				p_logfile.WriteLine(v_begin + " - *** OMNIDB DATABASE COMMAND ERROR ***");
				p_logfile.WriteLine("Command:\n");
				p_logfile.WriteLine(p_sql + "\n");
				p_logfile.WriteLine("Error:\n");
				p_logfile.WriteLine(e.v_message + "\n");
				p_logfile.Flush ();

			}
			catch (System.InvalidOperationException e) {
				System.DateTime v_begin = DateTime.Now;
				p_logfile.WriteLine(v_begin + " - *** OMNIDB DATABASE COMMAND ERROR ***");
				p_logfile.WriteLine("Command:\n");
				p_logfile.WriteLine(p_sql + "\n");
				p_logfile.WriteLine("Error:\n");
				p_logfile.WriteLine(e.Message + "\n");
				p_logfile.Flush ();

			}

		}

		/// <summary>
		/// Get data type representatives on target connection.
		/// </summary>
		/// <param name="p_database">Database object.</param>
		/// <param name="p_types">Data types datable.</param>
		/// <param name="p_src_tech">Source technology.</param>
		/// <param name="p_dst_tech">Target technology.</param>
		public static DataTable GetRepresentatives(OmniDatabase.Generic p_database, DataTable p_types, string p_src_tech, string p_dst_tech) {

			string v_query = "";
			bool v_first = true;

			foreach (DataRow v_type in p_types.Rows) {

				if (!v_first)
					v_query += "union ";

				v_first = false;

				v_query += "select '" + v_type["data_type"] + "' as src_dt_type, dt1.cat_st_name as cat_st_name, r.dt_type as dst_dt_type, r.rep_st_default as rep_st_default, dt1.dt_st_readformat as dt_st_readformat, dt2.dt_st_writeformat as dt_st_writeformat, dt2.dt_in_sufix as dst_dt_in_sufix " +
					"from data_types dt1, representatives r, data_types dt2 " +
					"where dt1.dbt_st_name='" + p_src_tech + "' and dt1.dt_type='" + v_type["data_type"].ToString().ToLower() +
					"' and r.cat_st_name=dt1.cat_st_name and r.dbt_st_name='" + p_dst_tech + "' " +
					"  and r.dt_type=dt2.dt_type and r.dbt_st_name=dt2.dbt_st_name " +
					" union " +
					"select '" + v_type["data_type"] + "' as data_type,'','','','#','#',0 where '" + v_type["data_type"].ToString().ToLower() + "' not in (select dt_type from data_types where dbt_st_name='" + p_src_tech + "') ";

			}

			return (p_database.v_connection.Query (v_query,"Representatives"));


		}

		/// <summary>
		/// Sort datatable by column table_name.
		/// </summary>
		/// <param name="p_table">Datatable.</param>
		public static DataTable SortByTableName(DataTable p_table) {

			DataView dv = p_table.DefaultView;
			dv.Sort = "table_name asc";
			return dv.ToTable();

		}

		/// <summary>
		/// Define which structures will be converted.
		/// </summary>
		/// <param name="p_tables">Target datatable.</param>
		/// <param name="p_conv_tables">Source datatable.</param>
		public static void AssingConversionTables(DataTable p_tables, DataTable p_conv_tables) {

			int v_index = 0;

			foreach (DataRow v_table in p_tables.Rows) {
				v_table ["drop_records"] = p_conv_tables.Rows [v_index] ["ctd_ch_droprecords"].ToString ();
				v_table ["create_table"] = p_conv_tables.Rows [v_index] ["ctd_ch_createtable"].ToString ();
				v_table ["transfer_data"] = p_conv_tables.Rows [v_index] ["ctd_ch_transferdata"].ToString ();
				v_table ["transfer_filter"] = p_conv_tables.Rows [v_index] ["ctd_st_transferfilter"].ToString ();
				v_index++;

			}

		}

		/// <summary>
		/// Setup tables datatable to store information about start and end index on associated columns at columns datatable.
		/// </summary>
		/// <param name="p_columns">Columns datatable.</param>
		/// <param name="p_tables">Tables datatable.</param>
		public static void SetupTablesDatatable(DataTable p_columns, DataTable p_tables) {

			int v_pos_counter = 0;
			string v_table_name = "";

			foreach (DataRow v_table in p_tables.Rows) {

				v_table ["position"] = v_pos_counter;
				v_table_name = v_table ["table_name"].ToString();

				int v_count_cols = 0;

				int v_curr_index = v_pos_counter;

				while ((v_curr_index < p_columns.Rows.Count) && p_columns.Rows [v_curr_index] ["table_name"].ToString () == v_table_name) {
					v_count_cols++;
					v_curr_index++;
				}

				v_table ["num_columns"] = v_count_cols;
				v_pos_counter += v_count_cols;


			}


		}

		/// <summary>
		/// Assigns indexes to columns, referencing correct representative on representatives datatable.
		/// </summary>
		/// <param name="p_columns">Columns datatable.</param>
		/// <param name="p_representatives">Representatives datatable.</param>
		public static void AssignRepresentatives(DataTable p_columns, DataTable p_representatives) {

			foreach (DataRow v_column in p_columns.Rows) {
				bool v_found = false;

				for (int i = 0; i < p_representatives.Rows.Count; i++) {
					if (v_column ["data_type"].ToString () == p_representatives.Rows [i] ["src_dt_type"].ToString ()) {
						v_column ["rep_index"] = i;
						v_found = true;
						break;
					}
				}

				if (!v_found) {
					v_column ["rep_index"] = -1;
				}


			}
		}

		/// <summary>
		/// Creates filter to remove unwanted tables.
		/// </summary>
		/// <param name="p_tables">Tables datatable.</param>
		public static string CreateFilter(DataTable p_tables) {

			string v_filter = "table_name not in (";

			bool v_first = true;

			foreach (DataRow v_table in p_tables.Rows) {

				if (!v_first)
					v_filter += ",";

				v_first = false;
				v_filter += "'" + v_table ["ctd_st_table"].ToString () + "'";

			}

			v_filter += ")";

			return v_filter;

		}

		/// <summary>
		/// Removes unwanted datarows in datatable based on filter.
		/// </summary>
		/// <param name="p_table_columns">Datatable.</param>
		/// <param name="p_filter">Filter.</param>
		public static void RemoveUnwantedRows(DataTable p_table_columns, string p_filter) {

			DataRow[] v_rows = p_table_columns.Select(p_filter);
			foreach (DataRow v_row in v_rows)
				v_row.Delete ();

		}

		/// <summary>
		/// Get distinct data_types on datatable.
		/// </summary>
		/// <param name="p_table_columns">Datatable.</param>
		public static DataTable GetUniqueDataTypes(DataTable p_table_columns) {

			DataView view = new DataView(p_table_columns);
			DataTable distinctValues = view.ToTable(true, "data_type");


			return distinctValues;
		}
	}
}