## Introduction

This creates a Postgres-XL 9.5 cluster with 4 nodes:

- xlgtm: 10.33.1.114
- xlcoord: 10.33.1.115
- xldata1: 10.33.1.116
- xldata2: 10.33.1.117

You can replace the IP address in the `Vagranfile` if you want.


## Create the VMs

```
vagrant up
```

It will take a long while. In my machine it takes around 1h. After it is done:

```
vagrant ssh xlcoord -c '/vagrant/setup.sh 10.33.1.115 10.33.1.116 10.33.1.117'
vagrant ssh xldata1 -c '/vagrant/setup.sh 10.33.1.115 10.33.1.116 10.33.1.117'
vagrant ssh xldata2 -c '/vagrant/setup.sh 10.33.1.115 10.33.1.116 10.33.1.117'
```


## Access the cluster

Best way is to first SSH to the coordinator, then become postgres:

```
vagrant ssh xlcoord
sudo su
su postgres
cd
psql
```

But you can do it in a single command too:

```
vagrant ssh xlcoord -c 'sudo su - postgres -c /usr/local/pgsql/bin/psql'
```

Or remotely, if you have defined a password for the postgres user:

```
psql -h 10.33.1.115 -U postgres
```


## Restarting the VMs

You can shutdown the VMs with:

```
vagrant halt
```

And then start them with:

```
vagrant up
```

And vagrant will start the cluster for you.
