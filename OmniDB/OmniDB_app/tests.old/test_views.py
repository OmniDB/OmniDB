from django.test import TestCase
from django.urls import reverse
from collections import OrderedDict

from OmniDB import settings
import OmniDB_app.include.OmniDatabase.SQLite
import OmniDB_app.include.Spartacus.Utils
from .utils_testing import (
    build_client_ajax_request,
    execute_client_login,
    get_client_ajax_response_content,
    get_client_omnidb_session,
    get_omnidb_database_connection,
    get_session_alert_message,
    USERS
)


class ConnectionsNoSession(TestCase):
    """Test views from connections.py file with no user session.
    """

    pass


class ConnectionsSession(TestCase):
    """Test views from connections.py file with user session.
    """

    pass


class LoginNoSession(TestCase):
    """Test views from login.py file with no user session.
    """

    def setUp(self):
        """Used to setup common properties between tests in this class.
        """

        self.user = {
            'user': USERS['ADMIN']['USER'],
            'password': USERS['ADMIN']['PASSWORD']
        }

        self.assertIsNone(get_client_omnidb_session(p_client=self.client))


    def test_get_index_user_pwd(self):
        """Test if is redirected to workspace when providing valid user and password parameters.
        """

        v_response = self.client.get(
            reverse('login'),
            {
                'user': self.user['user'],
                'pwd': self.user['password']
            },
            follow=True
        )

        self.assertEquals(v_response.status_code, 200)
        self.assertIn('OmniDB_app/workspace.html', [v_template.name for v_template in v_response.templates])
        self.assertEquals(len(v_response.redirect_chain), 1)
        self.assertEquals(v_response.redirect_chain[0][0], reverse('workspace'))
        self.assertEquals(v_response.redirect_chain[0][1], 302)
        self.assertIn('omnidb_short_version', v_response.context)
        self.assertEquals(v_response.context['omnidb_short_version'], settings.OMNIDB_SHORT_VERSION)


    def test_get_index_no_user_pwd(self):
        """Test if is redirected to workspace when providing invalid user and valid password parameters.
        """

        v_response = self.client.get(
            reverse('login'),
            {
                'user': '{p_user}kkk'.format(p_user=self.user['user']),
                'pwd': self.user['password']
            },
            follow=True
        )

        self.assertEquals(v_response.status_code, 200)
        self.assertEquals(len(v_response.redirect_chain), 0)
        self.assertEquals(v_response.content, b'INVALID APP TOKEN')


    def test_get_index_user_no_pwd(self):
        """Test if is redirected to workspace when providing valid user and invalid password parameters.
        """

        v_response = self.client.get(
            reverse('login'),
            {
                'user': self.user['user'],
                'pwd': '{p_password}kkk'.format(p_password=self.user['password'])
            },
            follow=True
        )

        self.assertEquals(v_response.status_code, 200)
        self.assertEquals(len(v_response.redirect_chain), 0)
        self.assertEquals(v_response.content, b'INVALID APP TOKEN')


    def test_get_logout(self):
        """Test if receives expected message while trying to logout.
        """

        v_response = self.client.get(
            reverse('logout'),
            follow=True
        )

        self.assertEquals(v_response.status_code, 200)
        self.assertIn('OmniDB_app/login.html', [v_template.name for v_template in v_response.templates])
        self.assertEquals(len(v_response.redirect_chain), 1)
        self.assertEquals(v_response.redirect_chain[0][0], reverse('login'))
        self.assertEquals(v_response.redirect_chain[0][1], 302)
        self.assertEquals(get_session_alert_message(p_client=self.client), 'Session object was already destroyed.')


    def test_sign_in_no_user_password(self):
        """Test if sign in fails with invalid user and valid password.
        """

        v_response = self.client.post(
            reverse('sign_in'),
            build_client_ajax_request(
                p_data={
                    'p_username': '{p_user}kkk'.format(p_user=self.user['user']),
                    'p_pwd': self.user['password']
                }
            )
        )

        self.assertEquals(v_response.status_code, 200)
        v_content = get_client_ajax_response_content(p_response=v_response)
        self.assertEquals(v_content['v_data'], -1)
        self.assertFalse(v_content['v_error'])
        self.assertIsNone(get_client_omnidb_session(p_client=self.client))


    def test_sign_in_no_user_password(self):
        """Test if sign in fails with valid user and invalid password.
        """

        v_response = self.client.post(
            reverse('sign_in'),
            build_client_ajax_request(
                p_data={
                    'p_username': self.user['user'],
                    'p_pwd': '{p_password}kkk'.format(p_password=self.user['password'])
                }
            )
        )

        self.assertEquals(v_response.status_code, 200)
        v_content = get_client_ajax_response_content(p_response=v_response)
        self.assertEquals(v_content['v_data'], -1)
        self.assertFalse(v_content['v_error'])
        self.assertIsNone(get_client_omnidb_session(p_client=self.client))


    def test_sign_in_user_password(self):
        """Test if sign in succeeds with valid user and valid password.
        """

        v_response = self.client.post(
            reverse('sign_in'),
            build_client_ajax_request(
                p_data={
                    'p_username': self.user['user'],
                    'p_pwd': self.user['password']
                }
            )
        )

        self.assertEquals(v_response.status_code, 200)
        v_content = get_client_ajax_response_content(p_response=v_response)
        self.assertTrue(v_content['v_data'] >= 0)
        self.assertFalse(v_content['v_error'])
        v_omnidb_session = get_client_omnidb_session(p_client=self.client)
        self.assertIsNotNone(v_omnidb_session)

        v_omnidb_database = get_omnidb_database_connection()

        v_user_table = v_omnidb_database.v_connection.Query(
            p_sql='''
                SELECT u.user_id,
                       u.password,
                       t.theme_id,
                       t.theme_name,
                       t.theme_type,
                       u.editor_font_size,
                       (CASE WHEN u.chat_enabled IS NULL
                             THEN 1
                             ELSE u.chat_enabled
                        END
                       ) AS chat_enabled,
                       (CASE WHEN u.super_user IS NULL
                             THEN 0
                             ELSE u.super_user
                        END
                       ) AS super_user,
                       u.csv_encoding,
                       u.csv_delimiter,
                       u.interface_font_size
                FROM users u,
                     themes t
                WHERE u.theme_id = t.theme_id
                  AND u.user_name = '{p_user}'
            '''.format(
                p_user=self.user['user']
            )
        )

        self.assertEquals(len(v_user_table.Rows), 1)
        v_user_row = v_user_table.Rows[0]
        self.assertEquals(v_omnidb_session.v_user_id, v_user_row['user_id'])
        self.assertEquals(v_omnidb_session.v_user_name, self.user['user'])
        self.assertIsInstance(v_omnidb_session.v_omnidb_database, OmniDB_app.include.OmniDatabase.SQLite)
        self.assertEquals(v_omnidb_session.v_editor_theme, v_user_row['theme_name'])
        self.assertEquals(v_omnidb_session.v_theme_type, v_user_row['theme_type'])
        self.assertEquals(v_omnidb_session.v_theme_id, v_user_row['theme_id'])
        self.assertEquals(v_omnidb_session.v_editor_font_size, v_user_row['editor_font_size'])
        self.assertEquals(v_omnidb_session.v_interface_font_size, v_user_row['interface_font_size'])
        self.assertEquals(v_omnidb_session.v_enable_omnichat, int(v_user_row['chat_enabled']))
        self.assertEquals(v_omnidb_session.v_super_user, int(v_user_row['super_user']))
        self.assertIsInstance(v_omnidb_session.v_cryptor, OmniDB_app.include.Spartacus.Utils.Cryptor)
        self.assertIsInstance(v_omnidb_session.v_database_index, int)
        self.assertTrue(isinstance(v_omnidb_session.v_databases, OrderedDict) or isinstance(v_omnidb_session.v_databases, dict))
        self.assertEquals(v_omnidb_session.v_user_key, self.client.session.session_key)
        self.assertEquals(v_omnidb_session.v_csv_encoding, v_user_row['csv_encoding'])
        self.assertEquals(v_omnidb_session.v_csv_delimiter, v_user_row['csv_delimiter'])
        self.assertIsInstance(v_omnidb_session.v_tab_connections, dict)


class LoginSession(TestCase):
    """Test views from login.py file with user session.
    """

    def setUp(self):
        """Used to setup common properties between tests in this class.
        """

        self.user = {
            'user': USERS['ADMIN']['USER'],
            'password': USERS['ADMIN']['PASSWORD']
        }

        self.assertIsNone(get_client_omnidb_session(p_client=self.client))
        v_successfull, v_response = execute_client_login(p_client=self.client, p_username=self.user['user'], p_password=self.user['password'])
        self.assertTrue(v_successfull)
        self.assertIsNotNone(get_client_omnidb_session(p_client=self.client))


    def test_get_index_user_pwd(self):
        """Test if is redirected to workspace when providing valid user and password parameters.
        """

        v_response = self.client.get(
            reverse('login'),
            {
                'user': self.user['user'],
                'pwd': self.user['password']
            },
            follow=True
        )

        self.assertEquals(v_response.status_code, 200)
        self.assertIn('OmniDB_app/workspace.html', [v_template.name for v_template in v_response.templates])
        self.assertEquals(len(v_response.redirect_chain), 1)
        self.assertEquals(v_response.redirect_chain[0][0], reverse('workspace'))
        self.assertEquals(v_response.redirect_chain[0][1], 302)
        self.assertIn('omnidb_short_version', v_response.context)
        self.assertEquals(v_response.context['omnidb_short_version'], settings.OMNIDB_SHORT_VERSION)


    def test_get_index_no_user_pwd(self):
        """Test if is redirected to workspace when providing invalid user and valid password parameters.
        """

        v_response = self.client.get(
            reverse('login'),
            {
                'user': '{p_user}kkk'.format(p_user=self.user['user']),
                'pwd': self.user['password']
            },
            follow=True
        )

        self.assertEquals(v_response.status_code, 200)
        self.assertEquals(len(v_response.redirect_chain), 0)
        self.assertEquals(v_response.content, b'INVALID APP TOKEN')


    def test_get_index_user_no_pwd(self):
        """Test if is redirected to workspace when providing valid user and invalid password parameters.
        """

        v_response = self.client.get(
            reverse('login'),
            {
                'user': self.user['user'],
                'pwd': '{p_password}kkk'.format(p_password=self.user['password'])
            },
            follow=True
        )

        self.assertEquals(v_response.status_code, 200)
        self.assertEquals(len(v_response.redirect_chain), 0)
        self.assertEquals(v_response.content, b'INVALID APP TOKEN')


    def test_get_logout(self):
        """Test if receives expected response while trying to logout.
        """

        v_response = self.client.get(
            reverse('logout'),
            follow=True
        )

        self.assertEquals(v_response.status_code, 200)
        self.assertIn('OmniDB_app/login.html', [v_template.name for v_template in v_response.templates])
        self.assertEquals(len(v_response.redirect_chain), 1)
        self.assertEquals(v_response.redirect_chain[0][0], reverse('login'))
        self.assertEquals(v_response.redirect_chain[0][1], 302)
        self.assertIsNone(get_session_alert_message(p_client=self.client))
        self.assertIsNone(self.client.session['omnidb_user_key'])
        self.assertIsNone(get_client_omnidb_session(p_client=self.client))


    def test_sign_in_no_user_password(self):
        """Test if sign in fails with invalid user and valid password.
        """

        v_response = self.client.post(
            reverse('sign_in'),
            build_client_ajax_request(
                p_data={
                    'p_username': '{p_user}kkk'.format(p_user=self.user['user']),
                    'p_pwd': self.user['password']
                }
            )
        )

        self.assertEquals(v_response.status_code, 200)
        v_content = get_client_ajax_response_content(p_response=v_response)
        self.assertEquals(v_content['v_data'], -1)
        self.assertFalse(v_content['v_error'])
        self.assertIsNone(get_client_omnidb_session(p_client=self.client))


    def test_sign_in_no_user_password(self):
        """Test if sign in fails with valid user and invalid password.
        """

        v_response = self.client.post(
            reverse('sign_in'),
            build_client_ajax_request(
                p_data={
                    'p_username': self.user['user'],
                    'p_pwd': '{p_password}kkk'.format(p_password=self.user['password'])
                }
            )
        )

        self.assertEquals(v_response.status_code, 200)
        v_content = get_client_ajax_response_content(p_response=v_response)
        self.assertEquals(v_content['v_data'], -1)
        self.assertFalse(v_content['v_error'])


    def test_sign_in_user_password(self):
        """Test if sign in succeeds with valid user and valid password.
        """

        v_response = self.client.post(
            reverse('sign_in'),
            build_client_ajax_request(
                p_data={
                    'p_username': self.user['user'],
                    'p_pwd': self.user['password']
                }
            )
        )

        self.assertEquals(v_response.status_code, 200)
        v_content = get_client_ajax_response_content(p_response=v_response)
        self.assertTrue(v_content['v_data'] >= 0)
        self.assertFalse(v_content['v_error'])
        v_omnidb_session = get_client_omnidb_session(p_client=self.client)
        self.assertIsNotNone(v_omnidb_session)

        v_omnidb_database = get_omnidb_database_connection()

        v_user_table = v_omnidb_database.v_connection.Query(
            p_sql='''
                SELECT u.user_id,
                       u.password,
                       t.theme_id,
                       t.theme_name,
                       t.theme_type,
                       u.editor_font_size,
                       (CASE WHEN u.chat_enabled IS NULL
                             THEN 1
                             ELSE u.chat_enabled
                        END
                       ) AS chat_enabled,
                       (CASE WHEN u.super_user IS NULL
                             THEN 0
                             ELSE u.super_user
                        END
                       ) AS super_user,
                       u.csv_encoding,
                       u.csv_delimiter,
                       u.interface_font_size
                FROM users u,
                     themes t
                WHERE u.theme_id = t.theme_id
                  AND u.user_name = '{p_user}'
            '''.format(
                p_user=self.user['user']
            )
        )

        self.assertEquals(len(v_user_table.Rows), 1)
        v_user_row = v_user_table.Rows[0]
        self.assertEquals(v_omnidb_session.v_user_id, v_user_row['user_id'])
        self.assertEquals(v_omnidb_session.v_user_name, self.user['user'])
        self.assertIsInstance(v_omnidb_session.v_omnidb_database, OmniDB_app.include.OmniDatabase.SQLite)
        self.assertEquals(v_omnidb_session.v_editor_theme, v_user_row['theme_name'])
        self.assertEquals(v_omnidb_session.v_theme_type, v_user_row['theme_type'])
        self.assertEquals(v_omnidb_session.v_theme_id, v_user_row['theme_id'])
        self.assertEquals(v_omnidb_session.v_editor_font_size, v_user_row['editor_font_size'])
        self.assertEquals(v_omnidb_session.v_interface_font_size, v_user_row['interface_font_size'])
        self.assertEquals(v_omnidb_session.v_enable_omnichat, int(v_user_row['chat_enabled']))
        self.assertEquals(v_omnidb_session.v_super_user, int(v_user_row['super_user']))
        self.assertIsInstance(v_omnidb_session.v_cryptor, OmniDB_app.include.Spartacus.Utils.Cryptor)
        self.assertIsInstance(v_omnidb_session.v_database_index, int)
        self.assertTrue(isinstance(v_omnidb_session.v_databases, OrderedDict) or isinstance(v_omnidb_session.v_databases, dict))
        self.assertEquals(v_omnidb_session.v_user_key, self.client.session.session_key)
        self.assertEquals(v_omnidb_session.v_csv_encoding, v_user_row['csv_encoding'])
        self.assertEquals(v_omnidb_session.v_csv_delimiter, v_user_row['csv_delimiter'])
        self.assertIsInstance(v_omnidb_session.v_tab_connections, dict)
