import asyncio
import json
import logging
import os
from collections import Counter
from typing import Any

from aio_pika import Message

from messageBroker import RabbitMQ
from password_module.main import get_files_from_path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_files_by_type(files: list[str]) -> dict[str, Any]:
    """
    Take a list of files and returns a dictionary containing the file types
    as keys and the number of files with that type as values.
    Sort the file types by most common to least common.

    :param files: list[str]: Get a list of files
    :return: A dictionary containing the file types and the number
    of files that are of each type
    """

    final_files = {"files_by_type": {}}
    counts = Counter()

    for file in files:
        file_type = os.path.splitext(file)[1]

        if "." not in file_type:
            # Checking if the file type is unknown. If it is,
            # then set the file type to unknown.
            file_type = "unknown"
        counts[file_type] += 1

    sorted_file_type = sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    for file_type, count in sorted_file_type:
        final_files["files_by_type"].update({file_type: count})
    return final_files


def get_sorted_file_sizes(files: list[str]) -> dict[str, Any]:
    """
    Return a dictionary of the top 10 files by size. The function sorts
    the files by size and then takes the top 10.

    :return: A dictionary with the path of the file as key and size
    in mb as value
    """

    final_files = {"sorted_file_sizes": {}}
    # Sorting the files by size and then taking the top 10 files.
    sorted_files = sorted(files, key=lambda x: os.stat(x).st_size, reverse=True)[:10]

    for path_of_file in sorted_files:
        size_of_file = os.stat(path_of_file).st_size
        # Show the size in megabytes
        size_of_file_mb = f"{str(round(size_of_file / (1024 * 1024), 3))} MB"
        final_files["sorted_file_sizes"].update({path_of_file: size_of_file_mb})
    return final_files


def get_final_files() -> str:
    """
    Return a JSON object containing the file names and sizes of all files
    in the `theHarvester` directory. The function first gets a list of
    all files in `theHarvester` directory, then it creates two
    dictionaries: one that contains only .py files and another that
    contains only .json files.

    It then sorts each dictionary by size (smallest to largest) and merges
    them into one dictionary which is returned as a JSON object.

    :return: A json string with all the files that are in
    the folder `theharvester` and their sizes
    """

    files = get_files_from_path("theHarvester")
    files_by_type = get_files_by_type(files)
    sorted_file_sizes = get_sorted_file_sizes(files)

    # Merging two dictionaries
    final_files = {**files_by_type, **sorted_file_sizes}
    return json.dumps(final_files)


async def publish_message(rabbitmq: RabbitMQ) -> None:
    """
    Publish a message to the letterbox exchange.
    The function takes one argument, `rabbitmq`, which is an instance
    of RabbitMQ.

    :param rabbitmq: RabbitMQ: Access the rabbitmq instance that
    has been created in the main function
    """

    body = get_final_files().encode()
    message = Message(body=body)
    await rabbitmq.publish(message, routing_key="letterbox")


async def main() -> None:
    """
    Create a RabbitMQ connection and publishes messages to it.
    """

    rabbitmq = await RabbitMQ()
    await publish_message(rabbitmq)


if __name__ == "__main__":
    logger.info("Analyze module is listening...")
    logger.info(get_final_files())

    try:
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main())
        asyncio.run(main())

        print("Files were sent!")
    except Exception as ex:
        print(f"Files were not sent {ex}")
