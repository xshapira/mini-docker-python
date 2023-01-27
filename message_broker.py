from typing import Any, Generator, Self

import confluent_kafka

from config import settings


class Kafka:
    def __init__(
        self,
        topic: list[str] = "",
        *,
        bootstrap_servers: str = settings.KAFKA_SERVER,
        security_protocol: str = "SASL_SSL",
        mechanisms: str = "PLAIN",
        username: str = settings.KAFKA_USERNAME,
        password: str = settings.KAFKA_PASSWORD,
        group_id: str = "my-group",
        timeout: float = 1.0,
        auto_offset_reset: str = "earliest",
        **kwargs
    ) -> None:

        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.security_protocol = security_protocol
        self.mechanisms = mechanisms
        self.username = username
        self.password = password
        self.group_id = group_id
        self.timeout = timeout
        self.auto_offset_reset = auto_offset_reset
        self.kwargs = kwargs

    async def connect(self) -> Self:
        self.producer = confluent_kafka.Producer(
            {
                "bootstrap.servers": self.bootstrap_servers,
                "security.protocol": self.security_protocol,
                "sasl.mechanisms": self.mechanisms,
                "sasl.username": self.username,
                "sasl.password": self.password,
            },
            **self.kwargs
        )
        self.consumer = confluent_kafka.Consumer(
            {
                "bootstrap.servers": self.bootstrap_servers,
                "security.protocol": self.security_protocol,
                "sasl.mechanisms": self.mechanisms,
                "sasl.username": self.username,
                "sasl.password": self.password,
                "group.id": self.group_id,
                "auto.offset.reset": self.auto_offset_reset,
                "session.timeout.ms": self.timeout,
            },
            **self.kwargs
        )
        return self

    def __await__(self) -> Generator[Any, None, Self]:
        return self.connect().__await__()

    # async def create_topic(self) -> None:
    #     topic = self.topic
    #     admin = confluent_kafka.AdminClient(
    #         {"bootstrap.servers": self.bootstrap_servers}
    #     )
    #     new_topics = [
    #         confluent_kafka.NewTopic(topic, num_partitions=1, replication_factor=1)
    #     ]
    #     admin.create_topics(new_topics)
