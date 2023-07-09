import torch

from experiments.Gions2ndApproach.ConfigReader import ConfigReader
from experiments.Gions2ndApproach.NNFactory import NNFactory


class StorageHandler:
    @staticmethod
    def save_model(model, model_name):
        try:
            # Save the model to a file
            torch.save(model.state_dict(), ConfigReader.read_model_storage_directory() + "\\" + model_name)
            print("Saved model")
        except Exception as e:
            print("Directory to safe model in not found (" + str(e) + ")")

    @staticmethod
    def load_model(model_name):
        try:
            # Load the model from a file
            net = NNFactory.create_v1()
            net.load_state_dict(torch.load(ConfigReader.read_model_storage_directory() + "\\" + model_name))
            print("Loaded model")
            return net
        except Exception as e:
            print("Failed to load model (" + str(e) + "), create one instead")
            return NNFactory.create_v1()
