import glob
import logging
import os
import pathlib
from collections import Counter
from os.path import join

# import messageBroker

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# if __name__ == "__main__":
#     logger.info("Analyze module is listening...")
#     # TODO


dir_path = join(pathlib.Path(), "theHarvester")
data_path = glob.glob(f"{dir_path}/**/*", recursive=True)
files = [i for i in data_path if os.path.isfile(i)]

final_files = {}


def get_file_type():
    counts = Counter()
    for file in files:
        file_type = os.path.splitext(file)[1]

        if "." in file_type:
            counts[file_type] += 1

    for file_type, count in counts.items():
        final_files.update({file_type: count})
    return final_files


def get_file_size():
    # Sort the top 10 files by size
    files_ascending = sorted(files, key=lambda x: os.stat(x).st_size, reverse=True)[:10]

    for path_of_file in files_ascending:
        size_of_file = os.stat(path_of_file).st_size
        # Show the size in megabytes
        size_of_file_mb = f"{str(round(size_of_file / (1024 * 1024), 3))} MB"
        final_files.update({path_of_file: size_of_file_mb})
    return final_files
