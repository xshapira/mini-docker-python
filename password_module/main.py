import glob
import json
import logging
import os
import pathlib
import re
from os.path import join

import messageBroker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Password module is listening...")

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

    logger.info(password_to_json)
    try:
        messageBroker.send_message("letterbox", password_to_json)
        print("Password was sent!")
    except Exception as ex:
        print(f"Password was not sent! {ex}")
