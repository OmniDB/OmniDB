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
cp dist/omnidb-config/omnidb-config dist/omnidb-server/
cp dist/omnidb-config/omnidb-config dist/omnidb-app/
mv dist/omnidb-server omnidb-build
mv dist/omnidb-app omnidb-build
rm -rf dist
echo "Done."

echo -n "Copying cefpython files... "
cp -r "/usr/local/lib/python$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1).$(python3 --version | cut -d' ' -f2 | cut -d'.' -f2)/dist-packages/cefpython3" omnidb-build/omnidb-app/
echo "Done."

echo -n "Copying libgconf... "
cp /usr/lib/x86_64-linux-gnu/libgconf-2.so.4 omnidb-build/omnidb-app/libgconf-2.so.4
chmod 755 omnidb-build/omnidb-app/libgconf-2.so.4
cp /usr/lib/x86_64-linux-gnu/libgconf-2.so.4 omnidb-build/omnidb-app/cefpython3/libgconf-2.so.4
chmod 755 omnidb-build/omnidb-app/cefpython3/libgconf-2.so.4
echo "Done."

echo -n "Renaming bundles... "
mv omnidb-build/omnidb-server omnidb-build/omnidb-server-64bits_$VERSION
mv omnidb-build/omnidb-app omnidb-build/omnidb-app-64bits_$VERSION
echo "Done."

echo "Generating zip packages... "
cd omnidb-build
tar -czvf omnidb-server-64bits_$VERSION.tar.gz omnidb-server-64bits_$VERSION
tar -czvf omnidb-app-64bits_$VERSION.tar.gz omnidb-app-64bits_$VERSION
cd ..
echo "Done"

