import os
import re

from typing import List


""" Migrate from 0.1.3 to 1.0.0.

This script will do the following changes :
- Replace `quotecast` module with `degiro_connector.quotecast`
- Replace `trading` module with `degiro_connector.trading`

If files might require manual update it will list those files.
"""


def need_manual_update(file_source: str) -> bool:
    x = re.search(
        pattern=r"(quotecast|trading)\s*=\s*[A-Z]",
        string=file_source,
    )

    return x is not None


def get_files_list(root_path=".") -> List[str]:
    files_list = list()

    for root, directories, files in os.walk(root_path):
        for name in files:
            if (
                name.endswith(".py")
                and ".tox" not in root
                and ".git" not in root
                and ".egg-info" not in root
                and "\\build\\lib" not in root
                and not name.endswith("setup.py")
            ):
                files_list.append(os.path.join(root, name))

    return files_list


def process(files_list: List[str]):
    manual_update_list = list()

    print("Processing the following files : ")

    for file_path in files_list:
        if os.path.realpath(file_path) != os.path.realpath(__file__):
            with open(file_path, "r+") as f:
                file_source = f.read()
                replace_string = file_source
                replace_string = replace_string.replace(
                    " quotecast.",
                    " degiro_connector.quotecast.",
                )
                replace_string = replace_string.replace(
                    " trading.",
                    " degiro_connector.trading.",
                )

                if need_manual_update(file_source):
                    print("UNCHANGED :", file_path)
                    manual_update_list.append(file_path)
                elif replace_string != file_source:
                    print("CHANGED   :", file_path)
                    f.seek(0)
                    f.write(replace_string)
                    f.truncate()
                else:
                    print("UNCHANGED :", file_path)

    if len(manual_update_list) > 0:
        print("The following files might need a manual update :")
        for file_path in manual_update_list:
            print(file_path)


files_list = get_files_list(root_path=".")
process(files_list=files_list)
