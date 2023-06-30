import random

import chess
import numpy as np
from keras.models import clone_model

from experiments.GionsApproach.ConfigReader import ConfigReader


class Helper:
    @staticmethod
    def generate_random_integer():
        random_float = random.random()  # Generate random float between 0 and 1
        if random_float <= 0.5:
            return 0
        else:
            return 1

    @staticmethod
    def create_deep_copy(model):
        # Clone the model
        copied_model = clone_model(model)

        # Copy the weights from the original model to the copied model
        copied_model.set_weights(model.get_weights())

        return copied_model

    @staticmethod
    def modify_model_weights(model):
        modification_factor = ConfigReader.read_modification_factor()

        # Get the current weights of the model
        weights = model.get_weights()

        # Modify the weights
        modified_weights = [w + modification_factor * np.random.randn(*w.shape) for w in weights]

        # Set the modified weights back to the model
        model.set_weights(modified_weights)

    @staticmethod
    def make_move(model, encoded_board):
        result = model.predict(encoded_board).reshape(4100)
        index_max = np.argmax(result)
        print("Attempt move #" + str(index_max))
        move = None
        if index_max >= 4096:
            # promote a pawn
            move = chess.Move(0, 0, index_max - 4096)
        else:
            # make a normal move
            piece_from = index_max // 64
            piece_to = index_max % 64
            move = chess.Move(piece_from, piece_to)
        return move
