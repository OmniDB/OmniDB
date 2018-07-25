# -*- mode: python -*-

block_cipher = None

data_files_app = [
  ('db.sqlite3','.'),
  ('omnidb.conf','.'),
  ('OmniDB_app/static','OmniDB_app/static'),
  ('OmniDB_app/include','OmniDB_app/include'),
  ('OmniDB_app/templates','OmniDB_app/templates'),
  ('OmniDB_app/plugins','OmniDB_app/plugins'),
  ('OmniDB/migrations','OmniDB/migrations')
]
data_files_server = [
  ('db.sqlite3','.'),
  ('omnidb.conf','.'),
  ('OmniDB_app/static','OmniDB_app/static'),
  ('OmniDB_app/include','OmniDB_app/include'),
  ('OmniDB_app/templates','OmniDB_app/templates'),
  ('OmniDB_app/plugins','OmniDB_app/plugins'),
  ('OmniDB/migrations','OmniDB/migrations'),
]

b = Analysis(['omnidb-server.py'],
             binaries=[],
             datas=data_files_server,
             hiddenimports=['cheroot.ssl','cheroot.ssl.builtin'],
             pathex=['C:/OmniDB/OmniDB-dev/OmniDB/OmniDB_app/include/'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz_b = PYZ(b.pure, b.zipped_data,
             cipher=block_cipher)
exe_b = EXE(pyz_b,
          b.scripts,
          exclude_binaries=True,
          name='omnidb-server',
          debug=False,
          strip=False,
          upx=True,
          console=True,
          icon='deploy/win-icon.ico' )
coll_b = COLLECT(exe_b,
               b.binaries,
               b.zipfiles,
               b.datas,
               strip=False,
               upx=True,
               name='omnidb-server')

c = Analysis(['omnidb-config.py'],
            binaries=[],
            datas=[],
            hiddenimports=[],
            hookspath=[],
            runtime_hooks=[],
            excludes=[],
            win_no_prefer_redirects=False,
            win_private_assemblies=False,
            cipher=block_cipher)
pyz_c = PYZ(c.pure, c.zipped_data,
            cipher=block_cipher)
exe_c = EXE(pyz_c,
         c.scripts,
         exclude_binaries=True,
         name='omnidb-config',
         debug=False,
         strip=False,
         upx=True,
         console=True,
         icon='deploy/win-icon.ico' )
coll_c = COLLECT(exe_c,
              c.binaries,
              c.zipfiles,
              c.datas,
              strip=False,
              upx=True,
              name='omnidb-config')
