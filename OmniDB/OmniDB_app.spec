# -*- mode: python -*-

block_cipher = None

data_files = [
  ('omnidb.db','.'),
  ('db.sqlite3','.'),
  ('log','log'),
  ('OmniDB_app/static','OmniDB_app/static'),
  ('OmniDB_app/templates','OmniDB_app/templates')
]

a = Analysis(['omnidb-app.py'],
             binaries=[],
             datas=data_files,
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
          console=True )
coll_a = COLLECT(exe_a,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='omnidb-app')

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
         console=True )
coll_c = COLLECT(exe_c,
              c.binaries,
              c.zipfiles,
              c.datas,
              strip=False,
              upx=True,
              name='omnidb-config')
