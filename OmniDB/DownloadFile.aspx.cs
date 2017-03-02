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
	/// Page to download exported data.
	/// </summary>
	public partial class DownloadFile : System.Web.UI.Page
	{

		/// <summary>
		/// Page load function.
		/// </summary>
		protected void Page_Load(object sender, EventArgs e)
		{

			string v_type = Session ["OMNIDB_EXPORTED_TYPE"].ToString ();
			string v_file = Session ["OMNIDB_EXPORTED_FILE"].ToString ();
			string v_name = Session ["OMNIDB_EXPORTED_NAME"].ToString ();

			System.IO.FileInfo v_file_info = new System.IO.FileInfo(System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.ExportedFilesFolder"] + "/" + v_file);

			this.Response.ContentType = "application/" + v_type;
			this.Response.AddHeader("content-disposition", "attachment; filename=\"" + v_name + "." + v_type + "\"");
			this.Response.AddHeader("content-length", v_file_info.Length.ToString());
			this.Response.TransmitFile(System.Web.Configuration.WebConfigurationManager.AppSettings ["OmniDB.ExportedFilesFolder"] + "/" + v_file);
			this.Response.End();

		}
		
	}
}

