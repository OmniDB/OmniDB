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
	/// Abstract class to store information of a generic database. Specific technologies inherit from this class.
	/// </summary>
	public abstract class Generic
	{
		/// <summary>
		/// Database alias, this will be referenced by cluster queries.
		/// </summary>
		public string v_alias;

		/// <summary>
		/// Connection ID
		/// </summary>
		public string v_conn_id;

		/// <summary>
		/// Technology of the database
		/// </summary>
		public string v_db_type;

		/// <summary>
		/// Connection address.
		/// </summary>
		public string v_server;

		/// <summary>
		/// Connection TCP port.
		/// </summary>
		public string v_port;

		/// <summary>
		/// Service name
		/// </summary>
		public string v_service;

		/// <summary>
		/// Schema name
		/// </summary>
		public string v_schema;

		/// <summary>
		/// Database user.
		/// </summary>
		public string v_user;

		//public System.Data.DataRow v_data;

		/// <summary>
		/// Database connection.
		/// </summary>
		public Spartacus.Database.Generic v_connection;

		/// <summary>
		/// Default string datatype.
		/// </summary>
		public string v_default_string;

		/// <summary>
		/// If technology supports schemas.
		/// </summary>
		public bool v_has_schema;

		/// <summary>
		/// If technology supports renaming table with ALTER TABLE commands.
		/// </summary>
		public bool v_can_rename_table;

		/// <summary>
		/// ALTER TABLE command to rename table.
		/// </summary>
		public string v_rename_table_command;

		/// <summary>
		/// CREATE TABLE command to add Primary Key.
		/// </summary>
		public string v_create_pk_command;

		/// <summary>
		/// CREATE TABLE command to add Foreign Key.
		/// </summary>
		public string v_create_fk_command;

		/// <summary>
		/// CREATE TABLE command to add Unique.
		/// </summary>
		public string v_create_unique_command;

		/// <summary>
		/// If technology supports renaming column with ALTER TABLE commands.
		/// </summary>
		public bool v_can_rename_column;

		/// <summary>
		/// ALTER TABLE command to rename column.
		/// </summary>
		public string v_rename_column_command;

		/// <summary>
		/// If technology supports changing column type with ALTER TABLE commands.
		/// </summary>
		public bool v_can_alter_type;

		/// <summary>
		/// ALTER TABLE command to change column type.
		/// </summary>
		public string v_alter_type_command;

		/// <summary>
		/// If technology supports changing column nullable with ALTER TABLE commands.
		/// </summary>
		public bool v_can_alter_nullable;

		/// <summary>
		/// ALTER TABLE command to set column as null.
		/// </summary>
		public string v_set_nullable_command;

		/// <summary>
		/// ALTER TABLE command to set column as not null.
		/// </summary>
		public string v_drop_nullable_command;

		/// <summary>
		/// If technology supports adding column with ALTER TABLE commands.
		/// </summary>
		public bool v_can_add_column;

		/// <summary>
		/// ALTER TABLE command to add new column.
		/// </summary>
		public string v_add_column_command;

		/// <summary>
		/// If technology supports dropping column with ALTER TABLE commands.
		/// </summary>
		public bool v_can_drop_column;

		/// <summary>
		/// ALTER TABLE command to drop column.
		/// </summary>
		public string v_drop_column_command;

		/// <summary>
		/// If technology supports adding constraint with ALTER TABLE commands.
		/// </summary>
		public bool v_can_add_constraint;

		/// <summary>
		/// ALTER TABLE command to add primary key.
		/// </summary>
		public string v_add_pk_command;

		/// <summary>
		/// ALTER TABLE command to add foreign key.
		/// </summary>
		public string v_add_fk_command;

		/// <summary>
		/// ALTER TABLE command to add unique.
		/// </summary>
		public string v_add_unique_command;

		/// <summary>
		/// If technology supports dropping constraint with ALTER TABLE commands.
		/// </summary>
		public bool v_can_drop_constraint;

		/// <summary>
		/// ALTER TABLE command to drop primary key.
		/// </summary>
		public string v_drop_pk_command;

		/// <summary>
		/// ALTER TABLE command to drop foreign key.
		/// </summary>
		public string v_drop_fk_command;

		/// <summary>
		/// ALTER TABLE command to drop unique.
		/// </summary>
		public string v_drop_unique_command;

		/// <summary>
		/// CREATE INDEX command.
		/// </summary>
		public string v_create_index_command;

		/// <summary>
		/// CREATE UNIQUE INDEX command.
		/// </summary>
		public string v_create_unique_index_command;

		/// <summary>
		/// DROP INDEX command.
		/// </summary>
		public string v_drop_index_command;

		/// <summary>
		/// TRIM function.
		/// </summary>
		public string v_trim_function;

		/// <summary>
		/// If technology has update rule.
		/// </summary>
		public bool v_has_update_rule;

		/// <summary>
		/// Transfer block size.
		/// </summary>
		public System.Collections.Generic.List<uint> v_transfer_block_size;

		/// <summary>
		/// Foreign Key Update Rules.
		/// </summary>
		public System.Collections.Generic.List<string> v_update_rules;

		/// <summary>
		/// Foreign Key Delete Rules.
		/// </summary>
		public System.Collections.Generic.List<string> v_delete_rules;

		/// <summary>
		/// If technology supports custom functions.
		/// </summary>
		public bool v_has_functions;

        /// <summary>
        /// If technology supports custom procedures.
        /// </summary>
        public bool v_has_procedures;

		/// <summary>
		/// If technology supports sequences.
		/// </summary>
		public bool v_has_sequences;

		/// <summary>
		/// ALTER TABLE command to create sequence.
		/// </summary>
		public string v_create_sequence_command;

		/// <summary>
		/// ALTER TABLE command to alter sequence.
		/// </summary>
		public string v_alter_sequence_command;

		/// <summary>
		/// If technology supports renaming sequence with ALTER SEQUENCE commands.
		/// </summary>
		public bool v_can_rename_sequence;

		/// <summary>
		/// ALTER TABLE command to rename sequence.
		/// </summary>
		public string v_rename_sequence_command;

		/// <summary>
		/// If technology supports altering sequence min value.
		/// </summary>
		public bool v_can_alter_sequence_min_value;

		/// <summary>
		/// If technology supports altering sequence min value.
		/// </summary>
		public bool v_can_alter_sequence_max_value;

		/// <summary>
		/// If technology supports altering sequence min value.
		/// </summary>
		public bool v_can_alter_sequence_curr_value;

		/// <summary>
		/// If technology supports altering sequence min value.
		/// </summary>
		public bool v_can_alter_sequence_increment;


		/// <summary>
		/// Initializes a new instance of the <see cref="OmniDB.Database.Generic"/> class.
		/// </summary>
		/// <param name="p_db_type">Technology.</param>
		public Generic(string p_db_type, string p_conn_id)
		{
			v_db_type = p_db_type;
			v_conn_id = p_conn_id;
		}

		/// <summary>
		/// Instantiates a database.
		/// </summary>
		/// <returns>The database.</returns>
		/// <param name="p_db_type">P db type.</param>
		/// <param name="p_server">Connection address.</param>
		/// <param name="p_port">Connection port.</param>
		/// <param name="p_service">Database name.</param>
		/// <param name="p_user">Database user.</param>
		/// <param name="p_password">Database password.</param>
		/// <param name="p_schema">Schema.</param>
		public static Generic InstantiateDatabase(string p_alias, string p_conn_id, string p_db_type, string p_server, string p_port, string p_service, string p_user, string p_password,string p_schema) {

			OmniDatabase.Generic v_database;

			switch (p_db_type)
			{
    			case "oracle":
    				v_database = new Oracle (p_conn_id, p_server, p_port, p_service, p_user, p_password);
    				break;
    			case "firebird":
    				v_database = new Firebird(p_conn_id,p_server,p_port,p_service,p_user,p_password);
    				break;
    			case "mysql":
    				v_database = new MySQL(p_conn_id,p_server,p_port,p_service,p_user,p_password);
    				break;
    			case "postgresql":
    				v_database = new PostgreSQL(p_conn_id,p_server,p_port,p_service,p_user,p_password,p_schema);
    				break;
    			case "sqlite":
    				v_database = new SQLite(p_conn_id,p_service);
    				break;
    			case "sqlserver":
    				v_database = new SqlServer(p_conn_id,p_server,p_port,p_service,p_user,p_password,p_schema);
    				break;
    			case "access":
    				v_database = new Access (p_conn_id, p_service);
    				break;
                case "sqlce":
                    v_database = new SqlCe(p_conn_id, p_service);
                    break;
                case "mariadb":
                    v_database = new MariaDB(p_conn_id, p_server, p_port, p_service, p_user, p_password);
                    break;
    			default:
    				return null;
			}

			v_database.v_alias = p_alias;

			return v_database;

		}

		/// <summary>
		/// Get a datatable with all tables.
		/// </summary>
		public abstract System.Data.DataTable QueryTables(bool p_all_schemas);

		/// <summary>
		/// Get a datatable with all views.
		/// </summary>
		public abstract System.Data.DataTable QueryViews();

		/// <summary>
		/// Get a datatable with all tables.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public abstract System.Data.DataTable QueryTablesFields(string p_table);

		/// <summary>
		/// Get a datatable with all tables foreign keys.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public abstract System.Data.DataTable QueryTablesForeignKeys(string p_table);

		/// <summary>
		/// Get a datatable with all tables primary keys.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public abstract System.Data.DataTable QueryTablesPrimaryKeys(string p_schema, string p_table);

		/// <summary>
		/// Get a datatable with all tables unique constraints.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public abstract System.Data.DataTable QueryTablesUniques(string p_schema, string p_table);

		/// <summary>
		/// Get a datatable with all tables indexes.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public abstract System.Data.DataTable QueryTablesIndexes(string p_table);

		/// <summary>
		/// Query limited number of records.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public abstract System.Data.DataTable QueryDataLimited(string p_query, int p_count);

		/// <summary>
		/// Query limited number of records.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public abstract System.Data.DataTable QueryTableRecords(string p_column_list, string p_table, string p_filter, int p_count);

		/// <summary>
		/// Create update and delete rules.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public abstract string HandleUpdateDeleteRules(string p_update_rule, string p_delete_rule);

		/// <summary>
		/// Test connection.
		/// </summary>
		public abstract string TestConnection();

		/// <summary>
		/// Get a datatable with all functions.
		/// </summary>
		public abstract System.Data.DataTable QueryFunctions();

        /// <summary>
        /// Get a datatable with all fields of a function.
        /// </summary>
        public abstract System.Data.DataTable QueryFunctionFields(string p_function);

		/// <summary>
		/// Get function definition.
		/// </summary>
		public abstract string GetFunctionDefinition(string p_function);

        /// <summary>
        /// Get a datatable with all procedures.
        /// </summary>
        public abstract System.Data.DataTable QueryProcedures();

        /// <summary>
        /// Get a datatable with all fields of a procedure.
        /// </summary>
        public abstract System.Data.DataTable QueryProcedureFields(string p_procedure);

        /// <summary>
        /// Get procedure definition.
        /// </summary>
        public abstract string GetProcedureDefinition(string p_function);

		/// <summary>
		/// Get a datatable with sequences.
		/// </summary>
		public abstract System.Data.DataTable QuerySequences(string p_sequence);

		/// <summary>
		/// Count all tables records.
		/// </summary>
		public System.Data.DataTable CountTablesRecords() 
		{

			System.Data.DataTable v_tables = QueryTables (false);

			System.Data.DataTable v_count_total_table = new System.Data.DataTable();

			int v_timeout = v_connection.v_timeout;

			v_connection.SetTimeout (0);

			string v_sql = "";

			bool v_first = true;

			int v_block_counter = 0;

			for (int j = 0; j < v_tables.Rows.Count; j++)
			{

				if (!v_first)
					v_sql += " union all ";

				v_first = false;

				v_block_counter++;


				string v_table_name = "";

				if (v_has_schema)
					v_table_name = v_schema + "." + v_tables.Rows [j] ["table_name"].ToString ();
				else
					v_table_name = v_tables.Rows [j] ["table_name"].ToString ();


				v_sql += "select count(*) as total, " + v_trim_function + "('" + v_tables.Rows [j] ["table_name"].ToString () + "') as table_name from " + v_table_name + " ";

	


				if (v_block_counter>=50 || (j==v_tables.Rows.Count-1)) {

					if (v_count_total_table==null)
						v_count_total_table = v_connection.Query (v_sql,"t1");
					else
						v_count_total_table.Merge(v_connection.Query (v_sql,"t1"));
					v_first=true;
					v_block_counter=0;

					v_sql = "";



				}

			}

			System.Data.DataTable dt2 = v_count_total_table.Clone();
			dt2.Columns["total"].DataType = Type.GetType("System.Int32");

			foreach (System.Data.DataRow dr in v_count_total_table.Rows)
			{
				dt2.ImportRow(dr);
			}

			dt2.AcceptChanges();
			System.Data.DataView dv = dt2.DefaultView;
			dv.Sort = "total DESC";

			v_count_total_table = dv.ToTable();

			v_connection.SetTimeout (v_timeout);

			return v_count_total_table;

		}

		/// <summary>
		/// Count all tables records.
		/// </summary>
		/// <param name="p_tables">List of table names.</param>
		/// <param name="p_filters">List of table filters.</param>
		public System.Data.DataTable CountTablesRecords(System.Collections.Generic.List<string> p_tables, System.Collections.Generic.List<string> p_filters) 
		{
			
			System.Data.DataTable v_count_total_table = new System.Data.DataTable();

			int v_timeout = v_connection.v_timeout;

			v_connection.SetTimeout (0);

			string v_sql = "";

			bool v_first = true;

			int v_block_counter = 0;

			for (int j = 0; j < p_tables.Count; j++)
			{

				if (!v_first)
					v_sql += " union all ";

				v_first = false;

				v_block_counter++;


				string v_table_name = "";

				if (v_has_schema)
					v_table_name = v_schema + "." + p_tables[j];
				else
					v_table_name = p_tables[j];


				v_sql += "select count(*) as total, " + v_trim_function + "('" + p_tables[j] + "') as table_name from " + v_table_name + " " + p_filters[j] + " ";




				if (v_block_counter>=50 || (j==p_tables.Count-1)) {

					if (v_count_total_table==null)
						v_count_total_table = v_connection.Query (v_sql,"t1");
					else
						v_count_total_table.Merge(v_connection.Query (v_sql,"t1"));
					v_first=true;
					v_block_counter=0;

					v_sql = "";



				}

			}

			System.Data.DataTable dt2 = v_count_total_table.Clone();
			dt2.Columns["total"].DataType = Type.GetType("System.Int32");

			foreach (System.Data.DataRow dr in v_count_total_table.Rows)
			{
				dt2.ImportRow(dr);
			}

			dt2.AcceptChanges();
			System.Data.DataView dv = dt2.DefaultView;
			dv.Sort = "total DESC";

			v_count_total_table = dv.ToTable();

			v_connection.SetTimeout (v_timeout);

			return v_count_total_table;

		}

		/// <summary>
		/// Get database name.
		/// </summary>
		public abstract string GetName();

		/// <summary>
		/// Print database info.
		/// </summary>
		public abstract string PrintDatabaseInfo();

		/// <summary>
		/// Print database details.
		/// </summary>
		public abstract string PrintDatabaseDetails();

	}
}

