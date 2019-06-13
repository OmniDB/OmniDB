# UAT - User Acceptance Test machines

These are machines with graphical user interface, intended to be used to test
both OmniDB app, server and plugin.


### Requirements

Download the required vagrant boxes:

```
vagrant box add debian/stretch64 --provider virtualbox
vagrant box add ubuntu/xenial64 --provider virtualbox
vagrant box add ubuntu/bionic64 --provider virtualbox
vagrant box add centos/6 --provider virtualbox
vagrant box add centos/7 --provider virtualbox
vagrant box add generic/rhel7 --provider virtualbox
```

Type `vagrant box list` to check if you have them all.


### Change VirtualBox default folder for VMs

If you want to build all machines inside an external storage, for example, you
can open VirtualBox, go to Preferences and then point the default folder for
VMs to somewhere else.


### Building the machines

Inside each folder of the `uat` folder:

```
vagrant up
```


### Restarting the machines

Inside each folder of the `uat` folder:

```
vagrant halt
vagrant up
```


### Logging into the machines

After building each machine and restarting, you will be prompted into the
graphical environment, asking for an user and password. On all machines, user
will be `vagrant` and password will also be `vagrant`.


### Installing OmniDB from repositories

Inside each machine, you can install OmniDB repository once, and then upgrade
to every new release in an easy way.

Debian / Ubuntu machines, as `root` user:

```
apt install apt-transport-https dirmngr
echo "deb https://dl.bintray.com/wind39/omnidb-deb debian main" > /etc/apt/sources.list.d/omnidb.list
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61
apt update

apt install omnidb-app        # for the app; or
apt install omnidb-server     # for the server; or
apt install omnidb-plugin     # for the plugin
```

CentOS 7 / RedHat 7 machines, as `root` user:

```
cat > /etc/yum.repos.d/omnidb.repo <<EOF
[omnidb]
name=omnidb
baseurl=https://dl.bintray.com/wind39/omnidb-rpm
gpgcheck=0
repo_gpgcheck=0
enabled=1
EOF

yum install omnidb-app        # for the app; or
yum install omnidb-server     # for the server; or
yum install omnidb-plugin     # for the plugin
```


### Installing OmniDB manually

CentOS 6 machines, as `root` user:

```
wget https://omnidb.org/dist/X.YY.Z/omnidb-server_X.YY.Z-centos6-amd64.rpm
rpm -ivU https://omnidb.org/dist/X.YY.Z/omnidb-server_X.YY.Z-centos6-amd64.rpm
```


### Upgrading OmniDB (when installed from repo)

Having OmniDB repository installed, upgrading OmniDB is easy:

Debian / Ubuntu machines, as `root` user:

```
apt update
apt upgrade
```

CentOS / RedHat machines, as `root` user:

```
yum update
```

Note that the commands above will also upgrade other packages in the system. If
you want to upgrade OmniDB only, then you can do as follows:

Debian / Ubuntu machines, as `root` user:

```
apt install omnidb-app        # for the app; or
apt install omnidb-server     # for the server; or
apt install omnidb-plugin     # for the plugin
```

CentOS / Fedora machines, as `root` user:

```
yum update omnidb-app        # for the app; or
yum update omnidb-server     # for the server; or
yum update omnidb-plugin     # for the plugin
```


### Destroying the machines

Inside each folder of the `uat` folder:

```
vagrant destroy
```
