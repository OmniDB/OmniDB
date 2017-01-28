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
	/// Class to store information of an Firebird database.
	/// </summary>
	public class Firebird : Generic
	{
		/// <summary>
		/// Initializes a new instance of the <see cref="OmniDB.Database.Firebird"/> class.
		/// </summary>
		/// <param name="p_server">Connection address.</param>
		/// <param name="p_port">Connection port.</param>
		/// <param name="p_service">Database name.</param>
		/// <param name="p_user">Database user.</param>
		/// <param name="p_password">Database password.</param>
		public Firebird (string p_conn_id, string p_server, string p_port, string p_service, string p_user, string p_password)
			: base ("firebird",p_conn_id)
		{

			if (p_service.Contains("/")) {

				string []v_strings = p_service.Split ('/');

				v_service = v_strings [v_strings.Length - 1];

			}
			else
				v_service = p_service;

			v_server = p_server;
			v_port   = p_port;
			v_user = p_user;
			v_has_schema = false;
			v_has_update_rule = true;
			v_schema = "";

			v_default_string = "BLOB SUB_TYPE TEXT";

			v_can_rename_table = false;

			v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)";
			v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#";
			v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)";

			v_can_alter_type = true;
			v_alter_type_command = "alter table #p_table_name# alter #p_column_name# type #p_new_data_type#";

			v_can_alter_nullable = false;

			v_can_rename_column = true;
			v_rename_column_command = "alter table #p_table_name# alter #p_column_name# to #p_new_column_name#";

			v_can_add_column = true;
			v_add_column_command = "alter table #p_table_name# add #p_column_name# #p_data_type# #p_nullable#";

			v_can_drop_column = true;
			v_drop_column_command = "alter table #p_table_name# drop #p_column_name#";

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
			v_transfer_block_size.Add (10);
			v_transfer_block_size.Add (20);
			v_transfer_block_size.Add (30);
			v_transfer_block_size.Add (40);

			v_connection = new Spartacus.Database.Firebird (p_server, p_port, p_service, p_user, p_password);
			v_connection.v_execute_security = false;

			v_has_functions = false;
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

			return v_user + "@" + v_service;

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

			if (p_update_rule.Trim() != "RESTRICT" && p_update_rule.Trim() != "")
				v_rules += " on update " + p_update_rule + " ";
			if (p_delete_rule.Trim() != "RESTRICT" && p_delete_rule.Trim() != "")
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

			return v_connection.Query (
				"select lower(trim(r.rdb$relation_name)) as table_name      " +
				"from rdb$relations r                                       " +
				"where r.rdb$view_blr is null                               " +
				"  and (r.rdb$system_flag is null or r.rdb$system_flag = 0) " +
				"order by r.rdb$relation_name", "Tables");

		}

		/// <summary>
		/// Get a datatable with all views.
		/// </summary>
		public override System.Data.DataTable QueryViews() {

			return v_connection.Query (
				"select trim(r.rdb$relation_name) as view_name                        " +
				"from rdb$relations r                                                 " +
				"where r.rdb$view_blr is not null                                     " +
				"and (r.rdb$system_flag is null or r.rdb$system_flag = 0)", "Views");

		}

		/// <summary>
		/// Get a datatable with all tables fields.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesFields(string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(trim(r.rdb$relation_name))='" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"SELECT lower(trim(r.rdb$relation_name)) as table_name,                                     " +
				"lower(trim(r.RDB$FIELD_NAME)) AS column_name,                                              " +
				"CASE WHEN f.RDB$FIELD_TYPE=261 THEN trim('blob')                                           " +
				"WHEN f.RDB$FIELD_TYPE=14 THEN trim('char')                                                 " +
				"WHEN f.RDB$FIELD_TYPE=40 THEN trim('cstring')                                              " +
				"WHEN f.RDB$FIELD_TYPE=11 THEN trim('d_float')                                              " +
				"WHEN f.RDB$FIELD_TYPE=27 THEN trim('double')                                               " +
				"WHEN f.RDB$FIELD_TYPE=10 THEN trim('float')                                                " +
				"WHEN f.RDB$FIELD_TYPE=16 and f.RDB$FIELD_SUB_TYPE=0 THEN trim('bigint')                    " +
				"WHEN f.RDB$FIELD_TYPE=16 and f.RDB$FIELD_PRECISION=0 THEN trim('integer')                  " +
				"WHEN f.RDB$FIELD_TYPE=16 and f.RDB$FIELD_SUB_TYPE=1 THEN trim('numeric')                   " +
				"WHEN f.RDB$FIELD_TYPE=16 and f.RDB$FIELD_SUB_TYPE=2 THEN trim('decimal')                   " +
				"WHEN f.RDB$FIELD_TYPE=8 THEN trim('integer')                                               " +
				"WHEN f.RDB$FIELD_TYPE=9 THEN trim('quad')                                                  " +
				"WHEN f.RDB$FIELD_TYPE=7 THEN trim('smallint')                                              " +
				"WHEN f.RDB$FIELD_TYPE=12 THEN trim('date')                                                 " +
				"WHEN f.RDB$FIELD_TYPE=13 THEN trim('time')                                                 " +
				"WHEN f.RDB$FIELD_TYPE=35 THEN trim('timestamp')                                            " +
				"WHEN f.RDB$FIELD_TYPE=37 THEN trim('varchar')                                              " +
				"ELSE trim('unknown')                                                                       " +
				"END AS data_type,                                                                          " +
				"CASE r.RDB$NULL_FLAG WHEN 1 THEN 'NO'                                                      " +
				"ELSE 'YES' END as nullable,                                                                " +
				"f.RDB$FIELD_LENGTH AS data_length,                                                         " +
				"18 as data_precision,                                                                      " +
				"ABS(f.RDB$FIELD_SCALE) as data_scale                                                       " +
				"FROM RDB$RELATION_FIELDS r LEFT JOIN RDB$FIELDS f ON r.RDB$FIELD_SOURCE = f.RDB$FIELD_NAME " +
				"WHERE r.RDB$RELATION_NAME in (select r.rdb$relation_name                                   " +
				"from rdb$relations r                                                                       " +
				"where r.rdb$view_blr is null                                                               " +
				"and (r.rdb$system_flag is null or r.rdb$system_flag = 0))                                  " +
				v_filter +
				"ORDER BY r.rdb$relation_name", "TableFields");

		}

		/// <summary>
		/// Get a datatable with all tables foreign keys.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesForeignKeys(string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(trim(FK.RDB$RELATION_NAME)) = '" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"select lower(trim(PK.RDB$RELATION_NAME)) as r_table_name, " +
				"lower(trim(ISP.RDB$FIELD_NAME)) as r_column_name,         " +
				"lower(trim(FK.RDB$RELATION_NAME)) as table_name,          " +
				"lower(trim(ISF.RDB$FIELD_NAME)) as column_name,           " +
				"lower(trim(PK.RDB$CONSTRAINT_NAME)) as r_constraint_name, " +
				"lower(trim(FK.RDB$CONSTRAINT_NAME)) as constraint_name,   " +
				"RC.RDB$UPDATE_RULE as update_rule,                        " +
				"RC.RDB$DELETE_RULE as delete_rule                         " +
				"from RDB$RELATION_CONSTRAINTS PK,                         " +
				"RDB$RELATION_CONSTRAINTS FK,                              " +
				"RDB$REF_CONSTRAINTS RC,                                   " +
				"RDB$INDEX_SEGMENTS ISP,                                   " +
				"RDB$INDEX_SEGMENTS ISF                                    " +
				"WHERE FK.RDB$CONSTRAINT_NAME = RC.RDB$CONSTRAINT_NAME     " +
				"and PK.RDB$CONSTRAINT_NAME = RC.RDB$CONST_NAME_UQ         " +
				"and ISP.RDB$INDEX_NAME = PK.RDB$INDEX_NAME                " +
				"and ISF.RDB$INDEX_NAME = FK.RDB$INDEX_NAME                " +
				"and ISP.RDB$FIELD_POSITION = ISF.RDB$FIELD_POSITION       " +
				v_filter +
				"order by FK.RDB$CONSTRAINT_NAME,ISP.RDB$FIELD_POSITION", "TableForeignKeys");

		}

		/// <summary>
		/// Get a datatable with all tables primary keys.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesPrimaryKeys(string p_schema,string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(trim(rc.rdb$relation_name)) = '" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"select                                                                        " +
				"lower(trim(rc.rdb$constraint_name)) as constraint_name,                       " +
				"lower(trim(s.rdb$field_name)) as column_name,                                 " +
				"lower(trim(rc.rdb$relation_name)) as table_name                               " +
				"from rdb$indices i                                                            " +
				"left join rdb$index_segments s on i.rdb$index_name = s.rdb$index_name         " +
				"left join rdb$relation_constraints rc on rc.rdb$index_name = i.rdb$index_name " +
				"where rc.rdb$constraint_type = 'PRIMARY KEY'                                  " +
				v_filter +
				"order by rc.rdb$relation_name,                                                " +
				"s.rdb$field_position", "TableForeignKeys");

		}

		/// <summary>
		/// Get a datatable with all tables unique constraints.
		/// </summary>
		/// <param name="p_schema">Schema name.</param>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesUniques(string p_schema, string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(trim(rc.rdb$relation_name)) = '" + p_table.ToLower() + "' ";

			return v_connection.Query (
				"select lower(trim(rc.rdb$constraint_name)) as constraint_name,                " +
				"lower(trim(s.rdb$field_name)) as column_name,                                 " +
				"lower(trim(rc.rdb$relation_name)) as table_name                               " +
				"from rdb$indices i                                                            " +
				"left join rdb$index_segments s on i.rdb$index_name = s.rdb$index_name         " +
				"left join rdb$relation_constraints rc on rc.rdb$index_name = i.rdb$index_name " +
				"where rc.rdb$constraint_type = 'UNIQUE'                                       " +
				v_filter +
				"order by rc.rdb$relation_name", "TableUniques");

		}

		/// <summary>
		/// Get a datatable with all tables indexes.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesIndexes(string p_table) {

			string v_filter = "";

			if (p_table != null)
				v_filter = "and lower(trim(rdb$indices.rdb$relation_name)) = '" + p_table.ToLower() + "' ";
			
			return v_connection.Query(
				"select lower(trim(rdb$indices.rdb$relation_name)) as table_name,               " +
				"lower(trim(rdb$indices.rdb$index_name)) as index_name,                         " +
				"lower(trim(rdb$index_segments.rdb$field_name)) as column_name,                 " +
				"(case when rdb$indices.rdb$unique_flag is not null                             " +
				"	and rdb$indices.rdb$unique_flag = 1                                         " +
				"	then 'Unique'                                                               " +
				"	else 'Non Unique'                                                           " +
				"	end) as uniqueness                                                          " +
				"from rdb$index_segments                                                        " +
				"left join rdb$indices                                                          " +
				"on rdb$indices.rdb$index_name = rdb$index_segments.rdb$index_name              " +
				"left join rdb$relation_constraints                                             " +
				"on rdb$relation_constraints.rdb$index_name = rdb$index_segments.rdb$index_name " +
				"where rdb$relation_constraints.rdb$constraint_type is null                     " +
				"and rdb$indices.rdb$relation_name not like 'RDB$%'                             " +
				v_filter,"TablesIndexes");
			
		}

		/// <summary>
		/// Query limited number of records.
		/// </summary>
		/// <param name="p_query">Query string.</param>
		/// <param name="p_count">Max number of records.</param>
		public override System.Data.DataTable QueryDataLimited(string p_query, int p_count) {

			string v_filter = "";
			if (p_count != -1)
				v_filter = " first  " + p_count;

			return v_connection.Query (
				"select " + v_filter + " * " +
				"from ( " + p_query + " )", "Limited Query");

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
				v_limit = " first  " + p_count;

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

            return v_connection.Query(
                "select lower(t.rdb$procedure_name) as id,  " +
                "       lower(t.rdb$procedure_name) as name " +
                "from rdb$procedures t                      " +
                "order by 1", "Procedures");

        }

        /// <summary>
        /// Get a datatable with all fields of a procedure.
        /// </summary>
        public override System.Data.DataTable QueryProcedureFields(string p_procedure) {

            return v_connection.Query(
                "select lower(t.rdb$parameter_name) || ' ' ||              " +
                "       case f.rdb$field_type                              " +
                "         when 261 then 'blob'                             " +
                "         when 14 then 'char'                              " +
                "         when 40 then 'cstring'                           " +
                "         when 11 then 'd_float'                           " +
                "         when 27 then 'double'                            " +
                "         when 10 then 'float'                             " +
                "         when 16 then 'int64'                             " +
                "         when 8 then 'integer'                            " +
                "         when 9 then 'quad'                               " +
                "         when 7 then 'smallint'                           " +
                "         when 12 then 'date'                              " +
                "         when 13 then 'time'                              " +
                "         when 35 then 'timestamp'                         " +
                "         when 37 then 'varchar'                           " +
                "         else 'unknown'                                   " +
                "       end as name,                                       " +
                "       case t.rdb$parameter_type                          " +
                "         when 0 then 'I'                                  " +
                "         else 'O'                                         " +
                "       end as type                                        " +
                "from rdb$procedure_parameters t,                          " +
                "     rdb$fields f                                         " +
                "where f.rdb$field_name = t.rdb$field_source               " +
                "  and lower(t.rdb$procedure_name) = '" + p_procedure + "' " +
                "order by 2 desc", "ProcedureFields");

        }

        /// <summary>
        /// Get procedure definition.
        /// </summary>
        public override string GetProcedureDefinition(string p_procedure) {

            string v_body, v_input, v_output;
            System.Data.DataTable v_table;
            int v_num_input, v_num_output;

            v_table = this.QueryProcedureFields(p_procedure);

            v_input = "";
            v_num_input = 0;
            v_output = "";
            v_num_output = 0;

            foreach (System.Data.DataRow v_row in v_table.Rows)
            {
                if (v_row["type"].ToString() == "I")
                {
                    if (v_num_input == 0)
                        v_input += System.Text.RegularExpressions.Regex.Replace(v_row["name"].ToString(), @"\s+", " ").Trim();
                    else
                        v_input += ", " + System.Text.RegularExpressions.Regex.Replace(v_row["name"].ToString(), @"\s+", " ").Trim();
                    v_num_input++;
                }
                else
                {
                    if (v_num_output == 0)
                        v_output += System.Text.RegularExpressions.Regex.Replace(v_row["name"].ToString(), @"\s+", " ").Trim();
                    else
                        v_output += ", " + System.Text.RegularExpressions.Regex.Replace(v_row["name"].ToString(), @"\s+", " ").Trim();
                    v_num_output++;
                }
            }

            v_body = "-- DROP PROCEDURE " + p_procedure.Trim() + ";\n";
            v_body += "CREATE OR ALTER PROCEDURE " + p_procedure.Trim() + " (" + v_input + ")\n";
            if (v_num_output > 0)
                v_body += "RETURNS (" + v_output + ")\n";
            v_body += "AS\n";

            v_body += v_connection.ExecuteScalar(
                "select t.rdb$procedure_source                             " +
                "from rdb$procedures t                                     " +
                "where lower(t.rdb$procedure_name) = '" + p_procedure + "' ");

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
