#### Requirements

Download Oracle Linux 7 base image:

```
docker pull oraclelinux:7
```

For more information about Oracle Linux official docker images, please check here:

https://hub.docker.com/_/oraclelinux

Change into the directory:

```
cd OmniDB/OmniDB/OmniDB_app/tests/oracle/
```

Download the installation rpm file from OTN into this folder - first time only:

https://www.oracle.com/technetwork/database/database-technologies/express-edition/downloads/index.html


#### Creating the test image

Create new test image:

```
docker build -t "omnidb:tests_oracle" .
```

After that you can delete the rpm file from this folder.


#### Starting the container

To test OmniDB, start a container from the test image, and a shell into the container:

```
docker run -it --rm -p 1521:1521 omnidb:tests_oracle /bin/bash
```

Inside the container, start the Oracle instance:

```
/etc/init.d/oracle-xe-18c start
```

Because of the `--rm` above, the container will be automatically destroyed when
you exit the container shell.


#### Running the tests

To run the tests, outside of the container, execute:

```
cd OmniDB/OmniDB/
python manage.py test OmniDB_app.tests.test_oracle
```


#### Destroying the container

If you don't use `--rm` to create the container, you can destroy the container
anytime.

First you need to list the containers:

```
docker container ls
```

Then you can remove with:

```
docker container rm <container_id>
```


#### Destroying the image

You don't need to destroy the image, as it will be used for the next OmniDB
deployment.

To list all images:

```
docker images
```

You can destroy the image with:

```
docker image rm omnidb:tests_oracle
```
