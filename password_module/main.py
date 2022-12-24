import asyncio
import glob
import json
import logging
import os
import pathlib
import re
from os.path import join

from aio_pika import Message

from messageBroker import RabbitMQ

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_files_from_path():
    dir_path = join(pathlib.Path(), "theHarvester")
    data_path = glob.glob(
        f"{dir_path}/**/*",
        recursive=True,
        include_hidden=True,
    )
    return [f for f in data_path if os.path.isfile(f)]


def get_password():
    string_to_match = "password"
    final_files = {"passwords": {}}
    files = get_files_from_path()

    for file in files:
        with open(file, "rb") as fp:
            data = fp.read()
            if string_to_match.encode() in data:
                output = data.decode("ISO-8859-1")
                pattern_to_find = re.findall(r"password. (\S+)", output)
                # Convert list to string and remove quotes
                # And confirm the password we get is not an empty string
                if match := str(pattern_to_find)[1:-1].strip("'"):
                    final_files["passwords"].update(
                        {"password": match, "filename": file}
                    )
    return final_files


def password_to_json():
    password = get_password()
    # Convert into a json string
    return json.dumps(password)


password_to_json = password_to_json()


async def publish_message(rabbitmq: RabbitMQ):
    message = Message(body=password_to_json.encode())
    await rabbitmq.publish(message, routing_key="password_info")


async def main():
    rabbitmq = await RabbitMQ()
    await publish_message(rabbitmq)

    # # Create an exchange
    # await rabbit.include_exchange("logs")
    # # Create a message to send
    # message = Message(body=password_to_json.encode())
    # # Publish the message to the exchange
    # await rabbit.publish(message, routing_key="info", exchange_name="logs")


if __name__ == "__main__":
    logger.info("Password module is listening...")
    logger.info(password_to_json)

    try:
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main())
        asyncio.run(main())

        print("Password was sent!")
    except Exception as ex:
        print(f"Password was not sent! {ex}")
