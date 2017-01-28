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
    /// Class to store information of an MariaDB database.
    /// </summary>
    public class MariaDB : Generic
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="OmniDB.Database.MariaDB"/> class.
        /// </summary>
        /// <param name="p_server">Connection address.</param>
        /// <param name="p_port">Connection port.</param>
        /// <param name="p_service">Database name.</param>
        /// <param name="p_user">Database user.</param>
        /// <param name="p_password">Database password.</param>
        /// <param name="p_schema">Schema.</param>
        public MariaDB (string p_conn_id, string p_server, string p_port, string p_service, string p_user, string p_password)
            : base ("mariadb",p_conn_id)
        {

            v_server = p_server;
            v_port   = p_port;
            v_service = p_service;
            v_user = p_user;
            v_has_schema = false;
            v_schema = "";

            v_has_update_rule = true;

            v_default_string = "varchar(500)";

            v_can_rename_table = true;
            v_rename_table_command = "alter table #p_table_name# rename to #p_new_table_name#";

            v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)";
            v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#";
            v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)";

            v_can_alter_type = true;
            v_alter_type_command = "alter table #p_table_name# modify #p_column_name# #p_new_data_type#";

            v_can_alter_nullable = true;
            v_set_nullable_command = "alter table #p_table_name# modify #p_column_name# #p_new_data_type#";
            v_drop_nullable_command = "alter table #p_table_name# modify #p_column_name# #p_new_data_type# not null";

            v_can_rename_column = true;
            v_rename_column_command = "alter table #p_table_name# change column #p_column_name# #p_new_column_name# #p_new_data_type# #p_new_nullable#";

            v_can_add_column = true;
            v_add_column_command = "alter table #p_table_name# add column #p_column_name# #p_data_type# #p_nullable#";

            v_can_drop_column = true;
            v_drop_column_command = "alter table #p_table_name# drop #p_column_name#";

            v_can_add_constraint = true;
            v_add_pk_command = "alter table #p_table_name# add constraint #p_constraint_name# primary key (#p_columns#)";
            v_add_fk_command = "alter table #p_table_name# add constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#";
            v_add_unique_command = "alter table #p_table_name# add constraint #p_constraint_name# unique (#p_columns#)";

            v_can_drop_constraint = true;
            v_drop_pk_command = "alter table #p_table_name# drop primary key";
            v_drop_fk_command = "alter table #p_table_name# drop foreign key #p_constraint_name#";
            v_drop_unique_command = "alter table #p_table_name# drop index #p_constraint_name#";

            v_create_index_command = "create index #p_index_name# on #p_table_name# (#p_columns#)";
            v_create_unique_index_command = "create unique index #p_index_name# on #p_table_name# (#p_columns#)";

            v_drop_index_command = "drop index #p_index_name# on #p_table_name#";

            v_update_rules = new System.Collections.Generic.List<string> ();
            v_delete_rules = new System.Collections.Generic.List<string> ();

            v_delete_rules.Add ("");
            v_delete_rules.Add ("NO ACTION");
            v_delete_rules.Add ("RESTRICT");
            v_delete_rules.Add ("SET NULL");
            v_delete_rules.Add ("CASCADE");

            v_update_rules.Add ("");
            v_update_rules.Add ("NO ACTION");
            v_update_rules.Add ("RESTRICT");
            v_update_rules.Add ("SET NULL");
            v_update_rules.Add ("CASCADE");

            v_trim_function = "trim";

            v_transfer_block_size = new System.Collections.Generic.List<uint> ();
            v_transfer_block_size.Add (50);
            v_transfer_block_size.Add (100);
            v_transfer_block_size.Add (200);
            v_transfer_block_size.Add (400);

            v_connection = new Spartacus.Database.Mariadb (p_server, p_port, p_service, p_user, p_password);
            v_connection.v_execute_security = false;

            v_has_functions = true;
            v_has_procedures = true;
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
                v_filter = " and lower(table_schema) = '" + v_service.ToLower() + "'";

            return v_connection.Query (
                "select table_name as table_name " +
                "from information_schema.tables  " +
                "where table_type = 'BASE TABLE' " +
                v_filter, "Tables");

        }

        /// <summary>
        /// Get a datatable with all views.
        /// </summary>
        public override System.Data.DataTable QueryViews() {

            return v_connection.Query (
                "select lower(table_name) as view_name, " +
                "'" + v_service + "' as table_schema    " +
                "from information_schema.tables         " +
                "where table_type = 'VIEW'              " +
                "AND lower(table_schema) = '" + v_service.ToLower() + "'", "Views");

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
                "select distinct c.table_name as table_name,               " +
                "lower(c.column_name) as column_name,                      " +
                "lower(c.data_type) as data_type,                          " +
                "c.is_nullable as nullable,                                " +
                "c.character_maximum_length as data_length,                " +
                "c.numeric_precision as data_precision,                    " +
                "c.numeric_scale as data_scale                             " +
                "from information_schema.columns c,                        " +
                "information_schema.tables t                               " +
                "where t.table_name = c.table_name                         " +
                "and lower(c.table_schema) = '" + v_service.ToLower() + "' " +
                "and t.table_type='BASE TABLE'                             " +
                v_filter +
                "order by c.table_name,                                    " +
                "c.ordinal_position", "TableFields");

        }

        /// <summary>
        /// Get a datatable with all tables foreign keys.
        /// </summary>
        /// <param name="p_table">Table name.</param>
        public override System.Data.DataTable QueryTablesForeignKeys(string p_table) {

            string v_filter = "";

            if (p_table != null)
                v_filter = "and lower(i.table_name) = '" + p_table.ToLower() + "' ";

            return v_connection.Query (
                "select lower(i.constraint_name) as constraint_name,                                             " +
                "i.table_name as table_name,                                                                     " +
                "k.referenced_table_name as r_table_name,                                                        " +
                "lower(k.column_name) as column_name,                                                            " +
                "lower(k.referenced_column_name) as r_column_name,                                               " +
                "lower(k.table_schema) as table_schema,                                                          " +
                "lower(k.referenced_table_schema) as r_table_schema,                                             " +
                "r.update_rule as update_rule,                                                                   " +
                "r.delete_rule as delete_rule                                                                    " +
                "from information_schema.table_constraints i                                                     " +
                "left join information_schema.key_column_usage k on i.constraint_name = k.constraint_name        " +
                "left join information_schema.referential_constraints r on i.constraint_name = r.constraint_name " +
                "where i.constraint_type = 'FOREIGN KEY'                                                         " +
                "and lower(i.table_schema)= '" + v_service.ToLower() + "'                                        " +
                v_filter + 
                "order by i.constraint_name,                                                                     " +
                "k.ordinal_position", "TableForeignKeys");

        }

        /// <summary>
        /// Get a datatable with all tables primary keys.
        /// </summary>
        /// <param name="p_schema">Schema name.</param>
        /// <param name="p_table">Table name.</param>
        public override System.Data.DataTable QueryTablesPrimaryKeys(string p_schema, string p_table) {

            string v_filter = "";

            if (p_table != null)
                v_filter = "and lower(k.table_name) = '" + p_table.ToLower() + "' ";

            return v_connection.Query (
                "SELECT concat('pk_',lower(k.table_name)) as constraint_name, " +
                "lower(k.column_name) as column_name,                         " +
                "k.table_name as table_name                                   " +
                "FROM information_schema.table_constraints t                  " +
                "JOIN information_schema.key_column_usage k                   " +
                "USING(constraint_name,table_schema,table_name)               " +
                "WHERE t.constraint_type='PRIMARY KEY'                        " +
                "AND lower(t.table_schema)='" + v_service.ToLower() + "'      " +
                v_filter +
                "order by k.table_name,                                       " +
                "k.ordinal_position", "TablePrimaryKeys");

        }

        /// <summary>
        /// Get a datatable with all tables unique constraints.
        /// </summary>
        /// <param name="p_schema">Schema name.</param>
        /// <param name="p_table">Table name.</param>
        public override System.Data.DataTable QueryTablesUniques(string p_schema, string p_table) {

            string v_filter = "";

            if (p_table != null)
                v_filter = "and lower(k.table_name) = '" + p_table.ToLower() + "' ";

            return v_connection.Query (
                "SELECT lower(k.constraint_name) as constraint_name,     " +
                "lower(k.column_name) as column_name,                    " +
                "k.table_name as table_name                              " +
                "FROM information_schema.table_constraints t             " +
                "JOIN information_schema.key_column_usage k              " +
                "USING(constraint_name,table_schema,table_name)          " +
                "WHERE t.constraint_type='UNIQUE'                        " +
                "AND lower(t.table_schema)='" + v_service.ToLower() + "' " +
                v_filter +
                "order by k.table_name,                                  " +
                "k.ordinal_position", "TableUniques");

        }

        /// <summary>
        /// Get a datatable with all tables indexes.
        /// </summary>
        /// <param name="p_table">Table name.</param>
        public override System.Data.DataTable QueryTablesIndexes(string p_table) {

            string v_filter = "";

            if (p_table != null)
                v_filter = "and lower(t.table_name) = '" + p_table.ToLower() + "' ";

            return v_connection.Query (
                "SELECT t.table_name AS table_name,                      " +
                "lower(t.index_name) AS index_name,                      " +
                "lower(t.column_name) AS column_name,                    " +
                "case when t.non_unique = 1 then 'Non Unique'            " +
                "else 'Unique'                                           " +
                "end as uniqueness                                       " +
                "FROM information_schema.statistics t                    " +
                "WHERE lower(table_schema)='" + v_service.ToLower() + "' " +
                v_filter +
                "order by t.table_name,                                  " +
                "         t.index_name,                                  " +
                "         t.seq_in_index", "TableIndexes");

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
                "select *                   " +
                "from ( " + p_query + " ) t " +
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
                "from " + p_table + " t       " +
                p_filter + "                  " +
                v_limit, "Limited Query");

        }

        /// <summary>
        /// Get a datatable with all functions.
        /// </summary>
        public override System.Data.DataTable QueryFunctions() {

            return v_connection.Query(
                "select t.routine_name as id,                      " +
                "       t.routine_name as name                     " +
                "from information_schema.routines t                " +
                "where t.routine_type = 'FUNCTION'                 " +
                "  and t.routine_schema = '" + this.v_service + "' " +
                "order by t.routine_name", "Functions");

        }

        /// <summary>
        /// Get a datatable with all fields of a function.
        /// </summary>
        public override System.Data.DataTable QueryFunctionFields(string p_function) {

            return v_connection.Query(
                "select concat('returns ', t.data_type) as name,            " +
                "       'O' as type                                         " +
                "from information_schema.routines t                         " +
                "where t.routine_type = 'FUNCTION'                          " +
                "  and t.routine_schema = '" + this.v_service + "'          " +
                "  and t.specific_name = '" + p_function + "'               " +
                "union                                                      " +
                "select concat(t.parameter_name, ' ', t.data_type) as name, " +
                "       (case t.parameter_mode                              " +
                "          when 'IN' then 'I'                               " +
                "          when 'OUT' then 'O'                              " +
                "          else 'R'                                         " +
                "        end) as type                                       " +
                "from information_schema.parameters t                       " +
                "where t.ordinal_position > 0                               " +
                "  and t.specific_schema = '" + this.v_service + "'         " +
                "  and t.specific_name = '" + p_function + "'               " +
                "order by 2 desc", "FunctionFields");


        }

        /// <summary>
        /// Get function definition.
        /// </summary>
        public override string GetFunctionDefinition(string p_function) {

            string v_body, v_input, v_output;
            System.Data.DataTable v_table;
            int v_num_input, v_num_output;

            v_table = this.QueryFunctionFields(p_function);

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

            v_body = "-- DROP FUNCTION " + p_function.Trim() + ";\n";
            v_body += "CREATE FUNCTION " + p_function.Trim() + " (" + v_input + ")\n";
            v_body += v_output + "\n";

            v_body += v_connection.ExecuteScalar(
                "select t.routine_definition                       " +
                "from information_schema.routines t                " +
                "where t.routine_type = 'FUNCTION'                 " +
                "  and t.routine_schema = '" + this.v_service + "' " +
                "  and t.routine_name = '" + p_function + "'");

            return v_body;

        }

        /// <summary>
        /// Get a datatable with all procedures.
        /// </summary>
        public override System.Data.DataTable QueryProcedures() {

            return v_connection.Query(
                "select t.routine_name as id,                      " +
                "       t.routine_name as name                     " +
                "from information_schema.routines t                " +
                "where t.routine_type = 'PROCEDURE'                " +
                "  and t.routine_schema = '" + this.v_service + "' " +
                "order by t.routine_name", "Procedures");

        }

        /// <summary>
        /// Get a datatable with all fields of a procedure.
        /// </summary>
        public override System.Data.DataTable QueryProcedureFields(string p_procedure) {

            return v_connection.Query(
                "select concat(t.parameter_name, ' ', t.data_type) as name, " +
                "       (case t.parameter_mode                              " +
                "          when 'IN' then 'I'                               " +
                "          when 'OUT' then 'O'                              " +
                "          else 'R'                                         " +
                "        end) as type                                       " +
                "from information_schema.parameters t                       " +
                "where t.specific_schema = '" + this.v_service + "'         " +
                "  and t.specific_name = '" + p_procedure + "'              " +
                "order by 2 desc", "ProcedureFields");

        }

        /// <summary>
        /// Get procedure definition.
        /// </summary>
        public override string GetProcedureDefinition(string p_procedure) {

            string v_body, v_input;
            System.Data.DataTable v_table;
            int v_num_input;

            v_table = this.QueryProcedureFields(p_procedure);

            v_input = "";
            v_num_input = 0;

            foreach (System.Data.DataRow v_row in v_table.Rows)
            {
                if (v_num_input == 0)
                    v_input += System.Text.RegularExpressions.Regex.Replace(v_row["name"].ToString(), @"\s+", " ").Trim();
                else
                    v_input += ", " + System.Text.RegularExpressions.Regex.Replace(v_row["name"].ToString(), @"\s+", " ").Trim();
                v_num_input++;
            }

            v_body = "-- DROP PROCEDURE " + p_procedure.Trim() + ";\n";
            v_body += "CREATE PROCEDURE " + p_procedure.Trim() + " (" + v_input + ")\n";

            v_body += v_connection.ExecuteScalar(
                "select t.routine_definition                       " +
                "from information_schema.routines t                " +
                "where t.routine_type = 'PROCEDURE'                " +
                "  and t.routine_schema = '" + this.v_service + "' " +
                "  and t.routine_name = '" + p_procedure + "'");

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
