import threading, time, datetime, json
import traceback

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado.httpserver
from tornado import gen
import ssl,os

import OmniDB_app.include.Spartacus as Spartacus
import OmniDB_app.include.Spartacus.Database as Database
import OmniDB_app.include.Spartacus.Utils as Utils
import OmniDB_app.include.OmniDatabase as OmniDatabase

from enum import IntEnum
from datetime import datetime
import sys

from . import settings

from django.contrib.sessions.backends.db import SessionStore

import logging
logger = logging.getLogger('OmniDB_app.ChatServer')

import re
import base64
import shutil
from enum import Enum
from .Chat import classes
from .Chat import exception

v_chatSessions = []
v_chatSessionsLock = threading.RLock()

class request(Enum):
    """Enum class that contains request types and codes.
    """

    Login = '0'
    SendGroupMessage = '1'
    RetrieveGroupHistory = '2'
    MarkGroupMessagesAsRead = '3'
    GetUserStatus = '4'
    SetGroupUserWriting = '5'
    ChangeGroupSilenceSettings = '6'
    RemoveGroupMessage = '7'
    UpdateGroupSnippetMessage = '8'
    UpdateGroupMessage = '9'
    SendChannelMessage = '10'
    RetrieveChannelHistory = '11'
    MarkChannelMessagesAsRead = '12'
    SetChannelUserWriting = '13'
    ChangeChannelSilenceSettings = '14'
    RemoveChannelMessage = '15'
    UpdateChannelSnippetMessage = '16'
    UpdateChannelMessage = '17'
    CreatePrivateChannel = '18'
    RenamePrivateChannel = '19'
    QuitPrivateChannel = '20'
    InvitePrivateChannelMembers = '21'
    Ping = '22'
    SetUserChatStatus = '23'
    SearchOldMessages = '24'
    SendMessageAsBot = '99'

class response(Enum):
    """Enum class that contains response types and codes.
    """

    LoginResult = '0'
    NewGroupMessage = '1'
    RetrievedGroupHistory = '2'
    MarkedGroupMessagesAsRead = '3'
    UserStatus = '4'
    GroupUserWriting = '5'
    GroupSilenceSettings = '6'
    RemovedGroupMessage = '7'
    UpdatedGroupSnippetMessage = '8'
    UpdatedGroupMessage = '9'
    NewChannelMessage = '10'
    RetrievedChannelHistory = '11'
    MarkedChannelMessagesAsRead = '12'
    ChannelUserWriting = '13'
    ChannelSilenceSettings = '14'
    RemovedChannelMessage = '15'
    UpdatedChannelSnippetMessage = '16'
    UpdatedChannelMessage = '17'
    NewPrivateChannel = '18'
    RenamedPrivateChannel = '19'
    QuittedPrivateChannel = '20'
    InvitedPrivateChannelMembers = '21'
    Pong = '22'
    UserChatStatus = '23'
    SearchedOldMessages = '24'
    NewMessageAsBot = '99'

def ToDict(o):
    return o.__dict__

class WSHandler(tornado.websocket.WebSocketHandler):
    """Implements the websocket server for Chat.

        Attributes:
            cookies (dict): a dict for custom use, containing key/value pairs.
    """

    def open(self):
        """Method executed when a new websocket connection opens.
        """

        try:
            v_chatSessionsLock.acquire()
            self.settings['websocket_max_message_size'] = 804857600
            v_chatSessions.append(self)
        finally:
            v_chatSessionsLock.release()

    def on_message(self, p_requestMessage):
        """Method executed when a websocket connection sends a message.
        """

        v_responseMessage = {
            'v_code': 0,
            'v_context_code': -1,
            'v_error': False,
            'v_data': ''
        }

        try:
            #Loads message from json.
            v_jsonObject = json.loads(p_requestMessage)
            v_code = v_jsonObject['v_code']
            v_contextCode = v_jsonObject['v_context_code']
            v_data = v_jsonObject['v_data']

            v_responseMessage['v_context_code'] = v_contextCode

            #Check if a new connection.
            if v_code == request.Login.value:
                if 'session_key' not in self.cookies:
                    self.cookies['session_key'] = str(v_data)

                    try:
                        self.session = SessionStore(session_key=v_data)['omnidb_session']
                    except Exception:
                        p_responseMessage['v_error'] = True
                        p_responseMessage['v_data'] = 'The user session is missing. Please, reconnect to the page.'
                        SendToClient(self, v_responseMessage, True)
                        return

            #Deal with message according to it request code.
            if v_code == request.Login.value:
                Login(self, v_jsonObject, v_responseMessage)
            elif v_code == request.SendGroupMessage.value:
                SendGroupMessage(self, v_jsonObject, v_responseMessage)
            elif v_code == request.RetrieveGroupHistory.value:
                RetrieveGroupHistory(self, v_jsonObject, v_responseMessage)
            elif v_code == request.MarkGroupMessagesAsRead.value:
                MarkGroupMessagesAsRead(self, v_jsonObject, v_responseMessage)
            elif v_code == request.GetUserStatus.value:
                GetUserStatus(self, v_jsonObject, v_responseMessage)
            elif v_code == request.SetGroupUserWriting.value:
                SetGroupUserWriting(self, v_jsonObject, v_responseMessage)
            elif v_code == request.ChangeGroupSilenceSettings.value:
                ChangeGroupSilenceSettings(self, v_jsonObject, v_responseMessage)
            elif v_code == request.RemoveGroupMessage.value:
                RemoveGroupMessage(self, v_jsonObject, v_responseMessage)
            elif v_code == request.UpdateGroupSnippetMessage.value:
                UpdateGroupSnippetMessage(self, v_jsonObject, v_responseMessage)
            elif v_code == request.UpdateGroupMessage.value:
                UpdateGroupMessage(self, v_jsonObject, v_responseMessage)
            elif v_code == request.SendChannelMessage.value:
                SendChannelMessage(self, v_jsonObject, v_responseMessage)
            elif v_code == request.RetrieveChannelHistory.value:
                RetrieveChannelHistory(self, v_jsonObject, v_responseMessage)
            elif v_code == request.MarkChannelMessagesAsRead.value:
                MarkChannelMessagesAsRead(self, v_jsonObject, v_responseMessage)
            elif v_code == request.SetChannelUserWriting.value:
                SetChannelUserWriting(self, v_jsonObject, v_responseMessage)
            elif v_code == request.ChangeChannelSilenceSettings.value:
                ChangeChannelSilenceSettings(self, v_jsonObject, v_responseMessage)
            elif v_code == request.RemoveChannelMessage.value:
                RemoveChannelMessage(self, v_jsonObject, v_responseMessage)
            elif v_code == request.UpdateChannelSnippetMessage.value:
                UpdateChannelSnippetMessage(self, v_jsonObject, v_responseMessage)
            elif v_code == request.UpdateChannelMessage.value:
                UpdateChannelMessage(self, v_jsonObject, v_responseMessage)
            elif v_code == request.CreatePrivateChannel.value:
                CreatePrivateChannel(self, v_jsonObject, v_responseMessage)
            elif v_code == request.RenamePrivateChannel.value:
                RenamePrivateChannel(self, v_jsonObject, v_responseMessage)
            elif v_code == request.QuitPrivateChannel.value:
                QuitPrivateChannel(self, v_jsonObject, v_responseMessage)
            elif v_code == request.InvitePrivateChannelMembers.value:
                InvitePrivateChannelMembers(self, v_jsonObject, v_responseMessage)
            elif v_code == request.Ping.value:
                Ping(self, v_jsonObject, v_responseMessage)
            elif v_code == request.SetUserChatStatus.value:
                SetUserChatStatus(self, v_jsonObject, v_responseMessage)
            elif v_code == request.SearchOldMessages.value:
                SearchOldMessages(self, v_jsonObject, v_responseMessage)
            elif v_code == request.SendMessageAsBot.value:
                SendMessageAsBot(self, v_jsonObject, v_responseMessage)
        except Exception as exc:
            logger.error('''*** Exception ***\n{0}'''.format(traceback.format_exc()))
            v_responseMessage['v_error'] = True
            v_responseMessage['v_data'] = 'An expeted error has occurred while dealing with your request. Please, contact system administrator.'
            SendToClient(self, v_responseMessage, True)
            return

    def on_close(self):
        """Method executed when a new websocket connection closes.
        """

        v_userCode = 0

        if 'user_id' in self.cookies:
            v_userCode = int(self.cookies['user_id'].value)

        try:
            v_chatSessionsLock.acquire()
            v_chatSessions.remove(self)
        finally:
            v_chatSessionsLock.release()

        if v_userCode != 0:
            v_found = False

            try:
                v_chatSessionsLock.acquire()

                for v_chatSession in v_chatSessions:
                    if 'user_id' in v_chatSession.cookies and int(v_chatSession.cookies['user_id'].value) == v_userCode:
                        v_found = True
                        break
            finally:
                v_chatSessionsLock.release()

            if not v_found:
                v_responseMessage = {
                    'v_code': response.UserStatus.value,
                    'v_context_code': None,
                    'v_error': False,
                    'v_data': {
                        'userCode': int(self.cookies['user_id'].value),
                        'userStatus': 'offline'
                    }
                }

                SendToAllClients(v_responseMessage)

    def check_origin(self, p_origin):
        """Ignore origin problems.
        """
        return True

def SendToClient(p_webSocketSession, p_responseMessage, p_sendToSame):
    """Send a message to a specific websocket client.

        Args:
            p_webSocketSession (WSHandler): the websocket client that will receive the message.
            p_responseMessage (dict): the message itself.
            p_sendToSame (bool): indicates if we should consider all connections of the same user
    """

    if 'user_id' in p_webSocketSession.cookies and p_sendToSame:
        for v_webSocketSession in v_chatSessions:
            if 'user_id' in v_webSocketSession.cookies and int(v_webSocketSession.cookies['user_id'].value) == int(p_webSocketSession.cookies['user_id'].value):
                v_webSocketSession.write_message(json.dumps(p_responseMessage, default=ToDict))
    else:
        p_webSocketSession.write_message(json.dumps(p_responseMessage, default=ToDict))

def SendToSomeClients(p_userList, p_responseMessage):
    """Send a message to a group of websocket clients.

        Args:
            p_userList (list): a list where each item is a user id (int).
            p_responseMessage (dict): the message itself.
    """

    for v_webSocketSession in v_chatSessions:
        if 'user_id' in v_webSocketSession.cookies and int(v_webSocketSession.cookies['user_id'].value) in p_userList:
            v_webSocketSession.write_message(json.dumps(p_responseMessage, default=ToDict))

def SendToAllClients(p_responseMessage):
    """Send a message to all websocket clients.

        Args:
            p_responseMessage (dict): the message itself.
    """

    for v_webSocketSession in v_chatSessions:
        v_webSocketSession.write_message(json.dumps(p_responseMessage, default=ToDict))

def GetUsersToSendMessageByGroupCode(p_webSocketSession, p_groupCode):
    """Verify users that must receive a message based on a given group code.

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_groupCode (int): the group code.

        Returns:
            list of user codes, where each item is a 'int' instance.
    """

    v_table = None
    v_userList = []

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_table = v_database.Query('''
            select usg.use_in_code
            from users_groups usg
            where usg.gro_in_code = {0}'''.format(p_groupCode)
        )

        v_database.Close()
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'GetUsersToSendMessageByGroupCode', traceback.format_exc())
        return None

    for v_row in v_table.Rows:
        v_userList.append(v_row['use_in_code'])

    return v_userList

def GetUsersLoginByGroupCode(p_webSocketSession, p_groupCode):
    """Verify users that are part of a group given group code.

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_groupCode (int): the group code.

        Returns:
            dict of user logins.
    """

    v_table = None
    v_userDict = {}

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_table = v_database.Query('''
            select use.user_name as use_st_login
            from users_groups usg
            inner join users use
                       on usg.use_in_code = use.user_id
            where usg.gro_in_code = {0}'''.format(p_groupCode)
        )

        v_database.Close()
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'GetUsersLoginByGroupCode', traceback.format_exc())
        return None

    for v_row in v_table.Rows:
        v_userDict[v_row['use_st_login']] = v_row['use_st_login']

    return v_userDict

def GetUsersToSendMessageByChannelCode(p_webSocketSession, p_channelCode):
    """Verify users that must receive a message based on a given channel code.

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_channelCode (int): the channel code.

        Returns:
            list of user codes, where each item is a 'int' instance.
    """

    v_table = None
    v_userList = []

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_table = v_database.Query('''
            select usc.use_in_code
            from users_channels usc
            where usc.cha_in_code = {0}'''.format(p_channelCode)
        )

        v_database.Close()
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'GetUsersToSendMessageByChannelCode', traceback.format_exc())
        return None

    for v_row in v_table.Rows:
        v_userList.append(v_row['use_in_code'])

    return v_userList

def GetUsersLoginByChannelCode(p_webSocketSession, p_channelCode):
    """Verify users that are part of a channel given channel code.

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_channelCode (int): the channel code.

        Returns:
            dict of user logins.
    """

    v_table = None
    v_userDict = {}

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_table = v_database.Query('''
            select use.user_name as use_st_login
            from users_channels usc
            inner join users use
                       on usc.use_in_code = use.user_id
            where usc.cha_in_code = {0}'''.format(p_channelCode)
        )

        v_database.Close()
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'GetUsersLoginByChannelCode', traceback.format_exc())
        return None

    for v_row in v_table.Rows:
        v_userDict[v_row['use_st_login']] = v_row['use_st_login']

    return v_userDict

def GetChannelInfo(p_webSocketSession, p_channelCode, p_userCode):
    """Get channel info based on a given channel and user code.

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_channelCode (int): the channel code.
            p_userCode (int): the user code.

        Returns:
            a classes.Channel instance or None.
    """

    v_channel = None

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_table = v_database.Query('''
            select cha.cha_in_code,
                   cha.cha_st_name,
                   cha.cha_bo_private,
                   usc.usc_bo_silenced
            from channels cha
            inner join users_channels usc
                       on cha.cha_in_code = usc.cha_in_code
            where usc.use_in_code = {0}
              and cha.cha_in_code = {1}'''.format(
                p_userCode,
                p_channelCode
            )
        )

        if len(v_table.Rows) == 1:
            v_row = v_table.Rows[0]

            v_channel = classes.Channel(v_row['cha_in_code'], v_row['cha_st_name'], (True if v_row['usc_bo_silenced'] else False), [], [], (True if v_row['cha_bo_private'] else False))

            v_table2 = v_database.Query('''
                select use.user_id as use_in_code,
                       use.user_name as use_st_login
                from users_channels usc
                inner join users use
                           on usc.use_in_code = use.user_id
                where usc.cha_in_code = {0}'''.format(v_channel.code)
            )

            for v_row2 in v_table2.Rows:
                v_user = classes.User(v_row2['use_in_code'], v_row2['use_st_login'], v_row2['use_st_login'], None)
                v_channel.userList.append(v_user)

            v_table2 = v_database.Query('''
                select x.*
                from (
                    select y.*
                    from (
                        select mes.mes_in_code,
                               mes.mes_dt_creation,
                               mes.mes_dt_update,
                               use.user_id as use_in_code,
                               use.user_name as use_st_login,
                               mes.met_in_code,
                               coalesce(mes.mes_st_content, '') as mes_st_content,
                               coalesce(mes.mes_st_title, '') as mes_st_title,
                               coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                               mec.mec_bo_viewed,
                               coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                               coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                        from messages_channels mec
                        inner join messages mes
                                   on mec.mes_in_code = mes.mes_in_code
                        inner join users use
                                   on mes.use_in_code = use.user_id
                        where mec.cha_in_code = {0}
                          and mec.use_in_code = {1}
                        order by mes.mes_dt_creation desc
                        limit 40
                    ) y

                    union

                    select y.*
                    from (
                        select mes.mes_in_code,
                               mes.mes_dt_creation,
                               mes.mes_dt_update,
                               use.user_id as use_in_code,
                               use.user_name as use_st_login,
                               mes.met_in_code,
                               coalesce(mes.mes_st_content, '') as mes_st_content,
                               coalesce(mes.mes_st_title, '') as mes_st_title,
                               coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                               mec.mec_bo_viewed,
                               coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                               coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                        from messages_channels mec
                        inner join messages mes
                                   on mec.mes_in_code = mes.mes_in_code
                        inner join users use
                                   on mes.use_in_code = use.user_id
                        where mec.cha_in_code = {0}
                          and mec.use_in_code = {1}
                          and mes.mes_dt_creation >= (select min(m.mes_dt_creation)
                                                     from messages_channels mc
                                                     inner join messages m
                                                                on mc.mes_in_code = m.mes_in_code
                                                     where mc.cha_in_code = {0}
                                                       and mc.use_in_code = {1}
                                                       and mc.mec_bo_viewed = 0
                                                    )
                        order by mes.mes_dt_creation desc
                    ) y
                ) x
                order by x.mes_dt_creation desc'''.format(
                    v_channel.code,
                    p_userCode
                )
            )

            for v_row2 in v_table2.Rows:
                v_user = classes.User(v_row2['use_in_code'], '', v_row2['use_st_login'], None)
                v_message = classes.Message(
                    int(v_row2['mes_in_code']),
                    v_row2['mes_dt_creation'],
                    v_row2['mes_dt_update'],
                    v_user,
                    int(v_row2['met_in_code']),
                    v_row2['mes_st_content'],
                    v_row2['mes_st_title'],
                    v_row2['mes_st_attachmentname'],
                    (True if v_row2['mec_bo_viewed'] else False),
                    v_row2['mes_st_snippetmode'],
                    v_row2['mes_st_originalcontent']
                )
                v_channel.messageList.append(v_message)

        v_database.Close()
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'GetChannelInfo', traceback.format_exc())
        return None

    return v_channel

def LogException(p_webSocketSession, p_class, p_title, p_method, p_error):
    """Generate a exception log.

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_class (str): python class where the exception has occurred.
            p_title (str): title to be displayed in the log.
            p_method (str): method where the exception has occurred.
            p_error (str): the error message to be displayed in the log.
    """

    logger.error('''*** Exception in {0}.{1} - {2}:\n{3}\n'''.format(p_class, p_method, p_title, p_error))

def Login(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles login message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    if 'user_id' not in p_webSocketSession.cookies:
        try:
            v_database = p_webSocketSession.session.v_omnidb_database.v_connection
            v_database.Open()

            v_userId = p_webSocketSession.session.v_user_id
            p_webSocketSession.cookies['user_id'] = v_userId

            v_userName = v_database.ExecuteScalar('''
                select use.user_name
                from users use
                where use.user_id = {0};'''.format(v_userId)
            )

            p_webSocketSession.cookies['user_name'] = v_userName

            v_database.Close()
        except Spartacus.Database.Exception as exc:
            LogException(p_webSocketSession, '', 'Database Exception', 'Login', traceback.format_exc())
            p_responseMessage['v_error'] = True
            p_responseMessage['v_data'] = 'Error while executing the static method "Login".'
            SendToClient(p_webSocketSession, p_responseMessage, True)
            return

    v_responseMessage = {
        'v_code': response.UserStatus.value,
        'v_context_code': None,
        'v_error': False,
        'v_data': {
            'userCode': int(p_webSocketSession.cookies['user_id'].value),
            'userStatus': 'online'
        }
    }

    SendToAllClients(v_responseMessage)

    v_data = {
        'groupList': [],
        'channelList': [],
        'onlineUserCodeList': [],
        'userList': []
    }

    try:
        v_chatSessionsLock.acquire()

        for v_webSocketSession in v_chatSessions:
            if 'user_id' in v_webSocketSession.cookies and int(v_webSocketSession.cookies['user_id'].value) not in v_data['onlineUserCodeList']:
                v_data['onlineUserCodeList'].append(int(v_webSocketSession.cookies['user_id'].value))
    finally:
        v_chatSessionsLock.release()

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        #Get user group list
        v_table = v_database.Query('''
            select gro.gro_in_code,
                   usg.usg_bo_silenced
            from groups gro
            inner join users_groups usg
                       on gro.gro_in_code = usg.gro_in_code
            where usg.use_in_code = {0}'''.format(int(p_webSocketSession.cookies['user_id'].value))
        )

        for v_row in v_table.Rows:
            v_group = classes.Group(v_row['gro_in_code'], (True if v_row['usg_bo_silenced'] else False), [], [])

            v_table2 = v_database.Query('''
                select use.user_id as use_in_code,
                       use.user_name as use_st_login
                from users_groups usg
                inner join users use
                           on usg.use_in_code = use.user_id
                where usg.gro_in_code = {0}'''.format(v_group.code)
            )

            for v_row2 in v_table2.Rows:
                v_user = classes.User(v_row2['use_in_code'], v_row2['use_st_login'], v_row2['use_st_login'], None)
                v_group.userList.append(v_user)

            v_table2 = v_database.Query('''
                select x.*
                from (
                    select y.*
                    from (
                        select mes.mes_in_code,
                               mes.mes_dt_creation,
                               mes.mes_dt_update,
                               use.user_id as use_in_code,
                               use.user_name as use_st_login,
                               mes.met_in_code,
                               coalesce(mes.mes_st_content, '') as mes_st_content,
                               coalesce(mes.mes_st_title, '') as mes_st_title,
                               coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                               meg.meg_bo_viewed,
                               coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                               coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                        from messages_groups meg
                        inner join messages mes
                                   on meg.mes_in_code = mes.mes_in_code
                        inner join users use
                                   on mes.use_in_code = use.user_id
                        where meg.gro_in_code = {0}
                          and meg.use_in_code = {1}
                        order by mes.mes_dt_creation desc
                        limit 40
                    ) y

                    union

                    select y.*
                    from (
                        select mes.mes_in_code,
                               mes.mes_dt_creation,
                               mes.mes_dt_update,
                               use.user_id as use_in_code,
                               use.user_name as use_st_login,
                               mes.met_in_code,
                               coalesce(mes.mes_st_content, '') as mes_st_content,
                               coalesce(mes.mes_st_title, '') as mes_st_title,
                               coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                               meg.meg_bo_viewed,
                               coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                               coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                        from messages_groups meg
                        inner join messages mes
                                   on meg.mes_in_code = mes.mes_in_code
                        inner join users use
                                   on mes.use_in_code = use.user_id
                        where meg.gro_in_code = {0}
                          and meg.use_in_code = {1}
                          and mes.mes_dt_creation >= (select min(m.mes_dt_creation)
                                                     from messages_groups mg
                                                     inner join messages m
                                                                on mg.mes_in_code = m.mes_in_code
                                                     where mg.gro_in_code = {0}
                                                       and mg.use_in_code = {1}
                                                       and mg.meg_bo_viewed = 0
                                                    )
                        order by mes.mes_dt_creation desc
                    ) y
                ) x
                order by x.mes_dt_creation desc'''.format(
                    v_group.code,
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            for v_row2 in v_table2.Rows:
                v_user = classes.User(v_row2['use_in_code'], '', v_row2['use_st_login'], None)
                v_message = classes.Message(
                    int(v_row2['mes_in_code']),
                    v_row2['mes_dt_creation'],
                    v_row2['mes_dt_update'],
                    v_user,
                    int(v_row2['met_in_code']),
                    v_row2['mes_st_content'],
                    v_row2['mes_st_title'],
                    v_row2['mes_st_attachmentname'],
                    (True if v_row2['meg_bo_viewed'] else False),
                    v_row2['mes_st_snippetmode'],
                    v_row2['mes_st_originalcontent']
                )
                v_group.messageList.append(v_message)

            v_data['groupList'].append(v_group)

        #Get user channel list
        v_table = v_database.Query('''
            select cha.cha_in_code,
                   cha.cha_st_name,
                   cha.cha_bo_private,
                   usc.usc_bo_silenced
            from channels cha
            inner join users_channels usc
                       on cha.cha_in_code = usc.cha_in_code
            where usc.use_in_code = {0}'''.format(int(p_webSocketSession.cookies['user_id'].value))
        )

        for v_row in v_table.Rows:
            v_channel = classes.Channel(v_row['cha_in_code'], v_row['cha_st_name'], (True if v_row['usc_bo_silenced'] else False), [], [], (True if v_row['cha_bo_private'] else False))

            v_table2 = v_database.Query('''
                select use.user_id as use_in_code,
                       use.user_name as use_st_login
                from users_channels usc
                inner join users use
                           on usc.use_in_code = use.user_id
                where usc.cha_in_code = {0}'''.format(v_channel.code)
            )

            for v_row2 in v_table2.Rows:
                v_user = classes.User(v_row2['use_in_code'], v_row2['use_st_login'], v_row2['use_st_login'], None)
                v_channel.userList.append(v_user)

            v_table2 = v_database.Query('''
                select x.*
                from (
                    select y.*
                    from (
                        select mes.mes_in_code,
                               mes.mes_dt_creation,
                               mes.mes_dt_update,
                               use.user_id as use_in_code,
                               use.user_name as use_st_login,
                               mes.met_in_code,
                               coalesce(mes.mes_st_content, '') as mes_st_content,
                               coalesce(mes.mes_st_title, '') as mes_st_title,
                               coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                               mec.mec_bo_viewed,
                               coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                               coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                        from messages_channels mec
                        inner join messages mes
                                   on mec.mes_in_code = mes.mes_in_code
                        inner join users use
                                   on mes.use_in_code = use.user_id
                        where mec.cha_in_code = {0}
                          and mec.use_in_code = {1}
                        order by mes.mes_dt_creation desc
                        limit 40
                    ) y

                    union

                    select y.*
                    from (
                        select mes.mes_in_code,
                               mes.mes_dt_creation,
                               mes.mes_dt_update,
                               use.user_id as use_in_code,
                               use.user_name as use_st_login,
                               mes.met_in_code,
                               coalesce(mes.mes_st_content, '') as mes_st_content,
                               coalesce(mes.mes_st_title, '') as mes_st_title,
                               coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                               mec.mec_bo_viewed,
                               coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                               coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                        from messages_channels mec
                        inner join messages mes
                                   on mec.mes_in_code = mes.mes_in_code
                        inner join users use
                                   on mes.use_in_code = use.user_id
                        where mec.cha_in_code = {0}
                          and mec.use_in_code = {1}
                          and mes.mes_dt_creation >= (select min(m.mes_dt_creation)
                                                     from messages_channels mc
                                                     inner join messages m
                                                                on mc.mes_in_code = m.mes_in_code
                                                     where mc.cha_in_code = {0}
                                                       and mc.use_in_code = {1}
                                                       and mc.mec_bo_viewed = 0
                                                    )
                        order by mes.mes_dt_creation desc
                    ) y
                ) x
                order by x.mes_dt_creation desc'''.format(
                    v_channel.code,
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            for v_row2 in v_table2.Rows:
                v_user = classes.User(v_row2['use_in_code'], '', v_row2['use_st_login'], None)
                v_message = classes.Message(
                    int(v_row2['mes_in_code']),
                    v_row2['mes_dt_creation'],
                    v_row2['mes_dt_update'],
                    v_user,
                    int(v_row2['met_in_code']),
                    v_row2['mes_st_content'],
                    v_row2['mes_st_title'],
                    v_row2['mes_st_attachmentname'],
                    (True if v_row2['mec_bo_viewed'] else False),
                    v_row2['mes_st_snippetmode'],
                    v_row2['mes_st_originalcontent']
                )
                v_channel.messageList.append(v_message)

            v_data['channelList'].append(v_channel)

        v_table = v_database.Query('''
            select use.user_id as use_in_code,
                   use.user_name as use_st_login,
                   coalesce(stc.stc_in_code, 1) as stc_in_code,
                   stc.stc_st_name
            from users use
            inner join status_chat stc
                       on coalesce(use.stc_in_code, 1) = stc.stc_in_code
            where coalesce(use.use_bo_bot, 0) = 0
              and use.user_id in (select distinct usg.use_in_code
                                        from users_groups usg
                                        where usg.gro_in_code in (select distinct ug.gro_in_code
                                                                    from users_groups ug
                                                                    where ug.use_in_code = {0}
                                                                   )

                                        union

                                        select {0} as use_in_code
                                       )
            order by use.user_name'''.format(
                int(p_webSocketSession.cookies['user_id'].value)
            )
        )

        for v_row in v_table.Rows:
            v_status = classes.Status(v_row['stc_in_code'], v_row['stc_st_name'])
            v_user = classes.User(v_row['use_in_code'], v_row['use_st_login'], v_row['use_st_login'], v_status)
            v_data['userList'].append(v_user)

        v_database.Close()
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'Login', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "Login".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

    p_responseMessage['v_code'] = response.LoginResult.value
    p_responseMessage['v_data'] = v_data
    SendToClient(p_webSocketSession, p_responseMessage, False)

def SendGroupMessage(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles send group message message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    v_messageCode = 0

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        if p_requestMessage['v_data']['messageType'] == 0: #Forward message
            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                )
                select {0} as mes_in_code,
                        datetime('now') as mes_dt_creation,
                        datetime('now') as mes_dt_update,
                        {1} as use_in_code,
                        mes.met_in_code as met_in_code,
                        mes.mes_st_content as mes_st_content,
                        mes.mes_st_title as mes_st_title,
                        mes.mes_st_attachmentname as mes_st_attachmentname,
                        mes.mes_st_attachmentpath as mes_st_attachmentpath,
                        mes.mes_st_snippetmode as mes_st_snippetmode,
                        mes.mes_st_originalcontent as mes_st_originalcontent
                 from messages mes
                 where mes.mes_in_code = {2}
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['forwardMessageCode']
                )
            )

            v_database.Execute('''
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                )
                select {0} as mes_in_code,
                        usg.gro_in_code as gro_in_code,
                        usg.use_in_code,
                        0 as meg_bo_viewed
                 from users_groups usg
                 where usg.gro_in_code = {2}
                   and usg.use_in_code <> {1}
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                ) values (
                    {0},
                    {2},
                    {1},
                    1
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            v_messageType = int(v_database.ExecuteScalar('''
                select mes.met_in_code
                from messages mes
                where mes.mes_in_code = {0}
                '''.format(
                    p_requestMessage['v_data']['forwardMessageCode']
                )
            ))

            if v_messageType == 2 or v_messageType == 4: #Pasted image or attachment
                try:
                    shutil.copyfile(
                        os.path.join(settings.CHAT_FOLDER, str(p_requestMessage['v_data']['forwardMessageCode'])),
                        os.path.join(settings.CHAT_FOLDER, str(v_messageCode)),
                    )
                except Exception as exc:
                    v_database.Execute('''
                        delete
                        from messages
                        where mes_in_code = {0}
                        '''.format(v_messageCode)
                    )

                    v_database.Execute('''
                        delete from messages_groups
                        where mes_in_code = {0}
                          and gro_in_code = {1}
                        '''.format(
                            v_messageCode,
                            p_requestMessage['v_data']['groupCode']
                        )
                    )

                    raise Exception() from exc
        elif p_requestMessage['v_data']['messageType'] == 1: #Plain Text
            v_content = p_requestMessage['v_data']['messageContent']

            #Format blockquote element
            if v_content[0:4] == '&gt;':
                v_content = '<blockquote>{0}</blockquote>'.format(v_content[4:])

            #Format pre elements
            v_match = re.search(r'```((.|\s)*?)```', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<pre>' + v_content[v_start + 3: v_end - 3] + '</pre>' + v_content[v_end:]
                v_match = re.search(r'```((.|\s)*?)```', v_content)

            #Format kbd elements
            v_match = re.search(r'``(.*?)``', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<kbd>' + v_content[v_start + 2: v_end - 2] + '</kbd>' + v_content[v_end:]
                v_match = re.search(r'``(.*?)``', v_content)

            #Format code elements
            v_match = re.search(r'`(.*?)`', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<code>' + v_content[v_start + 1: v_end - 1] + '</code>' + v_content[v_end:]
                v_match = re.search(r'`(.*?)`', v_content)

            #Format bold elements
            v_match = re.search(r'\*(.*?)\*', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<b>' + v_content[v_start + 1: v_end - 1] + '</b>' + v_content[v_end:]
                v_match = re.search(r'\*(.*?)\*', v_content)

            #Format italic elements
            v_match = re.search(r'\b_(.*?)_\b', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<i>' + v_content[v_start + 1: v_end - 1] + '</i>' + v_content[v_end:]
                v_match = re.search(r'\b_(.*?)_\b', v_content)

            #Format strike elements
            v_match = re.search(r'~(.*?)~', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<strike>' + v_content[v_start + 1: v_end - 1] + '</strike>' + v_content[v_end:]
                v_match = re.search(r'~(.*?)~', v_content)

            #Format anchor elements
            #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
            v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()

                v_prefix = ''

                if v_start > 0:
                    v_prefix = v_content[:v_start]

                v_content = v_prefix + '<a href="' + v_content[v_start:v_end] + '">' + v_content[v_start:v_end].replace('https://', '').replace('http://', '') + '</a>' + v_content[v_end:]

                #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
                v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

            #Format user notification
            v_userDict = GetUsersLoginByGroupCode(p_webSocketSession, int(p_requestMessage['v_data']['groupCode']))

            if v_userDict is not None:
                v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

                while v_match is not None:
                    v_start = v_match.start()
                    v_end = v_match.end()

                    v_prefix = ''

                    if v_start > 0:
                        v_prefix = v_content[:v_start]

                    if v_content[v_start + 1 : v_end] in v_userDict:
                        v_content = v_prefix + '<span class="span_notify_user">' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]
                    else:
                        v_content = v_prefix + '<span>' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]

                    v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

            v_content = re.sub("'", "''", v_content)

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes
                '''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    1, --Plain Text
                    '{2}',
                    null,
                    null,
                    null,
                    null,
                    '{3}'
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_content,
                    re.sub("'", "''", p_requestMessage['v_data']['messageRawContent'])
                )
            )

            v_database.Execute('''
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                )
                select {0} as mes_in_code,
                        usg.gro_in_code as gro_in_code,
                        usg.use_in_code,
                        0 as meg_bo_viewed
                 from users_groups usg
                 where usg.gro_in_code = {2}
                   and usg.use_in_code <> {1}
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                ) values (
                    {0},
                    {2},
                    {1},
                    1
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )
        elif p_requestMessage['v_data']['messageType'] == 2: #Pasted Image
            v_title = re.sub("'", "''", p_requestMessage['v_data']['messageTitle'])
            v_attachmentName = re.sub("'", "''", p_requestMessage['v_data']['messageAttachmentName'])
            v_attachmentPath = '{0}/{1}'.format(settings.CHAT_FOLDER, v_messageCode)
            v_attachmentPath = re.sub("'", "''", v_attachmentPath)

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    2, --Pasted Image
                    null,
                    '{3}',
                    '{2}',
                    '{4}',
                    null,
                    null
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_title,
                    v_attachmentName,
                    v_attachmentPath
                )
            )

            v_database.Execute('''
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                )
                select {0} as mes_in_code,
                        usg.gro_in_code as gro_in_code,
                        usg.use_in_code,
                        0 as meg_bo_viewed
                 from users_groups usg
                 where usg.gro_in_code = {2}
                   and usg.use_in_code <> {1}
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                ) values (
                    {0},
                    {2},
                    {1},
                    1
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            try:
                v_file = open('{0}/{1}'.format(settings.CHAT_FOLDER, v_messageCode), 'wb')
                v_file.write(base64.b64decode(p_requestMessage['v_data']['messageContent']))
                v_file.close()
            except Exception as exc:
                v_database.Execute('''
                    delete
                    from messages
                    where mes_in_code = {0}
                    '''.format(v_messageCode)
                )

                v_database.Execute('''
                    delete from messages_groups
                    where mes_in_code = {0}
                      and gro_in_code = {1}
                    '''.format(
                        v_messageCode,
                        p_requestMessage['v_data']['groupCode']
                    )
                )

                raise Exception() from exc
        elif p_requestMessage['v_data']['messageType'] == 3: #Snippet
            v_title = re.sub("'", "''", p_requestMessage['v_data']['messageTitle'])
            v_content = re.sub("'", "''", p_requestMessage['v_data']['messageContent'])
            v_snippetMode = re.sub("'", "''", p_requestMessage['v_data']['messageSnippetMode'])

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    3, --Snippet
                    '{3}',
                    '{2}',
                    null,
                    null,
                    '{4}',
                    null
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_title,
                    v_content,
                    v_snippetMode
                )
            )

            v_database.Execute('''
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                )
                select {0} as mes_in_code,
                        usg.gro_in_code as gro_in_code,
                        usg.use_in_code,
                        0 as meg_bo_viewed
                 from users_groups usg
                 where usg.gro_in_code = {2}
                   and usg.use_in_code <> {1}
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                ) values (
                    {0},
                    {2},
                    {1},
                    1
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )
        elif p_requestMessage['v_data']['messageType'] == 4: #Attachment
            v_title = re.sub("'", "''", p_requestMessage['v_data']['messageTitle'])
            v_attachmentName = re.sub("'", "''", p_requestMessage['v_data']['messageAttachmentName'])
            v_attachmentPath = '{0}/{1}'.format(settings.CHAT_FOLDER, v_messageCode)
            v_attachmentPath = re.sub("'", "''", v_attachmentPath)

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                 insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    4, --Attachment
                    null,
                    '{2}',
                    '{3}',
                    '{4}',
                    null,
                    null
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_title,
                    v_attachmentName,
                    v_attachmentPath
                )
            )

            v_database.Execute('''
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                )
                select {0} as mes_in_code,
                        usg.gro_in_code as gro_in_code,
                        usg.use_in_code,
                        0 as meg_bo_viewed
                 from users_groups usg
                 where usg.gro_in_code = {2}
                   and usg.use_in_code <> {1}
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                ) values (
                    {0},
                    {2},
                    {1},
                    1
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            try:
                v_file = open('{0}/{1}'.format(settings.CHAT_FOLDER, v_messageCode), 'wb')
                v_file.write(base64.b64decode(p_requestMessage['v_data']['messageContent']))
                v_file.close()
            except Exception as exc:
                v_database.Execute('''
                    delete
                    from messages
                    where mes_in_code = {0}
                    '''.format(v_messageCode)
                )

                v_database.Execute('''
                    delete from messages_groups
                    where mes_in_code = {0}
                      and gro_in_code = {1}
                    '''.format(
                        v_messageCode,
                        p_requestMessage['v_data']['groupCode']
                    )
                )

                raise Exception() from exc

        elif p_requestMessage['v_data']['messageType'] == 5: #Mention
            v_content = p_requestMessage['v_data']['commentMessageContent']

            #Format blockquote element
            if v_content[0:4] == '&gt;':
                v_content = '<blockquote>{0}</blockquote>'.format(v_content[4:])

            #Format pre elements
            v_match = re.search(r'```((.|\s)*?)```', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<pre>' + v_content[v_start + 3: v_end - 3] + '</pre>' + v_content[v_end:]
                v_match = re.search(r'```((.|\s)*?)```', v_content)

            #Format kbd elements
            v_match = re.search(r'``(.*?)``', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<kbd>' + v_content[v_start + 2: v_end - 2] + '</kbd>' + v_content[v_end:]
                v_match = re.search(r'``(.*?)``', v_content)

            #Format code elements
            v_match = re.search(r'`(.*?)`', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<code>' + v_content[v_start + 1: v_end - 1] + '</code>' + v_content[v_end:]
                v_match = re.search(r'`(.*?)`', v_content)

            #Format bold elements
            v_match = re.search(r'\*(.*?)\*', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<b>' + v_content[v_start + 1: v_end - 1] + '</b>' + v_content[v_end:]
                v_match = re.search(r'\*(.*?)\*', v_content)

            #Format italic elements
            v_match = re.search(r'\b_(.*?)_\b', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<i>' + v_content[v_start + 1: v_end - 1] + '</i>' + v_content[v_end:]
                v_match = re.search(r'\b_(.*?)_\b', v_content)

            #Format strike elements
            v_match = re.search(r'~(.*?)~', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<strike>' + v_content[v_start + 1: v_end - 1] + '</strike>' + v_content[v_end:]
                v_match = re.search(r'~(.*?)~', v_content)

            #Format anchor elements
            #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
            v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()

                v_prefix = ''

                if v_start > 0:
                    v_prefix = v_content[:v_start]

                v_content = v_prefix + '<a href="' + v_content[v_start:v_end] + '">' + v_content[v_start:v_end].replace('https://', '').replace('http://', '') + '</a>' + v_content[v_end:]

                #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
                v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

            #Format user notification
            v_userDict = GetUsersLoginByGroupCode(p_webSocketSession, int(p_requestMessage['v_data']['groupCode']))

            if v_userDict is not None:
                v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

                while v_match is not None:
                    v_start = v_match.start()
                    v_end = v_match.end()

                    v_prefix = ''

                    if v_start > 0:
                        v_prefix = v_content[:v_start]

                    if v_content[v_start + 1 : v_end] in v_userDict:
                        v_content = v_prefix + '<span class="span_notify_user">' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]
                    else:
                        v_content = v_prefix + '<span>' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]

                    v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

            v_content += '<blockquote>' + p_requestMessage['v_data']['mentionedMessageContent'] + '</blockquote>'
            v_originalContent = p_requestMessage['v_data']['commentMessageRawContent'] + '#start_mentioned_message#' + p_requestMessage['v_data']['mentionedMessageContent'] + '#end_mentioned_message#'

            v_content = re.sub("'", "''", v_content)
            v_originalContent = v_originalContent.replace("'", "''")

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    5, --Mention
                    '{2}',
                    null,
                    null,
                    null,
                    null,
                    '{3}'
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_content,
                    v_originalContent
                )
            )

            v_database.Execute('''
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                )
                select {0} as mes_in_code,
                        usg.gro_in_code as gro_in_code,
                        usg.use_in_code,
                        0 as meg_bo_viewed
                 from users_groups usg
                 where usg.gro_in_code = {2}
                   and usg.use_in_code <> {1}
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                ) values (
                    {0},
                    {2},
                    {1},
                    1
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['groupCode']
                )
            )

        v_database.Close()

        if v_messageCode != 0:
            v_database.Open()

            v_table = v_database.Query('''
                select mes.mes_in_code,
                       mes.mes_dt_creation,
                       mes.mes_dt_update,
                       use.user_id as use_in_code,
                       use.user_name as use_st_login,
                       mes.met_in_code,
                       coalesce(mes.mes_st_content, '') as mes_st_content,
                       coalesce(mes.mes_st_title, '') as mes_st_title,
                       coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                       coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                       coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                from messages mes
                inner join users use
                           on mes.use_in_code = use.user_id
                where mes.mes_in_code = {0}'''.format(v_messageCode)
            )

            v_database.Close()

            if len(v_table.Rows) > 0:
                v_user = classes.User(v_table.Rows[0]['use_in_code'], '', v_table.Rows[0]['use_st_login'], None)
                v_message = classes.Message(
                    int(v_table.Rows[0]['mes_in_code']),
                    v_table.Rows[0]['mes_dt_creation'],
                    v_table.Rows[0]['mes_dt_update'],
                    v_user,
                    int(v_table.Rows[0]['met_in_code']),
                    v_table.Rows[0]['mes_st_content'],
                    v_table.Rows[0]['mes_st_title'],
                    v_table.Rows[0]['mes_st_attachmentname'],
                    False,
                    v_table.Rows[0]['mes_st_snippetmode'],
                    v_table.Rows[0]['mes_st_originalcontent']
                )

                v_data = {
                    'groupCode': p_requestMessage['v_data']['groupCode'],
                    'message': v_message
                }

                v_userList = GetUsersToSendMessageByGroupCode(p_webSocketSession, p_requestMessage['v_data']['groupCode'])

                if v_userList is not None:
                    if int(p_webSocketSession.cookies['user_id'].value) in v_userList:
                        v_userList.remove(int(p_webSocketSession.cookies['user_id'].value))

                    p_responseMessage['v_data'] = v_data
                    p_responseMessage['v_code'] = response.NewGroupMessage.value
                    SendToSomeClients(v_userList, p_responseMessage)

                v_data['message'].viewed = True
                SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'SendGroupMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SendGroupMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        LogException(p_webSocketSession, '', 'Exceção de Sistema', 'SendGroupMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SendGroupMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def RetrieveGroupHistory(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles retrieve group history message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_data = {
            'groupCode': int(p_requestMessage['v_data']['groupCode']),
            'messageList': [],
            'fromMessageCode': p_requestMessage['v_data']['fromMessageCode']
        }

        v_table = None

        if p_requestMessage['v_data']['fromMessageCode'] is None:
            v_table = v_database.Query('''
                select mes.mes_in_code,
                       mes.mes_dt_creation,
                       mes.mes_dt_update,
                       use.user_id as use_in_code,
                       use.user_name as use_st_login,
                       mes.met_in_code,
                       coalesce(mes.mes_st_content, '') as mes_st_content,
                       coalesce(mes.mes_st_title, '') as mes_st_title,
                       coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                       meg.meg_bo_viewed,
                       coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                       coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                from messages_groups meg
                inner join messages mes
                           on meg.mes_in_code = mes.mes_in_code
                inner join users use
                           on mes.use_in_code = use.user_id
                where meg.gro_in_code = {0}
                  and meg.use_in_code = {1}
                order by mes.mes_dt_creation desc
                limit 20
                offset {2}'''.format(
                    p_requestMessage['v_data']['groupCode'],
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['offset']
                )
            )
        else:
            v_table = v_database.Query('''
                select mes.mes_in_code,
                       mes.mes_dt_creation,
                       mes.mes_dt_update,
                       use.user_id as use_in_code,
                       use.user_name as use_st_login,
                       mes.met_in_code,
                       coalesce(mes.mes_st_content, '') as mes_st_content,
                       coalesce(mes.mes_st_title, '') as mes_st_title,
                       coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                       meg.meg_bo_viewed,
                       coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                       coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                from messages_groups meg
                inner join messages mes
                           on meg.mes_in_code = mes.mes_in_code
                inner join users use
                           on mes.use_in_code = use.user_id
                where meg.gro_in_code = {0}
                  and meg.use_in_code = {1}
                  and mes.mes_dt_creation >= (select m.mes_dt_creation
                                              from messages m
                                              where m.mes_in_code = {3})
                order by mes.mes_dt_creation desc
                offset {2}'''.format(
                    p_requestMessage['v_data']['groupCode'],
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['offset'],
                    p_requestMessage['v_data']['fromMessageCode']
                )
            )

        v_database.Close()

        if v_table is not None:
            for v_row in v_table.Rows:
                v_user = classes.User(v_row['use_in_code'], '', v_row['use_st_login'], None)
                v_message = classes.Message(
                    int(v_row['mes_in_code']),
                    v_row['mes_dt_creation'],
                    v_row['mes_dt_update'],
                    v_user,
                    int(v_row['met_in_code']),
                    v_row['mes_st_content'],
                    v_row['mes_st_title'],
                    v_row['mes_st_attachmentname'],
                    (True if v_row['meg_bo_viewed'] else False),
                    v_row['mes_st_snippetmode'],
                    v_row['mes_st_originalcontent']
                )
                v_data['messageList'].append(v_message)

        p_responseMessage['v_data'] = v_data
        p_responseMessage['v_code'] = response.RetrievedGroupHistory.value
        SendToClient(p_webSocketSession, p_responseMessage, False)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'RetrieveGroupHistory', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "RetrieveGroupHistory".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        LogException(p_webSocketSession, '', 'Exceção de Sistema', 'RetrieveGroupHistory', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "RetrieveGroupHistory".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def MarkGroupMessagesAsRead(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles mark group messages as read message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        for i in range(0, len(p_requestMessage['v_data']['messageCodeList'])):
            v_database.Execute('''
                update messages_groups
                set meg_bo_viewed = 1
                where gro_in_code = {0}
                  and use_in_code = {1}
                  and mes_in_code = {2}
                '''.format(
                    p_requestMessage['v_data']['groupCode'],
                    p_webSocketSession.cookies['user_id'].value,
                    p_requestMessage['v_data']['messageCodeList'][i]
                )
            )

        v_database.Close()

        p_responseMessage['v_data'] = p_requestMessage['v_data']
        p_responseMessage['v_code'] = response.MarkedGroupMessagesAsRead.value
        SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'MarkGroupMessagesAsRead', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "MarkGroupMessagesAsRead".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        LogException(p_webSocketSession, '', 'Exceção de Sistema', 'MarkGroupMessagesAsRead', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "MarkGroupMessagesAsRead".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def GetUserStatus(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles get user status message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    v_data = {
        'userCode': p_requestMessage['v_data']['userCode'],
        'userStatus': 'offline'
    }

    try:
        v_chatSessionsLock.acquire()

        for v_webSocketSession in v_chatSessions:
            if int(v_webSocketSession.cookies['user_id'].value) == p_requestMessage['v_data']['userCode']:
                v_data['userStatus'] = 'online'
                break
    finally:
        v_chatSessionsLock.release()

    p_responseMessage['v_data'] = v_data
    p_responseMessage['v_code'] = response.UserStatus.value
    SendToClient(p_webSocketSession, p_responseMessage, True)

def SetGroupUserWriting(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles set group user writing message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    v_userList = GetUsersToSendMessageByGroupCode(p_webSocketSession, p_requestMessage['v_data']['groupCode'])

    if v_userList is not None:
        if int(p_webSocketSession.cookies['user_id'].value) in v_userList:
            v_userList.remove(int(p_webSocketSession.cookies['user_id'].value))

        p_responseMessage['v_data'] = p_requestMessage['v_data']
        p_responseMessage['v_code'] = response.GroupUserWriting.value
        SendToSomeClients(v_userList, p_responseMessage)

def ChangeGroupSilenceSettings(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles change group silence settings message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_database.Execute('''
            update users_groups
            set usg_bo_silenced = {2}
            where gro_in_code = {0}
              and use_in_code = {1}
            '''.format(
                p_requestMessage['v_data']['groupCode'],
                p_webSocketSession.cookies['user_id'].value,
                ('1' if p_requestMessage['v_data']['silenceGroup'] else '0')
            )
        )

        v_database.Close()

        v_data = {
            'groupCode': p_requestMessage['v_data']['groupCode'],
            'groupSilenced': p_requestMessage['v_data']['silenceGroup']
        }

        p_responseMessage['v_data'] = v_data
        p_responseMessage['v_code'] = response.GroupSilenceSettings.value
        SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'ChangeGroupSilenceSettings', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "ChangeGroupSilenceSettings".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def RemoveGroupMessage(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles remove group message message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_database.Execute('''
            delete from messages_groups
            where gro_in_code = {0}
              and use_in_code = {1}
              and mes_in_code = {2}
            '''.format(
                p_requestMessage['v_data']['groupCode'],
                p_webSocketSession.cookies['user_id'].value,
                p_requestMessage['v_data']['messageCode']
            )
        )

        v_database.Close()

        p_responseMessage['v_data'] = p_requestMessage['v_data']
        p_responseMessage['v_code'] = response.RemovedGroupMessage.value
        SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'RemoveGroupMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "RemoveGroupMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def UpdateGroupSnippetMessage(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles update group snippet message message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_database.Execute('''
            update messages
            set mes_dt_update = datetime('now'),
                mes_st_title = '{2}',
                mes_st_snippetmode = '{3}',
                mes_st_content = '{4}'
            where mes_in_code = {0}
              and use_in_code = {1};
            '''.format(
                p_requestMessage['v_data']['messageCode'],
                p_webSocketSession.cookies['user_id'].value,
                p_requestMessage['v_data']['snippetTitle'].replace("'", "''"),
                p_requestMessage['v_data']['snippetMode'].replace("'", "''"),
                p_requestMessage['v_data']['snippetContent'].replace("'", "''")
            )
        )

        v_updatedAt = v_database.ExecuteScalar('''
            select mes.mes_dt_update
            from messages mes
            where mes.mes_in_code = {0}
            '''.format(
                p_requestMessage['v_data']['messageCode']
            )
        )

        v_database.Close()

        v_userList = GetUsersToSendMessageByGroupCode(p_webSocketSession, p_requestMessage['v_data']['groupCode'])

        if v_userList is not None:
            p_responseMessage['v_data'] = p_requestMessage['v_data']
            p_responseMessage['v_data']['updatedAt'] = v_updatedAt
            p_responseMessage['v_code'] = response.UpdatedGroupSnippetMessage.value
            SendToSomeClients(v_userList, p_responseMessage)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'UpdateGroupSnippetMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "UpdateGroupSnippetMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def UpdateGroupMessage(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles update group message message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_content = p_requestMessage['v_data']['messageContent']
        v_index = v_content.find('#start_mentioned_message#')

        if v_index != -1:
            v_content = v_content[:v_index]

        #Format blockquote element
        if v_content[0:4] == '&gt;':
            v_content = '<blockquote>{0}</blockquote>'.format(v_content[4:])

        #Format pre elements
        v_match = re.search(r'```((.|\s)*?)```', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<pre>' + v_content[v_start + 3: v_end - 3] + '</pre>' + v_content[v_end:]
            v_match = re.search(r'```((.|\s)*?)```', v_content)

        #Format kbd elements
        v_match = re.search(r'``(.*?)``', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<kbd>' + v_content[v_start + 2: v_end - 2] + '</kbd>' + v_content[v_end:]
            v_match = re.search(r'``(.*?)``', v_content)

        #Format code elements
        v_match = re.search(r'`(.*?)`', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<code>' + v_content[v_start + 1: v_end - 1] + '</code>' + v_content[v_end:]
            v_match = re.search(r'`(.*?)`', v_content)

        #Format bold elements
        v_match = re.search(r'\*(.*?)\*', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<b>' + v_content[v_start + 1: v_end - 1] + '</b>' + v_content[v_end:]
            v_match = re.search(r'\*(.*?)\*', v_content)

        #Format italic elements
        v_match = re.search(r'\b_(.*?)_\b', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<i>' + v_content[v_start + 1: v_end - 1] + '</i>' + v_content[v_end:]
            v_match = re.search(r'\b_(.*?)_\b', v_content)

        #Format strike elements
        v_match = re.search(r'~(.*?)~', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<strike>' + v_content[v_start + 1: v_end - 1] + '</strike>' + v_content[v_end:]
            v_match = re.search(r'~(.*?)~', v_content)

        #Format anchor elements
        #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
        v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()

            v_prefix = ''

            if v_start > 0:
                v_prefix = v_content[:v_start]

            v_content = v_prefix + '<a href="' + v_content[v_start:v_end] + '">' + v_content[v_start:v_end].replace('https://', '').replace('http://', '') + '</a>' + v_content[v_end:]

            #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
            v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

        #Format user notification
        v_userDict = GetUsersLoginByGroupCode(p_webSocketSession, int(p_requestMessage['v_data']['groupCode']))

        if v_userDict is not None:
            v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()

                v_prefix = ''

                if v_start > 0:
                    v_prefix = v_content[:v_start]

                if v_content[v_start + 1 : v_end] in v_userDict:
                    v_content = v_prefix + '<span class="span_notify_user">' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]
                else:
                    v_content = v_prefix + '<span>' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]

                v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

        if v_index != -1:
            v_content += p_requestMessage['v_data']['messageContent'][v_index:]
            v_content = v_content.replace('#start_mentioned_message#', '<blockquote>')
            v_content = v_content.replace('#end_mentioned_message#', '</blockquote>')

        v_database.ExecuteScalar('''
            update messages
            set mes_dt_update = datetime('now'),
                mes_st_content = '{2}',
                mes_st_originalcontent = '{3}'
            where mes_in_code = {0}
              and use_in_code = {1}
            '''.format(
                p_requestMessage['v_data']['messageCode'],
                p_webSocketSession.cookies['user_id'].value,
                v_content.replace("'", "''"),
                p_requestMessage['v_data']['messageRawContent'].replace("'", "''")
            )
        )

        v_updatedAt = v_database.ExecuteScalar('''
            select mes.mes_dt_update
            from messages mes
            where mes.mes_in_code = {0}
            '''.format(
                p_requestMessage['v_data']['messageCode']
            )
        )

        v_database.Close()

        v_data = {
            'groupCode': p_requestMessage['v_data']['groupCode'],
            'messageCode': p_requestMessage['v_data']['messageCode'],
            'messageContent': v_content,
            'messageRawContent': p_requestMessage['v_data']['messageRawContent'],
            'updatedAt': v_updatedAt
        }

        v_userList = GetUsersToSendMessageByGroupCode(p_webSocketSession, p_requestMessage['v_data']['groupCode'])

        if v_userList is not None:
            p_responseMessage['v_data'] = v_data
            p_responseMessage['v_code'] = response.UpdatedGroupMessage.value
            SendToSomeClients(v_userList, p_responseMessage)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'UpdateGroupMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "UpdateGroupMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def SendChannelMessage(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles send channel message message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    v_messageCode = 0

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        if p_requestMessage['v_data']['messageType'] == 0: #Forward message
            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                )
                select {0} as mes_in_code,
                        datetime('now') as mes_dt_creation,
                        datetime('now') as mes_dt_update,
                        {1} as use_in_code,
                        mes.met_in_code as met_in_code,
                        mes.mes_st_content as mes_st_content,
                        mes.mes_st_title as mes_st_title,
                        mes.mes_st_attachmentname as mes_st_attachmentname,
                        mes.mes_st_attachmentpath as mes_st_attachmentpath,
                        mes.mes_st_snippetmode as mes_st_snippetmode,
                        mes.mes_st_originalcontent as mes_st_originalcontent
                 from messages mes
                 where mes.mes_in_code = {2}
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['forwardMessageCode']
                )
            )

            v_database.Execute('''
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                )
                select {0} as mes_in_code,
                        usc.cha_in_code as cha_in_code,
                        usc.use_in_code,
                        0 as mec_bo_viewed
                 from users_channels usc
                 where usc.cha_in_code = {1}
                   and usc.use_in_code <> {2}
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                ) values (
                    {0},
                    {1},
                    {2},
                    1
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            v_messageType = int(v_database.ExecuteScalar('''
                select mes.met_in_code
                from messages mes
                where mes.mes_in_code = {0}'''.format(p_requestMessage['v_data']['forwardMessageCode'])
            ))

            if v_messageType == 2 or v_messageType == 4: #Pasted image or attachment
                try:
                    shutil.copyfile(
                        os.path.join(settings.CHAT_FOLDER, str(p_requestMessage['v_data']['forwardMessageCode'])),
                        os.path.join(settings.CHAT_FOLDER, str(v_messageCode)),
                    )
                except Exception as exc:
                    v_database.Execute('''
                        delete
                        from messages
                        where mes_in_code = {0}
                        '''.format(v_messageCode)
                    )

                    v_database.Execute('''
                        delete from messages_channels
                        where mes_in_code = {0}
                          and gro_in_code = {1}
                        '''.format(
                            v_messageCode,
                            p_requestMessage['v_data']['channelCode']
                        )
                    )

                    raise Exception() from exc
        elif p_requestMessage['v_data']['messageType'] == 1: #Plain Text
            v_content = p_requestMessage['v_data']['messageContent']

            #Format blockquote element
            if v_content[0:4] == '&gt;':
                v_content = '<blockquote>{0}</blockquote>'.format(v_content[4:])

            #Format pre elements
            v_match = re.search(r'```((.|\s)*?)```', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<pre>' + v_content[v_start + 3: v_end - 3] + '</pre>' + v_content[v_end:]
                v_match = re.search(r'```((.|\s)*?)```', v_content)

            #Format kbd elements
            v_match = re.search(r'``(.*?)``', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<kbd>' + v_content[v_start + 2: v_end - 2] + '</kbd>' + v_content[v_end:]
                v_match = re.search(r'``(.*?)``', v_content)

            #Format code elements
            v_match = re.search(r'`(.*?)`', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<code>' + v_content[v_start + 1: v_end - 1] + '</code>' + v_content[v_end:]
                v_match = re.search(r'`(.*?)`', v_content)

            #Format bold elements
            v_match = re.search(r'\*(.*?)\*', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<b>' + v_content[v_start + 1: v_end - 1] + '</b>' + v_content[v_end:]
                v_match = re.search(r'\*(.*?)\*', v_content)

            #Format italic elements
            v_match = re.search(r'\b_(.*?)_\b', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<i>' + v_content[v_start + 1: v_end - 1] + '</i>' + v_content[v_end:]
                v_match = re.search(r'\b_(.*?)_\b', v_content)

            #Format strike elements
            v_match = re.search(r'~(.*?)~', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<strike>' + v_content[v_start + 1: v_end - 1] + '</strike>' + v_content[v_end:]
                v_match = re.search(r'~(.*?)~', v_content)

            #Format anchor elements
            #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
            v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()

                v_prefix = ''

                if v_start > 0:
                    v_prefix = v_content[:v_start]

                v_content = v_prefix + '<a href="' + v_content[v_start:v_end] + '">' + v_content[v_start:v_end].replace('https://', '').replace('http://', '') + '</a>' + v_content[v_end:]

                #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
                v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

            #Format user notification
            v_userDict = GetUsersLoginByChannelCode(p_webSocketSession, int(p_requestMessage['v_data']['channelCode']))

            if v_userDict is not None:
                v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

                while v_match is not None:
                    v_start = v_match.start()
                    v_end = v_match.end()

                    v_prefix = ''

                    if v_start > 0:
                        v_prefix = v_content[:v_start]

                    if v_content[v_start + 1 : v_end] in v_userDict:
                        v_content = v_prefix + '<span class="span_notify_user">' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]
                    else:
                        v_content = v_prefix + '<span>' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]

                    v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

            v_content = re.sub("'", "''", v_content)

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    1, --Plain Text
                    '{2}',
                    null,
                    null,
                    null,
                    null,
                    '{3}'
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_content,
                    re.sub("'", "''", p_requestMessage['v_data']['messageRawContent'])
                )
            )

            v_database.Execute('''
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                )
                select {0} as mes_in_code,
                        usc.cha_in_code as cha_in_code,
                        usc.use_in_code,
                        0 as mec_bo_viewed
                 from users_channels usc
                 where usc.cha_in_code = {1}
                   and usc.use_in_code <> {2}
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                ) values (
                    {0},
                    {1},
                    {2},
                    1
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )
        elif p_requestMessage['v_data']['messageType'] == 2: #Pasted Image
            v_title = re.sub("'", "''", p_requestMessage['v_data']['messageTitle'])
            v_attachmentName = re.sub("'", "''", p_requestMessage['v_data']['messageAttachmentName'])
            v_attachmentPath = '{0}/{1}'.format(settings.CHAT_FOLDER, v_messageCode)
            v_attachmentPath = re.sub("'", "''", v_attachmentPath)

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    2, --Pasted Image
                    null,
                    '{2}',
                    '{3}',
                    '{4}',
                    null,
                    null
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_title,
                    v_attachmentName,
                    v_attachmentPath
                )
            )

            v_database.Execute('''
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                )
                select {0} as mes_in_code,
                        usc.cha_in_code as cha_in_code,
                        usc.use_in_code,
                        0 as mec_bo_viewed
                 from users_channels usc
                 where usc.cha_in_code = {1}
                   and usc.use_in_code <> {2}
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                ) values (
                    {0},
                    {1},
                    {2},
                    1
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            try:
                v_file = open('{0}/{1}'.format(settings.CHAT_FOLDER, v_messageCode), 'wb')
                v_file.write(base64.b64decode(p_requestMessage['v_data']['messageContent']))
                v_file.close()
            except Exception as exc:
                v_database.Execute('''
                    delete
                    from messages
                    where mes_in_code = {0}
                    '''.format(v_messageCode)
                )

                v_database.Execute('''
                    delete from messages_channels
                    where mes_in_code = {0}
                      and gro_in_code = {1}
                    '''.format(
                        v_messageCode,
                        p_requestMessage['v_data']['channelCode']
                    )
                )

                raise Exception() from exc
        elif p_requestMessage['v_data']['messageType'] == 3: #Snippet
            v_title = re.sub("'", "''", p_requestMessage['v_data']['messageTitle'])
            v_content = re.sub("'", "''", p_requestMessage['v_data']['messageContent'])
            v_snippetMode = re.sub("'", "''", p_requestMessage['v_data']['messageSnippetMode'])

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    3, --Snippet
                    '{3}',
                    '{2}',
                    null,
                    null,
                    '{4}',
                    null
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_title,
                    v_content,
                    v_snippetMode
                )
            )

            v_database.Execute('''
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                )
                select {0} as mes_in_code,
                        usc.cha_in_code as cha_in_code,
                        usc.use_in_code,
                        0 as mec_bo_viewed
                 from users_channels usc
                 where usc.cha_in_code = {1}
                   and usc.use_in_code <> {2}
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                ) values (
                    {0},
                    {1},
                    {2},
                    1
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )
        elif p_requestMessage['v_data']['messageType'] == 4: #Attachment
            v_title = re.sub("'", "''", p_requestMessage['v_data']['messageTitle'])
            v_attachmentName = re.sub("'", "''", p_requestMessage['v_data']['messageAttachmentName'])
            v_attachmentPath = '{0}/{1}'.format(settings.CHAT_FOLDER, v_messageCode)
            v_attachmentPath = re.sub("'", "''", v_attachmentPath)

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    4, --Attachment
                    null,
                    '{2}',
                    '{3}',
                    '{4}',
                    null,
                    null
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_title,
                    v_attachmentName,
                    v_attachmentPath
                )
            )

            v_database.Execute('''
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                )
                select {0} as mes_in_code,
                        usc.cha_in_code as cha_in_code,
                        usc.use_in_code,
                        0 as mec_bo_viewed
                 from users_channels usc
                 where usc.cha_in_code = {1}
                   and usc.use_in_code <> {2}
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                ) values (
                    {0},
                    {1},
                    {2},
                    1
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            try:
                v_file = open('{0}/{1}'.format(settings.CHAT_FOLDER, v_messageCode), 'wb')
                v_file.write(base64.b64decode(p_requestMessage['v_data']['messageContent']))
                v_file.close()
            except Exception as exc:
                v_database.Execute('''
                    delete
                    from messages
                    where mes_in_code = {0}
                    '''.format(v_messageCode)
                )

                v_database.Execute('''
                    delete from messages_channels
                    where mes_in_code = {0}
                      and gro_in_code = {1}
                    '''.format(
                        v_messageCode,
                        p_requestMessage['v_data']['channelCode']
                    )
                )

                raise Exception() from exc

        elif p_requestMessage['v_data']['messageType'] == 5: #Mention
            v_content = p_requestMessage['v_data']['commentMessageContent']

            #Format blockquote element
            if v_content[0:4] == '&gt;':
                v_content = '<blockquote>{0}</blockquote>'.format(v_content[4:])

            #Format pre elements
            v_match = re.search(r'```((.|\s)*?)```', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<pre>' + v_content[v_start + 3: v_end - 3] + '</pre>' + v_content[v_end:]
                v_match = re.search(r'```((.|\s)*?)```', v_content)

            #Format kbd elements
            v_match = re.search(r'``(.*?)``', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<kbd>' + v_content[v_start + 2: v_end - 2] + '</kbd>' + v_content[v_end:]
                v_match = re.search(r'``(.*?)``', v_content)

            #Format code elements
            v_match = re.search(r'`(.*?)`', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<code>' + v_content[v_start + 1: v_end - 1] + '</code>' + v_content[v_end:]
                v_match = re.search(r'`(.*?)`', v_content)

            #Format bold elements
            v_match = re.search(r'\*(.*?)\*', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<b>' + v_content[v_start + 1: v_end - 1] + '</b>' + v_content[v_end:]
                v_match = re.search(r'\*(.*?)\*', v_content)

            #Format italic elements
            v_match = re.search(r'\b_(.*?)_\b', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<i>' + v_content[v_start + 1: v_end - 1] + '</i>' + v_content[v_end:]
                v_match = re.search(r'\b_(.*?)_\b', v_content)

            #Format strike elements
            v_match = re.search(r'~(.*?)~', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()
                v_content = v_content[:v_start] + '<strike>' + v_content[v_start + 1: v_end - 1] + '</strike>' + v_content[v_end:]
                v_match = re.search(r'~(.*?)~', v_content)

            #Format anchor elements
            #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
            v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()

                v_prefix = ''

                if v_start > 0:
                    v_prefix = v_content[:v_start]

                v_content = v_prefix + '<a href="' + v_content[v_start:v_end] + '">' + v_content[v_start:v_end].replace('https://', '').replace('http://', '') + '</a>' + v_content[v_end:]

                #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
                v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

            #Format user notification
            v_userDict = GetUsersLoginByChannelCode(p_webSocketSession, int(p_requestMessage['v_data']['channelCode']))

            if v_userDict is not None:
                v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

                while v_match is not None:
                    v_start = v_match.start()
                    v_end = v_match.end()

                    v_prefix = ''

                    if v_start > 0:
                        v_prefix = v_content[:v_start]

                    if v_content[v_start + 1 : v_end] in v_userDict:
                        v_content = v_prefix + '<span class="span_notify_user">' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]
                    else:
                        v_content = v_prefix + '<span>' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]

                    v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

            v_content += '<blockquote>' + p_requestMessage['v_data']['mentionedMessageContent'] + '</blockquote>'
            v_originalContent = p_requestMessage['v_data']['commentMessageRawContent'] + '#start_mentioned_message#' + p_requestMessage['v_data']['mentionedMessageContent'] + '#end_mentioned_message#'

            v_content = re.sub("'", "''", v_content)
            v_originalContent = v_originalContent.replace("'", "''")

            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    5, --Mention
                    '{2}',
                    null,
                    null,
                    null,
                    null,
                    '{3}'
                )
                '''.format(
                    v_messageCode,
                    int(p_webSocketSession.cookies['user_id'].value),
                    v_content,
                    v_originalContent
                )
            )

            v_database.Execute('''
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                )
                select {0} as mes_in_code,
                        usc.cha_in_code as cha_in_code,
                        usc.use_in_code,
                        0 as mec_bo_viewed
                 from users_channels usc
                 where usc.cha_in_code = {1}
                   and usc.use_in_code <> {2}
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                ) values (
                    {0},
                    {1},
                    {2},
                    1
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value)
                )
            )

        v_database.Close()

        if v_messageCode != 0:
            v_database.Open()

            v_table = v_database.Query('''
                select mes.mes_in_code,
                       mes.mes_dt_creation,
                       mes.mes_dt_update,
                       use.user_id as use_in_code,
                       use.user_name as use_st_login,
                       mes.met_in_code,
                       coalesce(mes.mes_st_content, '') as mes_st_content,
                       coalesce(mes.mes_st_title, '') as mes_st_title,
                       coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                       coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                       coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                from messages mes
                inner join users use
                           on mes.use_in_code = use.user_id
                where mes.mes_in_code = {0}'''.format(v_messageCode)
            )

            v_database.Close()

            if len(v_table.Rows) > 0:
                v_user = classes.User(v_table.Rows[0]['use_in_code'], '', v_table.Rows[0]['use_st_login'], None)
                v_message = classes.Message(
                    int(v_table.Rows[0]['mes_in_code']),
                    v_table.Rows[0]['mes_dt_creation'],
                    v_table.Rows[0]['mes_dt_update'],
                    v_user,
                    int(v_table.Rows[0]['met_in_code']),
                    v_table.Rows[0]['mes_st_content'],
                    v_table.Rows[0]['mes_st_title'],
                    v_table.Rows[0]['mes_st_attachmentname'],
                    False,
                    v_table.Rows[0]['mes_st_snippetmode'],
                    v_table.Rows[0]['mes_st_originalcontent']
                )

                v_data = {
                    'channelCode': p_requestMessage['v_data']['channelCode'],
                    'message': v_message
                }

                v_userList = GetUsersToSendMessageByChannelCode(p_webSocketSession, p_requestMessage['v_data']['channelCode'])

                if v_userList is not None:
                    if int(p_webSocketSession.cookies['user_id'].value) in v_userList:
                        v_userList.remove(int(p_webSocketSession.cookies['user_id'].value))

                    p_responseMessage['v_data'] = v_data
                    p_responseMessage['v_code'] = response.NewChannelMessage.value
                    SendToSomeClients(v_userList, p_responseMessage)

                v_data['message'].viewed = True
                SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'SendChannelMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SendChannelMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        LogException(p_webSocketSession, '', 'Exceção de Sistema', 'SendChannelMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SendChannelMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def RetrieveChannelHistory(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles retrieve channel history message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_data = {
            'channelCode': int(p_requestMessage['v_data']['channelCode']),
            'messageList': [],
            'fromMessageCode': p_requestMessage['v_data']['fromMessageCode']
        }

        v_table = None

        if p_requestMessage['v_data']['fromMessageCode'] is None:
            v_table = v_database.Query('''
                select mes.mes_in_code,
                       mes.mes_dt_creation,
                       mes.mes_dt_update,
                       use.user_id as use_in_code,
                       use.user_name as use_st_login,
                       mes.met_in_code,
                       coalesce(mes.mes_st_content, '') as mes_st_content,
                       coalesce(mes.mes_st_title, '') as mes_st_title,
                       coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                       mec.mec_bo_viewed,
                       coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                       coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                from messages_channels mec
                inner join messages mes
                           on mec.mes_in_code = mes.mes_in_code
                inner join users use
                           on mes.use_in_code = use.user_id
                where mec.cha_in_code = {0}
                  and mec.use_in_code = {1}
                order by mes.mes_dt_creation desc
                limit 20
                offset {2}'''.format(
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['offset']
                )
            )
        else :
            v_table = v_database.Query('''
                select mes.mes_in_code,
                       mes.mes_dt_creation,
                       mes.mes_dt_update,
                       use.user_id as use_in_code,
                       use.user_name as use_st_login,
                       mes.met_in_code,
                       coalesce(mes.mes_st_content, '') as mes_st_content,
                       coalesce(mes.mes_st_title, '') as mes_st_title,
                       coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                       mec.mec_bo_viewed,
                       coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                       coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                from messages_channels mec
                inner join messages mes
                           on mec.mes_in_code = mes.mes_in_code
                inner join users use
                           on mes.use_in_code = use.user_id
                where mec.cha_in_code = {0}
                  and mec.use_in_code = {1}
                  and mes.mes_dt_creation >= (select m.mes_dt_creation
                                              from messages m
                                              where m.mes_in_code = {3})
                order by mes.mes_dt_creation desc
                offset {2}'''.format(
                    p_requestMessage['v_data']['channelCode'],
                    int(p_webSocketSession.cookies['user_id'].value),
                    p_requestMessage['v_data']['offset'],
                    p_requestMessage['v_data']['fromMessageCode']
                )
            )

        v_database.Close()

        if v_table is not None:
            for v_row in v_table.Rows:
                v_user = classes.User(v_row['use_in_code'], '', v_row['use_st_login'], None)
                v_message = classes.Message(
                    int(v_row['mes_in_code']),
                    v_row['mes_dt_creation'],
                    v_row['mes_dt_update'],
                    v_user,
                    int(v_row['met_in_code']),
                    v_row['mes_st_content'],
                    v_row['mes_st_title'],
                    v_row['mes_st_attachmentname'],
                    (True if v_row['mec_bo_viewed'] else False),
                    v_row['mes_st_snippetmode'],
                    v_row['mes_st_originalcontent']
                )
                v_data['messageList'].append(v_message)

        p_responseMessage['v_data'] = v_data
        p_responseMessage['v_code'] = response.RetrievedChannelHistory.value
        SendToClient(p_webSocketSession, p_responseMessage, False)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'RetrieveChannelHistory', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "RetrieveChannelHistory".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        LogException(p_webSocketSession, '', 'Exceção de Sistema', 'RetrieveChannelHistory', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "RetrieveChannelHistory".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def MarkChannelMessagesAsRead(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles mark channel messages as read message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        for i in range(0, len(p_requestMessage['v_data']['messageCodeList'])):
            v_database.Execute('''
                update messages_channels
                set mec_bo_viewed = 1
                where cha_in_code = {0}
                  and use_in_code = {1}
                  and mes_in_code = {2}
                '''.format(
                    p_requestMessage['v_data']['channelCode'],
                    p_webSocketSession.cookies['user_id'].value,
                    p_requestMessage['v_data']['messageCodeList'][i]
                )
            )

        v_database.Close()

        p_responseMessage['v_data'] = p_requestMessage['v_data']
        p_responseMessage['v_code'] = response.MarkedChannelMessagesAsRead.value
        SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'MarkChannelMessagesAsRead', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "MarkChannelMessagesAsRead".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        LogException(p_webSocketSession, '', 'Exceção de Sistema', 'MarkChannelMessagesAsRead', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "MarkChannelMessagesAsRead".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def SetChannelUserWriting(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles set channel user writing message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    v_userList = GetUsersToSendMessageByChannelCode(p_webSocketSession, p_requestMessage['v_data']['channelCode'])

    if v_userList is not None:
        if int(p_webSocketSession.cookies['user_id'].value) in v_userList:
            v_userList.remove(int(p_webSocketSession.cookies['user_id'].value))

        p_responseMessage['v_data'] = p_requestMessage['v_data']
        p_responseMessage['v_code'] = response.ChannelUserWriting.value
        SendToSomeClients(v_userList, p_responseMessage)

def ChangeChannelSilenceSettings(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles change channel silence settings message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_database.Execute('''
            update users_channels
            set usc_bo_silenced = {2}
            where cha_in_code = {0}
              and use_in_code = {1}
            '''.format(
                p_requestMessage['v_data']['channelCode'],
                p_webSocketSession.cookies['user_id'].value,
                ('1' if p_requestMessage['v_data']['silenceChannel'] else '0')
            )
        )

        v_database.Close()

        v_data = {
            'channelCode': p_requestMessage['v_data']['channelCode'],
            'channelSilenced': p_requestMessage['v_data']['silenceChannel']
        }

        p_responseMessage['v_data'] = v_data
        p_responseMessage['v_code'] = response.ChannelSilenceSettings.value
        SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'ChangeChannelSilenceSettings', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "ChangeChannelSilenceSettings".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def RemoveChannelMessage(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles remove channel message message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_database.Execute('''
            delete from messages_channels
            where cha_in_code = {0}
              and use_in_code = {1}
              and mes_in_code = {2}
            '''.format(
                p_requestMessage['v_data']['channelCode'],
                p_webSocketSession.cookies['user_id'].value,
                p_requestMessage['v_data']['messageCode']
            )
        )

        v_database.Close()

        p_responseMessage['v_data'] = p_requestMessage['v_data']
        p_responseMessage['v_code'] = response.RemovedChannelMessage.value
        SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'RemoveChannelMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "RemoveChannelMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def UpdateChannelSnippetMessage(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles update channel snippet message message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_database.Execute('''
            update messages
            set mes_dt_update = datetime('now'),
                mes_st_title = '{2}',
                mes_st_snippetmode = '{3}',
                mes_st_content = '{4}'
            where mes_in_code = {0}
              and use_in_code = {1}
            '''.format(
                p_requestMessage['v_data']['messageCode'],
                p_webSocketSession.cookies['user_id'].value,
                p_requestMessage['v_data']['snippetTitle'].replace("'", "''"),
                p_requestMessage['v_data']['snippetMode'].replace("'", "''"),
                p_requestMessage['v_data']['snippetContent'].replace("'", "''")
            )
        )

        v_updatedAt = v_database.ExecuteScalar('''
            select mes.mes_dt_update
            from messages mes
            where mes.mes_in_code = {0}
            '''.format(
                p_requestMessage['v_data']['messageCode']
            )
        )

        v_database.Close()

        v_userList = GetUsersToSendMessageByChannelCode(p_webSocketSession, p_requestMessage['v_data']['channelCode'])

        if v_userList is not None:
            p_responseMessage['v_data'] = p_requestMessage['v_data']
            p_responseMessage['v_data']['updatedAt'] = v_updatedAt
            p_responseMessage['v_code'] = response.UpdatedChannelSnippetMessage.value
            SendToSomeClients(v_userList, p_responseMessage)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'UpdateChannelSnippetMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "UpdateChannelSnippetMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def UpdateChannelMessage(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles update channel message message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_content = p_requestMessage['v_data']['messageContent']
        v_index = v_content.find('#start_mentioned_message#')

        if v_index != -1:
            v_content = v_content[:v_index]

        #Format blockquote element
        if v_content[0:4] == '&gt;':
            v_content = '<blockquote>{0}</blockquote>'.format(v_content[4:])

        #Format pre elements
        v_match = re.search(r'```((.|\s)*?)```', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<pre>' + v_content[v_start + 3: v_end - 3] + '</pre>' + v_content[v_end:]
            v_match = re.search(r'```((.|\s)*?)```', v_content)

        #Format kbd elements
        v_match = re.search(r'``(.*?)``', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<kbd>' + v_content[v_start + 2: v_end - 2] + '</kbd>' + v_content[v_end:]
            v_match = re.search(r'``(.*?)``', v_content)

        #Format code elements
        v_match = re.search(r'`(.*?)`', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<code>' + v_content[v_start + 1: v_end - 1] + '</code>' + v_content[v_end:]
            v_match = re.search(r'`(.*?)`', v_content)

        #Format bold elements
        v_match = re.search(r'\*(.*?)\*', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<b>' + v_content[v_start + 1: v_end - 1] + '</b>' + v_content[v_end:]
            v_match = re.search(r'\*(.*?)\*', v_content)

        #Format italic elements
        v_match = re.search(r'\b_(.*?)_\b', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<i>' + v_content[v_start + 1: v_end - 1] + '</i>' + v_content[v_end:]
            v_match = re.search(r'\b_(.*?)_\b', v_content)

        #Format strike elements
        v_match = re.search(r'~(.*?)~', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<strike>' + v_content[v_start + 1: v_end - 1] + '</strike>' + v_content[v_end:]
            v_match = re.search(r'~(.*?)~', v_content)

        #Format anchor elements
        #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
        v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()

            v_prefix = ''

            if v_start > 0:
                v_prefix = v_content[:v_start]

            v_content = v_prefix + '<a href="' + v_content[v_start:v_end] + '">' + v_content[v_start:v_end].replace('https://', '').replace('http://', '') + '</a>' + v_content[v_end:]

            #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
            v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

        #Format user notification
        v_userDict = GetUsersLoginByChannelCode(p_webSocketSession, int(p_requestMessage['v_data']['channelCode']))

        if v_userDict is not None:
            v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

            while v_match is not None:
                v_start = v_match.start()
                v_end = v_match.end()

                v_prefix = ''

                if v_start > 0:
                    v_prefix = v_content[:v_start]

                if v_content[v_start + 1 : v_end] in v_userDict:
                    v_content = v_prefix + '<span class="span_notify_user">' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]
                else:
                    v_content = v_prefix + '<span>' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]

                v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

        if v_index != -1:
            v_content += p_requestMessage['v_data']['messageContent'][v_index:]
            v_content = v_content.replace('#start_mentioned_message#', '<blockquote>')
            v_content = v_content.replace('#end_mentioned_message#', '</blockquote>')

        v_database.Execute('''
            update messages
            set mes_dt_update = datetime('now'),
                mes_st_content = '{2}',
                mes_st_originalcontent = '{3}'
            where mes_in_code = {0}
              and use_in_code = {1}
            '''.format(
                p_requestMessage['v_data']['messageCode'],
                p_webSocketSession.cookies['user_id'].value,
                v_content.replace("'", "''"),
                p_requestMessage['v_data']['messageRawContent'].replace("'", "''")
            )
        )

        v_updatedAt = v_database.ExecuteScalar('''
            select mes.mes_dt_update
            from messages mes
            where mes.mes_in_code = {0}
            '''.format(
                p_requestMessage['v_data']['messageCode']
            )
        )

        v_database.Close()

        v_data = {
            'channelCode': p_requestMessage['v_data']['channelCode'],
            'messageCode': p_requestMessage['v_data']['messageCode'],
            'messageContent': v_content,
            'messageRawContent': p_requestMessage['v_data']['messageRawContent'],
            'updatedAt': v_updatedAt
        }

        v_userList = GetUsersToSendMessageByChannelCode(p_webSocketSession, p_requestMessage['v_data']['channelCode'])

        if v_userList is not None:
            p_responseMessage['v_data'] = v_data
            p_responseMessage['v_code'] = response.UpdatedChannelMessage.value
            SendToSomeClients(v_userList, p_responseMessage)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'UpdateChannelMessage', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "UpdateChannelMessage".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def CreatePrivateChannel(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles create private channel message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_channelCode = int(v_database.ExecuteScalar('''
            select coalesce(max(cha.cha_in_code), 0) + 1
            from channels cha'''
        ))

        v_database.Execute('''
            insert into channels (
                cha_in_code,
                cha_st_name,
                cha_bo_private
            ) values (
                {0},
                '{1}',
                1
            )
            '''.format(
                v_channelCode,
                p_requestMessage['v_data']['channelName'].replace("'", "''")
            )
        )

        v_database.Execute('''
            insert into users_channels (
                use_in_code,
                cha_in_code,
                usc_bo_silenced
            ) values (
                {1},
                {0},
                0
            )
            '''.format(
                v_channelCode,
                int(p_webSocketSession.cookies['user_id'].value)
            )
        )

        v_database.Close()

        #Get channel info
        v_channel = GetChannelInfo(p_webSocketSession, int(v_channelCode), int(p_webSocketSession.cookies['user_id'].value))

        v_data = {
            'channel': v_channel
        }

        p_responseMessage['v_code'] = response.NewPrivateChannel.value
        p_responseMessage['v_data'] = v_data
        SendToClient(p_webSocketSession, p_responseMessage, True)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'CreatePrivateChannel', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "CreatePrivateChannel".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def RenamePrivateChannel(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles rename private channel message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_database.Execute('''
            update channels
            set cha_st_name = '{1}'
            where cha_in_code = {0}
            '''.format(
                p_requestMessage['v_data']['channelCode'],
                p_requestMessage['v_data']['channelName'].replace("'", "''")
            )
        )

        v_database.Close()

        v_userList = GetUsersToSendMessageByChannelCode(p_webSocketSession, p_requestMessage['v_data']['channelCode'])

        if v_userList is not None:
            p_responseMessage['v_data'] = p_requestMessage['v_data']
            p_responseMessage['v_code'] = response.RenamedPrivateChannel.value
            SendToSomeClients(v_userList, p_responseMessage)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'RenamePrivateChannel', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "RenamePrivateChannel".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def QuitPrivateChannel(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles quit private channel message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_userList = GetUsersToSendMessageByChannelCode(p_webSocketSession, p_requestMessage['v_data']['channelCode'])

        v_database.Execute('''
            delete from users_channels
            where use_in_code = {1}
              and cha_in_code = {0}
            '''.format(
                p_requestMessage['v_data']['channelCode'],
                int(p_webSocketSession.cookies['user_id'].value)
            )
        )

        v_database.Close()

        if v_userList is not None:
            p_responseMessage['v_data'] = p_requestMessage['v_data']
            p_responseMessage['v_data']['userCode'] = int(p_webSocketSession.cookies['user_id'].value)
            p_responseMessage['v_code'] = response.QuittedPrivateChannel.value
            SendToSomeClients(v_userList, p_responseMessage)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'QuitPrivateChannel', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "QuitPrivateChannel".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def InvitePrivateChannelMembers(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles invite private channel message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        for v_userCode in p_requestMessage['v_data']['userCodeList']:
            v_database.Execute('''
                insert into users_channels (
                    use_in_code,
                    cha_in_code,
                    usc_bo_silenced
                ) values (
                    {1},
                    {0},
                    0
                )
                '''.format(
                    p_requestMessage['v_data']['channelCode'],
                    v_userCode
                )
            )

        v_database.Close()

        for v_userCode in GetUsersToSendMessageByChannelCode(p_webSocketSession, p_requestMessage['v_data']['channelCode']):
            #Get channel info
            v_channel = GetChannelInfo(p_webSocketSession, p_requestMessage['v_data']['channelCode'], v_userCode)

            if v_channel is not None:
                v_data = {
                    'channel': v_channel
                }

                p_responseMessage['v_code'] = response.InvitedPrivateChannelMembers.value
                p_responseMessage['v_data'] = v_data
                SendToSomeClients([v_userCode], p_responseMessage)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'InvitePrivateChannel', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "InvitePrivateChannel".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def Ping(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles ping message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    p_responseMessage['v_code'] = response.Pong.value
    p_responseMessage['v_data'] = None
    SendToClient(p_webSocketSession, p_responseMessage, False)

def SetUserChatStatus(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles set user chat status message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_database.Execute('''
            update users
            set stc_in_code = {1}
            where user_id = {0}
            '''.format(
                p_webSocketSession.cookies['user_id'].value,
                p_requestMessage['v_data']['userChatStatusCode']
            )
        )

        v_statusName = v_database.ExecuteScalar('''
            select stc.stc_st_name
            from status_chat stc
            where coalesce(stc.stc_in_code, 1) = {0}'''.format(
                p_requestMessage['v_data']['userChatStatusCode']
            )
        )

        v_database.Close()

        v_status = classes.Status(int(p_requestMessage['v_data']['userChatStatusCode']), v_statusName)

        p_responseMessage['v_code'] = response.UserChatStatus.value

        p_responseMessage['v_data'] = {
            'userCode': int(p_webSocketSession.cookies['user_id'].value),
            'userChatStatus': v_status
        }

        SendToAllClients(p_responseMessage)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'SetUserChatStatus', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SetUserChatStatus".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        LogException(p_webSocketSession, '', 'Exceção de Sistema', 'SetUserChatStatus', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SetUserChatStatus".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def SearchOldMessages(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles search old messages message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_table = v_database.Query('''
            select *
            from (
                select 2 as type,
                       meg.gro_in_code as code,
                       mes.mes_in_code,
                       mes.mes_dt_creation,
                       mes.mes_dt_update,
                       use.user_id as use_in_code,
                       use.user_name as use_st_login,
                       mes.met_in_code,
                       coalesce(mes.mes_st_content, '') as mes_st_content,
                       coalesce(mes.mes_st_title, '') as mes_st_title,
                       coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                       meg.meg_bo_viewed as visualizada,
                       coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                       (case instr(coalesce(mes.mes_st_originalcontent, ''), '#start_mentioned_message#')
                             when 0 then coalesce(mes.mes_st_originalcontent, '')
                             else substr(coalesce(mes.mes_st_originalcontent, ''), 1, instr(coalesce(mes.mes_st_originalcontent, ''), '#start_mentioned_message#'))
                        end
                       ) as mes_st_originalcontent
                from messages_groups meg
                inner join messages mes
                           on meg.mes_in_code = mes.mes_in_code
                inner join users use
                           on mes.use_in_code = use.user_id
                where meg.use_in_code = {0}

                union

                select 1 as type,
                       mec.cha_in_code as code,
                       mes.mes_in_code,
                       mes.mes_dt_creation,
                       mes.mes_dt_update,
                       use.user_id as use_in_code,
                       use.user_name as use_st_login,
                       mes.met_in_code,
                       coalesce(mes.mes_st_content, '') as mes_st_content,
                       coalesce(mes.mes_st_title, '') as mes_st_title,
                       coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                       mec.mec_bo_viewed as visualizada,
                       coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                       (case instr(coalesce(mes.mes_st_originalcontent, ''), '#start_mentioned_message#')
                             when 0 then coalesce(mes.mes_st_originalcontent, '')
                             else substr(coalesce(mes.mes_st_originalcontent, ''), 1, instr(coalesce(mes.mes_st_originalcontent, ''), '#start_mentioned_message#'))
                        end
                       ) as mes_st_originalcontent
                from messages_channels mec
                inner join messages mes
                           on mec.mes_in_code = mes.mes_in_code
                inner join users use
                           on mes.use_in_code = use.user_id
                where mec.use_in_code = {0}
            ) x
            where x.mes_st_originalcontent like '%{1}%'
            order by x.mes_dt_creation desc'''.format(
                int(p_webSocketSession.cookies['user_id'].value),
                p_requestMessage['v_data']['textPattern'].replace("'", "''")
            )
        )

        v_database.Close()

        v_data = {
            'textPattern': p_requestMessage['v_data']['textPattern'],
            'messageList': []
        }

        for v_row in v_table.Rows:
            v_user = classes.User(v_row['use_in_code'], '', v_row['use_st_login'], None)
            v_message = classes.Message(
                int(v_row['mes_in_code']),
                v_row['mes_dt_creation'],
                v_row['mes_dt_update'],
                v_user,
                int(v_row['met_in_code']),
                v_row['mes_st_content'],
                v_row['mes_st_title'],
                v_row['mes_st_attachmentname'],
                (True if v_row['visualizada'] else False),
                v_row['mes_st_snippetmode'],
                v_row['mes_st_originalcontent']
            )
            v_data['messageList'].append({
                'message': v_message,
                'type': v_row['type'],
                'code': v_row['code']
            })

        p_responseMessage['v_code'] = response.SearchedOldMessages.value
        p_responseMessage['v_data'] = v_data
        SendToClient(p_webSocketSession, p_responseMessage, False)
    except Spartacus.Database.Exception as exc:
        LogException(p_webSocketSession, '', 'Database Exception', 'SearchOldMessages', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SearchOldMessages".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        LogException(p_webSocketSession, '', 'Exceção de Sistema', 'SearchOldMessages', traceback.format_exc())
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SearchOldMessages".'
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return

def SendMessageAsBot(p_webSocketSession, p_requestMessage, p_responseMessage):
    """Handles send message as bot message requested by a client

        Args:
            p_webSocketSession (WSHandler): the websocket client that requested this.
            p_requestMessage (dict): the request message.
            p_responseMessage (dict): the response message.
    """

    try:
        v_database = p_webSocketSession.session.v_omnidb_database.v_connection
        v_database.Open()

        v_isBot = 0

        v_isBot = int(v_database.ExecuteScalar('''
            select coalesce(use.use_bo_bot, 0) as use_bo_bot
            from users use
            where use.user_id = {0}'''.format(p_requestMessage['v_data']['botCode'])
        ))

        if not v_isBot:
            return

        v_content = p_requestMessage['v_data']['messageContent']

        #Format blockquote element
        if v_content[0] == '>':
            v_content = '<blockquote>{0}</blockquote>'.format(v_content[1:])

        #Format pre elements
        v_match = re.search(r'```((.|\s)*?)```', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<pre>' + v_content[v_start + 3: v_end - 3] + '</pre>' + v_content[v_end:]
            v_match = re.search(r'```((.|\s)*?)```', v_content)

        #Format kbd elements
        v_match = re.search(r'``(.*?)``', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<kbd>' + v_content[v_start + 2: v_end - 2] + '</kbd>' + v_content[v_end:]
            v_match = re.search(r'``(.*?)``', v_content)

        #Format code elements
        v_match = re.search(r'`(.*?)`', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<code>' + v_content[v_start + 1: v_end - 1] + '</code>' + v_content[v_end:]
            v_match = re.search(r'`(.*?)`', v_content)

        #Format bold elements
        v_match = re.search(r'\*(.*?)\*', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<b>' + v_content[v_start + 1: v_end - 1] + '</b>' + v_content[v_end:]
            v_match = re.search(r'\*(.*?)\*', v_content)

        #Format italic elements
        v_match = re.search(r'\b_(.*?)_\b', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<i>' + v_content[v_start + 1: v_end - 1] + '</i>' + v_content[v_end:]
            v_match = re.search(r'\b_(.*?)_\b', v_content)

        #Format strike elements
        v_match = re.search(r'~(.*?)~', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()
            v_content = v_content[:v_start] + '<strike>' + v_content[v_start + 1: v_end - 1] + '</strike>' + v_content[v_end:]
            v_match = re.search(r'~(.*?)~', v_content)

        #Format anchor elements
        #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
        v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

        while v_match is not None:
            v_start = v_match.start()
            v_end = v_match.end()

            v_prefix = ''

            if v_start > 0:
                v_prefix = v_content[:v_start]

            v_content = v_prefix + '<a href="' + v_content[v_start:v_end] + '">' + v_content[v_start:v_end].replace('https://', '').replace('http://', '') + '</a>' + v_content[v_end:]

            #v_match = re.search(r'^(?!href=")https?:\/\/(www\.)?[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?', v_content)
            v_match = re.search(r'(?<!href=")(?<!src=")(https?):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?', v_content)

        if p_requestMessage['v_data']['destinyType'] == 1: #Channel
            #Format user notification
            v_userDict = GetUsersLoginByChannelCode(p_webSocketSession, int(p_requestMessage['v_data']['destinyCode']))

            if v_userDict is not None:
                v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

                while v_match is not None:
                    v_start = v_match.start()
                    v_end = v_match.end()

                    v_prefix = ''

                    if v_start > 0:
                        v_prefix = v_content[:v_start]

                    if v_content[v_start + 1 : v_end] in v_userDict:
                        v_content = v_prefix + '<span class="span_notify_user">' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]
                    else:
                        v_content = v_prefix + '<span>' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]

                    v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

        elif p_requestMessage['v_data']['destinyType'] == 2: #Group
            #Format user notification
            v_userDict = GetUsersLoginByGroupCode(p_webSocketSession, int(p_requestMessage['v_data']['destinyCode']))

            if v_userDict is not None:
                v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

                while v_match is not None:
                    v_start = v_match.start()
                    v_end = v_match.end()

                    v_prefix = ''

                    if v_start > 0:
                        v_prefix = v_content[:v_start]

                    if v_content[v_start + 1 : v_end] in v_userDict:
                        v_content = v_prefix + '<span class="span_notify_user">' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]
                    else:
                        v_content = v_prefix + '<span>' + v_content[v_start:v_end] + '</span>' + v_content[v_end:]

                    v_match = re.search(r'(^@|(?<=\s)@)([a-z]|[A-Z]|[0-9]|_|\.)+((?=\s)|\b)', v_content)

        v_content = re.sub("'", "''", v_content)

        v_messageCode = 0

        if p_requestMessage['v_data']['destinyType'] == 1: #Channel
            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    1, --Plain Text
                    '{2}',
                    null,
                    null,
                    null,
                    null,
                    '{3}'
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['botCode'],
                    v_content,
                    re.sub("'", "''", p_requestMessage['v_data']['messageContent'])
                )
            )

            v_database.Execute('''
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                )
                select {0} as mes_in_code,
                        usg.gro_in_code as gro_in_code,
                        usg.use_in_code,
                        0 as meg_bo_viewed
                 from users_groups usg
                 where usg.gro_in_code = {2}
                   and usg.use_in_code <> {1}
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['botCode'],
                    p_requestMessage['v_data']['destinyCode']
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_groups (
                    mes_in_code,
                    gro_in_code,
                    use_in_code,
                    meg_bo_viewed
                ) values (
                    {0},
                    {2},
                    {1},
                    1
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['botCode'],
                    p_requestMessage['v_data']['destinyCode']
                )
            )
        elif p_requestMessage['v_data']['destinyType'] == 2: #Group
            v_messageCode = int(v_database.ExecuteScalar('''
                select coalesce(max(mes.mes_in_code), 0) + 1
                from messages mes'''
            ))

            v_database.Execute('''
                insert into messages (
                    mes_in_code,
                    mes_dt_creation,
                    mes_dt_update,
                    use_in_code,
                    met_in_code,
                    mes_st_content,
                    mes_st_title,
                    mes_st_attachmentname,
                    mes_st_attachmentpath,
                    mes_st_snippetmode,
                    mes_st_originalcontent
                ) values (
                    {0},
                    datetime('now'),
                    datetime('now'),
                    {1},
                    1, --Plain Text
                    '{2}',
                    null,
                    null,
                    null,
                    null,
                    '{3}'
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['botCode'],
                    v_content,
                    re.sub("'", "''", p_requestMessage['v_data']['messageContent'])
                )
            )

            v_database.Execute('''
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                )
                select {0} as mes_in_code,
                        usc.cha_in_code as cha_in_code,
                        usc.use_in_code,
                        0 as mec_bo_viewed
                 from users_channels usc
                 where usc.cha_in_code = {1}
                   and usc.use_in_code <> {2}
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['destinyCode'],
                    p_requestMessage['v_data']['botCode']
                )
            )

            v_database.Execute('''
                --User that sent the message "has already seen it"
                insert into messages_channels (
                    mes_in_code,
                    cha_in_code,
                    use_in_code,
                    mec_bo_viewed
                ) values (
                    {0},
                    {1},
                    {2},
                    1
                )
                '''.format(
                    v_messageCode,
                    p_requestMessage['v_data']['destinyCode'],
                    p_requestMessage['v_data']['botCode']
                )
            )

        v_database.Close()

        if v_messageCode != 0:
            if p_requestMessage['v_data']['destinyType'] == 1: #Channel
                v_database.Open()

                v_table = v_database.Query('''
                    select mes.mes_in_code,
                           mes.mes_dt_creation,
                           mes.mes_dt_update,
                           use.user_id as use_in_code,
                           use.user_name as use_st_login,
                           mes.met_in_code,
                           coalesce(mes.mes_st_content, '') as mes_st_content,
                           coalesce(mes.mes_st_title, '') as mes_st_title,
                           coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                           coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                           coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                    from messages mes
                    inner join users use
                               on mes.use_in_code = use.user_id
                    where mes.mes_in_code = {0}'''.format(v_messageCode)
                )

                v_database.Close()

                if len(v_table.Rows) > 0:
                    v_user = classes.User(v_table.Rows[0]['use_in_code'], '', v_table.Rows[0]['use_st_login'], None)
                    v_message = classes.Message(
                        int(v_table.Rows[0]['mes_in_code']),
                        v_table.Rows[0]['mes_dt_creation'],
                        v_table.Rows[0]['mes_dt_update'],
                        v_user,
                        int(v_table.Rows[0]['met_in_code']),
                        v_table.Rows[0]['mes_st_content'],
                        v_table.Rows[0]['mes_st_title'],
                        v_table.Rows[0]['mes_st_attachmentname'],
                        False,
                        v_table.Rows[0]['mes_st_snippetmode'],
                        v_table.Rows[0]['mes_st_originalcontent']
                    )

                    v_data = {
                        'channelCode': p_requestMessage['v_data']['destinyCode'],
                        'message': v_message
                    }

                    v_userList = GetUsersToSendMessageByChannelCode(p_webSocketSession, p_requestMessage['v_data']['destinyCode'])

                    if v_userList is not None:
                        p_responseMessage['v_data'] = v_data
                        p_responseMessage['v_code'] = response.NewChannelMessage.value
                        SendToSomeClients(v_userList, p_responseMessage)

            elif p_requestMessage['v_data']['destinyType'] == 2: #Group
                v_database.Open()

                v_table = v_database.Query('''
                    select mes.mes_in_code,
                           mes.mes_dt_creation,
                           mes.mes_dt_update,
                           use.user_id as use_in_code,
                           use.user_name as use_st_login,
                           mes.met_in_code,
                           coalesce(mes.mes_st_content, '') as mes_st_content,
                           coalesce(mes.mes_st_title, '') as mes_st_title,
                           coalesce(mes.mes_st_attachmentname, '') as mes_st_attachmentname,
                           coalesce(mes.mes_st_snippetmode, '') as mes_st_snippetmode,
                           coalesce(mes.mes_st_originalcontent, '') as mes_st_originalcontent
                    from messages mes
                    inner join users use
                               on mes.use_in_code = use.user_id
                    where mes.mes_in_code = {0}'''.format(v_messageCode)
                )

                v_database.Close()

                if len(v_table.Rows) > 0:
                    v_user = classes.User(v_table.Rows[0]['use_in_code'], '', v_table.Rows[0]['use_st_login'], None)
                    v_message = classes.Message(
                        int(v_table.Rows[0]['mes_in_code']),
                        v_table.Rows[0]['mes_dt_creation'],
                        v_table.Rows[0]['mes_dt_update'],
                        v_user,
                        int(v_table.Rows[0]['met_in_code']),
                        v_table.Rows[0]['mes_st_content'],
                        v_table.Rows[0]['mes_st_title'],
                        v_table.Rows[0]['mes_st_attachmentname'],
                        False,
                        v_table.Rows[0]['mes_st_snippetmode'],
                        v_table.Rows[0]['mes_st_originalcontent']
                    )

                    v_data = {
                        'groupCode': p_requestMessage['v_data']['destinyCode'],
                        'message': v_message
                    }

                    v_userList = GetUsersToSendMessageByGroupCode(p_webSocketSession, p_requestMessage['v_data']['destinyCode'])

                    if v_userList is not None:
                        p_responseMessage['v_data'] = v_data
                        p_responseMessage['v_code'] = response.NewGroupMessage.value
                        SendToSomeClients(v_userList, p_responseMessage)
    except Spartacus.Database.Exception as exc:
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SendMessageAsBot": {0}'.format(traceback.format_exc())
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
    except Exception as exc:
        p_responseMessage['v_error'] = True
        p_responseMessage['v_data'] = 'Error while executing the static method "SendMessageAsBot": {0}'.format(traceback.format_exc())
        SendToClient(p_webSocketSession, p_responseMessage, True)
        return
