## Deployment

### Cloud Scheduler

Cloud scheduler deployment was done using console UI.

### Storage
Buckets creation was done using console UI. 

region selected for this was us-central1

### cloud run

Before deploying into cloud run you must login into the cloud sdk CLI using

```
gcloud init
```

Then create a Dockerfile in the root app folder

```
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
```

Run the command 

```
gcloud run deploy
```
when the cloud sdk ask for app name keep the default option twice,  then select the region, us-central1.

This will deploy the code automatically in cloud run.

If this is the first time you do this, some other API services permission will be required to perform this.