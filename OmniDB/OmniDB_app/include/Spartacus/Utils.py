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

class DataFile(object):
    def __init__(self):
        self.v_set = []
    def Load(self, p_filename, p_fieldnames=None):
        try:
            if not os.path.isfile(p_filename):
                raise Spartacus.Utils.Exception('File {0} does not exist or is not a file.'.format(p_filename))
            v_tmp = p_filename.split('.')
            if len(v_tmp) > 1:
                v_filename = ['.'.join(v_tmp[:-1]), v_tmp[-1].lower()]
            else:
                v_filename = [v_tmp[0], 'csv']
            if v_filename[1] == 'csv':
                with open(p_filename) as v_file:
                    v_sample = v_file.read(1024)
                    v_file.seek(0)
                    v_sniffer = csv.Sniffer()
                    if not v_sniffer.has_header(v_sample):
                        raise Spartacus.Utils.Exception('CSV file {0} does not have a header.'.format(p_filename))
                    v_dialect = v_sniffer.sniff(v_sample)
                    v_reader = csv.DictReader(v_file, p_fieldnames, None, None, v_dialect)
                    v_table = Spartacus.Database.DataTable(v_filename[0])
                    v_first = True
                    for v_row in v_reader:
                        if v_first:
                            if p_fieldnames:
                                v_table.Columns = p_fieldnames
                            else:
                                for k in v_row.keys():
                                    v_table.Columns.append(k)
                            v_first = False
                        v_table.Rows.append(v_row)
                    self.v_set.append(v_table)
            elif v_filename[1] == 'xlsx':
                v_file = openpyxl.load_workbook(p_filename)
                for v_sheetname in v_file.get_sheet_names():
                    v_worksheet = v_file[v_sheetname]
                    v_table = Spartacus.Database.DataTable(v_sheetname)
                    v_first = True
                    for v_row in tuple(v_worksheet.rows):
                        if v_first:
                            if p_fieldnames:
                                v_table.Columns = p_fieldnames
                            else:
                                for i in range(0, len(tuple(v_worksheet.columns))):
                                    v_table.Columns.append(v_row[i].value)
                            v_first = False
                        else:
                            v_table.Rows.append(OrderedDict(zip(v_table.Columns, [a.value for a in v_row])))
                    self.v_set.append(v_table)
            else:
                raise Spartacus.Utils.Exception('File extension "{0}" not supported.'.format(v_filename[1]))
        except Spartacus.Utils.Exception as exc:
            raise exc
        except Exception as exc:
            raise Spartacus.Utils.Exception(str(exc))
    def Save(self, p_filename, p_datatable=None):
        try:
            if p_datatable:
                v_localset = [p_datatable]
            else:
                v_localset = self.v_set
            v_tmp = p_filename.split('.')
            if len(v_tmp) > 1:
                v_filename = ['.'.join(v_tmp[:-1]), v_tmp[-1].lower()]
            else:
                v_filename = [v_tmp[0], 'csv']
            if v_filename[1] == 'csv':
                k = 0
                for v_table in v_localset:
                    if len(v_localset) > 1:
                        v_tmp = '{0}_{1}.csv'.format(v_filename[0], str(k).zfill(len(str(len(v_localset)))))
                    else:
                        v_tmp = p_filename
                    with open(v_tmp, 'w') as v_file:
                        v_writer = csv.DictWriter(v_file, fieldnames=v_table.Columns)
                        v_writer.writeheader()
                        for v_row in v_table.Rows:
                            v_writer.writerow(dict(v_row))
                    k = k + 1
            elif v_filename[1] == 'xlsx':
                v_file = openpyxl.Workbook()
                k = 0
                for v_table in v_localset:
                    if k == 0:
                        v_worksheet = v_file.active
                        if v_table.Name:
                            v_worksheet.title = v_table.Name
                    else:
                        if v_table.Name:
                            v_worksheet = v_file.create_sheet(v_table.Name)
                        else:
                            v_worksheet = v_file.create_sheet('Sheet{0}'.format(k))
                    for c in range(0, len(v_table.Columns)):
                        v_worksheet['{0}1'.format(self.__colstr__(c+1))] = v_table.Columns[c]
                    for r in range(0, len(v_table.Rows)):
                        for c in range(0, len(v_table.Columns)):
                            v_worksheet['{0}{1}'.format(self.__colstr__(c+1), r+2)] = v_table.Rows[r][v_table.Columns[c]]
                    k = k + 1
                v_file.save(p_filename)
            else:
                raise Spartacus.Utils.Exception('File extension "{0}" not supported.'.format(v_filename[1]))
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
