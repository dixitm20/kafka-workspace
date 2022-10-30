#!/usr/bin/env bash

# Set magic variables for current file, directory, os, etc.
__dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Present Working Dir: ${__dir}"

__parent_dir="$(dirname "${__dir}")"
echo "Parent Dir: ${__parent_dir}"

JOB="${__parent_dir}/flix_assignment/transformer.py"
CONFIG_FILE_PATH="${__parent_dir}/resources/conf/kafka-conf.ini"

python ${JOB} ${CONFIG_FILE_PATH}
# In case you want to reprocess the Input_topic from beginning then you can use the --reset flag as shown below (Instead of above line)
# python ${JOB} ${CONFIG_FILE_PATH} --reset