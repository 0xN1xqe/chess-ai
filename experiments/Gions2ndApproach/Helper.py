import random
import torch

from experiments.Gions2ndApproach.Encoder import Encoder


class Helper:
    @staticmethod
    def get_all_possible_moves(board):
        possible_moves = []

        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)
            possible_moves.append(new_board)

        return possible_moves

    @staticmethod
    def evaluate_board(model, board):
        encoded_board = Encoder.board_to_int_array(board)
        return model.forward(encoded_board)

    @staticmethod
    def evaluate_all_boards(model, boards):
        evaluations = []
        for board in boards:
            evaluations.append(Helper.evaluate_board(model, board))
        return evaluations

    @staticmethod
    def generate_random_integer():
        random_float = random.random()  # Generate random float between 0 and 1
        if random_float <= 0.5:
            return 0
        else:
            return 1

    @staticmethod
    def print_device():
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Check if GPU is available
        print(f"Running on device: {device}")

    @staticmethod
    def int_to_color(input_int):
        if input_int == 0:
            return "white"
        else:
            return "black"