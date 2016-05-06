/*
Copyright 2016 The OmniDB Team

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
		/// Editor Theme.
		/// </summary>
		public string v_editor_theme;

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
		/// Initializes a new instance of the <see cref="OmniDB.Session"/> class.
		/// </summary>
		/// <param name="p_user_id">User ID.</param>
		/// <param name="p_user_name">Username.</param>
		/// <param name="p_database">Database that manages the application.</param>
		public Session (string p_user_id, string p_user_name, OmniDatabase.Generic p_database, string p_editor_theme, string p_editor_font_size)
		{
			
			v_omnidb_database  = p_database;
			v_database_index   = -1;
			v_user_id          = p_user_id;
			v_user_name        = p_user_name;
			v_databases        = new System.Collections.Generic.List<OmniDatabase.Generic> ();
			v_editor_theme     = p_editor_theme;
			v_editor_font_size = p_editor_font_size;

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

	}
}
