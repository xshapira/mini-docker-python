import json

import pika


def getHostConfig():
    f = open("hostConfig.json")
    return json.load(f)


def getCredentials(username, password):
    return pika.PlainCredentials(username, password)


def initiateConnection(
    host="localhost", port=5672, vhost="", username="guest", password="guest"
):
    if username == "guest":
        return pika.BlockingConnection(pika.ConnectionParameters(host, port, vhost))
    credentials = getCredentials(username, password)
    return pika.BlockingConnection(
        pika.ConnectionParameters(host, port, vhost, credentials)
    )


def get_connection():
    config = getHostConfig()
    host = config["host"]
    username = config["username"]
    password = config["password"]
    port = 5672
    vhost = config["vhost"]

    return initiateConnection(host, port, vhost, username, password)


def sendMessage(queue, msg):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue)
    channel.basic_publish(exchange="", routing_key=queue, body=msg)
    connection.close()


def receiveMessage(queue, callback):
    connection = get_connection()
    channel = connection.channel()
    channel.queue_declare(queue)
    return channel
