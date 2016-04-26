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
	
	public partial class Default : System.Web.UI.Page
	{
		public Session v_session;

		protected void Page_Load(object sender, EventArgs e)
		{
			v_session = (Session)Session ["OMNIDB_SESSION"];

			if (v_session == null) {
				this.Response.Redirect("Login.aspx");

			}
			else if (v_session.v_databases.Count==0) {
				this.Response.Redirect("Connections.aspx");

			}
			else
				this.Response.Redirect("MainDB.aspx");


			Session["OMNIDB_SESSION"] = v_session;
		}
	}
}