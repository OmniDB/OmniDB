mkdir release
mkdir release/omnidb-app
unzip app.zip -d release/omnidb-app
cp ../app/index.html release/omnidb-app
cp ../app/package.json release/omnidb-app
../../../../AppData/Local/Programs/Python/Python36-32/Scripts/pyinstaller.exe ../../OmniDB/omnidb-win.spec
cp -R dist/omnidb-server release/omnidb-app
mv dist/omnidb-server release
rm -rf build
rm -rf dist
