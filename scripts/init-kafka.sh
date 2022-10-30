#!/usr/bin/env bash

# Set magic variables for current file, directory, os, etc.
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Present Working Dir: ${__dir}"

__parent_dir="$(dirname "${__dir}")"
echo "Parent Dir: ${__parent_dir}"

__kafka_docker_dir="${__parent_dir}/kafka-setup"
echo "Kafka Docker Compose Dir: ${__kafka_docker_dir}"

#################
### functions ###
#################

## params: <container_name>
function fnGetContainerState() {
  echo "$(docker ps --filter status=running --filter name=${1} --format "{{.State}}")"
}

############
### main ###
############

cd ${__kafka_docker_dir}

broker_status="$(fnGetContainerState broker)"
zookeeper_status="$(fnGetContainerState zookeeper)"

if [[ "${broker_status}" == "running" && "${zookeeper_status}" == "running" ]]
then
  echo "All containers already running. Skip docker-compose up."
else
  echo "All containers not in running state. Try recreating with docker-compose up."
  # Run Kafka containers 
  docker compose up -d

  echo "Wait for 30 Seconds for the containers to be ready"
  # Add delay of 30 seconds for the containers to be ready. This can be handled more intelligently but keeping it simple for now.
  sleep 30

  broker_status="$(fnGetContainerState broker)"
  zookeeper_status="$(fnGetContainerState zookeeper)"
fi

echo "broker_status: ${broker_status:-NA}"
echo "zookeeper_status: ${zookeeper_status:-NA}"

# Create topics
docker compose exec broker \
  kafka-topics --create \
    --topic input_topic \
    --if-not-exists \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1

docker compose exec broker \
  kafka-topics --create \
    --topic output_topic \
    --if-not-exists \
    --bootstrap-server localhost:9092 \
    --replication-factor 1 \
    --partitions 1
