import json


class LoadJson(object):
    """
    work with json files
    """

    def load(file_directory) -> any:

        with open(file_directory, 'r') as file:
            data = json.load(file)

        return data