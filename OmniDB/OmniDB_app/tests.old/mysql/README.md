#### Requirements

Download MySQL 8 base image:

```
docker pull mysql:8
```

For more information about MySQL official docker images, please check here:

https://hub.docker.com/_/mysql


#### Starting the container

To test OmniDB, start a container from the test image, and a shell into the container:

```
docker run -it --rm -p 3306:3306 -e MYSQL_ROOT_PASSWORD=omnidb -e MYSQL_DATABASE=omnidb_tests -e MYSQL_USER=omnidb -e MYSQL_PASSWORD=omnidb mysql:8 --bind-address=0.0.0.0
```


#### Running the tests

To run the tests, outside of the container, execute:

```
cd OmniDB/OmniDB/
python manage.py test OmniDB_app.tests.test_mysql
```


#### Destroying the container

Because you used `--rm` above, the container will be destroyed once it is stopped.

First you need to list the containers:

```
docker container ls
```

Then you can remove with:

```
docker container rm <container_id>
```
