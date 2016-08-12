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
	/// Class to store information of an SqlServer database.
	/// </summary>
	public class SqlServer : Generic
	{
		/// <summary>
		/// Initializes a new instance of the <see cref="OmniDB.Database.SqlServer"/> class.
		/// </summary>
		/// <param name="p_server">Connection address.</param>
		/// <param name="p_port">Connection port.</param>
		/// <param name="p_service">Database name.</param>
		/// <param name="p_user">Database user.</param>
		/// <param name="p_password">Database password.</param>
		/// <param name="p_schema">Schema.</param>
		public SqlServer (string p_conn_id, string p_server, string p_port, string p_service, string p_user, string p_password, string p_schema)
			: base ("sqlserver",p_conn_id)
		{

			v_server = p_server;
			v_port   = p_port;
			v_service = p_service;
			if (p_user!="")
				v_user = p_user;
			else v_user = "windows_user";
			v_has_schema = true;
			v_has_update_rule = true;

			v_default_string = "text";

			v_can_rename_table = true;
			v_rename_table_command = "sp_rename '#p_table_name#','#p_new_table_name#'";

			v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)";
			v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#";
			v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)";

			v_can_alter_type = true;
			v_alter_type_command = "alter table #p_table_name# alter column #p_column_name# #p_new_data_type#";

			v_can_alter_nullable = true;
			v_set_nullable_command = "alter table #p_table_name# alter column #p_column_name# #p_new_data_type#";
			v_drop_nullable_command = "alter table #p_table_name# alter column #p_column_name# #p_new_data_type# not null";

			v_can_rename_column = true;
			v_rename_column_command = "sp_rename '#p_table_name#.#p_column_name#','#p_new_column_name#'";

			v_can_add_column = true;
			v_add_column_command = "alter table #p_table_name# add #p_column_name# #p_data_type# #p_nullable#";

			v_can_drop_column = true;
			v_drop_column_command = "alter table #p_table_name# drop column #p_column_name#";

			v_can_add_constraint = true;
			v_add_pk_command = "alter table #p_table_name# add constraint #p_constraint_name# primary key (#p_columns#)";
			v_add_fk_command = "alter table #p_table_name# add constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#";
			v_add_unique_command = "alter table #p_table_name# add constraint #p_constraint_name# unique (#p_columns#)";

			v_can_drop_constraint = true;
			v_drop_pk_command = "alter table #p_table_name# drop constraint #p_constraint_name#";
			v_drop_fk_command = "alter table #p_table_name# drop constraint #p_constraint_name#";
			v_drop_unique_command = "alter table #p_table_name# drop constraint #p_constraint_name#";

			v_create_index_command = "create #p_uniqueness# index #p_index_name# on #p_table_name# (#p_columns#)";
			v_create_index_command = "create index #p_index_name# on #p_table_name# (#p_columns#)";
			v_create_unique_index_command = "create unique index #p_index_name# on #p_table_name# (#p_columns#)";

			v_drop_index_command = "drop index #p_table_name#.#p_index_name#";

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

			v_trim_function = "ltrim";

			v_transfer_block_size = new System.Collections.Generic.List<uint> ();
			v_transfer_block_size.Add (50);
			v_transfer_block_size.Add (100);
			v_transfer_block_size.Add (200);
			v_transfer_block_size.Add (400);

			if (p_schema == "")
				v_schema = "dbo";
			else
				v_schema = p_schema;

			if (p_user=="")
				v_connection = new Spartacus.Database.SqlServer (p_server, p_port, p_service, p_user, p_password,true);
			else
				v_connection = new Spartacus.Database.SqlServer (p_server, p_port, p_service, p_user, p_password);

			v_connection.v_execute_security = false;

			v_has_functions = false;

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

			return v_user + "@" + v_service + " - " + v_schema;

		}

		/// <summary>
		/// Print database details.
		/// </summary>
		public override string PrintDatabaseDetails() {

			return v_server + ":" + v_port;

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
				
				this.v_connection.Open();

				System.Data.DataTable v_schema = this.v_connection.Query("select schema_name from information_schema.schemata where lower(schema_name)='" + this.v_schema.ToLower() + "'","Schema");

				if (v_schema.Rows.Count > 0)
					v_return = "Connection successful.";
				else
					v_return = "Connection successful but schema '" + this.v_schema + "' does not exist.";

				this.v_connection.Close();

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

			string v_filter = "";

			if (!p_all_schemas)
				v_filter = "  and lower(table_schema) = '" + v_schema.ToLower () + "' ";
			else
				v_filter = " and lower(table_schema) not in ('information_schema','pg_catalog') ";

			return v_connection.Query (
				"select lower(table_name) as table_name, " +
				"lower(table_schema) as table_schema     " +
				"from information_schema.tables          " +
				"where table_type = 'BASE TABLE'         " +
				v_filter +
				"order by table_schema,table_name;", "Tables");

		}

		/// <summary>
		/// Get a datatable with all views.
		/// </summary>
		public override System.Data.DataTable QueryViews() {

			return v_connection.Query (
				"select lower(t.table_name) as view_name  " +
				"from information_schema.tables t         " +
				"where t.table_schema ='" + v_schema + "' " +
				"and t.table_type = 'VIEW'                " +
				"order by t.table_name", "Views");

		}

		/// <summary>
		/// Get a datatable with all tables fields.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesFields(string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(c.table_name) = '" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"select lower(c.table_name) as table_name,                                                             " +
				"lower(c.column_name) as column_name,                                                                  " +
				"lower(c.data_type) as data_type,                                                                      " +
				"c.is_nullable as nullable,                                                                            " +
				"c.character_maximum_length as data_length,                                                            " +
				"c.numeric_precision as data_precision,                                                                " +
				"c.numeric_scale as data_scale                                                                         " +
				"from information_schema.columns c                                                                     " +
				"join information_schema.tables t on (c.table_name = t.table_name and c.table_schema = t.table_schema) " +
				"where lower(t.table_schema) ='" + v_schema.ToLower() + "'                                             " +
				"and t.table_type = 'BASE TABLE'                                                                       " +
				v_filter +
				"order by c.table_name, c.ordinal_position", "TableFields");

		}

		/// <summary>
		/// Get a datatable with all tables foreign keys.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesForeignKeys(string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(KCU1.TABLE_NAME) = '" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"SELECT *                                                                                         " +
				"FROM (SELECT distinct                                                                            " +
				"lower(KCU1.CONSTRAINT_NAME) AS constraint_name,                                                  " +
				"lower(KCU1.TABLE_NAME) AS table_name,                                                            " +
				"lower(KCU1.COLUMN_NAME) AS column_name,                                                          " +
				"lower(KCU2.CONSTRAINT_NAME) AS r_constraint_name,                                                " +
				"lower(KCU2.TABLE_NAME) AS r_table_name,                                                          " +
				"lower(KCU2.COLUMN_NAME) AS r_column_name,                                                        " +
				"lower(KCU1.constraint_schema) as table_schema,                                                   " +
				"lower(KCU2.constraint_schema) as r_table_schema,                                                 " +
				"KCU1.ORDINAL_POSITION,                                                                           " +
				"RC.update_rule as update_rule,                                                                   " +
				"RC.delete_rule as delete_rule                                                                    " +
				"FROM INFORMATION_SCHEMA.REFERENTIAL_CONSTRAINTS RC                                               " +
				"JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU1 ON KCU1.CONSTRAINT_CATALOG = RC.CONSTRAINT_CATALOG " +
				"AND KCU1.CONSTRAINT_SCHEMA = RC.CONSTRAINT_SCHEMA                                                " +
				"AND KCU1.CONSTRAINT_NAME = RC.CONSTRAINT_NAME                                                    " +
				"JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE KCU2                                                    " +
				"ON KCU2.CONSTRAINT_CATALOG = RC.UNIQUE_CONSTRAINT_CATALOG                                        " +
				"AND KCU2.CONSTRAINT_SCHEMA = RC.UNIQUE_CONSTRAINT_SCHEMA                                         " +
				"AND KCU2.CONSTRAINT_NAME = RC.UNIQUE_CONSTRAINT_NAME                                             " +
				"AND KCU2.ORDINAL_POSITION = KCU1.ORDINAL_POSITION                                                " +
				"where lower(KCU1.TABLE_SCHEMA) ='" + v_schema.ToLower() + "'                                     " +
				v_filter +
				") t                                                                                              " +
				"order by CONSTRAINT_NAME,                                                                        " +
				"TABLE_NAME,                                                                                      " +
				"ORDINAL_POSITION", "TableForeignKeys");

		}

		/// <summary>
		/// Get a datatable with all tables primary keys.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesPrimaryKeys(string p_schema, string p_table) {

			string v_filter = "";

			string v_curr_schema = "";

			if (p_schema == "")
				v_curr_schema = v_schema;
			else
				v_curr_schema = p_schema;

			if (p_table != null)
				v_filter = "and lower(tc.table_name) = '" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"select lower(tc.constraint_name) as constraint_name,         " +
				"lower(kc.column_name) as column_name,                        " +
				"lower(tc.table_name) as table_name                           " +
				"from                                                         " +
				"information_schema.table_constraints tc,                     " +
				"information_schema.key_column_usage kc                       " +
				"where                                                        " +
				"tc.constraint_type = 'PRIMARY KEY'                           " +
				"and kc.table_name = tc.table_name                            " +
				"and kc.table_schema = tc.table_schema                        " +
				"and kc.constraint_name = tc.constraint_name                  " +
				"and lower(tc.table_schema)='" + v_curr_schema.ToLower() + "' " +
				v_filter + 
				"order by tc.constraint_name,                                 " +
				"tc.table_name,                                               " +
				"kc.ordinal_position", "TablePrimaryKeys");

		}

		/// <summary>
		/// Get a datatable with all tables unique constraints.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesUniques(string p_schema, string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(tc.table_name) = '" + p_table.ToLower() + "' ";

			string v_curr_schema = "";

			if (p_schema == "")
				v_curr_schema = v_schema;
			else
				v_curr_schema = p_schema;

			return v_connection.Query (
				"select lower(tc.constraint_name) as constraint_name,          " +
				"lower(kc.column_name) as column_name,                         " +
				"lower(tc.table_name) as table_name                            " +
				"from information_schema.table_constraints tc,                 " +
				"information_schema.key_column_usage kc                        " +
				"where tc.constraint_type = 'UNIQUE'                           " +
				"and kc.table_name = tc.table_name                             " +
				"and kc.table_schema = tc.table_schema                         " +
				"and kc.constraint_name = tc.constraint_name                   " +
				"and lower(tc.table_schema)='" + v_curr_schema.ToLower () + "' " +
				v_filter +
				"order by tc.constraint_name,                                  " +
				"tc.table_name,                                                " +
				"kc.ordinal_position", "TableUniques");

		}

		/// <summary>
		/// Get a datatable with all tables indexes.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesIndexes(string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(so.name) = '" + p_table.ToLower() + "' ";

			return v_connection.Query(
				"SELECT lower(so.name) AS table_name,                                                   " +
				"lower(si.name) AS index_name,                                                          " +
				"lower(c.name) as column_name,                                                          " +
				"case when si.is_unique='True' then 'Unique'                                            " +
				"else 'Non Unique' end as uniqueness                                                    " +
				"FROM sys.indexes si                                                                    " +
				"JOIN sys.objects so ON si.[object_id] = so.[object_id]                                 " +
				"JOIN sys.index_columns ic ON ic.object_id = si.object_id AND ic.index_id = si.index_id " +
				"JOIN sys.columns c ON c.object_id = ic.object_id AND c.column_id = ic.column_id        " +
				"JOIN sys.schemas s ON s.schema_id = so.schema_id                                       " +
				"WHERE so.type = 'U'                                                                    " +
				"AND si.name IS NOT NULL                                                                " +
				"AND lower(s.name) = '" + this.v_schema.ToLower() + "'                                  " +
				v_filter +
				"ORDER BY so.name, si.name, ic.column_id", "TableIndexes");

		}

		/// <summary>
		/// Query limited number of records.
		/// </summary>
		/// <param name="p_query">Query string.</param>
		/// <param name="p_count">Max number of records.</param>
		public override System.Data.DataTable QueryDataLimited(string p_query, int p_count) {

			string v_filter = "";
			if (p_count != -1)
				v_filter = " top  " + p_count;

			return v_connection.Query (
				"select " + v_filter + " limit_alias.* " +
				"from ( " + p_query + " ) limit_alias", "Limited Query");

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
				v_limit = " top  " + p_count;

			return v_connection.Query (
				"select " + v_limit + " " + p_column_list + " " +
				"from  " + p_table + " t                      " +
				p_filter, "Limited Query");

		}

		/// <summary>
		/// Get a datatable with all functions.
		/// </summary>
		public override System.Data.DataTable QueryFunctions() {

			return null;

		}

		/// <summary>
		/// Get function definition.
		/// </summary>
		public override string GetFunctionDefinition(string p_function) {

			return null;

		}

	}
}
