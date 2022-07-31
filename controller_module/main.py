import json
import logging

import messageBroker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def on_message_received(ch, method, properties, body):
    """Call back function when a message is received"""
    print("Received new message")

    body_dict = json.loads(body)

    with open("output.json", "a") as dict_to_json:
        dict_to_json.write(json.dumps(body_dict))

    # Get information for 3 of the tasks which are password, file type,
    # and file size, which makes the number of fields in the json to be
    # equal to 3
    counter = 0 + 1
    if counter == 3:
        print("JSON file is generated")


if __name__ == "__main__":
    logger.info("Controller module is running and listening...")

    message_broker = messageBroker.MessageBroker()
    channel = message_broker.get_channel()
    channel.queue_declare(queue="letterbox")
    channel.basic_consume(
        queue="letterbox",
        auto_ack=True,
        on_message_callback=on_message_received,
    )

    print("Starting consuming")

    # Start listening to the channel
    channel.start_consuming()
