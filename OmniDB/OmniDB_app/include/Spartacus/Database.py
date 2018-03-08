'''
The MIT License (MIT)

Copyright (c) 2014-2018 William Ivanski

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

from collections import OrderedDict
from abc import ABC, abstractmethod
import datetime
import prettytable
import math

import OmniDB_app.include.Spartacus as Spartacus

class Exception(Exception):
    pass

class DataTable(object):
    def __init__(self, p_name=None):
        self.Name = p_name
        self.Columns = []
        self.Rows = []
    def AddColumn(self, p_columnname):
        self.Columns.append(p_columnname)
    def AddRow(self, p_row, p_simple=False):
        if len(self.Columns) > 0 and len(p_row) > 0:
            if len(self.Columns) == len(p_row):
                v_rowtmp = OrderedDict(zip(self.Columns, tuple(p_row)))
                if p_simple:
                    v_row = []
                    for c in self.Columns:
                        v_row.append(v_rowtmp[c])
                else:
                    v_row = v_rowtmp
                self.Rows.append(v_row)
            else:
                raise Spartacus.Database.Exception('Can not add row to a table with different columns.')
        else:
            raise Spartacus.Database.Exception('Can not add row to a table with no columns.')
    def Select(self, p_key, p_value):
        try:
            v_table = Spartacus.Database.DataTable()
            for c in self.Columns:
                v_table.Columns.append(c)
            for r in self.Rows:
                if r[p_key] == p_value:
                    v_table.Rows.append(r)
            return v_table
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Merge(self, p_datatable):
        if len(self.Columns) > 0 and len(p_datatable.Columns) > 0:
            if self.Columns == p_datatable.Columns:
                for r in p_datatable.Rows:
                    self.Rows.append(r)
            else:
                raise Spartacus.Database.Exception('Can not merge tables with different columns.')
        else:
            raise Spartacus.Database.Exception('Can not merge tables with no columns.')
    def Compare(self, p_datatable, p_pkcols, p_statuscolname, p_diffcolname, p_keepequal=False):
        if len(self.Columns) > 0 and len(p_datatable.Columns) > 0:
            if self.Columns == p_datatable.Columns:
                v_table = DataTable()
                for c in self.Columns:
                    v_table.Columns.append(c)
                v_table.Columns.append(p_statuscolname)
                v_table.Columns.append(p_diffcolname)
                for r1 in self.Rows:
                    v_pkmatch = False
                    for r2 in p_datatable.Rows:
                        v_pkmatch = True
                        for pkcol in p_pkcols:
                            if r1[pkcol] != r2[pkcol]:
                                v_pkmatch = False
                                break
                        if v_pkmatch:
                            break;
                    if v_pkmatch:
                        v_allmatch = True
                        v_row = []
                        v_diff = []
                        for c in self.Columns:
                            if r1[c] != r2[c]:
                                v_row.append('{0} --> {1}'.format(r1[c], r2[c]))
                                v_diff.append(c)
                                v_allmatch = False
                            else:
                                v_row.append(r1[c])
                        if v_allmatch:
                            v_row.append('E')
                            v_row.append('')
                            if p_keepequal:
                                v_table.AddRow(v_row)
                        else:
                            v_row.append('U')
                            v_row.append(','.join(v_diff))
                            v_table.AddRow(v_row)
                    else:
                        v_row = []
                        for c in self.Columns:
                            v_row.append(r1[c])
                        v_row.append('D')
                        v_row.append('')
                        v_table.AddRow(v_row)
                for r2 in p_datatable.Rows:
                    v_pkmatch = False
                    for r1 in self.Rows:
                        v_pkmatch = True
                        for pkcol in p_pkcols:
                            if r1[pkcol] != r2[pkcol]:
                                v_pkmatch = False
                                break
                        if v_pkmatch:
                            break
                    if not v_pkmatch:
                        v_row = []
                        for c in p_datatable.Columns:
                            v_row.append(r2[c])
                        v_row.append('I')
                        v_row.append('')
                        v_table.AddRow(v_row)
                return v_table
            else:
                raise Spartacus.Database.Exception('Can not compare tables with different columns.')
        else:
            raise Spartacus.Database.Exception('Can not compare tables with no columns.')
    def Pretty(self, p_transpose=False):
        if p_transpose:
            v_maxc = 0
            for c in self.Columns:
                if len(c) > v_maxc:
                    v_maxc = len(c)
            if v_maxc < (14 + len(str(len(self.Rows)))):
                v_maxc = (14 + len(str(len(self.Rows))))
            else:
                v_maxc = v_maxc + 1
            k = 0
            s = 0
            v_maxf = 0
            for r in self.Rows:
                for c in self.Columns:
                    for v_snippet in str(r[c]).split('\n'):
                        k = k + 1
                        s = s + len(v_snippet)
                        if len(str(r[c])) > v_maxf:
                            v_maxf = len(v_snippet)
            if v_maxf > 30:
                v_maxf = int(s / k) + int((v_maxf - int(s / k)) / 2)
            v_maxf = v_maxf + 10
            v_string = ''
            v_row = 1
            for r in self.Rows:
                v_aux = '-[ RECORD {0} ]'.format(v_row)
                for k in range(len(v_aux), v_maxc):
                    v_aux = v_aux + '-'
                v_string = v_string + v_aux + '+'
                for k in range(0, v_maxf):
                    v_string = v_string + '-'
                v_string = v_string + '\n'
                for c in self.Columns:
                    v_first = True
                    for v_snippet in str(r[c]).split('\n'):
                        n = math.ceil(len(v_snippet) / (v_maxf-2))
                        j = 0
                        for i in range(0, n):
                            if v_first:
                                x = c.ljust(v_maxc)
                                v_first = False
                            else:
                                x = ' '.ljust(v_maxc)
                            if i < n-1:
                                y = ' ' + v_snippet[j:j+v_maxf-2] + '+'
                                j = j + v_maxf-2
                            else:
                                y = ' ' + v_snippet[j:]
                            v_string = v_string + '{0}|{1}\n'.format(x, y)
                v_row = v_row + 1
            return v_string
        else:
            v_pretty = prettytable.PrettyTable()
            v_pretty._set_field_names(self.Columns)
            for r in self.Rows:
                v_row = []
                for c in self.Columns:
                    v_row.append(r[c])
                v_pretty.add_row(v_row)
            return v_pretty.get_string()
    def Transpose(self, p_column1, p_column2):
        if len(self.Rows) == 1:
            v_table = Spartacus.Database.DataTable()
            v_table.AddColumn(p_column1)
            v_table.AddColumn(p_column2)
            for k in range(len(self.Columns)):
                v_table.AddRow([self.Columns[k], self.Rows[0][k]])
            return v_table
        else:
            raise Spartacus.Database.Exception('Can only transpose a table with a single row.')

class DataField(object):
    def __init__(self, p_name, p_type=None, p_dbtype=None, p_mask='#'):
        self.v_name = p_name
        self.v_truename = p_name
        self.v_type = p_type
        self.v_dbtype = p_dbtype
        self.v_mask = p_mask

class DataTransferReturn(object):
    def __init__(self):
        self.v_numrecords = 0
        self.v_log = None

class DataList(object):
    def __init__(self):
        self.v_list = []
    def append(self, p_item):
        self.v_list.append(p_item)

v_supported_rdbms = []
try:
    import sqlite3
    v_supported_rdbms.append('SQLite')
    v_supported_rdbms.append('Memory')
except ImportError:
    pass
try:
    import psycopg2
    from psycopg2 import extras
    from pgspecial.main import PGSpecial
    from pgspecial.namedqueries import NamedQueries
    v_supported_rdbms.append('PostgreSQL')
except ImportError:
    pass
try:
    import pymysql
    v_supported_rdbms.append('MySQL')
    v_supported_rdbms.append('MariaDB')
except ImportError:
    pass
try:
    import fdb
    v_supported_rdbms.append('Firebird')
except ImportError:
    pass
try:
    import cx_Oracle
    v_supported_rdbms.append('Oracle')
except ImportError:
    pass
try:
    import pymssql
    v_supported_rdbms.append('MSSQL')
except ImportError:
    pass
try:
    import ibm_db
    import ibm_db_dbi
    v_supported_rdbms.append('IBMDB2')
except ImportError:
    pass

'''
------------------------------------------------------------------------
Generic
------------------------------------------------------------------------
'''
class Generic(ABC):
    @abstractmethod
    def GetConnectionString(self):
        pass
    @abstractmethod
    def Open(self, p_autocommit=True):
        pass
    @abstractmethod
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        pass
    @abstractmethod
    def Execute(self, p_sql):
        pass
    @abstractmethod
    def ExecuteScalar(self, p_sql):
        pass
    @abstractmethod
    def Close(self):
        pass
    @abstractmethod
    def Cancel(self):
        pass
    @abstractmethod
    def GetPID(self):
        pass
    @abstractmethod
    def Terminate(self, p_pid):
        pass
    @abstractmethod
    def GetFields(self, p_sql):
        pass
    @abstractmethod
    def GetNotices(self):
        pass
    @abstractmethod
    def ClearNotices(self):
        pass
    @abstractmethod
    def GetStatus(self):
        pass
    @abstractmethod
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        pass
    @abstractmethod
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        pass
    @abstractmethod
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        pass
    @abstractmethod
    def Special(self, p_sql):
        pass
    @classmethod
    def Mogrify(self, p_row, p_fields):
        if len(p_row) == len(p_fields):
            k = 0
            v_mog = []
            while k < len(p_row):
                v_value = p_row[p_fields[k].v_name]
                if type(v_value) == type(None):
                    v_mog.append('null')
                elif type(v_value) == type(str()):
                    v_mog.append(p_fields[k].v_mask.replace('#', "'{0}'".format(v_value.replace("'", "''"))))
                elif type(v_value) == datetime.datetime:
                    v_mog.append(p_fields[k].v_mask.replace('#', "'{0}'".format(v_value)))
                else:
                    v_mog.append(p_fields[k].v_mask.replace('#', "{0}".format(v_value)))
                k = k + 1
            return '(' + ','.join(v_mog) + ')'
        else:
            raise Spartacus.Database.Exception('Can not mogrify with different number of parameters.')

'''
------------------------------------------------------------------------
SQLite
------------------------------------------------------------------------
'''
class SQLite(Generic):
    def __init__(self, p_service, p_foreignkeys=True, p_timeout=30):
        if 'SQLite' in v_supported_rdbms:
            self.v_host = None
            self.v_port = None
            self.v_service = p_service
            self.v_user = None
            self.v_password = None
            self.v_con = None
            self.v_cur = None
            self.v_foreignkeys = p_foreignkeys
            self.v_timeout = p_timeout
        else:
            raise Spartacus.Database.Exception("SQLite is not supported. Please install it.")
    def GetConnectionString(self):
        return None
    def Open(self, p_autocommit=True):
        try:
            if p_autocommit:
                self.v_con = sqlite3.connect(self.v_service, self.v_timeout, isolation_level=None)
            else:
                self.v_con = sqlite3.connect(self.v_service, self.v_timeout)

            #self.v_con.row_factory = sqlite3.Row
            self.v_cur = self.v_con.cursor()
            if self.v_foreignkeys:
                self.v_cur.execute('PRAGMA foreign_keys = ON')
            self.v_start = True
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_row = list(v_row)
                    if p_alltypesstr:
                        for j in range(0, len(v_table.Columns)):
                            if v_row[j] != None:
                                v_row[j] = str(v_row[j])
                            else:
                                v_row[j] = ''
                    v_table.AddRow(v_row, p_simple)
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        return None
    def Terminate(self, p_pid):
        pass
    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute('select * from ( ' + p_sql + ' ) t limit 1')
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=type(None)))
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def GetNotices(self):
        return []
    def ClearNotices(self):
        pass
    def GetStatus(self):
        return None
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                            k = k + 1
                    else:
                        while v_row is not None:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_insert = 'begin; '
            for r in p_block.Rows:
                v_insert = v_insert + 'insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + self.Mogrify(r, v_fields) + '; '
            v_insert = v_insert + 'commit;'
            self.Execute(v_insert)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()

'''
------------------------------------------------------------------------
Memory
------------------------------------------------------------------------
'''
class Memory(Generic):
    def __init__(self, p_foreignkeys=True, p_timeout=30):
        if 'Memory' in v_supported_rdbms:
            self.v_host = None
            self.v_port = None
            self.v_service = ':memory:'
            self.v_user = None
            self.v_password = None
            self.v_con = None
            self.v_cur = None
            self.v_foreignkeys = p_foreignkeys
            self.v_timeout = p_timeout
        else:
            raise Spartacus.Database.Exception("SQLite is not supported. Please install it.")
    def GetConnectionString(self):
        return None
    def Open(self, p_autocommit=True):
        try:
            self.v_con = sqlite3.connect(self.v_service, self.v_timeout)
            #self.v_con.row_factory = sqlite3.Row
            self.v_cur = self.v_con.cursor()
            if self.v_foreignkeys:
                self.v_cur.execute('PRAGMA foreign_keys = ON')
            self.v_start = True
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    v_row = self.v_cur.fetchone()
                    while v_row is not None:
                        v_row = list(v_row)
                        if p_alltypesstr:
                            for j in range(0, len(v_table.Columns)):
                                if v_row[j] != None:
                                    v_row[j] = str(v_row[j])
                                else:
                                    v_row[j] = ''
                        v_table.AddRow(v_row, p_simple)
                        v_row = self.v_cur.fetchone()
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Execute(self, p_sql):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def ExecuteScalar(self, p_sql):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                self.v_cur.execute(p_sql)
                r = self.v_cur.fetchone()
                if r != None:
                    s = r[0]
                else:
                    s = None
                return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        return None
    def Terminate(self, p_pid):
        pass
    def GetFields(self, p_sql):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                v_fields = []
                self.v_cur.execute('select * from ( ' + p_sql + ' ) t limit 1')
                r = self.v_cur.fetchone()
                if r != None:
                    k = 0
                    for c in self.v_cur.description:
                        v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                        k = k + 1
                else:
                    k = 0
                    for c in self.v_cur.description:
                        v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=type(None)))
                        k = k + 1
                return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetNotices(self):
        return []
    def ClearNotices(self):
        pass
    def GetStatus(self):
        return None
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                            k = k + 1
                    else:
                        while v_row is not None:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_insert = 'begin; '
            for r in p_block.Rows:
                v_insert = v_insert + 'insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + self.Mogrify(r, v_fields) + '; '
            v_insert = v_insert + 'commit;'
            self.Execute(v_insert)
        except Spartacus.Database.Exception as exc:
            raise exc
        except sqlite3.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()

'''
------------------------------------------------------------------------
PostgreSQL
------------------------------------------------------------------------
'''
class PostgreSQL(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password):
        if 'PostgreSQL' in v_supported_rdbms:
            self.v_host = p_host
            if p_port is None or p_port == '':
                self.v_port = 5432
            else:
                self.v_port = p_port
            if p_service is None or p_service == '':
                self.v_service = 'postgres'
            else:
                self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
            self.v_special = PGSpecial()
            self.v_help = Spartacus.Database.DataTable()
            self.v_help.Columns = ['Command', 'Syntax', 'Description']
            self.v_help.AddRow(['\\?', '\\?', 'Show Commands.'])
            self.v_help.AddRow(['\\h', '\\h', 'Show SQL syntax and help.'])
            self.v_help.AddRow(['\\list', '\\list', 'List databases.'])
            self.v_help.AddRow(['\\l', '\\l[+] [pattern]', 'List databases.'])
            self.v_help.AddRow(['\\du', '\\du[+] [pattern]', 'List roles.'])
            self.v_help.AddRow(['\\dx', '\\dx[+] [pattern]', 'List extensions.'])
            self.v_help.AddRow(['\\db', '\\db[+] [pattern]', 'List tablespaces.'])
            self.v_help.AddRow(['\\dn', '\\dn[+] [pattern]', 'List schemas.'])
            self.v_help.AddRow(['\\dt', '\\dt[+] [pattern]', 'List tables.'])
            self.v_help.AddRow(['\\dv', '\\dv[+] [pattern]', 'List views.'])
            self.v_help.AddRow(['\\ds', '\\ds[+] [pattern]', 'List sequences.'])
            self.v_help.AddRow(['\\d', '\\d[+] [pattern]', 'List or describe tables, views and sequences.'])
            self.v_help.AddRow(['DESCRIBE', 'DESCRIBE [pattern]', 'Describe tables, views and sequences.'])
            self.v_help.AddRow(['describe', 'DESCRIBE [pattern]', 'Describe tables, views and sequences.'])
            self.v_help.AddRow(['\\di', '\\di[+] [pattern]', 'List indexes.'])
            self.v_help.AddRow(['\\dm', '\\dm[+] [pattern]', 'List materialized views.'])
            self.v_help.AddRow(['\\df', '\\df[+] [pattern]', 'List functions.'])
            self.v_help.AddRow(['\\sf', '\\sf[+] FUNCNAME', "Show a function's definition."])
            self.v_help.AddRow(['\\dT', '\\dT[+] [pattern]', 'List data types.'])
            self.v_help.AddRow(['\\x', '\\x', 'Toggle expanded output.'])
            self.v_help.AddRow(['\\timing', '\\timing', 'Toggle timing of commands.'])
            self.v_expanded = False
            self.v_timing = False
            psycopg2.extras.register_default_json(loads=lambda x: x)
            psycopg2.extras.register_default_jsonb(loads=lambda x: x)
        else:
            raise Spartacus.Database.Exception("PostgreSQL is not supported. Please install it with 'pip install Spartacus[postgresql]'.")
    def GetConnectionString(self):
        if self.v_host is None or self.v_host == '':
            if self.v_password is None or self.v_password == '':
                return "port={0} dbname='{1}' user='{2}'".format(
                    self.v_port,
                    self.v_service,
                    self.v_user
                )
            else:
                return "port={0} dbname='{1}' user='{2}' password='{3}'".format(
                    self.v_port,
                    self.v_service,
                    self.v_user,
                    self.v_password
                )
        else:
            return "host='{0}' port={1} dbname='{2}' user='{3}' password='{4}'".format(
                self.v_host,
                self.v_port,
                self.v_service,
                self.v_user,
                self.v_password
            )
    def Open(self, p_autocommit=True):
        try:
            self.v_con = psycopg2.connect(
                self.GetConnectionString(),
                cursor_factory=psycopg2.extras.DictCursor
            )
            self.v_con.autocommit = p_autocommit
            self.v_cur = self.v_con.cursor()
            self.v_start = True
            # PostgreSQL types
            self.v_cur.execute('select oid, typname from pg_type')
            self.v_types = dict([(r['oid'], r['typname']) for r in self.v_cur.fetchall()])
            if not p_autocommit:
                self.v_con.commit()
            self.v_con.notices = DataList()
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                if p_alltypesstr:
                    for i in range(0, len(v_table.Rows)):
                        for j in range(0, len(v_table.Columns)):
                            if v_table.Rows[i][j] != None:
                                v_table.Rows[i][j] = str(v_table.Rows[i][j])
                            else:
                                v_table.Rows[i][j] = ''
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                return self.v_con.get_backend_pid()
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Terminate(self, p_pid):
        try:
            self.Execute('select pg_terminate_backend({0})'.format(p_pid))
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute('select * from ( ' + p_sql + ' ) t limit 1')
            r = self.v_cur.fetchone()
            v_sql = 'select '
            v_first = True
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=self.v_types[c[1]]))
                    if v_first:
                        v_sql = v_sql + "quote_ident('{0}')".format(c[0])
                        v_first = False
                    else:
                        v_sql = v_sql + ",quote_ident('{0}')".format(c[0])
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=self.v_types[c[1]]))
                    if v_first:
                        v_sql = v_sql + "quote_ident('{0}')".format(c[0])
                        v_first = False
                    else:
                        v_sql = v_sql + ",quote_ident('{0}')".format(c[0])
                    k = k + 1
            self.v_cur.execute(v_sql)
            r = self.v_cur.fetchone()
            for k in range(0, len(self.v_cur.description)):
                v_fields[k].v_truename = r[k]
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def GetNotices(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                return self.v_con.notices.v_list
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def ClearNotices(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                del self.v_con.notices.v_list[:]
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetStatus(self):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                return self.v_cur.statusmessage
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    if p_blocksize > 0:
                        v_table.Rows = self.v_cur.fetchmany(p_blocksize)
                    else:
                        v_table.Rows = self.v_cur.fetchall()
                    if p_alltypesstr:
                        for i in range(0, len(v_table.Rows)):
                            for j in range(0, len(v_table.Columns)):
                                if v_table.Rows[i][j] != None:
                                    v_table.Rows[i][j] = str(v_table.Rows[i][j])
                                else:
                                    v_table.Rows[i][j] = ''
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute('insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + ','.join(v_values) + '')
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_command = p_sql.lstrip().split(' ')[0].rstrip('+')
            v_title = None
            v_table = None
            v_status = None
            if v_command == '\\?':
                v_table = self.v_help
            else:
                v_aux = self.v_help.Select('Command', v_command)
                if len(v_aux.Rows) > 0:
                    for r in self.v_special.execute(self.v_cur, p_sql):
                        v_result = r
                    if v_result[0]:
                        v_title = v_result[0]
                    if v_result[1]:
                        v_table = DataTable()
                        v_table.Columns = v_result[2]
                        if isinstance(v_result[1], type(self.v_cur)):
                            if v_result[1].description:
                                v_table.Rows = v_result[1].fetchall()
                        else:
                            for r in v_result[1]:
                                v_table.AddRow(r)
                    if v_result[3]:
                        v_status = v_result[3]
                        if v_status.strip() == 'Expanded display is on.':
                            self.v_expanded = True
                        elif v_status.strip() == 'Expanded display is off.':
                            self.v_expanded = False
                        elif v_status.strip() == 'Timing is on.':
                            self.v_timing = True
                        elif v_status.strip() == 'Timing is off.':
                            self.v_timing = False
                else:
                    if self.v_timing:
                        v_timestart = datetime.datetime.now()
                    v_table = self.Query(p_sql)
                    v_status = self.GetStatus()
                    if self.v_timing:
                        v_status = v_status + '\nTime: {0}'.format(datetime.datetime.now() - v_timestart)

            if v_title and v_table and len(v_table.Rows) > 0 and v_status:
                return v_title + '\n' + v_table.Pretty(self.v_expanded) + '\n' + v_status
            elif v_title and v_table and len(v_table.Rows) > 0:
                return v_title + '\n' + v_table.Pretty(self.v_expanded)
            elif v_title and v_status:
                return v_title + '\n' + v_status
            elif v_title:
                return v_title
            elif v_table and len(v_table.Rows) > 0 and v_status:
                return v_table.Pretty(self.v_expanded) + '\n' + v_status
            elif v_table and len(v_table.Rows) > 0:
                return v_table.Pretty(self.v_expanded)
            elif v_status:
                return v_status
            else:
                return ''
        except Spartacus.Database.Exception as exc:
            raise exc
        except psycopg2.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()


'''
------------------------------------------------------------------------
MySQL
------------------------------------------------------------------------
'''
class MySQL(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password):
        if 'MySQL' in v_supported_rdbms:
            self.v_host = p_host
            self.v_port = p_port
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
        else:
            raise Spartacus.Database.Exception("MySQL is not supported. Please install it with 'pip install Spartacus[mysql]'.")
    def GetConnectionString(self):
        return None
    def Open(self, p_autocommit=True):
        try:
            self.v_con = pymysql.connect(
                host=self.v_host,
                port=int(self.v_port),
                db=self.v_service,
                user=self.v_user,
                password=self.v_password,
                cursorclass=pymysql.cursors.DictCursor)
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                if p_alltypesstr:
                    for i in range(0, len(v_table.Rows)):
                        for j in range(0, len(v_table.Columns)):
                            if v_table.Rows[i][j] != None:
                                v_table.Rows[i][j] = str(v_table.Rows[i][j])
                            else:
                                v_table.Rows[i][j] = ''
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        return None
    def Terminate(self, p_pid):
        pass
    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute('select * from ( ' + p_sql + ' ) t limit 1')
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=type(None)))
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def GetNotices(self):
        return []
    def ClearNotices(self):
        pass
    def GetStatus(self):
        return None
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    if p_blocksize > 0:
                        v_table.Rows = self.v_cur.fetchmany(p_blocksize)
                    else:
                        v_table.Rows = self.v_cur.fetchall()
                    if p_alltypesstr:
                        for i in range(0, len(v_table.Rows)):
                            for j in range(0, len(v_table.Columns)):
                                if v_table.Rows[i][j] != None:
                                    v_table.Rows[i][j] = str(v_table.Rows[i][j])
                                else:
                                    v_table.Rows[i][j] = ''
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute('insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + ','.join(v_values) + '')
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()

'''
------------------------------------------------------------------------
MariaDB
------------------------------------------------------------------------
'''
class MariaDB(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password):
        if 'MariaDB' in v_supported_rdbms:
            self.v_host = p_host
            self.v_port = p_port
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
        else:
            raise Spartacus.Database.Exception("MariaDB is not supported. Please install it with 'pip install Spartacus[mariadb]'.")
    def GetConnectionString(self):
        return None
    def Open(self, p_autocommit=True):
        try:
            self.v_con = pymysql.connect(
                host=self.v_host,
                port=int(self.v_port),
                db=self.v_service,
                user=self.v_user,
                password=self.v_password,
                cursorclass=pymysql.cursors.DictCursor)
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_table.Rows = self.v_cur.fetchall()
                if p_alltypesstr:
                    for i in range(0, len(v_table.Rows)):
                        for j in range(0, len(v_table.Columns)):
                            if v_table.Rows[i][j] != None:
                                v_table.Rows[i][j] = str(v_table.Rows[i][j])
                            else:
                                v_table.Rows[i][j] = ''
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        return None
    def Terminate(self, p_pid):
        pass
    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute('select * from ( ' + p_sql + ' ) t limit 1')
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=type(None)))
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def GetNotices(self):
        return []
    def ClearNotices(self):
        pass
    def GetStatus(self):
        return None
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    if p_blocksize > 0:
                        v_table.Rows = self.v_cur.fetchmany(p_blocksize)
                    else:
                        v_table.Rows = self.v_cur.fetchall()
                    if p_alltypesstr:
                        for i in range(0, len(v_table.Rows)):
                            for j in range(0, len(v_table.Columns)):
                                if v_table.Rows[i][j] != None:
                                    v_table.Rows[i][j] = str(v_table.Rows[i][j])
                                else:
                                    v_table.Rows[i][j] = ''
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute('insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + ','.join(v_values) + '')
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymysql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()

'''
------------------------------------------------------------------------
Firebird
------------------------------------------------------------------------
'''
class Firebird(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password):
        if 'Firebird' in v_supported_rdbms:
            self.v_host = p_host
            self.v_port = p_port
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
        else:
            raise Spartacus.Database.Exception("Firebird is not supported. Please install it with 'pip install Spartacus[firebird]'.")
    def GetConnectionString(self):
        return None
    def Open(self, p_autocommit=True):
        try:
            self.v_con = fdb.connect(
                host=self.v_host,
                port=int(self.v_port),
                database=self.v_service,
                user=self.v_user,
                password=self.v_password)
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_row = list(v_row)
                    if p_alltypesstr:
                        for j in range(0, len(v_table.Columns)):
                            if v_row[j] != None:
                                v_row[j] = str(v_row[j])
                            else:
                                v_row[j] = ''
                    v_table.AddRow(v_row, p_simple)
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        return None
    def Terminate(self, p_pid):
        pass
    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute('select first 1 * from ( ' + p_sql + ' )')
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=type(None)))
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def GetNotices(self):
        return []
    def ClearNotices(self):
        pass
    def GetStatus(self):
        return None
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                            k = k + 1
                    else:
                        while v_row is not None:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute('insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + ','.join(v_values) + '')
        except Spartacus.Database.Exception as exc:
            raise exc
        except fdb.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()

'''
------------------------------------------------------------------------
Oracle
------------------------------------------------------------------------
'''
class Oracle(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password):
        if 'Oracle' in v_supported_rdbms:
            self.v_host = p_host
            if p_port is None or p_port == '':
                self.v_port = 1521
            else:
                self.v_port = p_port
            if p_service is None or p_service == '':
                self.v_service = 'xe'
            else:
                self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
        else:
            raise Spartacus.Database.Exception("Oracle is not supported. Please install it with 'pip install Spartacus[oracle]'.")
    def GetConnectionString(self):
        return '{0}/{1}@{2}:{3}/{4}'.format(
            self.v_user,
            self.v_password,
            self.v_host,
            self.v_port,
            self.v_service
        )
    def Open(self, p_autocommit=True):
        try:
            self.v_con = cx_Oracle.connect(self.GetConnectionString())
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))

    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_row = list(v_row)
                    if p_alltypesstr:
                        for j in range(0, len(v_table.Columns)):
                            if v_row[j] != None:
                                v_row[j] = str(v_row[j])
                            else:
                                v_row[j] = ''
                    v_table.AddRow(v_row, p_simple)
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        return None
    def Terminate(self, p_pid):
        try:
            self.Execute("alter system kill session '{0}' immediate".format(p_pid))
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute('select * from ( ' + p_sql + ' ) t where rownum <= 1')
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=c[1].__name__))
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=c[1].__name__))
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def GetNotices(self):
        return []
    def ClearNotices(self):
        pass
    def GetStatus(self):
        return None
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                            k = k + 1
                    else:
                        while v_row is not None:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute('insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + ','.join(v_values) + '')
        except Spartacus.Database.Exception as exc:
            raise exc
        except cx_Oracle.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()
'''
------------------------------------------------------------------------
MSSQL
------------------------------------------------------------------------
'''
class MSSQL(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password):
        if 'MSSQL' in v_supported_rdbms:
            self.v_host = p_host
            self.v_port = p_port
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
        else:
            raise Spartacus.Database.Exception("MSSQL is not supported. Please install it with 'pip install Spartacus[mssql]'.")
    def GetConnectionString(self):
        return None
    def Open(self, p_autocommit=True):
        try:
            self.v_con = pymssql.connect(
                host=self.v_host,
                port=int(self.v_port),
                database=self.v_service,
                user=self.v_user,
                password=self.v_password
            )
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_row = list(v_row)
                    if p_alltypesstr:
                        for j in range(0, len(v_table.Columns)):
                            if v_row[j] != None:
                                v_row[j] = str(v_row[j])
                            else:
                                v_row[j] = ''
                    v_table.AddRow(v_row, p_simple)
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        return None
    def Terminate(self, p_pid):
        pass
    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute('select top 1 limit_alias.* from ( ' + p_sql + ' ) limit_alias')
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=type(None)))
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def GetNotices(self):
        return []
    def ClearNotices(self):
        pass
    def GetStatus(self):
        return None
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                            k = k + 1
                    else:
                        while v_row is not None:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute('insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + ','.join(v_values) + '')
        except Spartacus.Database.Exception as exc:
            raise exc
        except pymssql.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()

'''
------------------------------------------------------------------------
IBM DB2
------------------------------------------------------------------------
'''
class IBMDB2(Generic):
    def __init__(self, p_host, p_port, p_service, p_user, p_password):
        if 'IBMDB2' in v_supported_rdbms:
            self.v_host = p_host
            self.v_port = p_port
            self.v_service = p_service
            self.v_user = p_user
            self.v_password = p_password
            self.v_con = None
            self.v_cur = None
        else:
            raise Spartacus.Database.Exception("IBM DB2 is not supported. Please install it with 'pip install Spartacus[ibmdb2]'.")
    def GetConnectionString(self):
        return 'DATABASE={0};HOSTNAME={1};PORT={2};PROTOCOL=TCPIP;UID={3};PWD={4}'.format(
            self.v_service,
            self.v_host,
            self.v_port,
            self.v_user,
            self.v_password
        )
    def Open(self, p_autocommit=True):
        try:
            c = ibm_db.connect(self.GetConnectionString(), '', '')
            self.v_con = ibm_db_dbi.Connection(c)
            self.v_cur = self.v_con.cursor()
            self.v_start = True
        except ibm_db.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Query(self, p_sql, p_alltypesstr=False, p_simple=False):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            v_table = DataTable()
            if self.v_cur.description:
                for c in self.v_cur.description:
                    v_table.Columns.append(c[0])
                v_row = self.v_cur.fetchone()
                while v_row is not None:
                    v_row = list(v_row)
                    if p_alltypesstr:
                        for j in range(0, len(v_table.Columns)):
                            if v_row[j] != None:
                                v_row[j] = str(v_row[j])
                            else:
                                v_row[j] = ''
                    v_table.AddRow(v_row, p_simple)
                    v_row = self.v_cur.fetchone()
            return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Execute(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def ExecuteScalar(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            self.v_cur.execute(p_sql)
            r = self.v_cur.fetchone()
            if r != None:
                s = r[0]
            else:
                s = None
            return s
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def Close(self):
        try:
            if self.v_con:
                self.v_con.commit()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Cancel(self):
        try:
            if self.v_con:
                self.v_con.cancel()
                if self.v_cur:
                    self.v_cur.close()
                    self.v_cur = None
                self.v_con.close()
                self.v_con = None
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def GetPID(self):
        return None
    def Terminate(self, p_pid):
        pass
    def GetFields(self, p_sql):
        try:
            v_keep = None
            if self.v_con is None:
                self.Open()
                v_keep = False
            else:
                v_keep = True
            v_fields = []
            self.v_cur.execute('select * from ( ' + p_sql + ' ) t limit 1')
            r = self.v_cur.fetchone()
            if r != None:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(r[k]), p_dbtype=type(r[k])))
                    k = k + 1
            else:
                k = 0
                for c in self.v_cur.description:
                    v_fields.append(DataField(c[0], p_type=type(None), p_dbtype=type(None)))
                    k = k + 1
            return v_fields
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        finally:
            if not v_keep:
                self.Close()
    def GetNotices(self):
        return []
    def ClearNotices(self):
        pass
    def GetStatus(self):
        return None
    def QueryBlock(self, p_sql, p_blocksize, p_alltypesstr=False, p_simple=False):
        try:
            if self.v_con is None:
                raise Spartacus.Database.Exception('This method should be called in the middle of Open() and Close() calls.')
            else:
                if self.v_start:
                    self.v_cur.execute(p_sql)
                v_table = DataTable()
                if self.v_cur.description:
                    for c in self.v_cur.description:
                        v_table.Columns.append(c[0])
                    v_row = self.v_cur.fetchone()
                    if p_blocksize > 0:
                        k = 0
                        while v_row is not None and k < p_blocksize:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                            k = k + 1
                    else:
                        while v_row is not None:
                            v_row = list(v_row)
                            if p_alltypesstr:
                                for j in range(0, len(v_table.Columns)):
                                    if v_row[j] != None:
                                        v_row[j] = str(v_row[j])
                                    else:
                                        v_row[j] = ''
                            v_table.AddRow(v_row, p_simple)
                            v_row = self.v_cur.fetchone()
                if self.v_start:
                    self.v_start = False
                return v_table
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def InsertBlock(self, p_block, p_tablename, p_fields=None):
        try:
            v_columnames = []
            if p_fields is None:
                v_fields = []
                for c in p_block.Columns:
                    v_columnames.append(c)
                    v_fields.append(DataField(c))
            else:
                v_fields = p_fields
                for p in v_fields:
                    v_columnames.append(p.v_name)
            v_values = []
            for r in p_block.Rows:
                v_values.append(self.Mogrify(r, v_fields))
            self.Execute('insert into ' + p_tablename + '(' + ','.join(v_columnames) + ') values ' + ','.join(v_values) + '')
        except Spartacus.Database.Exception as exc:
            raise exc
        except ibm_db_dbi.Error as exc:
            raise Spartacus.Database.Exception(str(exc))
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
    def Transfer(self, p_sql, p_targetdatabase, p_tablename, p_blocksize, p_fields=None, p_alltypesstr=False):
        v_return = DataTransferReturn()
        try:
            v_table = self.QueryBlock(p_sql, p_blocksize, p_alltypesstr)
            if len(v_table.Rows) > 0:
                p_targetdatabase.InsertBlock(v_table, p_tablename, p_fields)
            v_return.v_numrecords = len(v_table.Rows)
        except Spartacus.Database.Exception as exc:
            v_return.v_log = str(exc)
        except Exception as exc:
            raise Spartacus.Database.Exception(str(exc))
        return v_return
    def Special(self, p_sql):
        return self.Query(p_sql).Pretty()
