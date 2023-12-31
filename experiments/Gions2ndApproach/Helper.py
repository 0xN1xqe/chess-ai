import random
import math

import chess
import torch

from experiments.Gions2ndApproach.ConfigReader import ConfigReader
from experiments.Gions2ndApproach.Encoder import Encoder


class Helper:
    @staticmethod
    def determine_winner(board):
        result = board.result()
        if result == "1-0":
            return 0  # White won
        elif result == "0-1":
            return 1  # Black won
        else:
            return None  # No winner yet

    @staticmethod
    def custom_round(number):
        decimal_part = number - math.floor(number)  # Extract the decimal part
        if decimal_part >= 0.5:
            return math.ceil(number)  # Round up if decimal part is greater than or equal to 0.5
        else:
            return math.floor(number)  # Round down if decimal part is less than 0.5

    @staticmethod
    def train_models(models, combinations, winners):
        number_of_models = len(models)
        num_combinations = len(combinations)

        # Zähler für die Anzahl der Siege jedes Modells initialisieren
        wins_count = [0] * number_of_models

        # Siege für jedes Modell zählen
        for i in range(num_combinations):
            winner_index = winners[i]
            if winner_index == -2:
                continue
            wins_count[combinations[i][winner_index]] += 1

        # Relative Anzahl der Siege jedes Modells berechnen
        total_wins = sum(wins_count)
        num_copies = [0] * number_of_models

        # wenn keiner gewonnen hat, wird so getan als hätte die erste hälfte gewonnen
        if total_wins == 0:
            for i in range(number_of_models):
                if i * 2 < number_of_models:
                    num_copies[i] = 2
                else:
                    num_copies[i] = 0
        else:
            # Anzahl der Kopien jedes Modells berechnen (proportional zu den Siegen)
            win_ratios = [wins / total_wins for wins in wins_count]
            num_copies = [Helper.custom_round(ratio * number_of_models) for ratio in win_ratios]

            # Werte ggf. korrigieren
            if sum(num_copies) != number_of_models:
                decimals = [x - int(x) for x in win_ratios]
                max_index = decimals.index(max(decimals))
                num_copies[max_index] += 1

        new_models = []
        for i in range(number_of_models):
            for q in range(num_copies[i]):
                if q == 0 and num_copies[i] != 1:
                    new_models.append(models[i].create_copy())
                else:
                    new_models.append(models[i].create_modified_copy(ConfigReader.read_modification_factor()))

        return new_models

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
    def log(path, summed_moves, summed_checkmates, safe_frequency, number_of_matches):
        try:
            with open(path, 'a') as file:
                average_turns = summed_moves / (safe_frequency * number_of_matches)
                checkmate_percentage = summed_checkmates / (safe_frequency * number_of_matches)
                line = f"{average_turns},{checkmate_percentage};"
                file.write(line + '\n')
            print("Integers appended successfully.")
        except IOError:
            print(f"Error: Unable to open or write to the file at path: {path}")

    @staticmethod
    def print_game_result_v2(iteration, summed_turns, summed_checkmate, matches_per_iteration):
        msg = "Iteration:               " + str(iteration) + "\n"
        msg += "Average turns per game:  " + str(round((summed_turns / matches_per_iteration), 1)) + "\n"
        msg += "Checkmate ratio:         " + str(round((summed_checkmate / matches_per_iteration),3)) + "\n"
        print(msg)

