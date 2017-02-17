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
using SuperSocket.Common;
using SuperSocket.SocketBase;
using SuperSocket.SocketBase.Command;
using SuperSocket.SocketBase.Config;
using SuperSocket.SocketEngine;
using SuperSocket.SocketEngine.Configuration;
using SuperSocket.ServerManager;
using SuperSocket.WebSocket;
using log4net;
using Newtonsoft.Json;

namespace OmniDB
{
	public class Global : System.Web.HttpApplication
	{
		private List<WebSocketSession> v_chatSessions = new List<WebSocketSession>();
		private object v_chatSessionsSyncRoot = new object();
		private Dictionary<string, Session> v_httpSessions = new Dictionary<string, Session>();

		protected void Application_Start (Object sender, EventArgs e)
		{
			StartChatServer();
		}

		void StartChatServer()
		{
			var v_socketServer = new WebSocketServer();
			v_socketServer.Setup(new RootConfig(),
				new ServerConfig
				{
					Name = "ChatServer",
					Ip = "Any",
					Port = 2011,
					MaxRequestLength = 804857600,
					SyncSend = false,
					Mode = SocketMode.Tcp,
					ReceiveBufferSize = 9999999,
					SendBufferSize = 9999999
				});

			v_socketServer.NewMessageReceived += new SessionHandler<WebSocketSession, string>(ChatServerNewMessageReceived);
			v_socketServer.NewSessionConnected += new SessionHandler<WebSocketSession>(ChatServerNewSessionConnected);
			v_socketServer.SessionClosed += new SessionHandler<WebSocketSession, CloseReason>(ChatServerSessionClosed);

			Application["ChatServerPort"] = v_socketServer.Config.Port;
			v_socketServer.Start();
		}

		void ChatServerNewSessionConnected(WebSocketSession p_session)
		{
			lock(v_chatSessionsSyncRoot)
				v_chatSessions.Add(p_session);

			//SendToAll("System: " + session.Cookies["name"] + " connected");
		}

		void ChatServerSessionClosed(WebSocketSession p_session, CloseReason p_reason)
		{
			//Console.WriteLine("o cara saiu");

			lock(v_chatSessionsSyncRoot)
				v_chatSessions.Remove(p_session);

			if(p_reason == CloseReason.ServerShutdown)
				return;

			//SendToAll("System: " + session.Cookies["name"] + " disconnected");
		}

		void ChatServerNewMessageReceived(WebSocketSession p_session, string p_message)
		{
			/*Thread v_sendResponse = new Thread(SendResponse);
			v_sendResponse.Start((Object)p_session);*/
			ChatServerSendToAll ("kkk");
		}

		void ChatServerSendToAll(string p_message)
		{
			lock(v_chatSessionsSyncRoot)
			{
				foreach(var v_chatSession in v_chatSessions)
				{
					v_chatSession.Send(p_message);
				}
			}
		}

		/*void SendResponse(Object p_session)
		{
			WebSocketSession v_session = (WebSocketSession)p_session;
			List<string> v_response = new List<string>();;

			try
			{
				for(int i = 0; i < 1000000; i++)
				{
					v_response.Add("aaaaa");
				}
			}
			catch(System.Exception e)
			{
				Console.WriteLine(e);
			}

			v_session.Send(JsonConvert.SerializeObject(v_response));
		}*/

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
