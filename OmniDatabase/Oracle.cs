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
	/// Class to store information of an Oracle database.
	/// </summary>
	public class Oracle : Generic
	{
		/// <summary>
		/// Initializes a new instance of the <see cref="OmniDB.Database.Oracle"/> class.
		/// </summary>
		/// <param name="p_server">Connection address.</param>
		/// <param name="p_port">Connection port.</param>
		/// <param name="p_service">Database name.</param>
		/// <param name="p_user">Database user.</param>
		/// <param name="p_password">Database password.</param>
		public Oracle (string p_conn_id, string p_server, string p_port, string p_service, string p_user, string p_password) : base ("oracle",p_conn_id) {

			v_server = p_server;
			v_port   = p_port;
			v_service = p_service;
			v_user = p_user;
			v_has_schema = true;
			v_schema = v_user;
			v_has_update_rule = false;

			v_default_string = "varchar2(500)";

			v_can_rename_table = true;
			v_rename_table_command = "alter table #p_table_name# rename to #p_new_table_name#";

			v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)";
			v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#";
			v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)";

			v_can_alter_type = true;
			v_alter_type_command = "alter table #p_table_name# modify #p_column_name# #p_new_data_type#";

			v_can_alter_nullable = true;
			v_set_nullable_command = "alter table #p_table_name# modify #p_column_name# null";
			v_drop_nullable_command = "alter table #p_table_name# modify #p_column_name# not null";

			v_can_rename_column = true;
			v_rename_column_command = "alter table #p_table_name# rename column #p_column_name# to #p_new_column_name#";

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

			v_create_index_command = "create index #p_index_name# on #p_table_name# (#p_columns#)";
			v_create_unique_index_command = "create unique index #p_index_name# on #p_table_name# (#p_columns#)";

			v_drop_index_command = "drop index #p_index_name#";

			v_update_rules = new System.Collections.Generic.List<string> ();
			v_delete_rules = new System.Collections.Generic.List<string> ();

			v_delete_rules.Add ("");
			v_delete_rules.Add ("NO ACTION");
			v_delete_rules.Add ("CASCADE");
			v_delete_rules.Add ("SET NULL");

			v_trim_function = "trim";

			v_transfer_block_size = new System.Collections.Generic.List<uint> ();
			v_transfer_block_size.Add (50);
			v_transfer_block_size.Add (100);
			v_transfer_block_size.Add (200);
			v_transfer_block_size.Add (400);

			v_connection = new Spartacus.Database.Oracle (p_server, p_port, p_service, p_user, p_password);
			v_connection.v_execute_security = false;

			v_has_functions = true;
            v_has_procedures = true;
			v_has_sequences = true;

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

			return  v_user + "@" + v_service;

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

			if (p_delete_rule != "NO ACTION" && p_delete_rule.Trim() != "")
				v_rules += " on delete " + p_delete_rule.Trim() + " ";

			return v_rules;

		}

		/// <summary>
		/// Test connection.
		/// </summary>
		public override string TestConnection() {

			string v_return = "";

			try {
				
				this.v_connection.Open();
				this.v_connection.Close();
				v_return = "Connection successful.";

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
				v_filter = "where lower(owner)='" + v_schema.ToLower () + "' ";
			else
				v_filter = "where OWNER not in ('APEX_040200','MDSYS','OUTLN','CTXSYS','OLAPSYS','FLOWS_FILES','SYSTEM','DVSYS','AUDSYS',\n'SCOTT','DBSNMP','GSMADMIN_INTERNAL','OJVMSYS','ORDSYS','APPQOSSYS','XDB','ORDDATA','SYS','WMSYS','LBACSYS','HR','APEX_040000') ";

			return v_connection.Query (
				"select lower(table_name) as table_name, " +
				"lower(owner) as table_schema            " +
				"from all_tables                         " +
				v_filter +
				"order by owner, table_name", "Tables");

		}

		/// <summary>
		/// Get a datatable with all views.
		/// </summary>
		public override System.Data.DataTable QueryViews() {

			return v_connection.Query (
				"select lower(view_name) as view_name,         " +
				"owner as table_schema                         " +
				"from all_views                                " +
				"where lower(owner)='" + v_user.ToLower() + "' " +
				"order by view_name", "Views");

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
				"select lower(c.table_name) as table_name,                          " +
				"lower(c.column_name) as column_name,                               " +
				"CASE WHEN c.DATA_TYPE='NUMBER' and c.DATA_SCALE='0' THEN 'integer' " +
				"ELSE lower(c.DATA_TYPE) END as data_type,                          " +
				"CASE c.nullable                                                    " +
				"WHEN 'Y' THEN 'YES'                                                " +
				"ELSE 'NO' END as nullable,                                         " +
				"c.data_length,                                                     " +
				"c.data_precision,                                                  " +
				"c.data_scale                                                       " +
				"from all_tab_columns c                                             " +
				"where lower(c.owner)='" + v_schema.ToLower() + "'                  " +
				v_filter +
				"order by c.table_name,                                             " +
				"c.column_id", "TableFields");
		}


		/// <summary>
		/// Get a datatable with all tables foreign keys.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesForeignKeys(string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(detail_table.TABLE_NAME) = '" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"SELECT lower(master_table.TABLE_NAME)  as r_table_name,              " +
				"lower(master_table.owner) as r_table_schema,                         " +
				"lower(master_table.column_name) r_column_name,                       " +
				"lower(detail_table.TABLE_NAME)  table_name,                          " +
				"lower(detail_table.column_name) column_name,                         " +
				"lower(detail_table.owner) as table_schema,                           " +
				"lower(constraint_info.constraint_name) as constraint_name,           " +
				"constraint_info.delete_rule as delete_rule,                          " +
				"'' as update_rule                                                    " +
				"FROM user_constraints  constraint_info,                              " +
				"user_cons_columns detail_table,                                      " +
				"user_cons_columns master_table                                       " +
				"WHERE constraint_info.constraint_name = detail_table.constraint_name " +
				"AND constraint_info.r_constraint_name = master_table.constraint_name " +
				"AND detail_table.POSITION = master_table.POSITION                    " +
				"AND constraint_info.constraint_type = 'R'                            " +
				"AND lower(constraint_info.OWNER) = '" + v_schema.ToLower() + "'      " +
				v_filter +
				"ORDER BY constraint_info.constraint_name,                            " +
				"detail_table.table_name,                                             " +
				"detail_table.position ", "TableForeignKeys");

		}

		/// <summary>
		/// Get a datatable with all tables primary keys.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesPrimaryKeys(string p_schema, string p_table) {

			string v_filter = "";

			string v_curr_schema = "";

			if (p_table != null)
				v_filter = "where table_name = '" + p_table.ToLower() + "' ";

			if (p_schema == "") {
				v_curr_schema = v_schema;

				return v_connection.Query (
					"SELECT distinct *                                             " +
					"from ( select lower(cons.constraint_name) as constraint_name, " +
					"lower(cols.column_name) as column_name,                       " +
					"lower(cols.table_name) as table_name                          " +
					"FROM user_constraints cons,                                   " +
					"user_cons_columns cols                                        " +
					"WHERE cons.constraint_type = 'P'                              " +
					"AND cons.constraint_name = cols.constraint_name               " +
					"AND cons.owner = cols.owner                                   " +
					"ORDER BY cols.table_name,                                     " +
					"cons.constraint_name,                                         " +
					"cols.position)                                                " +
					v_filter, "TablePrimaryKeys");
			} 
			else {
				v_curr_schema = p_schema;

				return v_connection.Query (
					"SELECT distinct *                                             " +
					"from ( select lower(cons.constraint_name) as constraint_name, " +
					"lower(cols.column_name) as column_name,                       " +
					"lower(cols.table_name) as table_name                          " +
					"FROM all_constraints cons,                                    " +
					"all_cons_columns cols,                                        " +
					"all_tables t                                                  " +
					"WHERE cons.constraint_type = 'P'                              " +
					"AND t.table_name = cols.table_name                            " +
					"AND cons.constraint_name = cols.constraint_name               " +
					"AND cons.owner = cols.owner                                   " +
					"AND lower(cons.owner)='" + v_curr_schema.ToLower () + "'      " +
					"ORDER BY cols.table_name,                                     " +
					"cons.constraint_name,                                         " +
					"cols.position)                                                " +
					v_filter, "TablePrimaryKeys");
			}

		}

		/// <summary>
		/// Get a datatable with all tables unique constraints.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesUniques(string p_schema, string p_table) {
			
			string v_filter = "";

			string v_curr_schema = "";

			if (p_table != null)
				v_filter = "where table_name = '" + p_table.ToLower() + "' ";

			if (p_schema == "") {
				v_curr_schema = v_schema;

				return v_connection.Query (
					"SELECT distinct *                                             " +
					"from ( select lower(cons.constraint_name) as constraint_name, " +
					"lower(cols.column_name) as column_name,                       " +
					"lower(cols.table_name) as table_name                          " +
					"FROM user_constraints cons,                                   " +
					"user_cons_columns cols                                        " +
					"WHERE cons.constraint_type = 'U'                              " +
					"AND cons.constraint_name = cols.constraint_name               " +
					"AND cons.owner = cols.owner                                   " +
					"ORDER BY cols.table_name,                                     " +
					"cons.constraint_name,                                         " +
					"cols.position)                                                " +
					v_filter, "TablePrimaryKeys");

			} 
			else {
				v_curr_schema = p_schema;

				return v_connection.Query (
					"SELECT distinct *                                             " +
					"from ( select lower(cons.constraint_name) as constraint_name, " +
					"lower(cols.column_name) as column_name,                       " +
					"lower(cols.table_name) as table_name                          " +
					"FROM all_constraints cons,                                    " +
					"all_cons_columns cols,                                        " +
					"all_tables t                                                  " +
					"WHERE cons.constraint_type = 'U'                              " +
					"AND t.table_name = cols.table_name                            " +
					"AND cons.constraint_name = cols.constraint_name               " +
					"AND cons.owner = cols.owner                                   " +
					"AND lower(cons.owner)='" + v_curr_schema.ToLower () + "'      " +
					"ORDER BY cols.table_name,                                     " +
					"cons.constraint_name,                                         " +
					"cols.position)                                                " +
					v_filter, "TablePrimaryKeys");

			}

		}

		/// <summary>
		/// Get a datatable with all tables indexes.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesIndexes(string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(c.table_name) = '" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"select lower(t.table_name) as table_name,                        " +
				"lower(t.index_name) as index_name,                               " +
				"lower(c.column_name) as column_name,                             " +
				"case when t.uniqueness='UNIQUE' then 'Unique'                    " +
				"else 'Non Unique' end as uniqueness                              " +
				"from all_indexes t,                                              " +
				"all_ind_columns c                                                " +
				"where t.table_name = c.table_name                                " +
				"  and t.index_name = c.index_name                                " +
				"  and lower(t.owner)='" + v_schema.ToLower() + "'                " +
				"  and t.owner = c.index_owner                                    " +
				v_filter +
				"order by t.table_name, t.index_name", "TableIndexes");

		}

		/// <summary>
		/// Query limited number of records.
		/// </summary>
		/// <param name="p_query">Query string.</param>
		/// <param name="p_count">Max number of records.</param>
		public override System.Data.DataTable QueryDataLimited(string p_query, int p_count) {

			string v_filter = "";
			if (p_count != -1)
				v_filter = "where rownum <= " + p_count;

			return v_connection.Query (
				"select *                        " +
				"from ( " + p_query + " ) t      " +
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
				v_filter = "where rownum <= " + p_count;

			return v_connection.QuerySList(
				"select *                        " +
				"from ( " + p_query + " ) t      " +
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

			string v_filter = "";

			if (p_count != -1)
				v_filter = " where rownum <= " + p_count;

			return v_connection.Query (
				"select * from ( select  " +
				p_column_list + "        " +
				"from " + p_table + "  t " +
				p_filter + " )           " +
				v_filter, "Limited Query");

		}

		/// <summary>
		/// Get a datatable with all functions.
		/// </summary>
		public override System.Data.DataTable QueryFunctions() {

            return v_connection.Query(
                "select t.object_name as id, " +
                "       lower(t.object_name) as name                 " +
                "from all_procedures t                               " +
                "where t.object_type = 'FUNCTION'                    " +
                "  and lower(t.owner) = '" + v_schema.ToLower() + "' " +
                "order by 2", "Functions");

		}

        /// <summary>
        /// Get a datatable with all fields of a function.
        /// </summary>
        public override System.Data.DataTable QueryFunctionFields(string p_function) {

            return v_connection.Query(
                "select (case t.in_out                                                     " +
                "          when 'IN' then 'I'                                              " +
                "          when 'OUT' then 'O'                                             " +
                "          else 'R'                                                        " +
                "        end) as type,                                                     " +
                "       (case when t.position = 0                                          " +
                "             then 'return ' || lower(t.data_type)                         " +
                "             else lower(t.argument_name) || ' ' || lower(t.data_type)     " +
                "        end) as name                                                      " +
                "from all_arguments t                                                      " +
                "where lower(t.owner) = '" + v_schema.ToLower() + "'                       " +
                "  and lower(t.object_name) = '" + p_function.ToLower() + "'               " +
                "order by 1 desc", "FunctionFields");

        }

		/// <summary>
		/// Get function definition.
		/// </summary>
		public override string GetFunctionDefinition(string p_function) {

            string v_body;

            v_body = "-- DROP FUNCTION " + p_function + ";\n";
            v_body += v_connection.ExecuteScalar("select dbms_metadata.get_ddl('FUNCTION','" + p_function + "') from dual");

            return v_body;

		}

        /// <summary>
        /// Get a datatable with all procedures.
        /// </summary>
        public override System.Data.DataTable QueryProcedures() {

            return v_connection.Query(
                "select t.object_name as id, " +
                "       lower(t.object_name) as name                 " +
                "from all_procedures t                               " +
                "where t.object_type = 'PROCEDURE'                   " +
                "  and lower(t.owner) = '" + v_schema.ToLower() + "' " +
                "order by 2", "Procedures");

        }

        /// <summary>
        /// Get a datatable with all fields of a procedure.
        /// </summary>
        public override System.Data.DataTable QueryProcedureFields(string p_procedure) {

            return v_connection.Query(
                "select (case t.in_out                                                     " +
                "          when 'IN' then 'I'                                              " +
                "          when 'OUT' then 'O'                                             " +
                "          else 'R'                                                        " +
                "        end) as type,                                                     " +
                "       lower(t.argument_name) || ' ' || lower(t.data_type) as name        " +
                "from all_arguments t                                                      " +
                "where lower(t.owner) = '" + v_schema.ToLower() + "'                       " +
                "  and lower(t.object_name) = '" + p_procedure.ToLower() + "' ", "ProcedureFields");

        }

        /// <summary>
        /// Get procedure definition.
        /// </summary>
        public override string GetProcedureDefinition(string p_procedure) {

            string v_body;

            v_body = "-- DROP PROCEDURE " + p_procedure + ";\n";
            v_body += v_connection.ExecuteScalar("select dbms_metadata.get_ddl('PROCEDURE','" + p_procedure + "') from dual");

            return v_body;

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