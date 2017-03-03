/*
Copyright 2015-2017 The OmniDB Team

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

	}
}

