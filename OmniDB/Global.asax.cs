/*
Copyright 2016 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

using System;
using System.Collections;
using System.ComponentModel;
using System.Web;
using System.Web.SessionState;
using System.Collections.Generic;
using System.Threading;

namespace OmniDB
{
	public class Global : System.Web.HttpApplication
	{
		private Dictionary<string, Session> v_httpSessions = new Dictionary<string, Session>();
		private ChatServer v_chatServer;

		protected void Application_Start (Object sender, EventArgs e)
		{
			//StartChatServer();
			this.v_chatServer = new ChatServer(2011, this.v_httpSessions);
			v_chatServer.Start();
		}

		protected void Application_AcquireRequestState(Object sender, EventArgs e)
		{
			if(System.Web.HttpContext.Current != null && System.Web.HttpContext.Current.Session != null)
			{
				Session v_httpSession = (Session)System.Web.HttpContext.Current.Session["OMNIDB_SESSION"];

				if(v_httpSession != null)
				{
					if(!v_httpSessions.ContainsKey(v_httpSession.v_user_id))
					{
						v_httpSessions.Add(v_httpSession.v_user_id, v_httpSession);
					}
				}
			}
		}

		protected void Session_Start (Object sender, EventArgs e)
		{

		}

		protected void Application_BeginRequest (Object sender, EventArgs e)
		{

		}

		protected void Application_EndRequest (Object sender, EventArgs e)
		{

		}

		protected void Application_AuthenticateRequest (Object sender, EventArgs e)
		{

		}

		protected void Application_Error (Object sender, EventArgs e)
		{

		}

		protected void Session_End (Object sender, EventArgs e)
		{

		}

		protected void Application_End (Object sender, EventArgs e)
		{
			
		}
	}
}
