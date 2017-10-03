'''
The MIT License (MIT)

Copyright (c) 2017 William Ivanski

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

import pyscrypt
import pyaes
import base64
import os
import csv
import openpyxl
from collections import OrderedDict

import OmniDB_app.include.Spartacus as Spartacus

class Exception(Exception):
    pass

class Cryptor(object):
    def __init__(self, p_key, p_encoding='utf-8'):
        try:
            self.v_encoding = p_encoding
            self.v_hash = pyscrypt.hash(
                password = p_key.encode('utf-8'),
                salt = '0123456789ABCDEF'.encode('utf-8'),
                N = 1024,
                r = 1,
                p = 1,
                dkLen = 32
            )
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))
    def Encrypt(self, p_plaintext):
        try:
            v_aes = pyaes.AESModeOfOperationCTR(self.v_hash)
            return base64.b64encode(v_aes.encrypt(p_plaintext)).decode(self.v_encoding)
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))
    def Decrypt(self, p_cyphertext):
        try:
            v_aes = pyaes.AESModeOfOperationCTR(self.v_hash)
            return v_aes.decrypt(base64.b64decode(p_cyphertext)).decode(self.v_encoding)
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))

class DataFileReader(object):
    def __init__(self, p_filename, p_fieldnames=None):
        v_tmp = p_filename.split('.')
        if len(v_tmp) > 1:
            self.v_extension = v_tmp[-1].lower()
        else:
            self.v_extension = 'csv'
        self.v_filename = p_filename
        self.v_file = None
        self.v_header = p_fieldnames
    def Open(self):
        try:
            if not os.path.isfile(self.v_filename):
                raise Spartacus.Utils.Exception('File {0} does not exist or is not a file.'.format(self.v_filename))
            if self.v_extension == 'csv':
                self.v_file = open(self.v_filename)
                v_sample = self.v_file.read(1024)
                self.v_file.seek(0)
                v_sniffer = csv.Sniffer()
                if not v_sniffer.has_header(v_sample):
                    raise Spartacus.Utils.Exception('CSV file {0} does not have a header.'.format(self.v_filename))
                v_dialect = v_sniffer.sniff(v_sample)
                self.v_object = csv.DictReader(self.v_file, self.v_header, None, None, v_dialect)
            elif self.v_extension == 'xlsx':
                self.v_object = openpyxl.load_workbook(self.v_filename)
            else:
                raise Spartacus.Utils.Exception('File extension "{0}" not supported.'.format(self.v_extension))
        except Spartacus.Utils.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))
    def Read(self, p_blocksize=None, p_sheetname=None):
        try:
            if self.v_extension == 'csv':
                v_table = Spartacus.Database.DataTable()
                v_first = True
                x = 0
                for v_row in self.v_object:
                    if v_first:
                        if self.v_header:
                            v_table.Columns = self.v_header
                        else:
                            for k in v_row.keys():
                                v_table.Columns.append(k)
                        v_first = False
                    v_table.Rows.append(v_row)
                    x = x + 1
                    if x == p_blocksize:
                        yield v_table
                        x = 0
                        v_table.Rows = []
                self.v_file.close()
                if len(v_table.Rows) > 0:
                    yield v_table
            else:
                if p_sheetname:
                    v_worksheet = self.v_object[p_sheetname]
                    v_table = Spartacus.Database.DataTable(v_sheetname)
                else:
                    v_worksheet = self.v_object.active
                    v_table = Spartacus.Database.DataTable()
                v_first = True
                x = 0
                for v_row in tuple(v_worksheet.rows):
                    if v_first:
                        if self.v_header:
                            v_table.Columns = self.v_header
                        else:
                            for i in range(0, len(tuple(v_worksheet.columns))):
                                v_table.Columns.append(v_row[i].value)
                        v_first = False
                    else:
                        v_table.Rows.append(OrderedDict(zip(v_table.Columns, [a.value for a in v_row])))
                        x = x + 1
                        if x == p_blocksize:
                            yield v_table
                            x = 0
                            v_table.Rows = []
                if len(v_table.Rows) > 0:
                    yield v_table
        except Spartacus.Utils.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))
    def Sheets(self):
        try:
            if self.v_extension == 'xlsx' and self.v_object:
                return self.v_object.get_sheet_names()
            else:
                return []
        except Spartacus.Utils.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))

class DataFileWriter(object):
    def __init__(self, p_filename, p_fieldnames=None):
        v_tmp = p_filename.split('.')
        if len(v_tmp) > 1:
            self.v_extension = v_tmp[-1].lower()
        else:
            self.v_extension = 'csv'
        self.v_filename = p_filename
        self.v_file = None
        self.v_header = p_fieldnames
        self.v_currentrow = 1
    def Open(self):
        try:
            if self.v_extension == 'csv':
                self.v_file = open(self.v_filename, 'w')
                self.v_object = csv.DictWriter(v_file, fieldnames=self.v_header)
                self.v_object.writeheader()
            elif self.v_extension == 'xlsx':
                self.v_object = openpyxl.Workbook()
            else:
                raise Spartacus.Utils.Exception('File extension "{0}" not supported.'.format(self.v_extension))
        except Spartacus.Utils.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))
    def Write(self, p_datatable, p_sheetname=None):
        try:
            if self.v_extension == 'csv':
                for v_row in p_datatable.Rows:
                    self.v_object.writerow(dict(v_row))
            else:
                if p_sheetname:
                    v_worksheet = self.v_object.create_sheet(p_sheetname)
                else:
                    v_worksheet = self.v_object.active
                if self.v_currentrow == 1:
                    for c in range(0, len(p_datatable.Columns)):
                        v_worksheet['{0}1'.format(self.__colstr__(c+1))] = p_datatable.Columns[c]
                    self.v_currentrow = self.v_currentrow + 1
                for r in range(0, len(p_datatable.Rows)):
                    for c in range(0, len(p_datatable.Columns)):
                        v_worksheet['{0}{1}'.format(self.__colstr__(c+1), r+self.v_currentrow)] = p_datatable.Rows[r][p_datatable.Columns[c]]
                self.v_currentrow = self.v_currentrow + len(p_datatable.Rows)
        except Spartacus.Utils.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))
    def Flush(self):
        try:
            if self.v_extension == 'csv':
                self.v_file.close()
            else:
                self.v_object.save(self.v_filename)
        except Spartacus.Utils.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))
    def __colstr__(self, p_index):
        v_div = p_index
        v_text = ''
        v_tmp = 0
        while v_div > 0:
            v_mod = (v_div - 1) % 26
            v_text = chr(65 + v_mod) + v_text
            v_div = int((v_div - v_mod) / 26)
        return v_text
