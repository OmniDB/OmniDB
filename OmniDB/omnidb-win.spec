# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

data_files_server = [
  ('omnidb.db','.'),
  ('config.py','.'),
  ('OmniDB_app/static','OmniDB_app/static'),
  ('OmniDB_app/include','OmniDB_app/include'),
  ('OmniDB_app/templates','OmniDB_app/templates'),
  ('OmniDB_app/plugins','OmniDB_app/plugins')
]


a = Analysis(['omnidb-server.py'],
             pathex=['C:\\Users\\omnidb\\OmniDB\\OmniDB\\OmniDB'],
             binaries=[],
             datas=data_files_server,
             hiddenimports=['cheroot.ssl','cheroot.ssl.builtin','psycopg2','paramiko'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='omnidb-server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='omnidb-server')
