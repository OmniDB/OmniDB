#!/bin/sh -e

PYTHON_VERSION=3.5.2

echo "Installing dependencies..."
yum install -y gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel rpm-build wget
yum groupinstall -y gnome
echo "Done"

echo "Installing p7zip..."
wget https://www.mirrorservice.org/sites/dl.fedoraproject.org/pub/epel/7/x86_64/Packages/p/p7zip-16.02-2.el7.x86_64.rpm
rpm -U --quiet p7zip-16.02-2.el7.x86_64.rpm
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

echo "Downloading OIC..."
wget https://github.com/OmniDB/OracleInstantClient/raw/master/oic/linux_x64.7z
7za x linux_x64.7z
echo "Done"

echo "Building..."
cd ~/OmniDB/OmniDB/deploy/app_fedora_amd64/
./build.sh
echo "Done"
