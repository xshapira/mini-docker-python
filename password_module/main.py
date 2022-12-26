import asyncio
import glob
import json
import logging
import os
import pathlib
import re
from os.path import join
from typing import Any, Callable

from aio_pika import Message

from messageBroker import RabbitMQ

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_files_from_path() -> list[str]:
    """
    Return a list of files from the harvester directory.
    The function is called by the main function and used to create a list
    of files that are then passed into the `get_data_from_file`
    and `send_message` functions.

    :return: A list of all the files in the directory
    """
    dir_path = join(pathlib.Path(), "theHarvester")
    data_path = glob.glob(
        f"{dir_path}/**/*",
        recursive=True,
        include_hidden=True,
    )
    return [f for f in data_path if os.path.isfile(f)]


def get_password() -> dict[str, dict[str, str]]:
    """
    Search through all the files in a given directory and return
    any file that contains the word `password`. It will then return
    a dictionary with the filename and password as key value pairs.

    :return: A dictionary containing the password and the filename
    """
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


def password_to_json() -> str:
    password: dict[str, Any] = get_password()
    # Convert into a json string
    return json.dumps(password)


# password_to_json = password_to_json()


async def publish_message(
    rabbitmq: RabbitMQ, password_to_json: Callable[[], str]
) -> None:
    """
    Publish a message to the `letterbox` exchange. The function takes
    one argument, `rabbitmq`, which is an instance of RabbitMQ.

    :param rabbitmq: RabbitMQ: Access the rabbitmq instance
    """

    message = Message(body=password_to_json().encode())
    await rabbitmq.publish(message, routing_key="letterbox")


async def main() -> None:
    """
    Create a RabbitMQ object and calls publish_message() on it.
    """

    rabbitmq = await RabbitMQ()
    await publish_message(rabbitmq, password_to_json)


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
