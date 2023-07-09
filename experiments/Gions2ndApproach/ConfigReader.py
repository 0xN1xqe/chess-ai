import os
import json


class ConfigReader:
    @staticmethod
    def read(config_element):
        # Get the current directory of the Python script
        current_directory = os.path.dirname(os.path.abspath(__file__))

        # Construct the file path of the JSON file
        json_file_path = os.path.join(current_directory, "config.json")

        # Read and parse the JSON file
        with open(json_file_path) as file:
            data = json.load(file)

        # Extract the value of "model_storage_directory" key
        config_element_value = data[config_element]

        return config_element_value

    @staticmethod
    def read_model_storage_directory():
        return ConfigReader.read("model_storage_directory")


    @staticmethod
    def read_modification_factor():
        return ConfigReader.read("modification_factor")

    @staticmethod
    def read_save_frequency():
        return ConfigReader.read("save_frequency")
