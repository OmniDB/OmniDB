# Tests with PostgreSQL

There are vagrant scripts to automatically:

- Create a Debian 9 VM
- Install the specific version of PostgreSQL into the VM
- Restore tests/database/dellstore2-normal-1.0.sql into the specific version of PostgreSQL

Make sure you have the following installed in your computer:

- VirtualBox
- vagrant
- vagrant plugin vbguest

So, choose a specific version of PostgreSQL to run the tests, and then:

- cd into the folder tests/vagrant/postgresql-xx
- vagrant up
- ./restore.sh
- cd ../../../../
- python manage.py test OmniDB_app.tests.test_postgresqlxx

When you are done with the tests, you can run:

- cd OmniDB_app/tests/vagrant/postgresql-xx/
- vagrant halt


# Tests with Selenium (automating use of browsers)

- Put file OmniDB_app/tests/webdrivers/geckodriver in your PATH
- Run python manage.py test OmniDB_app.tests.test_selenium
