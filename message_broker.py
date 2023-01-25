from typing import Any, Generator, Self

import confluent_kafka


class Kafka:
    def __init__(
        self,
        topic: str,
        *,
        bootstrap_servers: str = "localhost:9092",
        client_id: str = "",
        group_id: str = "",
        **kwargs
    ) -> None:

        self.topic = topic
        self.bootstrap_servers = bootstrap_servers
        self.client_id = client_id
        self.group_id = group_id
        self.kwargs = kwargs

    async def connect(self) -> Self:
        self.producer = confluent_kafka.Producer(
            {"bootstrap.servers": self.bootstrap_servers, "client.id": self.client_id},
            **self.kwargs
        )
        self.consumer = confluent_kafka.Consumer(
            {
                "bootstrap.servers": self.bootstrap_servers,
                "group.id": self.group_id,
                "client.id": self.client_id,
            },
            **self.kwargs
        )
        return self

    def __await__(self) -> Generator[Any, None, Self]:
        return self.connect().__await__()

    async def create_topic(self) -> None:
        topic = self.topic
        admin = confluent_kafka.AdminClient(
            {"bootstrap.servers": self.bootstrap_servers}
        )
        new_topics = [
            confluent_kafka.NewTopic(topic, num_partitions=1, replication_factor=1)
        ]
        admin.create_topics(new_topics)
