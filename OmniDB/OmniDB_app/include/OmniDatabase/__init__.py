'''
The MIT License (MIT)

Portions Copyright (c) 2015-2018, The OmniDB Team
Portions Copyright (c) 2017-2018, 2ndQuadrant Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from OmniDB_app.include.OmniDatabase.SQLite import SQLite
from OmniDB_app.include.OmniDatabase.PostgreSQL import PostgreSQL
from OmniDB_app.include.OmniDatabase.Oracle import Oracle
from OmniDB_app.include.OmniDatabase.MariaDB import MariaDB
from OmniDB_app.include.OmniDatabase.MySQL import MySQL

'''
------------------------------------------------------------------------
Generic
------------------------------------------------------------------------
'''
class Generic(object):
    @staticmethod
    def InstantiateDatabase(p_db_type,
                            p_server,
                            p_port,
                            p_service,
                            p_user,
                            p_password,
                            p_conn_id=0,
                            p_alias='',
                            p_foreignkeys=True,
                            p_application_name='OmniDB',
                            p_conn_string='',
                            p_parse_conn_string = False):

        if p_db_type == 'postgresql':
            return PostgreSQL(p_server, p_port, p_service, p_user, p_password, p_conn_id, p_alias, p_application_name, p_conn_string, p_parse_conn_string)
        if p_db_type == 'oracle':
            return Oracle(p_server, p_port, p_service, p_user, p_password, p_conn_id, p_alias, p_conn_string, p_parse_conn_string)
        if p_db_type == 'mariadb':
            return MariaDB(p_server, p_port, p_service, p_user, p_password, p_conn_id, p_alias, p_conn_string, p_parse_conn_string)
        if p_db_type == 'mysql':
            return MySQL(p_server, p_port, p_service, p_user, p_password, p_conn_id, p_alias, p_conn_string, p_parse_conn_string)
        if p_db_type == 'sqlite':
            return SQLite(p_service, p_conn_id, p_alias, p_foreignkeys)
