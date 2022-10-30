#!/usr/bin/env bash

# Set magic variables for current file, directory, os, etc.
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Present Working Dir: ${__dir}"

__parent_dir="$(dirname "${__dir}")"
echo "Parent Dir: ${__parent_dir}"

JOB="${__parent_dir}/flix_assignment/producer.py"
CONFIG_FILE_PATH="${__parent_dir}/resources/conf/kafka-conf.ini"
DATA_FILE="${__parent_dir}/resources/data/input-topic-initializer.json"

python ${JOB} ${CONFIG_FILE_PATH} ${DATA_FILE}
