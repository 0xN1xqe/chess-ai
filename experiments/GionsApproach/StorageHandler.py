import keras
import os

from experiments.GionsApproach.ConfigReader import ConfigReader


class StorageHandler:
    @staticmethod
    def get_files_in_directory():
        directory = ConfigReader.read_model_storage_directory()
        file_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)
        return file_paths

    @staticmethod
    def save_model_to_json(model, name):
        filename = ConfigReader.read_model_storage_directory() + name
        # Save model to JSON
        model_json = model.to_json()
        with open(filename, "w") as json_file:
            json_file.write(model_json)

    @staticmethod
    def load_model_from_json(path):
        # Load model from JSON
        with open(path, "r") as json_file:
            loaded_model_json = json_file.read()
        loaded_model = keras.models.model_from_json(loaded_model_json)
        return loaded_model

    @staticmethod
    def save_model(model, architecture_filename, weights_filename):
        # Save model architecture to JSON
        model_json = model.to_json()
        with open(architecture_filename, "w") as json_file:
            json_file.write(model_json)

        # Save model weights to HDF5
        model.save_weights(weights_filename)

    @staticmethod
    def load_model(architecture_filename, weights_filename):
        # Load model architecture from JSON
        with open(architecture_filename, "r") as json_file:
            loaded_model_json = json_file.read()
        loaded_model = keras.models.model_from_json(loaded_model_json)

        # Load model weights from HDF5
        loaded_model.load_weights(weights_filename)
        return loaded_model

