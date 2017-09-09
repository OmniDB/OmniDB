# -*- mode: python -*-

block_cipher = None

data_files_app = [
  ('omnidb.db','.'),
  ('db.sqlite3','.'),
  ('log','log'),
  ('OmniDB_app/static','OmniDB_app/static'),
  ('OmniDB_app/include','OmniDB_app/include'),
  ('OmniDB_app/templates','OmniDB_app/templates')
]
data_files_server = [
  ('omnidb.db','.'),
  ('db.sqlite3','.'),
  ('omnidb.conf','.'),
  ('log','log'),
  ('OmniDB_app/static','OmniDB_app/static'),
  ('OmniDB_app/include','OmniDB_app/include'),
  ('OmniDB_app/templates','OmniDB_app/templates')

a = Analysis(['omnidb-app.py'],
             binaries=[],
             datas=data_files_app,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz_a = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe_a = EXE(pyz_a,
          a.scripts,
          exclude_binaries=True,
          name='omnidb-app',
          debug=False,
          strip=False,
          upx=True,
          console=False,
          icon='deploy/win-icon.ico' )
coll_a = COLLECT(exe_a,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='omnidb-app')

b = Analysis(['omnidb-server.py'],
             binaries=[],
             datas=data_files_server,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz_b = PYZ(b.pure, b.zipped_data,
             cipher=block_cipher)
exe_b = EXE(pyz_a,
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
