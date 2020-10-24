from django.test import TestCase, Client
from django.http import JsonResponse
import json

class Login(TestCase):

    def test_sign_in_ok(self):
        c = Client()
        response = c.post('/sign_in/', {'data': '{"p_username": "admin", "p_pwd": "admin"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 0 <= data['v_data']
        session = c.session
        assert 'admin' == session['omnidb_session'].v_user_name

    def test_sign_in_nok(self):
        c = Client()
        response = c.post('/sign_in/', {'data': '{"p_username": "admin", "p_pwd": "ad"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_data']


class Connections(TestCase):

    def test_connections_nosession(self):
        c = Client()
        response = c.post('/connections/', follow=True)
        assert '/login/' == response.redirect_chain[0][0]
        assert 302 == response.redirect_chain[0][1]

    def test_get_connections_nosession(self):
        c = Client()
        response = c.post('/get_connections/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_save_connections_nosession(self):
        c = Client()
        response = c.post('/save_connections/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_test_connection_nosession(self):
        c = Client()
        response = c.post('/test_connection/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']


class Users(TestCase):

    def test_get_users_nosession(self):
        c = Client()
        response = c.post('/get_users/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_new_user_nosession(self):
        c = Client()
        response = c.post('/new_user/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_remove_user_nosession(self):
        c = Client()
        response = c.post('/remove_user/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_save_users_nosession(self):
        c = Client()
        response = c.post('/save_users/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']


class Workspace(TestCase):

    def test_workspace_nosession(self):
        c = Client()
        response = c.post('/workspace/', follow=True)
        assert '/login/' == response.redirect_chain[0][0]
        assert 302 == response.redirect_chain[0][1]

    def test_save_config_user_nosession(self):
        c = Client()
        response = c.post('/save_config_user/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_database_list_nosession(self):
        c = Client()
        response = c.post('/get_database_list/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_renew_password_nosession(self):
        c = Client()
        response = c.post('/renew_password/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_draw_graph_nosession(self):
        c = Client()
        response = c.post('/draw_graph/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_alter_table_data_nosession(self):
        c = Client()
        response = c.post('/alter_table_data/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_save_alter_table_nosession(self):
        c = Client()
        response = c.post('/save_alter_table/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_start_edit_data_nosession(self):
        c = Client()
        response = c.post('/start_edit_data/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_completions_nosession(self):
        c = Client()
        response = c.post('/get_completions/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_completions_table_nosession(self):
        c = Client()
        response = c.post('/get_completions_table/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_command_list_nosession(self):
        c = Client()
        response = c.post('/get_command_list/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_clear_command_list_nosession(self):
        c = Client()
        response = c.post('/clear_command_list/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']


class TreeSnippets(TestCase):

    def test_get_node_children_nosession(self):
        c = Client()
        response = c.post('/get_node_children/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_get_snippet_text_nosession(self):
        c = Client()
        response = c.post('/get_snippet_text/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_new_node_snippet_nosession(self):
        c = Client()
        response = c.post('/new_node_snippet/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_delete_node_snippet_nosession(self):
        c = Client()
        response = c.post('/delete_node_snippet/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_save_snippet_text_nosession(self):
        c = Client()
        response = c.post('/save_snippet_text/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']

    def test_rename_node_snippet_nosession(self):
        c = Client()
        response = c.post('/rename_node_snippet/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert 1 == data['v_error_id']
