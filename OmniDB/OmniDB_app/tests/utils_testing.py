import django.http.response
import django.test
from django.urls import reverse
import json

from OmniDB import settings
import OmniDB_app.include.OmniDatabase as OmniDatabase
import OmniDB_app.include.Spartacus.Utils as Utils


USERS = {
    'ADMIN': {
        'USER': 'admin',
        'PASSWORD': 'admin'
    }
}


class InvalidParameterTypeException(Exception):
    """Used to raise an error of parameter type.
    """

    pass


class InvalidParameterValueException(Exception):
    """Used to raise an error of parameter value.
    """

    pass


def build_client_ajax_request(p_data=None, p_error=False):
    """Build an AJAX django client request object based on given data object.

        Args:
            p_data (object): anything that will be used as data in the request. Defaults to None.

        Returns:
            dict: the built django request object containing the data passed as parameter.
    """

    return {
        'data': json.dumps(p_data)
    }


def get_client_ajax_response_content(p_response=None):
    """Extract content from AJAX response in django client.

        Args:
            p_response (django.http.response.JsonResponse): the django client json response. Defaults to None.

        Returns:
            object: anything that was passed as data in an AJAX request.

        Raises:
            InvalidParameterTypeException.
    """

    if not isinstance(p_response, django.http.response.JsonResponse):
        raise InvalidParameterTypeException('"p_response" parameter must be a "django.http.response.JsonResponse" instance.')

    return json.loads(p_response.content.decode())


def get_client_omnidb_session(p_client=None):
    """Get OmniDB session from django client.

        Args:
            p_client(django.test.Client): the django client the session will be get from. Defaults to None.

        Returns:
            OmniDB_app.include.Session.Session: the OmniDB session of the django client, if any.
            None: otherwise

        Raises:
            InvalidParameterTypeException.
    """

    if not isinstance(p_client, django.test.Client):
        raise InvalidParameterTypeException('"p_client" parameter must be a "django.test.Client" instance.')

    if 'omnidb_session' in p_client.session:
        return p_client.session['omnidb_session']

    return None


def execute_client_login(p_client=None, p_username=None, p_password=None):
    """Used to execute login feature in a django client while testing.

        Args:
            p_client (django.test.Client): the django client where login feature will be executed. Defaults to None.
            p_username (str): the user name that will be used to log in into the system. Defaults to None.
            p_password (str): the password corresponding to the given username. Defaults to None.

        Returns:
            (bool, django.http.response.JsonResponse):
                If the login was successfully done or not.
                The response object from sigin call.

        Raises:
            InvalidParameterTypeException.
    """

    if not isinstance(p_client, django.test.Client):
        raise InvalidParameterTypeException('"p_client" parameter must be a "django.test.Client" instance.')

    if not isinstance(p_username, str):
        raise InvalidParameterTypeException('"p_username" parameter must be a "str" instance.')

    if not isinstance(p_password, str):
        raise InvalidParameterTypeException('"p_password" parameter must be a "str" instance.')

    v_response = p_client.post(
        reverse('sign_in'),
        build_client_ajax_request(
            p_data={
                'p_username': p_username,
                'p_pwd': p_password
            }
        )
    )

    if v_response.status_code != 200:
        return (False, v_response)

    if get_client_omnidb_session(p_client=p_client) is None:
        return (False, v_response)

    return (True, v_response)


def get_session_alert_message(p_client=None):
    """Get alert message from session.

        Args:
            p_client (django.test.Client): the django client where login feature will be executed. Defaults to None.

        Returns:
            str: if any message.
            None: otherwise

        Raises:
            InvalidParameterTypeException.
    """

    if not isinstance(p_client, django.test.Client):
        raise InvalidParameterTypeException('"p_client" parameter must be a "django.test.Client" instance.')

    if 'omnidb_alert_message' in p_client.session:
        return p_client.session['omnidb_alert_message']

    return None


def get_omnidb_database_connection():
    """Get omnidb.db database connection

        Returns:
            OmniDB_app.include.OmniDatabase.SQLite: a connection to the omnidb database.
    """

    return OmniDatabase.Generic.InstantiateDatabase(
        p_db_type='sqlite',
        p_server='',
        p_port='',
        p_service=settings.OMNIDB_DATABASE,
        p_user='',
        p_password='',
        p_conn_id='0',
        p_alias='',
        p_foreignkeys=True
    )


def get_cryptor():
    """Get a cryptor used by OmniDB.

        Returns:
            OmniDB_app.include.Spartacus.Utils.Cryptor: corresponding cryptor.
    """

    return Utils.Cryptor(
        p_key='omnidb',
        p_encoding='iso-8859-1'
    )
