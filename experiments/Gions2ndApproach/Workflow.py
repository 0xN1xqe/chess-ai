import chess
import time

from experiments.Gions2ndApproach.ConfigReader import ConfigReader
from experiments.Gions2ndApproach.Helper import Helper
from experiments.Gions2ndApproach.StorageHandler import StorageHandler


class Workflow:
    @staticmethod
    def work():
        Helper.print_device()

        models = []
        number_of_models = 8
        if number_of_models % 2 != 0:
            raise ValueError("number_of_models has to be an even number")

        for i in range(number_of_models):
            models.append(StorageHandler.load_model("m"+str(i)))

        safe_frequency = ConfigReader.read_save_frequency()
        games_played = 0
        iterations = 0
        summed_moves = 0
        summed_checkmates = 0
        summed_moves_per_iteration = 0
        summed_checkmates_per_iteration = 0
        combinations = Helper.generate_chess_combinations(number_of_models)
        number_of_matches = len(combinations)
        while True:
            start_time = time.time()
            boards = []
            for i in range(number_of_matches):
                boards.append(chess.Board())
            turn = 0
            winners = [-1] * number_of_matches

            for i in range(number_of_models):
                models[i].load_to_gpu()

            ongoing_matches = number_of_matches

            while True:
                if ongoing_matches == 0:
                    break
                for i in range(number_of_matches):
                    if winners[i] != -1:
                        continue
                    possible_boards = Helper.get_all_possible_moves(boards[i])
                    evaluations = Helper.evaluate_all_boards(models[combinations[i][turn % 2]], possible_boards)

                    # if playing white, choose the best board for white
                    if turn % 2 == 0:
                        boards[i] = possible_boards[evaluations.index(max(evaluations))]
                    # if playing black, choose the worst board for white
                    else:
                        boards[i] = possible_boards[evaluations.index(min(evaluations))]

                    summed_moves_per_iteration += 1
                    summed_moves += turn + 1

                    # check if the game is over
                    if boards[i].is_checkmate():
                        winners[i] = (turn % 2)
                        summed_checkmates_per_iteration += 1
                        summed_checkmates += 1
                        ongoing_matches -= 1
                        break

                    if boards[i].is_stalemate() or boards[i].is_insufficient_material() or boards[i].is_seventyfive_moves() or boards[i].is_fivefold_repetition():
                        material_values = Helper.calculate_material(boards[i])
                        winners[i] = material_values.index(max(material_values))
                        ongoing_matches -= 1
                        break

                turn = turn + 1

            iterations = iterations + 1
            games_played = games_played + number_of_matches

            # copy the winner and slightly modify the copy
            indices = Helper.sort_indices_by_number_of_wins(combinations, winners, number_of_models)
            models = Helper.train_models(models, combinations, winners, indices)

            Helper.print_game_result_v2(iterations, summed_moves_per_iteration, summed_checkmates_per_iteration, number_of_matches)
            summed_moves_per_iteration = 0
            summed_checkmates_per_iteration = 0

            # safe every now and then
            if iterations % safe_frequency == 0:
                for i in range(number_of_models):
                    StorageHandler.save_model(models[i], "m" + str(i))
                Helper.append_integers_to_file(
                    ConfigReader.read_model_storage_directory() + "\\logs",
                    summed_moves, summed_checkmates, safe_frequency)
                summed_moves = 0
                summed_checkmates = 0

            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds \n --------------------------------------------------")


