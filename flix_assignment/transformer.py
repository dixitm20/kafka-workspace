import datetime
import json
from argparse import ArgumentParser, FileType
from configparser import ConfigParser

import pytz
from confluent_kafka import Consumer, OFFSET_BEGINNING
from confluent_kafka import Producer

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('config_file', type=FileType('r'))
    parser.add_argument('--reset', action='store_true')
    args = parser.parse_args()

    config_parser = ConfigParser()

    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    producer = Producer(config)

    config.update(config_parser['consumer'])
    consumer = Consumer(config)


    def reset_offset(consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            consumer.assign(partitions)


    def delivery_callback(err, msg):
        if err:
            print('ERROR: Message failed delivery: {}'.format(err))
        else:
            print("<= Produced event to topic '{topic}': key = {key:12} value = {value:12}".format(
                topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))


    topic = "input_topic"
    consumer.subscribe([topic], on_assign=reset_offset)

    output_topic = "output_topic"
    max_continuous_wait_retry_count = 10

    try:
        continuous_wait_retry_count = 0
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                if continuous_wait_retry_count > max_continuous_wait_retry_count:
                    print(f"Exceeded max_continuous_wait_retry_count of: {max_continuous_wait_retry_count} & "
                          f"No new messages were found. Exiting Application.")
                    break
                print(f"\nWaiting (continuous_wait_retry_count = {continuous_wait_retry_count})...")
                continuous_wait_retry_count += 1
            elif msg.error():
                continuous_wait_retry_count = 0
                print("ERROR: %s".format(msg.error()))
            else:
                continuous_wait_retry_count = 0
                key = msg.key().decode('utf-8')
                value = json.loads(msg.value().decode('utf-8'))
                print(f"\n=> Read event from topic '{msg.topic()}':    key = {key:12} value = {value}")

                if value['myTimestamp'] != '':
                    timestamp_format = '%Y-%m-%dT%H:%M:%S%z'
                    try:
                        input_datetime = datetime.datetime.strptime(value['myTimestamp'], timestamp_format)
                        timestamp_utc = input_datetime.astimezone(pytz.UTC).strftime('%Y-%m-%dT%H:%M:%S') + '+00:00'
                        print(f"* Transformed input timestamp: '{value['myTimestamp']}' "
                              f"to UTC timestamp: '{timestamp_utc}'")
                        value['myTimestamp'] = timestamp_utc
                    except ValueError as message:
                        print('* Unknown Datetime format, Skip UTC Conversion and retain value as it is.')
                else:
                    print('* Skip UTC Conversion as input date time is missing')

                producer.produce(output_topic, json.dumps(value), key, callback=delivery_callback)
                producer.poll()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()
        producer.flush()
