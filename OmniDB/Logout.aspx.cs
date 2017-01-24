/*
Copyright 2016 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

using System;
using System.Web;
using System.Web.UI;

namespace OmniDB
{
	/// <summary>
	/// Page to logout from the application.
	/// </summary>
	public partial class Logout : System.Web.UI.Page
	{

		protected void Page_Load(object sender, EventArgs e)
		{
			Session["OMNIDB_SESSION"] = null;

			this.Response.Redirect("Login.aspx");
		}

		/// <summary>
		/// Logging out from the application.
		/// </summary>
		/// <returns>The out.</returns>
		/// <param name="p_username">Username.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn SignOut(string p_userid)
		{
			AjaxReturn v_return = new AjaxReturn ();

			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			// Instantiating tool management database.
			OmniDatabase.Generic v_omnidb_database = OmniDatabase.Generic.InstantiateDatabase ("","0",
				"sqlite",
				"",
				"",
				System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.Database"].ToString (),
				"",
				"",
				"");
				
			try {
				
				v_omnidb_database.v_connection.Execute (
					"update users " +
					"set online = 0 " +
					"where user_id = '" + p_userid + "'");

			} catch (Spartacus.Database.Exception e) {
				v_return.v_error = true;
				v_return.v_data = e.v_message;
			}

			return v_return;

		}
	}
}

