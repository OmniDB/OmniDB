rm -rf release
mkdir release
cp -R ../../../OmniDB.app release
cp ../app/* release/OmniDB.app/Contents/Resources/app.nw
pyinstaller ../../OmniDB/omnidb-mac.spec
mv dist/omnidb-server release/OmniDB.app/Contents/Resources/app.nw
