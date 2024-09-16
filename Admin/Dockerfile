FROM debian:stable-slim
WORKDIR /elasticdt

RUN apt-get update && apt-get upgrade -y apt && apt-get install -y wget less

# Get cypher-shell for Neo4j
RUN wget https://dist.neo4j.org/cypher-shell/cypher-shell_5.13.0_all.deb \
 && apt-get install -y ./cypher-shell_5.13.0_all.deb

# Get MySQL
RUN apt-get install -y mycli

# Get influxdb and copy to /usr/local/bin
RUN wget https://download.influxdata.com/influxdb/releases/influxdb2-client-2.7.5-linux-amd64.tar.gz \
 && tar xvzf ./influxdb2-client-2.7.5-linux-amd64.tar.gz ./influx \
 && install -o root -g root -m 0755 influx /usr/local/bin/influx \
 && rm ./influxdb2-client-2.7.5-linux-amd64.tar.gz

# Install kubectl, note we don't have to configure anything to use kubectl from inside the cluster
RUN wget "https://dl.k8s.io/release/v1.31.0/bin/linux/amd64/kubectl" \
 && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
RUN wget https://github.com/kubecolor/kubecolor/releases/download/v0.4.0/kubecolor_0.4.0_linux_amd64.tar.gz \
&& tar xvzf ./kubecolor_0.4.0_linux_amd64.tar.gz kubecolor \
 && install -o root -g root -m 0755 kubecolor /usr/local/bin/kubecolor

###### END INSTALLATIONS #####


# Create the influx config.
# The token can be set later using `influx config set -n elasticdt -t <token>`.
RUN influx config create \
  -n elasticdt \
  -u http://ds-influxdb.elasticdt:8086 \
  -o camdt \
  --active

# Copy bashrc script
COPY root.bashrc /root/.bashrc
COPY splash.sh /elasticdt/splash.sh

# Keep the container alive
CMD ["sleep", "infinity"]