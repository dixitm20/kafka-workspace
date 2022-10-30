#!/usr/bin/env bash

# Set magic variables for current file, directory, os, etc.
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Present Working Dir: ${__dir}"

__parent_dir="$(dirname "${__dir}")"
echo "Parent Dir: ${__parent_dir}"

__kafka_docker_dir="${__parent_dir}/kafka-setup"
echo "Kafka Docker Compose Dir: ${__kafka_docker_dir}"

cd ${__kafka_docker_dir}
docker compose down
