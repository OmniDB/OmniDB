Recommended machine settings for graphical environment:

- Disk size: 80GB
- RAM size: 2048MB


Upon installation:

- Language: English
- Keyboard: us
- User: vagrant
- Password: vagrant


Inside the machine, as vagrant user:

```
mkdir .ssh
chmod 700 .ssh
cd .ssh
wget https://raw.githubusercontent.com/hashicorp/vagrant/master/keys/vagrant.pub
mv vagrant.pub authorized_keys
chmod 600 authorized_keys
```


Outside the machine, to create the box:

```
vagrant package --base <machine_name>
```
