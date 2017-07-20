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
