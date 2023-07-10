import random

import chess
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
            return "White"
        else:
            return "Black"

    @staticmethod
    def print_game_result(games_played, turn, material_values, winner, checkmate):
        round_number_string_length_max = 5
        turn_string_length_max = 3
        msg = "Done playing round number "
        for i in range(len(str(games_played)), round_number_string_length_max):
            msg += " "
        msg += str(games_played) + "; "

        for i in range(len(str(turn + 1)), turn_string_length_max):
            msg += " "

        msg += str(turn + 1) + " moves were played. Winner:   "
        msg += Helper.int_to_color(winner)
        msg += " | Materials: [White - "
        if material_values[0] < 10:
            msg += " "
        msg += str(material_values[0])
        msg += "] [Black: "
        if material_values[1] < 10:
            msg += " "
        msg += str(material_values[1])
        msg += "] | Won by: "
        if checkmate:
            msg += "Checkmate"
        else:
            msg += "Material advantage"
        print(msg)

    @staticmethod
    def calculate_material(board):
        material_values = {'q': 9, 'r': 5, 'n': 3, 'b': 3, 'p': 1}
        white_material = 0
        black_material = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece is not None:
                piece_symbol = piece.symbol().lower()
                if piece_symbol in material_values:
                    value = material_values[piece_symbol]
                    if piece.color == chess.WHITE:
                        white_material += value
                    else:
                        black_material += value

        return [white_material, black_material]

    @staticmethod
    def append_integers_to_file(path, integer1, integer2, integer3, integer4):
        try:
            with open(path, 'a') as file:
                line = f"{integer1},{integer2},{integer3},{integer4};"
                file.write(line + '\n')
            print("Integers appended successfully.")
        except IOError:
            print(f"Error: Unable to open or write to the file at path: {path}")

