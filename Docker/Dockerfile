FROM ubuntu:16.04

# install dependencies
RUN apt update -y && \
        apt install -y wget mono-xsp4 unzip

# setup omniDB
RUN mkdir -p /opt \
	&& cd /tmp \
	&& wget https://github.com/OmniDB/OmniDB/releases/download/v1.4/OmniDB-1.4.zip \
	&& unzip OmniDB-1.4.zip \
	&& cd OmniDB-1.4 \
	&& mv * /opt \
	&& cd .. \
	&& rm -rf Omni*

# clean up
RUN apt-get remove -y wget unzip \
	&& apt-get autoremove -y \
        && apt-get -y clean

COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
EXPOSE 9000
