import certifi
from uuid import uuid4

from confluent_kafka import KafkaError, KafkaException, Message
from confluent_kafka import SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

class MskSerializingProducer:
    kafka_brokers = None
    sr_client = None

    def __init__(self, 
                 schema_string: str, 
                 data_tag:str, 
                 avro_serializer: AvroSerializer):
        self.schema_string = schema_string
        self.data_tag = data_tag
        
        config = dict()
        config['bootstrap.servers'] = 'SSL://' + MskSerializingProducer.kafka_brokers
        config['security.protocol'] = 'SSL'
        config['ssl.ca.location'] = certifi.where()
        config['batch.size'] = 1024 * 1024 * 2
        config['message.max.bytes'] = 1024 * 1024 * 2
        config['linger.ms'] = 10000
        config['sticky.partitioning.linger.ms'] = 20000
        config['compression.type'] = 'lz4'
        config['error_cb'] = self.__error_callback_func
        config['value.serializer'] = avro_serializer
        
        self.producer = SerializingProducer(config)

    @classmethod
    def register_kafka_brokers(cls, kafka_brokers: str):
        cls.kafka_brokers = kafka_brokers

    @classmethod
    def register_schema_registry_client(cls, 
                                        schema_registry_endpoint: str, 
                                        auth_info: str):
        schema_config = {
            'url': schema_registry_endpoint,
            'basic.auth.user.info': auth_info
        }
        
        cls.sr_client = SchemaRegistryClient(schema_config)

    @classmethod
    def register_avro_serializer(cls, data_tag: str):
        schema_name = data_tag + '-value'
        schema_object = MskSerializingProducer.sr_client.get_latest_version(schema_name)
        
        schema_string = schema_object.schema.schema_str
        avro_serializer = AvroSerializer(
            schema_registry_client=MskSerializingProducer.sr_client,
            schema_str=schema_object.schema.schema_str
        )
        
        return cls(schema_string, data_tag, avro_serializer)

    def get_schema_string(self) -> str:
        return self.schema_string

    def send_message(self, message:dict):
        self.producer.poll(0)
        
        self.producer.produce(
            topic=self.data_tag,
            key=str(uuid4()),
            value=message,
            on_delivery=self.__delivery_func)

    def __error_callback_func(self, kafka_error: KafkaError):
        raise KafkaException(kafka_error)

    def __delivery_func(self,
                        kafka_error: KafkaError, 
                        msg: Message):
        if kafka_error is not None:
            print("Delivery failed for User record {}: {}".format(msg.key(), err))
            return
        print('User record {} successfully produced to {} [{}] at offset {}'.format(
            msg.key(), msg.topic(), msg.partition(), msg.offset()))
