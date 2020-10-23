Vagrant.configure("2") do |config|
  #config.vbguest.auto_update = false
  config.vm.define "xlgtm" do |xlgtm|
    xlgtm.vm.box = "debian/stretch64"
    xlgtm.vm.hostname = 'xlgtm'
    xlgtm.vm.network :private_network, ip: '10.33.1.114'
    xlgtm.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--name", "xlgtm"]
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    end
    xlgtm.vm.provision "shell", preserve_order: true, path: "install.sh"
    xlgtm.vm.provision "shell", preserve_order: true, path: "init.sh", args: "gtm"
    xlgtm.vm.provision "shell", preserve_order: true, path: "start.sh", args: "gtm", run: "always"
  end
  config.vm.define "xlcoord" do |xlcoord|
    xlcoord.vm.box = "debian/stretch64"
    xlcoord.vm.hostname = 'xlcoord'
    xlcoord.vm.network :private_network, ip: '10.33.1.115'
    xlcoord.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--name", "xlcoord"]
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    end
    xlcoord.vm.provision "shell", preserve_order: true, path: "install.sh"
    xlcoord.vm.provision "shell", preserve_order: true, path: "init.sh", args: "coordinator 40100 10.33.1.114 10.33.1.0/24"
    xlcoord.vm.provision "shell", preserve_order: true, path: "start.sh", args: "coordinator", run: "always"
  end
  config.vm.define "xldata1" do |xldata1|
    xldata1.vm.box = "debian/stretch64"
    xldata1.vm.hostname = 'xldata1'
    xldata1.vm.network :private_network, ip: '10.33.1.116'
    xldata1.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--name", "xldata1"]
      v.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    end
    xldata1.vm.provision "shell", preserve_order: true, path: "install.sh"
    xldata1.vm.provision "shell", preserve_order: true, path: "init.sh", args: "datanode 40101 10.33.1.114 10.33.1.0/24"
    xldata1.vm.provision "shell", preserve_order: true, path: "start.sh", args: "datanode", run: "always"
  end
  config.vm.define "xldata2" do |xldata2|
    xldata2.vm.box = "debian/stretch64"
    xldata2.vm.hostname = 'xldata2'
    xldata2.vm.network :private_network, ip: '10.33.1.117'
    xldata2.vm.provider :virtualbox do |v|
      v.customize ["modifyvm", :id, "--name", "xldata2"]
      v.customize ["modifyvm", :id, "--natdnshostresolver2", "on"]
    end
    xldata2.vm.provision "shell", preserve_order: true, path: "install.sh"
    xldata2.vm.provision "shell", preserve_order: true, path: "init.sh", args: "datanode 40102 10.33.1.114 10.33.1.0/24"
    xldata2.vm.provision "shell", preserve_order: true, path: "start.sh", args: "datanode", run: "always"
  end
end
