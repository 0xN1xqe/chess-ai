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
    def make_move(model, encoded_board, board, turn):
        result = model.predict(encoded_board).reshape(4100)
        normal_move_res = result[:4096]
        promotion_res = result[-4:]

        if turn % 2 == 1:
            normal_move_res = normal_move_res[::-1]

        index_max_normal = np.argmax(normal_move_res)
        index_max_promotion = np.argmax(promotion_res)
        square_number_from = index_max_normal // 64
        square_number_to = index_max_normal % 64
        square = chess.square(chess.square_file(square_number_from), chess.square_rank(square_number_from))
        piece = board.piece_at(square)
        move = None
        # if a pawn is moved...
        if piece is not None and piece.piece_type == chess.PAWN:
            # to a back-rank
            if square_number_to % 8 == 0 or square_number_to % 8 == 7:
                # move with promotion
                piece_to_promote_to = None
                if index_max_promotion == 0:
                    piece_to_promote_to = chess.QUEEN
                    pass
                elif index_max_promotion == 1:
                    piece_to_promote_to = chess.ROOK
                    pass
                elif index_max_promotion == 2:
                    piece_to_promote_to = chess.BISHOP
                    pass
                elif index_max_promotion == 3:
                    piece_to_promote_to = chess.KNIGHT
                    pass
                else:
                    pass
                move = chess.Move(square_number_from, square_number_to, piece_to_promote_to)
        else:
            move = chess.Move(square_number_from, square_number_to)

        fromString = chess.square_name(square_number_from)
        toString = chess.square_name(square_number_to)
        if piece is None:
            print("Attempt moving from an empty square (" + fromString + ") to " + toString)
        else:
            print("Attempt moving " + piece.symbol() + " from " + fromString + " to " + toString)

        return move
