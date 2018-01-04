#!/bin/sh -e

PYTHON_VERSION=3.5.2

echo "Installing dependencies..."
zypper install -y gcc gcc-c++ make patch libopenssl-devel readline-devel libbz2-devel rpm-build libgconfmm-2_6-1 desktop-file-utils sqlite3-devel
zypper install -y gnome-shell
echo "Done"

echo "Installing pyenv..."
git clone --depth 1 https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc
echo "Done"

echo "Installing Python $PYTHON_VERSION..."
env PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install $PYTHON_VERSION
pyenv global $PYTHON_VERSION
echo "Done"

echo "Cloning OmniDB repo..."
rm -rf ~/OmniDB
git clone --depth 1 --branch dev https://github.com/OmniDB/OmniDB ~/OmniDB
echo "Done"

echo "Building..."
cd ~/OmniDB/OmniDB/deploy/app_opensuse_leap_amd64/
./build.sh
echo "Done"
