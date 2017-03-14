/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

using System;

namespace OmniDB
{
	/// <summary>
	/// Class to store all information required to run the web application.
	/// An Instance of this class is stored in browser session.
	/// </summary>
	public class Session
	{
		/// <summary>
		/// Management tool database.
		/// </summary>
		public OmniDatabase.Generic v_omnidb_database;


		/// <summary>
		/// List of all databases.
		/// </summary>
		public System.Collections.Generic.List<OmniDatabase.Generic> v_databases;

		/// <summary>
		/// Index of the selected database.
		/// </summary>
		public int v_database_index;

		/// <summary>
		/// User id.
		/// </summary>
		public string v_user_id;

		/// <summary>
		/// Username.
		/// </summary>
		public string v_user_name;

		/// <summary>
		/// Theme id.
		/// </summary>
		public string v_theme_id;

		/// <summary>
		/// Editor Theme.
		/// </summary>
		public string v_editor_theme;

		/// <summary>
		/// Theme type.
		/// </summary>
		public string v_theme_type;

		/// <summary>
		/// Editor Font Size.
		/// </summary>
		public string v_editor_font_size;

		/// <summary>
		/// Editor Font Size.
		/// </summary>
		public string v_omnidb_version;

		/// <summary>
		/// Current OS.
		/// </summary>
		public string v_current_os;

		/// <summary>
		/// If Omnichat is enabled.
		/// </summary>
		public int v_enable_omnichat;


		/// <summary>
		/// Initializes a new instance of the <see cref="OmniDB.Session"/> class.
		/// </summary>
		/// <param name="p_user_id">User ID.</param>
		/// <param name="p_user_name">Username.</param>
		/// <param name="p_database">Database that manages the application.</param>
		public Session (string p_user_id, string p_user_name, OmniDatabase.Generic p_database, string p_editor_theme, string p_theme_type, string p_theme_id, string p_editor_font_size, int p_enable_chat)
		{
			
			v_omnidb_database  = p_database;
			v_database_index   = -1;
			v_user_id          = p_user_id;
			v_user_name        = p_user_name;
			v_databases        = new System.Collections.Generic.List<OmniDatabase.Generic> ();
			v_theme_id 		   = p_theme_id;
			v_editor_theme     = p_editor_theme;
			v_theme_type       = p_theme_type;
			v_editor_font_size = p_editor_font_size;
			v_enable_omnichat  = p_enable_chat;

			if (Environment.OSVersion.ToString ().ToLower ().Contains ("unix"))
				v_current_os = "unix";
			else
				v_current_os = "windows";


			RefreshDatabaseList ();

		}

		/// <summary>
		/// Refreshing session databases.
		/// </summary>
		public void RefreshDatabaseList() {

            Spartacus.Utils.Cryptor v_cryptor = new Spartacus.Utils.Cryptor("omnidb_spartacus");

			v_databases.Clear ();

			// Getting connections from OmniDB database and instantiating databases.
			System.Data.DataTable v_connections = v_omnidb_database.v_connection.Query ("select * " +
				"from connections " +
				"where user_id=" + v_user_id + " " +
				"order by dbt_st_name, conn_id",
				"Connections");

			int v_count = 0;

			foreach (System.Data.DataRow v_connection in v_connections.Rows) 
			{

				OmniDatabase.Generic v_database;
				string v_timeout;

                try
                {
					v_database = OmniDatabase.Generic.InstantiateDatabase(
						v_cryptor.Decrypt(v_connection["alias"].ToString()),
						v_connection["conn_id"].ToString(),
						v_connection["dbt_st_name"].ToString(),
						v_cryptor.Decrypt(v_connection["server"].ToString()),
						v_cryptor.Decrypt(v_connection["port"].ToString()),
						v_cryptor.Decrypt(v_connection["service"].ToString()),
						v_cryptor.Decrypt(v_connection["user"].ToString()),
						v_cryptor.Decrypt(v_connection["password"].ToString()),
						v_cryptor.Decrypt(v_connection["schema"].ToString())
					);

					v_timeout = System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Timeout." + v_connection["dbt_st_name"].ToString()].ToString ();

					if (v_timeout!="-1")
						v_database.v_connection.SetTimeout(Convert.ToInt32(v_timeout));

					v_database.v_connection.SetExecuteSecurity(false);
					
					AddDatabase(v_database);
                }
                catch (Spartacus.Utils.Exception)
                {
					v_database = OmniDatabase.Generic.InstantiateDatabase (
						v_connection ["alias"].ToString (),
						v_connection ["conn_id"].ToString (),
						v_connection ["dbt_st_name"].ToString (),
						v_connection ["server"].ToString (),
						v_connection ["port"].ToString (),
						v_connection ["service"].ToString (),
						v_connection ["user"].ToString (),
						v_connection ["password"].ToString (),
						v_connection ["schema"].ToString ()
					);

					v_timeout = System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Timeout." + v_connection["dbt_st_name"].ToString()].ToString ();

					if (v_timeout!="-1")
						v_database.v_connection.SetTimeout(Convert.ToInt32(v_timeout));
					
					AddDatabase(v_database);
                }

				v_count++;
			}

		}

		/// <summary>
		/// Add a new database to session database list.
		/// </summary>
		/// <param name="p_database">Database.</param>
		public void AddDatabase(OmniDatabase.Generic p_database) {
			
			if (v_databases.Count == 0)
				v_database_index = 0;

			v_databases.Add (p_database);

		}

		/// <summary>
		/// Returns the selected database.
		/// </summary>
		public OmniDatabase.Generic GetSelectedDatabase() {
			
			return v_databases [v_database_index];

		}

        /// <summary>
        /// Execute the specified SQL string.
        /// </summary>
        /// <param name="p_database_index">Database index.</param>
        /// <param name="p_sql">SQL string.</param>
        /// <param name="p_loghistory">If set to <c>true</c>, logs the command to the history.</param>
        /// <param name="p_logmigration">If set to <c>true</c>, logs the command to the migration.</param>
        public void Execute(OmniDatabase.Generic p_database, string p_sql, bool p_loghistory, bool p_logmigration) {

			p_database.v_connection.Execute(p_sql);

            if (p_loghistory)
                this.LogHistory(p_sql);

            if (p_logmigration)
                this.LogMigration(p_database, p_sql);

        }

        /// <summary>
        /// Queries the specified SQL string.
        /// </summary>
        /// <param name="p_database_index">Database index.</param>
        /// <param name="p_sql">SQL string.</param>
        /// <param name="p_loghistory">If set to <c>true</c>, logs the command to the history.</param>
        /// <param name="p_logmigration">If set to <c>true</c>, logs the command to the migration.</param>
        public System.Data.DataTable Query(OmniDatabase.Generic p_database, string p_sql, bool p_loghistory, bool p_logmigration) {

			System.Data.DataTable v_table = p_database.v_connection.Query(p_sql, "Data");

            if (p_loghistory)
                this.LogHistory(p_sql);

            if (p_logmigration)
                this.LogMigration(p_database, p_sql);

            return v_table;

        }

		public System.Collections.Generic.List<System.Collections.Generic.List<string>> QueryList(OmniDatabase.Generic p_database, string p_sql, bool p_loghistory, bool p_logmigration, out System.Collections.Generic.List<string> p_columns)
		{

			if (p_loghistory)
				this.LogHistory(p_sql);

			if (p_logmigration)
				this.LogMigration(p_database, p_sql);

			return p_database.v_connection.QuerySList(p_sql, out p_columns);

		}

        /// <summary>
        /// Queries the specified SQL string, limited by a number of registers.
        /// </summary>
        /// <param name="p_database_index">Database index.</param>
        /// <param name="p_sql">SQL string.</param>
        /// <param name="p_count">Number of registers.</param>
        /// <param name="p_loghistory">If set to <c>true</c>, logs the command to the history.</param>
        /// <param name="p_logmigration">If set to <c>true</c>, logs the command to the migration.</param>
        public System.Data.DataTable QueryDataLimited(OmniDatabase.Generic p_database, string p_sql, int p_count, bool p_loghistory, bool p_logmigration) {

            System.Data.DataTable v_table = p_database.QueryDataLimited(p_sql, p_count);

            if (p_loghistory)
                this.LogHistory(p_sql);

            if (p_logmigration)
                this.LogMigration(p_database, p_sql);

            return v_table;

        }

		public System.Collections.Generic.List<System.Collections.Generic.List<string>> QueryListLimited(OmniDatabase.Generic p_database, string p_sql, int p_count, bool p_loghistory, bool p_logmigration, out System.Collections.Generic.List<string> p_columns)
		{

			if (p_loghistory)
				this.LogHistory(p_sql);

			if (p_logmigration)
				this.LogMigration(p_database, p_sql);

			return p_database.QueryDataLimitedList(p_sql,p_count, out p_columns);

		}

        private void LogHistory(string p_sql) {

            System.Data.DataTable v_command_table;

            int v_numcommands = int.Parse(v_omnidb_database.v_connection.ExecuteScalar("select count(*) from command_list"));
            if (v_numcommands > 0)
                v_command_table = v_omnidb_database.v_connection.Query ("select max(cl_in_codigo)+1 as next_id from command_list", "Command List");
            else
                v_command_table = v_omnidb_database.v_connection.Query ("select 1 as next_id", "Command List");

            v_omnidb_database.v_connection.Execute ("insert into command_list values ( " +
                v_user_id + "," +
                v_command_table.Rows [0] ["next_id"].ToString () + ",'" +
                p_sql.Replace("'","''") +
                "','" +
                DateTime.Now +
                "')");

        }

        private void LogMigration(OmniDatabase.Generic p_database, string p_sql) {

            OmniDatabase.Generic v_database = p_database;
            System.Data.DataTable v_command_table;
            string v_schema;

            if (v_database.v_has_schema)
                v_schema = v_database.v_schema + ".";
            else
                v_schema = "";

            try
            {
                int v_migid = int.Parse(v_database.v_connection.ExecuteScalar("select max(mig_id) from " + v_schema + "omnidb_migrations where mig_status = 'E'"));

                int v_numcommands = int.Parse(v_database.v_connection.ExecuteScalar("select count(*) from " + v_schema + "omnidb_mig_commands"));
                if (v_numcommands > 0)
                    v_command_table = v_database.v_connection.Query ("select max(cmd_id)+1 as next_id from " + v_schema + "omnidb_mig_commands", "Command List");
                else
                    v_command_table = v_database.v_connection.Query ("select 1 as next_id", "Command List");

                v_database.v_connection.Execute ("insert into " + v_schema + "omnidb_mig_commands values ( " +
                    v_migid.ToString() + "," +
                    v_command_table.Rows [0] ["next_id"].ToString () + ",'" +
                    DateTime.Now + "','" +
                    v_user_name + "','" +
                    p_sql.Replace("'","''") +
                    "')");
            }
            catch
            {
            }
        }

	}
}
