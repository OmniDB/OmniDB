v_cryptor = Utils.Cryptor('omnidb', 'iso-8859-1')

p_database.v_connection.Open()
p_database.v_connection.Execute('BEGIN TRANSACTION;')

v_table = p_database.v_connection.Query('SELECT user_id, password FROM users')
for v_row in v_table.Rows:
    v_hashed_pwd = v_cryptor.Hash(v_row['password'])
    p_database.v_connection.Execute("UPDATE users SET password = '{0}' WHERE user_id = {1};".format(v_hashed_pwd, v_row['user_id']))

p_database.v_connection.Execute("UPDATE version SET ver_id = '2.12.1';")

p_database.v_connection.Execute('COMMIT;')
p_database.v_connection.Close()
p_database.v_connection.Execute('VACUUM;')
