/*
Copyright 2015-2017 The OmniDB Team
This file is part of OmniDB.
OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

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
	public class QueryData
	{
		public string v_sql_cmd;
		public int v_cmd_type;
		public int v_db_index;
	}

	/// <summary>
	/// Query WebSocket Server.
	/// </summary>
	public class QueryServer
	{
		private List<WebSocketSession> v_querySessions;
		private object v_querySessionsSyncRoot;
		private int v_port;
		private Dictionary<string, Session> v_httpSessions;

		//Message codes received from client requests
		private enum request
		{
			Login,
			Query,
			Execute,
			Script
		}

		//Message codes send to clients in response
		private enum response
		{
			LoginResult,
			QueryResult
		}

		public QueryServer(int p_port, ref Dictionary<string, Session> p_httpSessions)
		{
			this.v_querySessions = new List<WebSocketSession>();
			this.v_querySessionsSyncRoot = new object();
			this.v_port = p_port;
			this.v_httpSessions = p_httpSessions;
		}

		/// <summary>
		/// Starts the chat websocket server.
		/// </summary>
		public void Start()
		{
			WebSocketServer v_socketServer = new WebSocketServer();

			v_socketServer.Setup
			(
				new RootConfig(),
				new ServerConfig
				{
					Name = "QueryServer",
					Ip = "Any",
					Port = this.v_port,
					MaxRequestLength = 804857600,
					SyncSend = false,
					Mode = SocketMode.Tcp
				}
			);

			v_socketServer.NewMessageReceived += new SessionHandler<WebSocketSession, string>(NewMessageReceived);
			v_socketServer.NewSessionConnected += new SessionHandler<WebSocketSession>(NewSessionConnected);
			v_socketServer.SessionClosed += new SessionHandler<WebSocketSession, CloseReason>(SessionClosed);

			v_socketServer.Start();
		}

		/// <summary>
		/// Handler called when a new client connects to the server.
		/// </summary>
		/// <param name="p_webSocketSession">The connection session.</param>
		private void NewSessionConnected(WebSocketSession p_webSocketSession)
		{
			lock (this.v_querySessionsSyncRoot)
				this.v_querySessions.Add(p_webSocketSession);
		}

		/// <summary>
		/// Handler called when a new message from a client arrives to the server.
		/// </summary>
		/// <param name="p_webSocketSession">The connection session.</param>
		/// <param name="p_message">The message send by the client session.</param>
		private void NewMessageReceived(WebSocketSession p_webSocketSession, string p_message)
		{
			WebSocketMessage v_request = JsonConvert.DeserializeObject<WebSocketMessage>(p_message);

			if (v_request.v_code == (int)request.Login)
			{
				string v_userId = (string)v_request.v_data;

				if (!p_webSocketSession.Cookies.ContainsKey("user_id"))
				{
					p_webSocketSession.Cookies.Add("user_id", v_userId);
				}
			}

			WebSocketMessage v_response = new WebSocketMessage();
			v_response.v_context_code = v_request.v_context_code;

			if (!this.v_httpSessions.ContainsKey(p_webSocketSession.Cookies["user_id"]))
			{
				v_response.v_error = true;
				v_response.v_data = "Session Object was destroyed. Please, restart the application.";
				SendToClient(p_webSocketSession, v_response);

				return;
			}

			Session v_httpSession = this.v_httpSessions[p_webSocketSession.Cookies["user_id"]];

			if (v_httpSession == null)
			{
				v_response.v_error = true;
				v_response.v_data = "Session Object was destroyed. Please, restart the application.";
				SendToClient(p_webSocketSession, v_response);

				return;
			}

			switch (v_request.v_code)
			{
				case (int)request.Login:
					{
						v_response.v_code = (int)response.LoginResult;
						SendToClient(p_webSocketSession, v_response);

						return;
					}
				case (int)request.Query:
					{
						
						Thread thread = new Thread(() => ExecuteQuery(v_response,p_webSocketSession,v_request.v_data.ToString(), v_httpSession));
						thread.Start();

						return;
					}
				default:
					{
						v_response.v_error = true;
						v_response.v_data = "Unrecognized request code.";
						SendToClient(p_webSocketSession, v_response);

						return;
					}
			}


		}

		private void ExecuteQuery(WebSocketMessage p_response, WebSocketSession p_webSocketSession, string p_query_data, Session v_httpSession)
		{

			WebSocketMessage v_response = p_response;

			QueryData v_query_data = JsonConvert.DeserializeObject<QueryData>(p_query_data);

			v_response.v_code = (int)response.QueryResult;

			QueryReturn v_g1 = new QueryReturn();

			System.Collections.Generic.List<System.Collections.Generic.List<string>> v_table = new System.Collections.Generic.List<System.Collections.Generic.List<string>>();

			OmniDatabase.Generic v_database2 = v_httpSession.v_databases[v_query_data.v_db_index];

			OmniDatabase.Generic v_database = OmniDatabase.Generic.InstantiateDatabase(
				v_database2.v_alias,
				v_database2.v_conn_id,
				v_database2.v_db_type,
				v_database2.v_server,
				v_database2.v_port,
				v_database2.v_service,
				v_database2.v_user,
				v_database2.v_connection.v_password,
				v_database2.v_schema
					);

			v_database.v_connection.SetTimeout(0);

			if (v_query_data.v_cmd_type == -2)
			{

				try
				{
					v_httpSession.Execute(v_database, v_query_data.v_sql_cmd, true, true);
				}
				catch (Spartacus.Database.Exception e)
				{

					v_response.v_error = true;
					v_response.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
					SendToClient(p_webSocketSession, v_response);

					return;

				}
				catch (System.InvalidOperationException e)
				{
					v_response.v_error = true;
					v_response.v_data = e.Message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
					SendToClient(p_webSocketSession, v_response);

					return;
				}
			}
			else if (v_query_data.v_cmd_type == -3)
			{

				string[] v_commands = v_query_data.v_sql_cmd.Split(';');

				string v_return_html = "";

				int v_num_success_commands = 0;
				int v_num_error_commands = 0;

				v_database.v_connection.Open();

				foreach (string v_command in v_commands)
				{

					if (v_command.Trim() != "")
					{

						try
						{
							v_httpSession.Execute(v_database, v_command, true, true);
							v_num_success_commands++;

						}
						catch (Spartacus.Database.Exception e)
						{
							v_num_error_commands++;
							v_return_html += "<b>Command:</b> " + v_command + "<br/><br/><b>Message:</b> " + e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>") + "<br/><br/>";
						}

					}
				}


				v_response.v_data = "<b>Successful commands:</b> " + v_num_success_commands + "<br/>";
				v_response.v_data += "<b>Errors: </b> " + v_num_error_commands + "<br/><br/>";

				if (v_num_error_commands > 0)
				{
					v_response.v_data += "<b>Errors details:</b><br/><br/>" + v_return_html;
				}

				v_database.v_connection.Close();

			}
			else
			{
				try
				{
					System.Collections.Generic.List<string> v_columns;

					if (v_query_data.v_cmd_type == -1)
						v_table = v_httpSession.QueryList(v_database, v_query_data.v_sql_cmd, true, true, out v_columns);
					else
						v_table = v_httpSession.QueryListLimited(v_database, v_query_data.v_sql_cmd, v_query_data.v_cmd_type, true, false, out v_columns);

					v_g1.v_query_info = "Number of records: " + v_table.Count.ToString();
					v_g1.v_data = v_table;
					v_g1.v_col_names = v_columns;

					v_response.v_data = v_g1;

				}
				catch (Spartacus.Database.Exception e)
				{
					v_response.v_error = true;
					v_response.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
					SendToClient(p_webSocketSession, v_response);

					return;
				}
				catch (System.InvalidOperationException e)
				{
					v_response.v_error = true;
					v_response.v_data = e.Message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
					SendToClient(p_webSocketSession, v_response);

					return;
				}
				catch (System.Data.DuplicateNameException e)
				{
					v_response.v_error = true;
					v_response.v_data = e.Message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
					SendToClient(p_webSocketSession, v_response);

					return;
				}

			}

			SendToClient(p_webSocketSession, v_response);
		}

		/// <summary>
		/// Handler called when a connection is closed.
		/// </summary>
		/// <param name="p_webSocketSession">The connection session.</param>
		/// <param name="p_reason">The reason why connection was closed.</param>
		private void SessionClosed(WebSocketSession p_webSocketSession, CloseReason p_reason)
		{
			lock (v_querySessionsSyncRoot)
				this.v_querySessions.Remove(p_webSocketSession);

			if (p_reason == CloseReason.ServerShutdown)
				return;

			WebSocketMessage v_response = new WebSocketMessage();

			SendToAllClients(v_response);
		}

		/// <summary>
		/// Sends a message to the client that generated the request.
		/// </summary>
		/// <param name="p_webSocketSession">The connection session.</param>
		/// <param name="p_message">The message to be send to the client.</param>
		private void SendToClient(WebSocketSession p_webSocketSession, WebSocketMessage p_message)
		{
			p_webSocketSession.Send(JsonConvert.SerializeObject(p_message));
		}

		/// <summary>
		/// Sends a message to all clients connected to the server.
		/// </summary>
		/// <param name="p_message">The message to be send to the clients.</param>
		private void SendToAllClients(WebSocketMessage p_message)
		{
			lock (this.v_querySessionsSyncRoot)
			{
				foreach (var v_chatSession in this.v_querySessions)
				{
					v_chatSession.Send(JsonConvert.SerializeObject(p_message));
				}
			}
		}

	}

}
