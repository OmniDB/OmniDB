/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

using System;

namespace OmniDatabase
{
	/// <summary>
	/// Class to store information of a Spartacus FileDB (PollyDB) database.
	/// </summary>
	public class FileDB : Generic
	{
		/// <summary>
		/// Initializes a new instance of the <see cref="OmniDB.Database.FileDB"/> class.
		/// </summary>
		/// <param name="p_database">Database file.</param>
		public FileDB (string p_conn_id, string p_database)
			: base ("filedb",p_conn_id)
		{

			v_service = p_database;

			v_has_schema = false;
			v_schema = "";
			v_has_update_rule = false;

			v_default_string = "text";

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
			v_delete_rules.Add ("SET NULL");

			v_update_rules.Add ("");
			v_update_rules.Add ("SET NULL");

			v_trim_function = "trim";

			v_transfer_block_size = new System.Collections.Generic.List<uint> ();
			v_transfer_block_size.Add (10);
			v_transfer_block_size.Add (20);
			v_transfer_block_size.Add (30);
			v_transfer_block_size.Add (40);

			v_connection = new Spartacus.Database.Pollydb (p_database);
			v_connection.v_execute_security = false;

			v_has_functions = false;
			v_has_procedures = false;
			v_has_sequences = false;

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

			if (this.v_service.Contains("/")) {

				string []v_strings = this.v_service.Split ('/');

				return v_strings [v_strings.Length - 1];

			}
			else
				return this.v_service;

		}

		/// <summary>
		/// Print database details.
		/// </summary>
		public override string PrintDatabaseDetails() {

			return "Local Folder";

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
				if (System.IO.Directory.Exists(this.v_connection.v_service))
					v_return = "Connection successful.";
				else
					v_return = "Folder does not exist.";

			}
			catch (Spartacus.Database.Exception e) {

				v_return = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");

			}

			return v_return;

		}

		/// <summary>
		/// Get a datatable with all tables.
		/// </summary>
		public override System.Data.DataTable QueryTables(bool p_all_schemas) {

			System.Data.DataTable v_table;
			System.Data.DataRow v_row;
			System.Collections.Generic.List<string> v_tmpfiles;
			System.IO.DirectoryInfo v_info;

			v_table = new System.Data.DataTable("Tables");
			v_table.Columns.Add("table_name");

			v_tmpfiles = new System.Collections.Generic.List<string>();
			v_info = new System.IO.DirectoryInfo(this.v_service);

			if (v_info.Exists)
			{
				v_tmpfiles.AddRange(System.IO.Directory.GetFiles(this.v_service, "*.csv", System.IO.SearchOption.TopDirectoryOnly));
				v_tmpfiles.AddRange(System.IO.Directory.GetFiles(this.v_service, "*.CSV", System.IO.SearchOption.TopDirectoryOnly));
				v_tmpfiles.AddRange(System.IO.Directory.GetFiles(this.v_service, "*.dbf", System.IO.SearchOption.TopDirectoryOnly));
				v_tmpfiles.AddRange(System.IO.Directory.GetFiles(this.v_service, "*.DBF", System.IO.SearchOption.TopDirectoryOnly));
				v_tmpfiles.AddRange(System.IO.Directory.GetFiles(this.v_service, "*.xlsx", System.IO.SearchOption.TopDirectoryOnly));
				v_tmpfiles.AddRange(System.IO.Directory.GetFiles(this.v_service, "*.XLSX", System.IO.SearchOption.TopDirectoryOnly));

				foreach(string s in v_tmpfiles)
				{
					v_row = v_table.NewRow();
					Spartacus.Utils.File f = new Spartacus.Utils.File(Spartacus.Utils.FileType.FILE, s);
					v_row["table_name"] = "[" + f.v_name + "]";
					v_table.Rows.Add(v_row);
				}
			}

			return v_table;
		}

		/// <summary>
		/// Get a datatable with all views.
		/// </summary>
		public override System.Data.DataTable QueryViews() {

			return null;

		}

		/// <summary>
		/// Get a datatable with all tables fields.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesFields(string p_table) {

			if (p_table == null) {

				return null; // Open all files at once just to retrieve column list can be VERY slow.

			} 
			else {

				System.Data.DataRow v_row;

				System.Data.DataTable v_table_columns = new System.Data.DataTable("TableFields");
				v_table_columns.Columns.Add("column_name");
				v_table_columns.Columns.Add("data_type");
				v_table_columns.Columns.Add ("nullable");
				v_table_columns.Columns.Add ("data_length");
				v_table_columns.Columns.Add ("data_precision");
				v_table_columns.Columns.Add ("data_scale");

				com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
				com.healthmarketscience.jackcess.Table v_table = v_database.getTable(p_table.Replace("[", "").Replace("]", ""));
				java.util.List v_list = v_table.getColumns();
				object[] v_obj = v_list.toArray();
				foreach (object o in v_obj) {

					com.healthmarketscience.jackcess.Column c = (com.healthmarketscience.jackcess.Column) o;

					v_row = v_table_columns.NewRow();
					v_row["column_name"] = c.getName();
					v_row["data_type"] = c.getType().ToString();
					v_row["nullable"] = "YES";
					v_row["data_length"] = c.getLength().ToString();
					v_row["data_precision"] = c.getPrecision().ToString();
					v_row["data_scale"] = c.getScale().ToString();
					v_table_columns.Rows.Add(v_row);

				}

				return v_table_columns;

			}

		}

		/// <summary>
		/// Get a datatable with all tables foreign keys.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesForeignKeys(string p_table) {

			return null;

		}

		/// <summary>
		/// Get a datatable with all tables primary keys.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesPrimaryKeys(string p_schema, string p_table) {

			return null;

		}

		/// <summary>
		/// Get a datatable with all tables unique constraints.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesUniques(string p_schema, string p_table) {

			return null;

		}

		/// <summary>
		/// Get a datatable with all tables indexes.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesIndexes(string p_table) {

			return null;

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
		/// <param name="p_query">Query string.</param>
		/// <param name="p_count">Max number of records.</param>
		/// <param name="p_columns">Column names.</param>
		public override System.Collections.Generic.List<System.Collections.Generic.List<string>> QueryDataLimitedList(string p_query, int p_count, out System.Collections.Generic.List<string> p_columns)
		{

			string v_filter = "";
			if (p_count != -1)
				v_filter = " limit  " + p_count;

			return v_connection.QuerySList(
				"select *                 " +
				"from ( " + p_query + " ) " +
				v_filter, out p_columns);

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

		/// <summary>
		/// Get a datatable with all functions.
		/// </summary>
		public override System.Data.DataTable QueryFunctions() {

			return null;

		}

		/// <summary>
		/// Get a datatable with all fields of a function.
		/// </summary>
		public override System.Data.DataTable QueryFunctionFields(string p_function) {

			return null;

		}

		/// <summary>
		/// Get function definition.
		/// </summary>
		public override string GetFunctionDefinition(string p_function) {

			return null;

		}

		/// <summary>
		/// Get a datatable with all procedures.
		/// </summary>
		public override System.Data.DataTable QueryProcedures() {

			return null;

		}

		/// <summary>
		/// Get a datatable with all fields of a procedure.
		/// </summary>
		public override System.Data.DataTable QueryProcedureFields(string p_procedure) {

			return null;

		}

		/// <summary>
		/// Get procedure definition.
		/// </summary>
		public override string GetProcedureDefinition(string p_procedure) {

			return null;

		}

		/// <summary>
		/// Get a datatable with sequences.
		/// </summary>
		public override System.Data.DataTable QuerySequences(string p_sequence)
		{

			return null;

		}

	}
}