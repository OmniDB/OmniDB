from . import exception

class Message:
    """Represent a message from database.

        Attributes:
            code (int): the message code.
            createdAt (str): string representating when message was created.
            updatedAt (str): string representating when message was updated.
            user (classes.User): the user that created the message.
            type (int): the message type.
            content (str): the message content.
            title (str): the message title.
            attachmentName (str): the message attachment.
            viewed (bool): if the message was viewed by the user.
            snippetMode (str): the language used in the snippet, if any.
            rawContent (str): the message raw content (before formatting).
    """

    def __init__(self, p_code = 0, p_createdAt = '', p_updatedAt = '', p_user = None, p_type = 0, p_content = '', p_title = '', p_attachmentName = '', p_viewed = False, p_snippetMode = '', p_rawContent = ''):
        """Create a new classes.Message instance.

            Args:
                p_code (int): the message code.
                p_createdAt (str): string representating when message was created.
                p_updatedAt (str): string representating when message was updated.
                p_user (classes.User): the user that created the message.
                p_type (int): the message type.
                p_content (str): the message content.
                p_title (str): the message title.
                p_attachmentName (str): the message attachment.
                p_viewed (bool): if the message was viewed by the user.
                p_snippetMode (str): the language used in the snippet, if any.
                p_rawContent (str): the message raw content (before formatting).

            Raises:
                exception.Exception: custom exceptions occurred in this script.
        """

        if not isinstance(p_code, int):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_code" deve ser do tipo "int".')

        if not isinstance(p_createdAt, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_createdAt" deve ser do tipo "str".')

        if not isinstance(p_updatedAt, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_updatedAt" deve ser do tipo "str".')

        if not isinstance(p_user, User):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_user" deve ser do tipo "User".')

        if not isinstance(p_type, int):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_type" deve ser do tipo "int".')

        if not isinstance(p_content, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_content" deve ser do tipo "str".')

        if not isinstance(p_title, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_title" deve ser do tipo "str".')

        if not isinstance(p_attachmentName, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_attachmentName" deve ser do tipo "str".')

        if not isinstance(p_viewed, bool):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_viewed" deve ser do tipo "bool".')

        if not isinstance(p_snippetMode, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_snippetMode" deve ser do tipo "str".')

        if not isinstance(p_rawContent, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Message": O parâmetro "p_rawContent" deve ser do tipo "str".')

        self.code = p_code
        self.createdAt = p_createdAt
        self.updatedAt = p_updatedAt
        self.user = p_user
        self.type = p_type
        self.content = p_content
        self.title = p_title
        self.attachmentName = p_attachmentName
        self.viewed = p_viewed
        self.snippetMode = p_snippetMode
        self.rawContent = p_rawContent

class Status:
    """Represent a chat status from database.

        Attributes:
            code (int): the status code.
            name (str): the status name.
    """

    def __init__(self, p_code = 1, p_name = 'Nenhum'):
        """Create a new classes.Status instance.

            Args:
                p_code (int): the status code.
                p_name (str): the status name.

            Raises:
                exception.Exception: custom exceptions occurred in this script.
        """

        if not isinstance(p_code, int):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Status": O parâmetro "p_code" deve ser do tipo "int".')

        if not isinstance(p_name, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Status": O parâmetro "p_name" deve ser do tipo "str".')

        self.code = p_code
        self.name = p_name

class User:
    """Represent a group from database.

        Attributes:
            code (int): the user code.
            name (str): the user name.
            login (str): the user login.
            status (classes.Status): the user chat status.
    """

    def __init__(self, p_code = 0, p_name = '', p_login = '', p_status = None):
        """Create a new classes.Group instance.

            Args:
                p_code (int): the user code.
                p_name (str): the user name.
                p_login (str): the user login.
                p_status (classes.Status): the user chat status.

            Raises:
                exception.Exception: custom exceptions occurred in this script.
        """

        if not isinstance(p_code, int):
            raise exception.Exception('Erro durante a instanciação da classe "classes.User": O parâmetro "p_code" deve ser do tipo "int".')

        if not isinstance(p_name, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.User": O parâmetro "p_name" deve ser do tipo "str".')

        if not isinstance(p_login, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.User": O parâmetro "p_login" deve ser do tipo "str".')

        if p_status is not None and not isinstance(p_status, Status):
            raise exception.Exception('Erro durante a instanciação da classe "classes.User": O parâmetro "p_status" deve ser do tipo "classes.Status".')

        self.code = p_code
        self.name = p_name
        self.login = p_login
        self.status = p_status

class Group:
    """Represent a group from database.

        Attributes:
            code (int): the group code.
            silenced (bool): if this group was silenced by the user.
            userList (list): a list where each item is a classes.User.
            messageList (list): a list where each item is a classes.Message.
    """

    def __init__(self, p_code = 0, p_silenced = False, p_userList = [], p_messageList = []):
        """Create a new classes.Group instance.

            Args:
                p_code (int): the group code.
                p_silenced (bool): if this group was silenced by the user.
                p_userList (list): a list where each item is a classes.User.
                p_messageList (list): a list where each item is a classes.Message.

            Raises:
                exception.Exception: custom exceptions occurred in this script.
        """

        if not isinstance(p_code, int):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Group": O parâmetro "p_code" deve ser do tipo "int".')

        if not isinstance(p_silenced, bool):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Group": O parâmetro "p_silenced" deve ser do tipo "bool".')

        if not isinstance(p_userList, list):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Group": O parâmetro "p_userList" deve ser do tipo "list".')

        if not isinstance(p_messageList, list):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Group": O parâmetro "p_messageList" deve ser do tipo "list".')

        self.code = p_code
        self.silenced = p_silenced
        self.userList = p_userList
        self.messageList = p_messageList

class Channel:
    """Represent a channel from database.

        Attributes:
            code (int): the channel code.
            name (str): the channel name.
            silenced (bool): if this channel was silenced by the user.
            userList (list): a list where each item is a classes.User.
            messageList (list): a list where each item is a classes.Message.
            private (bool): it this channel is private. In other words, if it was created by a chat user.
    """

    def __init__(self, p_code = 0, p_name = '', p_silenced = False, p_userList = [], p_messageList = [], p_private = False):
        """Create a new classes.Channel instance.

            Args:
                p_code (int): the channel code.
                p_name (str): the channel name.
                p_silenced (bool): if this group was silenced by the user.
                p_userList (list): a list where each item is a classes.User instance.
                p_messageList (list): a list where each item is a classes.Message.
                p_private (bool): it this channel is private. In other words, if it was created by a chat user.

            Raises:
                exception.Exception: custom exceptions occurred in this script.
        """

        if not isinstance(p_code, int):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Channel": O parâmetro "p_code" deve ser do tipo "int".')

        if not isinstance(p_name, str):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Channel": O parâmetro "p_name" deve ser do tipo "str".')

        if not isinstance(p_silenced, bool):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Channel": O parâmetro "p_silenced" deve ser do tipo "bool".')

        if not isinstance(p_userList, list):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Channel": O parâmetro "p_userList" deve ser do tipo "list".')

        if not isinstance(p_messageList, list):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Channel": O parâmetro "p_messageList" deve ser do tipo "list".')

        if not isinstance(p_private, bool):
            raise exception.Exception('Erro durante a instanciação da classe "classes.Channel": O parâmetro "p_private" deve ser do tipo "bool".')

        self.code = p_code
        self.name = p_name
        self.silenced = p_silenced
        self.userList = p_userList
        self.messageList = p_messageList
        self.private = p_private
