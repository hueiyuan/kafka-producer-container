import os
import sys
import logging
import argparse

from confluent_kafka.error import ValueSerializationError
from confluent_kafka import KafkaException

from example_producer.project_libs.common import loadconfig
from example_producer.kafka_helper import MskSerializingProducer


ENV = os.environ.get('ENV', 'develop')
SR_USR = os.environ['SR_USR']
SR_PWD = os.environ['SR_PWD']

LOG_FORMAT = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%Y-%m-%dT%H:%M:%S')
LOGGER = logging.getLogger('ETLWorker')
LOGGER.setLevel(logging.INFO)
CONSOLE_HANDLER = logging.StreamHandler(sys.stdout)
CONSOLE_HANDLER.setFormatter(LOG_FORMAT)
LOGGER.addHandler(CONSOLE_HANDLER)

class User(object):
    def __init__(self, name, address, favorite_number, favorite_color):
        self.name = name
        self.favorite_number = favorite_number
        self.favorite_color = favorite_color
        self._address = address


def user_to_dict(user, ctx):
    return dict(name=user.name,
                favorite_number=user.favorite_number,
                favorite_color=user.favorite_color)


def main(config):
    MskSerializingProducer.register_kafka_brokers(config['kafka_brokers'])
    MskSerializingProducer.register_schema_registry_client(
        schema_registry_endpoint=config['schema_registry_url'],
        auth_info=f'{SR_USR}:{SR_PWD}'
    )
    topic = config['test_topic']

    schema_str = """
    {
        "namespace": "confluent.io.examples.serialization.avro",
        "name": "User",
        "type": "record",
        "fields": [
            {"name": "name", "type": "string"},
            {"name": "favorite_number", "type": "int"},
            {"name": "favorite_color", "type": "string"}
        ]
    }
    """
    
    msk_producer = MskSerializingProducer.register_avro_serializer(topic)

    print("Producing user records to topic {}. ^C to exit.".format(topic))
    while True:
        try:
            user = User(name="Mars_testig",
                        address="test_address",
                        favorite_color="favorite_testing",
                        favorite_number="color_testing")
            
            msk_producer.send_message(message=user)
            
        except ValueSerializationError as schema_error:
            LOGGER.exception(schema_error)

        except KafkaException as kafka_error:
            LOGGER.exception(kafka_error)

if __name__ == '__main__':
    example_config = loadconfig.config(
        service_name='worker',
        config_folder_prefix='project_configs',
        config_prefix_name='example')._load()
    
    main(example_config)
    
