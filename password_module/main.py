import glob
import logging
import os
import pathlib
import re
from os.path import join

# import messageBroker

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# if __name__ == "__main__":
#     logger.info("Password module is listening...")
#     # TODO


project_root = pathlib.Path.cwd()
dir_path = join(project_root, "theHarvester")
data_path = glob.glob(f"{dir_path}/**/*", recursive=True)
string_to_match = "password:"

files = [i for i in data_path if os.path.isfile(i)]

for file in files:
    with open(file, "rb") as fp:
        data = fp.read()
        if string_to_match.encode() in data:
            output = data.decode("ISO-8859-1")
            pattern = re.findall(r"password: ([^\n]*)", output)
            print(pattern)
