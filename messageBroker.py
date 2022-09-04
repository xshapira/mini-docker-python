import pika

from config import settings


def get_credentials(username, password):
    return pika.PlainCredentials(username, password)


def initiate_connection(
    host="localhost", port=5672, vhost="", username="guest", password="guest"
):
    if username == "guest":
        return pika.BlockingConnection(pika.ConnectionParameters(host, port, vhost))
    credentials = get_credentials(username, password)
    return pika.BlockingConnection(
        pika.ConnectionParameters(host, port, vhost, credentials)
    )


def get_connection():
    host = settings.rabbitmq_host
    username = settings.rabbitmq_username
    password = settings.rabbitmq_password
    port = settings.rabbitmq_port
    vhost = settings.rabbitmq_vhost

    return initiate_connection(host, port, vhost, username, password)


def send_message(queue, message):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue)
    channel.basic_publish(exchange="", routing_key=queue, body=message)
    connection.close()


def consume_message(queue, callback):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue)
    channel.basic_consume(
        queue=queue,
        auto_ack=True,
        on_message_callback=callback,
    )
    channel.start_consuming()
