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
	/// Class to store information of an Access database.
	/// </summary>
	public class Access : Generic
	{
		/// <summary>
		/// Initializes a new instance of the <see cref="OmniDB.Database.Access"/> class.
		/// </summary>
		/// <param name="p_server">Connection address.</param>
		/// <param name="p_port">Connection port.</param>
		/// <param name="v_database">Database file.</param>
		/// <param name="v_user">Database user.</param>
		/// <param name="v_password">Database password.</param>
		public Access (string p_conn_id, string p_database)
			: base ("access",p_conn_id)
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

			v_default_string = "text";

			v_can_rename_table = true;
			v_rename_table_command = "alter table #p_table_name# rename to #p_new_table_name#";

			v_create_pk_command = "constraint #p_constraint_name# primary key (#p_columns#)";
			v_create_fk_command = "constraint #p_constraint_name# foreign key (#p_columns#) references #p_r_table_name# (#p_r_columns#) #p_delete_update_rules#";
			v_create_unique_command = "constraint #p_constraint_name# unique (#p_columns#)";

			v_can_alter_type = true;

			v_can_alter_nullable = true;

			v_can_rename_column = true;

			v_can_add_column = true;
			v_add_column_command = "alter table #p_table_name# add column #p_column_name# #p_data_type# #p_nullable#";

			v_can_drop_column = true;

			v_can_add_constraint = true;

			v_can_drop_constraint = true;

			v_create_index_command = "create index #p_index_name# on #p_table_name# (#p_columns#)";
			v_create_unique_index_command = "create unique index #p_index_name# on #p_table_name# (#p_columns#)";
			v_drop_index_command = "drop index #p_index_name#";

			v_update_rules = new System.Collections.Generic.List<string> ();
			v_delete_rules = new System.Collections.Generic.List<string> ();

			v_delete_rules.Add ("");
			v_delete_rules.Add ("SET NULL");
			v_delete_rules.Add ("CASCADE");

			v_update_rules.Add ("");
			v_update_rules.Add ("SET NULL");
			v_update_rules.Add ("CASCADE");

			v_trim_function = "trim";

			v_transfer_block_size = new System.Collections.Generic.List<uint> ();
			v_transfer_block_size.Add (50);
			v_transfer_block_size.Add (100);
			v_transfer_block_size.Add (200);
			v_transfer_block_size.Add (400);

			v_connection = new Spartacus.Database.Access (p_database);
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
					v_return = "File does not exist.";

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

			v_table = new System.Data.DataTable("Tables");
			v_table.Columns.Add("table_name");

			com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
			java.util.Set v_set = v_database.getTableNames();
			object[] v_obj = v_set.toArray();
			foreach (object o in v_obj) {
				
				v_row = v_table.NewRow();
                if (((string)o).Contains(" "))
                    v_row["table_name"] = "[" + (string)o + "]";
                else
                    v_row["table_name"] = (string)o;
				v_table.Rows.Add(v_row);

			}

			return v_table;
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

                foreach (System.Data.DataRow v_tabletemp in v_tables.Rows) {

                    System.Data.DataRow v_row;

                    System.Data.DataTable v_table_columns = new System.Data.DataTable("TableFields");
                    v_table_columns.Columns.Add("column_name");
                    v_table_columns.Columns.Add("data_type");
                    v_table_columns.Columns.Add ("nullable");
                    v_table_columns.Columns.Add ("data_length");
                    v_table_columns.Columns.Add ("data_precision");
                    v_table_columns.Columns.Add ("data_scale");
                    v_table_columns.Columns.Add ("table_name");

                    com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
                    com.healthmarketscience.jackcess.Table v_table = v_database.getTable(v_tabletemp["table_name"].ToString().Replace("[", "").Replace("]", ""));
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
                        v_row["table_name"] = v_tabletemp["table_name"].ToString();
                        v_table_columns.Rows.Add(v_row);

                    }

                    v_table_columns_all.Merge (v_table_columns);

                }

                return v_table_columns_all;

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

			if (p_table == null) {

                System.Data.DataTable v_tables = this.QueryTables (false);

				System.Data.DataTable v_all_fks = new System.Data.DataTable();
				v_all_fks.Columns.Add("table_name");
				v_all_fks.Columns.Add("constraint_name");
				v_all_fks.Columns.Add("r_table_name");
				v_all_fks.Columns.Add("column_name");
				v_all_fks.Columns.Add("r_column_name");
				v_all_fks.Columns.Add("update_rule");
				v_all_fks.Columns.Add("delete_rule");
				
                foreach (System.Data.DataRow v_tabletemp in v_tables.Rows) {

                    System.Data.DataRow v_row;

                    System.Data.DataTable v_fks = new System.Data.DataTable("TableForeignKeys");
                    v_fks.Columns.Add("table_name");
                    v_fks.Columns.Add("constraint_name");
                    v_fks.Columns.Add("r_table_name");
                    v_fks.Columns.Add("column_name");
                    v_fks.Columns.Add("r_column_name");
                    v_fks.Columns.Add("update_rule");
                    v_fks.Columns.Add("delete_rule");

                    com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));

                    com.healthmarketscience.jackcess.Table v_table = v_database.getTable(v_tabletemp["table_name"].ToString().Replace("[", "").Replace("]", ""));

                    java.util.Set v_set = v_database.getTableNames();
                    object[] v_obj = v_set.toArray();
                    foreach (object v_tablename in v_obj) {
						
                        com.healthmarketscience.jackcess.Table v_table2 = v_database.getTable((string) v_tablename);

                        try {
							
                            com.healthmarketscience.jackcess.Index v_index = v_table.getForeignKeyIndex(v_table2);

                            if (! v_index.getName().StartsWith(".")) {
								
                                com.healthmarketscience.jackcess.Index v_index2 = v_index.getReferencedIndex();

                                java.util.List v_list = v_index.getColumns();
                                object[] v_obj2 = v_list.toArray();

                                java.util.List v_list2 = v_index2.getColumns();
                                object[] v_obj3 = v_list2.toArray();

                                java.util.List v_list3 = v_database.getRelationships(v_table, v_table2);
                                object[] v_obj4 = v_list3.toArray();
                                bool v_dcascade = false;
                                bool v_ucascade = false;
                                foreach (object o in v_obj4) {
									
                                    com.healthmarketscience.jackcess.Relationship r = (com.healthmarketscience.jackcess.Relationship)o;

                                    if (r.getName() == v_index.getName()) {
										
                                        v_dcascade = r.cascadeDeletes();
                                        v_ucascade = r.cascadeUpdates();

                                    }

                                }

                                int k = 0;
                                foreach (object o in v_obj2) {
									
                                    com.healthmarketscience.jackcess.Index.Column c = (com.healthmarketscience.jackcess.Index.Column) o;
                                    com.healthmarketscience.jackcess.Index.Column c2 = (com.healthmarketscience.jackcess.Index.Column) v_obj3[k];

                                    v_row = v_fks.NewRow();
                                    v_row["table_name"] = v_tabletemp["table_name"].ToString();
                                    v_row["constraint_name"] = v_index.getName();
                                    v_row["r_table_name"] = (string) v_tablename;
                                    v_row["column_name"] = c.getName();
                                    v_row["r_column_name"] = c2.getName();
                                    if (v_ucascade)
                                        v_row["update_rule"] = "CASCADE";
                                    else
                                        v_row["update_rule"] = "SET NULL";
                                    if (v_dcascade)
                                        v_row["delete_rule"] = "CASCADE";
                                    else
                                        v_row["delete_rule"] = "SET NULL";
                                    v_fks.Rows.Add(v_row);

                                    k++;

                                }

                            }

                        }
                        catch (java.lang.IllegalArgumentException) {
							
                        }

                    }

                    v_all_fks.Merge(v_fks);

                }

                return v_all_fks;

			} 
			else {

				System.Data.DataRow v_row;

				System.Data.DataTable v_fks = new System.Data.DataTable("TableForeignKeys");
                v_fks.Columns.Add("table_name");
                v_fks.Columns.Add("constraint_name");
				v_fks.Columns.Add("r_table_name");
				v_fks.Columns.Add("column_name");
				v_fks.Columns.Add("r_column_name");
				v_fks.Columns.Add("update_rule");
				v_fks.Columns.Add("delete_rule");

				com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
				
                com.healthmarketscience.jackcess.Table v_table = v_database.getTable(p_table.Replace("[", "").Replace("]", ""));

                java.util.Set v_set = v_database.getTableNames();
                object[] v_obj = v_set.toArray();
                foreach (object v_tablename in v_obj) {
					
                    com.healthmarketscience.jackcess.Table v_table2 = v_database.getTable((string) v_tablename);

                    try {
						
						com.healthmarketscience.jackcess.Index v_index = v_table.getForeignKeyIndex(v_table2);

                        if (! v_index.getName().StartsWith(".")) {
							
                            com.healthmarketscience.jackcess.Index v_index2 = v_index.getReferencedIndex();

                            java.util.List v_list = v_index.getColumns();
    						object[] v_obj2 = v_list.toArray();

                            java.util.List v_list2 = v_index2.getColumns();
                            object[] v_obj3 = v_list2.toArray();

                            java.util.List v_list3 = v_database.getRelationships(v_table, v_table2);
                            object[] v_obj4 = v_list3.toArray();
                            bool v_dcascade = false;
                            bool v_ucascade = false;
                            foreach (object o in v_obj4) {
								
                                com.healthmarketscience.jackcess.Relationship r = (com.healthmarketscience.jackcess.Relationship)o;

                                if (r.getName() == v_index.getName()) {
									
                                    v_dcascade = r.cascadeDeletes();
                                    v_ucascade = r.cascadeUpdates();

                                }

                            }

                            int k = 0;
    						foreach (object o in v_obj2) {
								
    							com.healthmarketscience.jackcess.Index.Column c = (com.healthmarketscience.jackcess.Index.Column) o;
                                com.healthmarketscience.jackcess.Index.Column c2 = (com.healthmarketscience.jackcess.Index.Column) v_obj3[k];

    							v_row = v_fks.NewRow();
                                v_row["table_name"] = p_table;
                                v_row["constraint_name"] = v_index.getName();
    							v_row["r_table_name"] = (string) v_tablename;
    							v_row["column_name"] = c.getName();
    							v_row["r_column_name"] = c2.getName();
                                if (v_ucascade)
                                    v_row["update_rule"] = "CASCADE";
                                else
                                    v_row["update_rule"] = "SET NULL";
                                if (v_dcascade)
                                    v_row["delete_rule"] = "CASCADE";
                                else
    							    v_row["delete_rule"] = "SET NULL";
    							v_fks.Rows.Add(v_row);

                                k++;

    						}

                        }

					}
					catch (java.lang.IllegalArgumentException) {
						
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

                System.Data.DataTable v_tables = this.QueryTables (false);

				System.Data.DataTable v_pk_all = new System.Data.DataTable ();
				v_pk_all.Columns.Add ("constraint_name");
				v_pk_all.Columns.Add ("column_name");
				v_pk_all.Columns.Add ("table_name");

                foreach (System.Data.DataRow v_tabletemp in v_tables.Rows) {

                    System.Data.DataRow v_row;

                    System.Data.DataTable v_pk = new System.Data.DataTable ("TablePrimaryKeys");
                    v_pk.Columns.Add ("constraint_name");
                    v_pk.Columns.Add ("column_name");
                    v_pk.Columns.Add ("table_name");

                    com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
                    com.healthmarketscience.jackcess.Table v_table = v_database.getTable(v_tabletemp["table_name"].ToString().Replace("[", "").Replace("]", ""));
                    com.healthmarketscience.jackcess.Index v_index = v_table.getPrimaryKeyIndex();

                    java.util.List v_list = v_index.getColumns();
                    object[] v_obj = v_list.toArray();
                    foreach (object o in v_obj) {
						
                        com.healthmarketscience.jackcess.Index.Column c = (com.healthmarketscience.jackcess.Index.Column) o;

                        v_row = v_pk.NewRow();
                        v_row["constraint_name"] = v_index.getName();
                        v_row["column_name"] = c.getName();
                        v_row["table_name"] = v_tabletemp["table_name"].ToString();
                        v_pk.Rows.Add(v_row);

                    }

                    v_pk_all.Merge(v_pk);

                }

				return v_pk_all;

			} 
			else {
				
				System.Data.DataRow v_row;

				System.Data.DataTable v_pk = new System.Data.DataTable ("TablePrimaryKeys");
				v_pk.Columns.Add ("constraint_name");
				v_pk.Columns.Add ("column_name");
				v_pk.Columns.Add ("table_name");

				com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
                com.healthmarketscience.jackcess.Table v_table = v_database.getTable(p_table.Replace("[", "").Replace("]", ""));
				com.healthmarketscience.jackcess.Index v_index = v_table.getPrimaryKeyIndex();

				java.util.List v_list = v_index.getColumns();
				object[] v_obj = v_list.toArray();
				foreach (object o in v_obj) {
					
					com.healthmarketscience.jackcess.Index.Column c = (com.healthmarketscience.jackcess.Index.Column) o;

					v_row = v_pk.NewRow();
					v_row["constraint_name"] = v_index.getName();
					v_row["column_name"] = c.getName();
					v_row["table_name"] = p_table;
					v_pk.Rows.Add(v_row);

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

			if (p_table == null) {

                System.Data.DataTable v_tables = this.QueryTables (false);

                System.Data.DataTable v_all_uniques = new System.Data.DataTable();
				v_all_uniques.Columns.Add("table_name");
				v_all_uniques.Columns.Add("constraint_name");
				v_all_uniques.Columns.Add("column_name");

                foreach (System.Data.DataRow v_tabletemp in v_tables.Rows) {

                    System.Data.DataRow v_row;

                    System.Data.DataTable v_uniques = new System.Data.DataTable("TableUniques");
                    v_uniques.Columns.Add("table_name");
                    v_uniques.Columns.Add("constraint_name");
                    v_uniques.Columns.Add("column_name");

                    com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
                    com.healthmarketscience.jackcess.Table v_table = v_database.getTable(v_tabletemp["table_name"].ToString().Replace("[", "").Replace("]", ""));
                    java.util.List v_list = v_table.getIndexes();
                    object[] v_obj = v_list.toArray();
                    foreach (object o in v_obj) {
						
                        com.healthmarketscience.jackcess.Index v_index = (com.healthmarketscience.jackcess.Index)o;

                        if (v_index.isUnique()) {
							
                            java.util.List v_list2 = v_index.getColumns();
                            object[] v_obj2 = v_list2.toArray();
                            foreach (object o2 in v_obj2) {
								
                                com.healthmarketscience.jackcess.Index.Column c = (com.healthmarketscience.jackcess.Index.Column)o2;

                                v_row = v_uniques.NewRow();
                                v_row["table_name"] = v_tabletemp["table_name"].ToString();
                                v_row["constraint_name"] = v_index.getName();
                                v_row["column_name"] = c.getName();
                                v_uniques.Rows.Add(v_row);
                            
							}
                        
						}
                    
					}

                    v_all_uniques.Merge(v_uniques);

                }

				return v_all_uniques;

			}
			else {

				System.Data.DataRow v_row;

				System.Data.DataTable v_uniques = new System.Data.DataTable("TableUniques");
				v_uniques.Columns.Add("table_name");
				v_uniques.Columns.Add("constraint_name");
				v_uniques.Columns.Add("column_name");

				com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
                com.healthmarketscience.jackcess.Table v_table = v_database.getTable(p_table.Replace("[", "").Replace("]", ""));
				java.util.List v_list = v_table.getIndexes();
				object[] v_obj = v_list.toArray();
				foreach (object o in v_obj) {
					
					com.healthmarketscience.jackcess.Index v_index = (com.healthmarketscience.jackcess.Index)o;

					if (v_index.isUnique()) {
						
						java.util.List v_list2 = v_index.getColumns();
						object[] v_obj2 = v_list2.toArray();
						foreach (object o2 in v_obj2) {
							
							com.healthmarketscience.jackcess.Index.Column c = (com.healthmarketscience.jackcess.Index.Column)o2;

							v_row = v_uniques.NewRow();
							v_row["table_name"] = p_table;
							v_row["constraint_name"] = v_index.getName();
							v_row["column_name"] = c.getName();
							v_uniques.Rows.Add(v_row);
						
						}
					
					}
				
				}

				return v_uniques;

			}

		}

		/// <summary>
		/// Get a datatable with all tables indexes.
		/// </summary>
		/// <param name="p_table">Table name.</param>
		public override System.Data.DataTable QueryTablesIndexes(string p_table) {

			if (p_table == null) {

                System.Data.DataTable v_tables = this.QueryTables (false);

                System.Data.DataTable v_all_indexes = new System.Data.DataTable();
				v_all_indexes.Columns.Add("table_name");
				v_all_indexes.Columns.Add("index_name");
				v_all_indexes.Columns.Add("column_name");
				v_all_indexes.Columns.Add("uniqueness");

                foreach (System.Data.DataRow v_tabletemp in v_tables.Rows) {

                    System.Data.DataRow v_row;

                    System.Data.DataTable v_indexes = new System.Data.DataTable("TableIndexes");
                    v_indexes.Columns.Add("table_name");
                    v_indexes.Columns.Add("index_name");
                    v_indexes.Columns.Add("column_name");
                    v_indexes.Columns.Add("uniqueness");

                    com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
                    com.healthmarketscience.jackcess.Table v_table = v_database.getTable(v_tabletemp["table_name"].ToString().Replace("[", "").Replace("]", ""));
                    java.util.List v_list = v_table.getIndexes();
                    object[] v_obj = v_list.toArray();
                    foreach (object o in v_obj) {
						
                        com.healthmarketscience.jackcess.Index v_index = (com.healthmarketscience.jackcess.Index)o;
                        java.util.List v_list2 = v_index.getColumns();
                        object[] v_obj2 = v_list2.toArray();
                        foreach (object o2 in v_obj2) {
							
                            com.healthmarketscience.jackcess.Index.Column c = (com.healthmarketscience.jackcess.Index.Column)o2;

                            v_row = v_indexes.NewRow();
                            v_row["table_name"] = v_tabletemp["table_name"].ToString();
                            v_row["index_name"] = v_index.getName();
                            v_row["column_name"] = c.getName();
                            if (v_index.isUnique())
                                v_row["uniqueness"] = "Unique";
                            else
                                v_row["uniqueness"] = "Non Unique";
                            v_indexes.Rows.Add(v_row);
                        
						}

                    }

                    v_all_indexes.Merge(v_indexes);

                }

				return v_all_indexes;

			}
			else {

				System.Data.DataRow v_row;

				System.Data.DataTable v_indexes = new System.Data.DataTable("TableIndexes");
				v_indexes.Columns.Add("table_name");
				v_indexes.Columns.Add("index_name");
				v_indexes.Columns.Add("column_name");
				v_indexes.Columns.Add("uniqueness");

				com.healthmarketscience.jackcess.Database v_database = com.healthmarketscience.jackcess.DatabaseBuilder.open(new java.io.File(this.v_connection.v_service));
                com.healthmarketscience.jackcess.Table v_table = v_database.getTable(p_table.Replace("[", "").Replace("]", ""));
				java.util.List v_list = v_table.getIndexes();
				object[] v_obj = v_list.toArray();
				foreach (object o in v_obj) {
					
					com.healthmarketscience.jackcess.Index v_index = (com.healthmarketscience.jackcess.Index)o;
					java.util.List v_list2 = v_index.getColumns();
					object[] v_obj2 = v_list2.toArray();
					foreach (object o2 in v_obj2) {
						
						com.healthmarketscience.jackcess.Index.Column c = (com.healthmarketscience.jackcess.Index.Column)o2;

						v_row = v_indexes.NewRow();
						v_row["table_name"] = p_table;
						v_row["index_name"] = v_index.getName();
						v_row["column_name"] = c.getName();
						if (v_index.isUnique())
							v_row["uniqueness"] = "Unique";
						else
							v_row["uniqueness"] = "Non Unique";
						v_indexes.Rows.Add(v_row);
					
					}
				
				}

				return v_indexes;

			}

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