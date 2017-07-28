VERSION=2.0.2

echo -n "Cleaning... "
rm -rf build
rm -rf dist
rm -rf omnidb-build
echo "Done."

echo "Generating bundles... "
pyinstaller OmniDB.spec
echo "Done."

echo -n "Organizing bundles..."
rm -rf build
mkdir omnidb-build
cp dist/omnidb-config/omnidb-config dist/omnidb-server
cp dist/omnidb-config/omnidb-config dist/omnidb-client
mv dist/omnidb-server omnidb-build
mv dist/omnidb-client omnidb-build
rm -rf dist
echo "Done."

echo -n "Copying cefpython files... "
cp -r "/usr/local/lib/python$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1).$(python3 --version | cut -d' ' -f2 | cut -d'.' -f2)/dist-packages/cefpython3" omnidb-build/omnidb-client/
echo "Done."

echo -n "Renaming bundles... "
mv omnidb-build/omnidb-server omnidb-build/omnidb-server_$VERSION
mv omnidb-build/omnidb-client omnidb-build/omnidb-client_$VERSION
echo "Done."

echo "Generating zip packages... "
cd omnidb-build
zip -r omnidb-server_$VERSION.zip omnidb-server_$VERSION
zip -r omnidb-client_$VERSION.zip omnidb-client_$VERSION
cd ..
echo "Done"

