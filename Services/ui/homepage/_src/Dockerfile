# Use an official Python runtime as a parent image
FROM python:3.9-slim

LABEL org.opencontainers.image.source=https://github.com/cam-digital-hospitals/ElasticDT

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install CherryPy
RUN pip3 install cherrypy

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Run the CherryPy web server
CMD ["python3", "webserver.py"]
