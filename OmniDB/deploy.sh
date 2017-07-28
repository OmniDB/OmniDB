rm -rf build
rm -rf dist
rm -rf omnidb-build
python3 /usr/local/bin/pyinstaller OmniDB.spec
rm -rf build
mkdir omnidb-build
cp dist/omnidb-config/omnidb-config dist/omnidb-server
cp dist/omnidb-config/omnidb-config dist/omnidb-client
mv dist/omnidb-server omnidb-build
mv dist/omnidb-client omnidb-build
rm -rf dist
