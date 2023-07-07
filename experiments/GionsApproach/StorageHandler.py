import keras
import os

from experiments.GionsApproach.ConfigReader import ConfigReader
from experiments.GionsApproach.ModelFactory import ModelFactory
from keras.models import model_from_json


class StorageHandler:
    @staticmethod
    def save_model_0(model):
        StorageHandler.save_model(model, ConfigReader.read_model_storage_directory_arch_0(), ConfigReader.read_model_storage_directory_neurons_0())

    @staticmethod
    def save_model_1(model):
        StorageHandler.save_model(model, ConfigReader.read_model_storage_directory_arch_1(),
                                  ConfigReader.read_model_storage_directory_neurons_1())

    @staticmethod
    def save_model(model, path_architecture_file, path_weights_file):
        # Save model architecture to JSON
        model_json = model.to_json()
        with open(path_architecture_file, "w") as json_file:
            json_file.write(model_json)

        # Save model weights to HDF5
        model.save_weights(path_weights_file)

    @staticmethod
    def load_model(json_path_arch, json_path_neurons):
        try:
            json_file = open(json_path_arch, 'r')
            loaded_model_json = json_file.read()
            json_file.close()
            loaded_model = model_from_json(loaded_model_json)
            loaded_model.load_weights(json_path_neurons)
            return loaded_model
        except Exception as e:
            return None

    @staticmethod
    def load_model_0():
        return StorageHandler.load_model(ConfigReader.read_model_storage_directory_arch_0(), ConfigReader.read_model_storage_directory_neurons_0())

    @staticmethod
    def load_model_1():
        return StorageHandler.load_model(ConfigReader.read_model_storage_directory_arch_1(), ConfigReader.read_model_storage_directory_neurons_1())


