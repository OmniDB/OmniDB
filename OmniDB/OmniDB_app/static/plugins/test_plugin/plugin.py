def test_func(p_database_object, p_data):
    result = p_database_object.v_connection.ExecuteScalar('select version()')
    return { 'version': result }
