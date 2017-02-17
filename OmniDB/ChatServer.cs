using System;
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
	public class ChatServer
	{
		private List<WebSocketSession> v_chatSessions;
		private object v_chatSessionsSyncRoot;
		private int v_port;
		private Dictionary<string, Session> v_httpSessions;

		public ChatServer(int p_port, Dictionary<string, Session> p_httpSessions)
		{
			this.v_chatSessions = new List<WebSocketSession>();
			this.v_chatSessionsSyncRoot = new object();
			this.v_port = p_port;
			this.v_httpSessions = p_httpSessions;
		}

		public void Start()
		{
			WebSocketServer v_socketServer = new WebSocketServer();

			v_socketServer.Setup
			(
				new RootConfig(),
				new ServerConfig
				{
					Name = "ChatServer",
					Ip = "Any",
					Port = this.v_port,
					MaxRequestLength = 804857600,
					SyncSend = false,
					Mode = SocketMode.Tcp,
					ReceiveBufferSize = 9999999,
					SendBufferSize = 9999999
				}
			);

			v_socketServer.NewMessageReceived += new SessionHandler<WebSocketSession, string>(NewMessageReceived);
			v_socketServer.NewSessionConnected += new SessionHandler<WebSocketSession>(NewSessionConnected);
			v_socketServer.SessionClosed += new SessionHandler<WebSocketSession, CloseReason>(SessionClosed);

			//Application["ChatServerPort"] = v_socketServer.Config.Port;
			v_socketServer.Start();
		}

		private void NewSessionConnected(WebSocketSession p_session)
		{
			lock(this.v_chatSessionsSyncRoot)
				this.v_chatSessions.Add(p_session);

			//SendToAll("System: " + session.Cookies["name"] + " connected");
		}

		private void NewMessageReceived(WebSocketSession p_session, string p_message)
		{
			/*Thread v_sendResponse = new Thread(SendResponse);
			v_sendResponse.Start((Object)p_session);*/

			WebSocketMessage v_request = JsonConvert.DeserializeObject<WebSocketMessage>(p_message);

			WebSocketMessage v_response = new WebSocketMessage();
			v_response.v_user_id = v_request.v_user_id;

			if(!this.v_httpSessions.ContainsKey(v_request.v_user_id.ToString()))
			{
				v_response.v_error = true;
				v_response.v_data = "Session Object was destroyed. Please, restart the application.";

				SendToClient(v_response);
			}

			Session v_session = this.v_httpSessions[v_request.v_user_id.ToString()];

			switch(v_request.v_code)
			{
			}

			//v_response.v_data = v_session.v_databases.Count;
			//SendToAllClients(v_response);
		}

		private void SessionClosed(WebSocketSession p_session, CloseReason p_reason)
		{
			//Console.WriteLine("o cara saiu");

			lock(v_chatSessionsSyncRoot)
				this.v_chatSessions.Remove(p_session);

			if(p_reason == CloseReason.ServerShutdown)
				return;

			//SendToAll("System: " + session.Cookies["name"] + " disconnected");
		}

		private void SendToClient(WebSocketMessage p_message)
		{
			
		}

		private void SendToAllClients(WebSocketMessage p_message)
		{
			lock(this.v_chatSessionsSyncRoot)
			{
				foreach(var v_chatSession in this.v_chatSessions)
				{
					v_chatSession.Send(JsonConvert.SerializeObject(p_message));
				}
			}
		}

		/*private void SendResponse(Object p_session)
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
	}
}