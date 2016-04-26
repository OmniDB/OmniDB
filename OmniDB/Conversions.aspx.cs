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
	/// Conversions Data.
	/// </summary>
	public class ConversionsData
	{
		public System.Collections.Generic.List<System.Collections.Generic.List<string>> v_data;
	}

	/// <summary>
	/// Page to list and add new schema conversions.
	/// </summary>
	public partial class Conversions : System.Web.UI.Page
	{
		/// <summary>
		/// Session variable
		/// </summary>
		public Session v_session;

		/// <summary>
		/// Page load function.
		/// </summary>
		protected void Page_Load(object sender, EventArgs e)
		{

			v_session = (Session)Session ["OMNIDB_SESSION"];

			if (v_session == null) {
				Session ["OMNIDB_ALERT_MESSAGE"] = "Session object was destroyed, please sign in again.";
				this.Response.Redirect("Login.aspx");

			}
			else if (v_session.v_databases.Count==0) {
				Session ["OMNIDB_ALERT_MESSAGE"] = "There are no database connections, please add at least one before using the application.";
				this.Response.Redirect("Connections.aspx");

			}

			Session["OMNIDB_SESSION"] = v_session;
		}

		/// <summary>
		/// Gets log for specific conversion.
		/// </summary>
		/// <param name="p_conv_id">Conversion ID.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetConvLog(int p_conv_id)
		{
			AjaxReturn v_return = new AjaxReturn();

			string v_log = "";

			try {
				using (System.IO.StreamReader v_reader = new System.IO.StreamReader("log/conv_" + p_conv_id + ".txt"))
				{
					string v_line;
					while ( (v_line=v_reader.ReadLine()) != null)
					{
						v_log += v_line.Replace("<",".").Replace(">",".") + "\n";
					}
				}
			}
			catch (System.IO.FileNotFoundException) {
				v_log = "File does not exist.";
			}
			catch (System.IO.IOException e) {
				v_log = e.Message;
			}

			v_return.v_data = v_log;

			return v_return;

		}

		/// <summary>
		/// Retrieving all conversions.
		/// </summary>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetConversions()
		{

			AjaxReturn v_return = new AjaxReturn();
			ConversionsData v_return_data = new ConversionsData ();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			System.Data.DataTable v_conversions = v_session.v_omnidb_database.v_connection.Query ("select * from conversions where user_id = " + v_session.v_user_id + " order by conv_id desc", "Conversions");


			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_conv_list = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			int v_index = 0;

			foreach (System.Data.DataRow v_conv in v_conversions.Rows) 
			{

				System.Collections.Generic.List<string> v_connection_data_list = new System.Collections.Generic.List<string>();

				string v_src_conn = "";
				string v_dst_conn = "";
				string v_src_tech = "";
				string v_dst_tech = "";

				foreach (OmniDatabase.Generic v_database in v_session.v_databases) {
					if (v_database.v_conn_id == v_conv ["conn_id_src"].ToString ()) {
						v_src_conn = v_database.PrintDatabaseInfo();
						v_src_tech = v_database.v_db_type;
						break;
					}
				}

				foreach (OmniDatabase.Generic v_database in v_session.v_databases) {
					if (v_database.v_conn_id == v_conv ["conn_id_dst"].ToString ()) {
						v_dst_conn = v_database.PrintDatabaseInfo();
						v_dst_tech = v_database.v_db_type;
						break;
					}
				}

				string v_bar = "";


				if (v_conv ["conv_re_perc"].ToString () == "100")
					v_bar = "bar_green";
				else
					v_bar = "bar_yellow";

				string v_perc = "<div id=\"progress\" class=\"progress\"><div class=\"" + v_bar + "\" style=\"width:" + v_conv["conv_re_perc"].ToString().Replace(",",".") + "%\"></div ><div class=\"percent\" >" + v_conv["conv_re_perc"].ToString() + "%</div></div></div>";

				string v_actions = "<img src='images/table_edit.png' class='img_ht' onclick='conversionDetails(" + v_conv ["conv_id"].ToString () + ")'/>" +
					"<img src='images/log.png' class='img_ht' onclick='viewLog(" + v_conv ["conv_id"].ToString () + ")'/>";

				if (v_conv ["conv_ch_status"].ToString () != "E")
					v_actions +=  "<img src='images/start.png' class='img_ht' onclick='startConversion(" + v_conv ["conv_id"].ToString () + ")'/>" +
						"<img src='images/tab_close.png' class='img_ht' onclick='deleteConversion(" + v_conv ["conv_id"].ToString () + ")'/>";
				else
					v_actions +=  "<img src='images/stop.png' class='img_ht' onclick='stopConversion(" + v_conv ["conv_id"].ToString () + ")'/>";

				v_connection_data_list.Add("<img src='images/" + v_src_tech + "_medium.png' class='img_ht' style='margin-right: 5px;'/>" + v_src_conn);
				v_connection_data_list.Add("<img src='images/" + v_dst_tech + "_medium.png' class='img_ht' style='margin-right: 5px;'/>" + v_dst_conn);
				v_connection_data_list.Add(v_conv["conv_st_start"].ToString());
				v_connection_data_list.Add(v_conv["conv_st_end"].ToString());
				v_connection_data_list.Add(v_perc);
				v_connection_data_list.Add(v_conv["conv_ch_status"].ToString());
				v_connection_data_list.Add(v_conv["conv_st_comments"].ToString());
				v_connection_data_list.Add(v_conv["conv_st_duration"].ToString());
				v_connection_data_list.Add(v_actions);

				v_index++;

				v_conv_list.Add(v_connection_data_list);		

			}

			v_return_data.v_data = v_conv_list;

			v_return.v_data = v_return_data;
			return v_return;

		}

		/// <summary>
		/// Gets the conversion details.
		/// </summary>
		/// <param name="p_conv_id">Conversion ID.</param>
		/// <param name="p_mode">Mode.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn GetConversionDetails(int p_conv_id, int p_mode)
		{

			AjaxReturn v_return = new AjaxReturn();
			ConversionsData v_return_data = new ConversionsData ();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			string v_filter = "";

			if (p_mode == 1)
				v_filter = " and ctd_ch_transferdata='F' ";
			else if (p_mode == 2)
				v_filter = " and ctd_ch_transferdata<>'F' ";

			System.Data.DataTable v_conversions = v_session.v_omnidb_database.v_connection.Query ("select * from conv_tables_data where conv_id=" + p_conv_id + v_filter + " order by conv_id desc", "Conversions");


			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_conv_list = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			int v_index = 0;

			foreach (System.Data.DataRow v_conv in v_conversions.Rows) 
			{

				System.Collections.Generic.List<string> v_connection_data_list = new System.Collections.Generic.List<string>();

				string v_bar = "";

				if (v_conv ["ctd_re_transfperc"].ToString () == "100")
					v_bar = "bar_green";
				else
					v_bar = "bar_yellow";

				string v_perc = "<div id=\"progress\" class=\"progress\"><div class=\"" + v_bar + "\" style=\"width:" + v_conv["ctd_re_transfperc"].ToString().Replace(",",".") + "%\"></div ><div class=\"percent\" >" + v_conv["ctd_re_transfperc"].ToString() + "%</div></div></div>";

				string v_estimate = "";

				if (v_conv["ctd_ch_transferdata"].ToString()=="E") {

					double v_est = Convert.ToDouble(v_conv["ctd_re_transferrate"].ToString());

					if (v_est != 0) {
						int v_total = int.Parse (v_conv ["ctd_in_totalrecords"].ToString ());
						int v_transf = int.Parse (v_conv ["ctd_in_transfrecords"].ToString ());
						int v_remain = v_total - v_transf;

						double v_time_left = v_remain / v_est;

						v_estimate = string.Format ("{0:00}:{1:00}:{2:00}", v_time_left / 3600, (v_time_left / 60) % 60, v_time_left % 60);

					}

				}

				v_connection_data_list.Add(v_conv["ctd_st_table"].ToString());
				v_connection_data_list.Add("<div style='width: 100%; text-align: center;'><img class='img_ht' src='images/status/status_" + v_conv["ctd_ch_droprecords"].ToString() + ".png'/></div>");
				v_connection_data_list.Add("<div style='width: 100%; text-align: center;'><img class='img_ht' src='images/status/status_" + v_conv["ctd_ch_createtable"].ToString() + ".png'/></div>");
				v_connection_data_list.Add("<div style='width: 100%; text-align: center;'><img class='img_ht' src='images/status/status_" + v_conv["ctd_ch_createpk"].ToString() + ".png'/></div>");
				v_connection_data_list.Add("<div style='width: 100%; text-align: center;'><img class='img_ht' src='images/status/status_" + v_conv["ctd_ch_createfk"].ToString() + ".png'/></div>");
				v_connection_data_list.Add("<div style='width: 100%; text-align: center;'><img class='img_ht' src='images/status/status_" + v_conv["ctd_ch_createuq"].ToString() + ".png'/></div>");
				v_connection_data_list.Add("<div style='width: 100%; text-align: center;'><img class='img_ht' src='images/status/status_" + v_conv["ctd_ch_createidx"].ToString() + ".png'/></div>");
				v_connection_data_list.Add("<div style='width: 100%; text-align: center;'><img class='img_ht' src='images/status/status_" + v_conv["ctd_ch_transferdata"].ToString() + ".png'/></div>");
				v_connection_data_list.Add(v_conv["ctd_st_transferfilter"].ToString());
				v_connection_data_list.Add(String.Format("{0:0,0}",int.Parse(v_conv["ctd_in_totalrecords"].ToString())));
				v_connection_data_list.Add(String.Format("{0:0,0}",int.Parse(v_conv["ctd_in_transfrecords"].ToString())));
				v_connection_data_list.Add(v_perc);
				v_connection_data_list.Add(v_conv["ctd_re_transferrate"].ToString() + " records/s");
				v_connection_data_list.Add(v_estimate);
				v_connection_data_list.Add(v_conv["ctd_st_starttransfer"].ToString());
				v_connection_data_list.Add(v_conv["ctd_st_endtransfer"].ToString());
				v_connection_data_list.Add(v_conv["ctd_st_duration"].ToString());

				v_index++;

				v_conv_list.Add(v_connection_data_list);		

			}

			v_return_data.v_data = v_conv_list;

			v_return.v_data = v_return_data;
			return v_return;

		}

		/// <summary>
		/// Deletes the conversion.
		/// </summary>
		/// <param name="p_conv_id">Conversion ID.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn DeleteConversion(int p_conv_id)
		{

			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			v_session.v_omnidb_database.v_connection.Execute ("delete from conv_tables_data where conv_id=" + p_conv_id);
			v_session.v_omnidb_database.v_connection.Execute ("delete from conversions where conv_id=" + p_conv_id);

			if (System.IO.File.Exists ("log/conv_" + p_conv_id + ".txt"))
				System.IO.File.Delete ("log/conv_" + p_conv_id + ".txt");

			return v_return;

		}

		/// <summary>
		/// Starts a conversion.
		/// </summary>
		/// <param name="p_conv_id">Conversion ID.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn StartConversion(int p_conv_id)
		{

			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			v_session.v_omnidb_database.v_connection.Execute ("update conv_tables_data set ctd_in_totalrecords = 0, " +
				"ctd_in_transfrecords = 0, " +
				"ctd_re_transfperc = 0, " +
				"ctd_re_transferrate = 0, " +
				"ctd_st_starttransfer = '', " +
				"ctd_st_endtransfer = '', " +
				"ctd_st_duration = '', " +
				"ctd_ch_droprecords  = (case when ctd_ch_droprecords<>'N' then 'R' else ctd_ch_droprecords end), " +
				"ctd_ch_createtable  = (case when ctd_ch_createtable<>'N' then 'R' else ctd_ch_createtable end), " +
				"ctd_ch_createpk     = (case when ctd_ch_createpk<>'N' then 'R' else ctd_ch_createpk end), " +
				"ctd_ch_createfk     = (case when ctd_ch_createfk<>'N' then 'R' else ctd_ch_createfk end), " +
				"ctd_ch_createuq     = (case when ctd_ch_createuq<>'N' then 'R' else ctd_ch_createuq end), " +
				"ctd_ch_createidx    = (case when ctd_ch_createidx<>'N' then 'R' else ctd_ch_createidx end), " +
				"ctd_ch_transferdata = (case when ctd_ch_transferdata<>'N' then 'R' else ctd_ch_transferdata end) " +
				"where conv_id=" + p_conv_id);

			System.Diagnostics.Process process = new System.Diagnostics.Process ();
			System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo ();
			startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;

			if (v_session.v_current_os == "unix") {
				startInfo.FileName = "mono";
				startInfo.Arguments = " --gc=sgen bin/OmniConversion.exe " + p_conv_id;
			} 
			else {
				startInfo.FileName = Environment.CurrentDirectory + "/bin/OmniConversion.exe";
				startInfo.Arguments = p_conv_id.ToString();
			}
			process.StartInfo = startInfo;
			process.Start ();

			v_session.v_omnidb_database.v_connection.Execute ("update conversions set conv_st_end = '', conv_re_perc = 0, conv_st_duration= '', conv_ch_status='E', process_id=" + process.Id + " where conv_id=" + p_conv_id);

			return v_return;

		}

		/// <summary>
		/// Stops a conversion.
		/// </summary>
		/// /// <param name="p_conv_id">Conversion ID.</param>
		[System.Web.Services.WebMethod]
		public static AjaxReturn StopConversion(int p_conv_id)
		{

			AjaxReturn v_return = new AjaxReturn();
			Session v_session = (Session)System.Web.HttpContext.Current.Session ["OMNIDB_SESSION"];

			if (v_session == null) 
			{
				v_return.v_error = true;
				v_return.v_error_id = 1;
				return v_return;
			} 

			System.Data.DataTable v_conversion_data = v_session.v_omnidb_database.v_connection.Query ("select process_id from conversions where conv_id=" + p_conv_id, "ConversionData");

			if (v_session.v_current_os == "unix") {
				System.Diagnostics.Process process = new System.Diagnostics.Process ();
				System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo ();
				startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
				startInfo.FileName = "kill";
				startInfo.Arguments = " -9 " + v_conversion_data.Rows [0] [0].ToString ();
				process.StartInfo = startInfo;
				process.Start ();
			} 
			else {
				try {
					System.Diagnostics.Process process = System.Diagnostics.Process.GetProcessById(Convert.ToInt32(v_conversion_data.Rows [0] [0]));
					process.Kill();
				}
				catch (System.ArgumentException) {

				}
			}

			v_session.v_omnidb_database.v_connection.Execute ("update conversions set conv_ch_status='C' where conv_id=" + p_conv_id);

			return v_return;

		}

	}
}

