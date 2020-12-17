mkdir release
curl https://dl.nwjs.io/v0.49.0/nwjs-v0.49.0-win-ia32.zip -o app.zip
unzip app.zip -d release
rm app.zip
mv release/nwjs-v0.49.0-win-ia32 release/OmniDB
mv release/OmniDB/nw.exe release/OmniDB/omnidb-app.exe
cp ../app/index.html release/OmniDB
cp ../app/package.json release/OmniDB
cp ../app/omnidb_icon.png release/OmniDB
../../../../AppData/Local/Programs/Python/Python36-32/Scripts/pyinstaller.exe ../../OmniDB/omnidb-win.spec
mv dist/omnidb-server release/OmniDB
#../../../../../../Arquivos\ de\ Programas/Resource\ Hacker/ResourceHacker.exe -open release/OmniDB/omnidb-app.exe -save release/OmniDB/omnidb-app.exe -action addoverwrite -res ../win-icon.ico -mask ICONGROUP,IDR_MAINFRAME,
#../../../../../../Arquivos\ de\ Programas/Resource\ Hacker/ResourceHacker.exe -open release/OmniDB/omnidb-server/omnidb-server.exe -save release/OmniDB/omnidb-server/omnidb-server.exe -action addoverwrite -res ../win-icon.ico -mask ICONGROUP,IDR_MAINFRAME,
rm -rf build
rm -rf dist
