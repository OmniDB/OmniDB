from django.test import TestCase, Client
from django.http import JsonResponse
import json

class PostgreSQL(TestCase):

    def test_get_tree_info_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_tree_info_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_tables_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_tables_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_schemas_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_schemas_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_columns_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_pk_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_pk_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_fks_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_fks_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_uniques_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_uniques_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_indexes_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_indexes_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_functions_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_functions_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_function_fields_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_function_fields_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_function_definition_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_function_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_sequences_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_sequences_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_views_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_views_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_views_columns_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_views_columns_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_view_definition_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_view_definition_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_databases_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_databases_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_tablespaces_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_tablespaces_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']

    def test_get_roles_postgresql_nosession(self):
        c = Client()
        response = c.post('/get_roles_postgresql/')
        assert 200 == response.status_code
        data = json.loads(response.content.decode())
        assert -1 == data['v_error_id']
