FROM python:3.5-alpine

# Environment stuff
ENV OMNIDB_HOME /app
ENV OMNIDB_PORT 8000


# Copy the project
RUN mkdir $OMNIDB_HOME && \
    apk --update add build-base \
                     postgresql-dev
COPY . $OMNIDB_HOME/ 
WORKDIR $OMNIDB_HOME/OmniDB

# Install deppendencies
RUN pip3 install -r ../requirements.txt  && \
    pip3 install -r ../requirements.txt  && \
    apk del build-base \
            postgresql-dev

# Start server
EXPOSE $OMNIDB_PORT
ENTRYPOINT ["python3"]
# ENTRYPOINT ["sh"]
CMD ["manage.py", "runserver"]
# 