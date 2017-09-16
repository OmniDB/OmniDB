FROM python:3.5

# Environment stuff
ENV OMNIDB_HOME /app
ENV OMNIDB_PORT 8000


# Copy the project
RUN mkdir $OMNIDB_HOME 
COPY . $OMNIDB_HOME/ 
WORKDIR $OMNIDB_HOME/OmniDB

# # Install deppendencies
RUN pip3 install pip --upgrade && \
    pip3 install -r ../requirements.txt
    
# Start server
EXPOSE $OMNIDB_PORT
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]