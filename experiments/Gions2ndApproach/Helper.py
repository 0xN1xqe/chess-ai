import random

import chess
import torch

from experiments.Gions2ndApproach.Encoder import Encoder


class Helper:
    @staticmethod
    def generate_chess_combinations(num_players):
        combinations = []
        for i in range(num_players - 1):
            for j in range(i + 1, num_players):
                combinations.append([i, j])
        return combinations

    @staticmethod
    def sort_indices_by_number_of_wins(combinations, winners, num_players):
        wins = [0] * num_players
        for i in range(len(combinations)):
            wins[combinations[i][winners[i]]] += 1
        sorted_indices = [index for index, _ in sorted(enumerate(wins), key=lambda x: x[1], reverse=True)]
        return sorted_indices

    @staticmethod
    def get_all_possible_moves(board):
        possible_moves = []

        for move in board.legal_moves:
            new_board = board.copy()
            new_board.push(move)
            possible_moves.append(new_board)

        return possible_moves

    @staticmethod
    def evaluate_all_boards(model, boards):
        encoded_boards = []
        for board in boards:
            encoded_boards.append(Encoder.board_to_int_array(board))
        return model.evaluate_all_boards(encoded_boards)

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
    def append_integers_to_file(path, integer1, integer2, integer3):
        try:
            with open(path, 'a') as file:
                line = f"{integer1},{integer2},{integer3};"
                file.write(line + '\n')
            print("Integers appended successfully.")
        except IOError:
            print(f"Error: Unable to open or write to the file at path: {path}")

    @staticmethod
    def print_game_result_v2(iteration, summed_turns, summed_checkmate, matches_per_iteration):
        msg = "Iteration:              " + str(iteration) + "\n"
        msg += "Average turns per game: " + str(summed_turns / matches_per_iteration) + "\n"
        msg += "Checkmate ratio:        " + str(summed_checkmate / matches_per_iteration) + "\n"
        msg += "----------------------------------------------------------------" + "\n"
        print(msg)

