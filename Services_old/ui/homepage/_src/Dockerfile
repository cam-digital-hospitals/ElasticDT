# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install the necessary Python dependencies
RUN pip3 install cherrypy

# Install kubectl to run the kubectl commands
RUN apt-get update && apt-get install -y curl \
    && curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Run the CherryPy web server
CMD ["python3", "webserver_dynamic.py"]
