from django.test import TestCase, Client
from django.http import JsonResponse
import json

class Login(TestCase):

    def test_sign_in_ok(self):
        c = Client()
        response = c.post('/sign_in/', {'data': '{"p_username": "admin", "p_pwd": "admin"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert True == data['v_data']

    def test_sign_in_nok(self):
        c = Client()
        response = c.post('/sign_in/', {'data': '{"p_username": "admin", "p_pwd": "ad"}'})
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert False == data['v_data']


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
        assert -1 == data['v_error_id']

    def test_new_connection_nosession(self):
        c = Client()
        response = c.post('/new_connection/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_remove_connection_nosession(self):
        c = Client()
        response = c.post('/remove_connection/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_save_connections_nosession(self):
        c = Client()
        response = c.post('/save_connections/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_test_connection_nosession(self):
        c = Client()
        response = c.post('/test_connection/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']


class Users(TestCase):

    def test_users_nosession(self):
        c = Client()
        response = c.post('/users/', follow=True)
        assert '/login/' == response.redirect_chain[0][0]
        assert 302 == response.redirect_chain[0][1]

    def test_get_users_nosession(self):
        c = Client()
        response = c.post('/get_users/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_new_user_nosession(self):
        c = Client()
        response = c.post('/new_user/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_remove_user_nosession(self):
        c = Client()
        response = c.post('/remove_user/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_save_users_nosession(self):
        c = Client()
        response = c.post('/save_users/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    
