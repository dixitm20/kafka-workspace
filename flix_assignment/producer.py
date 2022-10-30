import json
from argparse import ArgumentParser, FileType
from configparser import ConfigParser

from confluent_kafka import Producer

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('data_file', type=FileType('r'))
    args = parser.parse_args()

    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])

    producer = Producer(config)


    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("Produced event to topic {topic}: key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


    topic = "input_topic"

    with open(args.data_file.name) as f:
        for json_msg in f:
            msg_dict = json.loads(json_msg)
            key = str(msg_dict['myKey'])
            value = msg_dict['myTimestamp']
            producer.produce(topic, json.dumps(msg_dict), key, callback=delivery_callback)

    producer.poll(10000)
    producer.flush()
