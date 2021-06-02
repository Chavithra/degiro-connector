import os

current_path = '.'
files_list = list()

for root, directories, files in os.walk(current_path):
    for name in files:
        if name.endswith(".py") \
        and not ".tox" in root \
        and not ".git" in root \
        and not ".egg-info" in root \
        and not "\\build\\lib" in root \
        and not name.endswith("setup.py"):
            files_list.append(os.path.join(root, name))
            print(os.path.join(root, name))

for file_path in files_list:
    print(file_path)
    with open(file_path, 'r+') as f:
        file_source = f.read()

        print("file_source")
        print(file_source)

        replace_string = file_source
        replace_string = replace_string.replace(" degiro_connector.quotecast.", ' degiro_connector.quotecast.')
        replace_string = replace_string.replace(" degiro_connector.trading.", ' degiro_connector.trading.')
        if replace_string != file_source:
            f.seek(0)
            f.write(replace_string)
            f.truncate()