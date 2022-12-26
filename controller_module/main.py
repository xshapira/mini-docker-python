import asyncio
import json
import logging
import os

from aio_pika import Message

from messageBroker import RabbitMQ

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_message_received(message: Message) -> None:
    """
    Callback function when a message is received.
    We load the current content into a python dict, then update this dict
    with the new data, and finally overwrite the JSON file to disk.
    This done in order to append all our 3 dictionaries and end up with
    a valid JSON file.
    """
    logger.info("Received new message")
    body = message.body.decode()
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
    await message.ack()


async def consume_messages(rabbitmq: RabbitMQ) -> None:
    """
    Consume messages from the `letterbox` queue.
    It is a coroutine that takes in a RabbitMQ object as an argument
    and uses it to connect to the message queue.

    Once connected, it declares a new queue named `letterbox`
    and then starts consuming messages from this queue using
    the `on_message_received` function as its callback.
    The consume_messages function is called by main().

    :param rabbitmq: RabbitMQ: Access the rabbitmq object
    :return: The result of the on_message_received function
    """
    async with rabbitmq.connection.channel() as channel:
        queue = await channel.declare_queue("letterbox")
        await queue.consume(on_message_received)


async def main() -> None:
    """
    Create a RabbitMQ object and then calls an async function
    to consume messages from it.
    """
    rabbitmq = await RabbitMQ()
    await consume_messages(rabbitmq)


if __name__ == "__main__":
    try:
        logger.info("Controller module is running and listening...")
        logger.info("Starting Consuming")

        if os.path.exists("data/output.json"):
            print("File Exists")
            os.remove("data/output.json")

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main())
        asyncio.run(main())

        print("Finished consuming messages!")
    except Exception as e:
        logger.info(f"controller not listening {e}")
