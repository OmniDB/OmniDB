FROM centos:7

RUN  yum -y install wget \
  && yum clean all

RUN mkdir /app
WORKDIR /app

RUN  wget https://omnidb.org/dist/2.12.0/omnidb-server_2.12.0-centos7-amd64.rpm \
  && rpm -Uvh /app/omnidb-server_2.12.0-centos7-amd64.rpm \
  && rm -rf omnidb-server_2.12.0-centos7-amd64.rpm

EXPOSE 8000
EXPOSE 25482

CMD  omnidb-server -H 0.0.0.0 -p 8000
