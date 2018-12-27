# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
echo "I am provisioning..."
apt-get update
wget -q https://omnidb.org/dist/2.14.0/omnidb-server_2.14.0-debian-amd64.deb
dpkg -i omnidb-server_2.14.0-debian-amd64.deb
cat > /etc/systemd/system/omnidb.service << EOF
[Unit]
After=network.target

[Service]
Type=forking
ExecStart=/bin/bash -c "/opt/omnidb-server/omnidb-server &"
RemainAfterExit=yes

[Install]
WantedBy=default.target
EOF
chmod 664 /etc/systemd/system/omnidb.service
systemctl daemon-reload
systemctl enable omnidb.service
systemctl start omnidb.service
date > /etc/vagrant_provisioned_at
echo "OmniDB is running on localhost:8000"
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: $script
  config.vm.box = "debian/stretch64"
  config.vm.box_url = "https://app.vagrantup.com/debian/boxes/stretch64"
  config.vm.host_name = "omnidb"
  config.vm.provider :virtualbox do |vb|
    vb.name = "omnidb"
  end
  config.vm.network "forwarded_port", guest: 8000, host: 8000
end
