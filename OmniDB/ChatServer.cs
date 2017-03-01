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
	/// <summary>
	/// Chat WebSocket Server.
	/// </summary>
	public class ChatServer
	{
		private List<WebSocketSession> v_chatSessions;
		private object v_chatSessionsSyncRoot;
		private int v_port;
		private Dictionary<string, Session> v_httpSessions;

		//Message codes received from client requests
		private enum request
		{
			Login,
			GetOldMessages,
			ViewMessage,
			SendMessage,
			Writing,
			NotWriting
		}

		//Message codes send to clients in response
		private enum response
		{
			OldMessages,
			NewMessage,
			UserList,
			UserWriting,
			UserNotWriting
		}

		public ChatServer(int p_port, ref Dictionary<string, Session> p_httpSessions)
		{
			this.v_chatSessions = new List<WebSocketSession>();
			this.v_chatSessionsSyncRoot = new object();
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
					Name = "ChatServer",
					Ip = "Any",
					Port = this.v_port,
					MaxRequestLength = 804857600,
					SyncSend = false,
					Mode = SocketMode.Tcp
					//ReceiveBufferSize = 9999999,
					//SendBufferSize = 9999999
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
			lock(this.v_chatSessionsSyncRoot)
				this.v_chatSessions.Add(p_webSocketSession);
		}

		/// <summary>
		/// Handler called when a new message from a client arrives to the server.
		/// </summary>
		/// <param name="p_webSocketSession">The connection session.</param>
		/// <param name="p_message">The message send by the client session.</param>
		private void NewMessageReceived(WebSocketSession p_webSocketSession, string p_message)
		{
			WebSocketMessage v_request = JsonConvert.DeserializeObject<WebSocketMessage>(p_message);

			if(v_request.v_code == (int)request.Login)
			{
				string v_userId = (string)v_request.v_data;

				if(!p_webSocketSession.Cookies.ContainsKey("user_id"))
				{
					p_webSocketSession.Cookies.Add("user_id", v_userId);
				}
			}

			WebSocketMessage v_response = new WebSocketMessage();
			
			if(!this.v_httpSessions.ContainsKey(p_webSocketSession.Cookies["user_id"]))
			{
				v_response.v_error = true;
				v_response.v_data = "Session Object was destroyed. Please, restart the application.";
				SendToClient(p_webSocketSession, v_response);

				return;
			}

			Session v_httpSession = this.v_httpSessions[p_webSocketSession.Cookies["user_id"]];

			if(v_httpSession == null) 
			{
				v_response.v_error = true;
				v_response.v_data = "Session Object was destroyed. Please, restart the application.";
				SendToClient(p_webSocketSession, v_response);

				return;
			}

			switch(v_request.v_code)
			{
				case (int)request.Login:
				{
					OmniDatabase.Generic v_database = v_httpSession.v_omnidb_database;
					List<ChatUser> v_userList = new List<ChatUser>();

					try
					{
						string v_onlineUsers = "";

						for(int i = 0; i < this.v_chatSessions.Count; i++)
						{
							if(this.v_chatSessions[i].Cookies.ContainsKey("user_id"))
							{
								v_onlineUsers += this.v_chatSessions[i].Cookies["user_id"] + ", ";
							}
						}

						v_onlineUsers = v_onlineUsers.Remove(v_onlineUsers.Length - 2);

						string v_sql =
							"select x.*" +
							"from (" +
							"    select user_id, " +
							"           user_name, " + 
							"           1 as online " +
							"    from users " +
							"    where user_id in ( " + 
							     v_onlineUsers + ") " +
							"     " +
							"    union " +
							"     " +
							"    select user_id, " +
							"           user_name, " +
							"           0 as online " +
							"    from users " +
							"    where user_id not in ( " + 
							     v_onlineUsers + ") " +
							") x " +
							"order by x.online desc, x.user_name ";

						System.Data.DataTable v_table = v_database.v_connection.Query(v_sql, "chat_users");

						if(v_table != null && v_table.Rows.Count > 0)
						{
							for(int i = 0; i < v_table.Rows.Count; i++)
							{
								ChatUser v_user = new ChatUser();

								v_user.v_user_id = int.Parse(v_table.Rows[i]["user_id"].ToString());
								v_user.v_user_name = v_table.Rows[i]["user_name"].ToString();
								v_user.v_user_online = int.Parse(v_table.Rows[i]["online"].ToString());

								v_userList.Add(v_user);
							}
						}
					}
					catch(Spartacus.Database.Exception e)
					{
						v_response.v_error = true;
						v_response.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
						SendToClient(p_webSocketSession, v_response);

						return;
					}

					v_response.v_code = (int)response.UserList;
					v_response.v_data = v_userList;
					SendToAllClients(v_response);

					return;
				}
				case (int)request.GetOldMessages:
				{
					OmniDatabase.Generic v_database = v_httpSession.v_omnidb_database;
					List<ChatMessage> v_messageList = new List<ChatMessage>();

					try
					{
						string v_sql =
							"select mes.mes_in_code, " +
							"       use.user_name, " +
							"       mes.mes_st_text, " +
							"       mes.mes_dt_timestamp " +
							"from messages mes " +
							"inner join messages_users meu " +
							"           on mes.mes_in_code = meu.mes_in_code " +
							"inner join users use " +
							"           on mes.user_id = use.user_id " +
							"where meu.user_id = " + v_httpSession.v_user_id + " " +
							"  and meu.meu_bo_viewed = 'N';";

						System.Data.DataTable v_table = v_database.v_connection.Query(v_sql, "chat_messages");

						if (v_table != null && v_table.Rows.Count > 0)
						{
							for (int i = 0; i < v_table.Rows.Count; i++)
							{
								ChatMessage v_message = new ChatMessage();
								v_message.v_message_id = int.Parse(v_table.Rows[i]["mes_in_code"].ToString());
								v_message.v_user_name = v_table.Rows[i]["user_name"].ToString();
								v_message.v_text = v_table.Rows[i]["mes_st_text"].ToString();
								v_message.v_timestamp = v_table.Rows[i]["mes_dt_timestamp"].ToString();

								v_messageList.Add(v_message);
							}
						}
					}
					catch(Spartacus.Database.Exception e)
					{
						v_response.v_error = true;
						v_response.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
						SendToClient(p_webSocketSession, v_response);

						return;
					}
						
					v_response.v_code = (int)response.OldMessages;
					v_response.v_data = v_messageList;
					SendToClient(p_webSocketSession, v_response);
					
					return;
				}
				case (int)request.ViewMessage:
				{
					OmniDatabase.Generic v_database = v_httpSession.v_omnidb_database;
					ChatMessage v_message = JsonConvert.DeserializeObject<ChatMessage>(v_request.v_data.ToString());

					try
					{
						string v_sql =
							"update messages_users " +
							"set meu_bo_viewed = 'Y' " +
							"where user_id = " + v_httpSession.v_user_id + " " +
							"  and mes_in_code = " + v_message.v_message_id;

						v_database.v_connection.Execute(v_sql);
					}
					catch(Spartacus.Database.Exception e)
					{
						v_response.v_error = true;
						v_response.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
						SendToClient(p_webSocketSession, v_response);

						return;
					}

					return;
				}
				case (int)request.SendMessage:
				{
					OmniDatabase.Generic v_database = v_httpSession.v_omnidb_database;
					string v_text = (string)v_request.v_data;

					ChatMessage v_message;

					try 
					{
						string v_sql = 
							"insert into messages (" +
							"    mes_st_text, " +
							"    mes_dt_timestamp, " +
							"    user_id " +
							") values ( " +
							"  '" + v_text + "', " +
							"    datetime('now', 'localtime'), " +
							"  " + v_httpSession.v_user_id +
							");" +
							"select max(mes_in_code) " +
							"from messages;";

						int v_messsageCode = int.Parse(v_database.v_connection.ExecuteScalar(v_sql));

						v_sql =
							"insert into messages_users (" +
							"    mes_in_code, " +
							"    meu_bo_viewed, " +
							"    user_id " +
							")" +
							"select " + v_messsageCode + ", " +
							"    'N', " +
							"    use.user_id " +
							"from users use ";// +
							//"where use.user_id <> " + v_httpSession.v_user_id + ";";

						v_database.v_connection.Execute(v_sql);

						v_sql = 
							"select mes_dt_timestamp " +
							"from messages " +
							"where mes_in_code = " + v_messsageCode;

						v_message = new ChatMessage();
						v_message.v_message_id = v_messsageCode;
						v_message.v_user_name = v_httpSession.v_user_name;
						v_message.v_text = v_text;
						v_message.v_timestamp = v_database.v_connection.ExecuteScalar(v_sql);
					}
					catch(Spartacus.Database.Exception e)
					{
						v_response.v_error = true;
						v_response.v_data = e.v_message.Replace("<","&lt;").Replace(">","&gt;").Replace(System.Environment.NewLine, "<br/>");
						SendToClient(p_webSocketSession, v_response);

						return;
					}

					v_response.v_code = (int)response.NewMessage;
					v_response.v_data = v_message;
					SendToAllClients(v_response);

					return;
				}
				case (int)request.Writing:
				{
					v_response.v_code = (int)response.UserWriting;
					v_response.v_data = v_httpSession.v_user_id;
					SendToAllClients(v_response);

					return;
				}
				case (int)request.NotWriting:
				{
					v_response.v_code = (int)response.UserNotWriting;
					v_response.v_data = v_httpSession.v_user_id;
					SendToAllClients(v_response);

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

			/*Thread v_sendResponse = new Thread(SendResponse);
			v_sendResponse.Start((Object)p_webSocketSession);*/
		}

		/// <summary>
		/// Handler called when a connection is closed.
		/// </summary>
		/// <param name="p_webSocketSession">The connection session.</param>
		/// <param name="p_reason">The reason why connection was closed.</param>
		private void SessionClosed(WebSocketSession p_webSocketSession, CloseReason p_reason)
		{
			lock(v_chatSessionsSyncRoot)
				this.v_chatSessions.Remove(p_webSocketSession);

			if(p_reason == CloseReason.ServerShutdown)
				return;

			WebSocketMessage v_response = new WebSocketMessage();

			if(!this.v_httpSessions.ContainsKey(p_webSocketSession.Cookies["user_id"]))
			{
				v_response.v_error = true;
				v_response.v_data = "Session Object was destroyed. Please, restart the application.";
				SendToClient(p_webSocketSession, v_response);

				return;
			}

			Session v_httpSession = this.v_httpSessions[p_webSocketSession.Cookies["user_id"]];

			if(v_httpSession == null) 
			{
				v_response.v_error = true;
				v_response.v_data = "Session Object was destroyed. Please, restart the application.";
				SendToClient(p_webSocketSession, v_response);

				return;
			}

			OmniDatabase.Generic v_database = v_httpSession.v_omnidb_database;
			List<ChatUser> v_userList = new List<ChatUser>();

			try
			{
				string v_onlineUsers = "";

				for(int i = 0; i < this.v_chatSessions.Count; i++)
				{
					if(this.v_chatSessions[i].Cookies.ContainsKey("user_id"))
					{
						v_onlineUsers += this.v_chatSessions[i].Cookies["user_id"] + ", ";
					}
				}

				v_onlineUsers = v_onlineUsers.Remove(v_onlineUsers.Length - 2);

				string v_sql =
					"select x.*" +
					"from (" +
					"    select user_id, " +
					"           user_name, " + 
					"           1 as online " +
					"    from users " +
					"    where user_id in ( " + 
					v_onlineUsers + ") " +
					"     " +
					"    union " +
					"     " +
					"    select user_id, " +
					"           user_name, " +
					"           0 as online " +
					"    from users " +
					"    where user_id not in ( " + 
					v_onlineUsers + ") " +
					") x " +
					"order by x.online desc, x.user_name ";

				System.Data.DataTable v_table = v_database.v_connection.Query(v_sql, "chat_users");

				if(v_table != null && v_table.Rows.Count > 0)
				{
					for(int i = 0; i < v_table.Rows.Count; i++)
					{
						ChatUser v_user = new ChatUser();

						v_user.v_user_id = int.Parse(v_table.Rows[i]["user_id"].ToString());
						v_user.v_user_name = v_table.Rows[i]["user_name"].ToString();
						v_user.v_user_online = int.Parse(v_table.Rows[i]["online"].ToString());

						v_userList.Add(v_user);
					}
				}
			}
			catch(Spartacus.Database.Exception e)
			{
				v_response.v_error = true;
				v_response.v_data = e.v_message.Replace("<", "&lt;").Replace(">", "&gt;").Replace(System.Environment.NewLine, "<br/>");
				SendToClient(p_webSocketSession, v_response);

				return;
			}

			v_response.v_code = (int)response.UserList;
			v_response.v_data = v_userList;
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
			lock(this.v_chatSessionsSyncRoot)
			{
				foreach(var v_chatSession in this.v_chatSessions)
				{
					v_chatSession.Send(JsonConvert.SerializeObject(p_message));
				}
			}
		}

		/*private void SendResponse(Object p_webSocketSession)
		{
			WebSocketSession v_session = (WebSocketSession)p_webSocketSession;
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

	/// <summary>
	/// Chat message.
	/// </summary>
	public class ChatMessage
	{
		public int v_message_id;
		public string v_user_name;
		public string v_text;
		public string v_timestamp;
	}

	/// <summary>
	/// Chat user.
	/// </summary>
	public class ChatUser
	{
		public int v_user_id;
		public string v_user_name;
		public int v_user_online;
	}
}