import json
import logging
import os

import messageBroker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def on_message_received(ch, method, properties, body):
    """
    Callback function when a message is received.
    To append all our 3 dictionaries and end up with a valid JSON,
    we load the current content into a python dict, then update this dict
    with the new data, and finally overwrite the JSON file to disk.
    """
    logger.info("Received new message")
    body_dict = json.loads(body)
    logger.info(body)
    if os.path.exists("data/output.json"):
        with open("data/output.json", "r+") as dict_to_json:
            # Load the current content into a python dict
            json_object = json.loads(dict_to_json.read())
            # Merge dictionaries
            json_object.update(body_dict)
            # Move cursor to the beginning of the file
            dict_to_json.seek(0)
            # Write the updated dictionary to JSON
            dict_to_json.write(json.dumps(json_object, indent=4))
    else:
        with open("data/output.json", "w+") as dict_to_json:
            dict_to_json.write(json.dumps(body_dict, indent=4))


if __name__ == "__main__":
    try:
        logger.info("Controller module is running and listening...")

        logger.info("Starting Consuming")

        if os.path.exists("data/output.json"):
            print("File Exists")
            os.remove("data/output.json")

        # Consume message from queue
        messageBroker.consume_message("letterbox", on_message_received)
    except Exception as e:
        logger.info(f"controller not listening{e}")
