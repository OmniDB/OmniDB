#!/bin/sh -e

PYTHON_VERSION=3.5.2

echo "Installing dependencies..."
yum install -y gcc gcc-c++ make git patch openssl-devel zlib-devel readline-devel sqlite-devel bzip2-devel
echo "Done"

echo "Installing pyenv..."
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
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
git clone https://github.com/OmniDB/OmniDB ~/OmniDB
cd ~/OmniDB
git checkout dev
echo "Done"

echo "Installing OmniDB dependencies..."
pip install pip --upgrade
pip install -r ~/OmniDB/requirements.txt
pip install -r ~/OmniDB/OmniDB/deploy/requirements_for_deploy_server.txt
echo "Done"

echo "Building..."
cd ~/OmniDB/OmniDB/deploy/centos_server_amd64/
./build.sh
echo "Done"
