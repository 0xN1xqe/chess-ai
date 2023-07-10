import chess

from experiments.Gions2ndApproach.ConfigReader import ConfigReader
from experiments.Gions2ndApproach.Helper import Helper
from experiments.Gions2ndApproach.StorageHandler import StorageHandler


class Workflow:
    @staticmethod
    def work():
        Helper.print_device()

        model_name_1 = "m1_v3"
        model_name_2 = "m2_v3"
        models = [StorageHandler.load_model(model_name_1), StorageHandler.load_model(model_name_2)]

        safe_frequency = ConfigReader.read_save_frequency()
        games_played = 0

        summed_moves = 0
        summed_checkmates = 0
        summed_material = 0
        while True:
            # start a new game
            # initialize a new chess board
            board = chess.Board()
            turn = 0
            winner = None
            checkmate = False
            material_values = None
            while True:
                # get all possible moves
                possible_boards = Helper.get_all_possible_moves(board)
                # evaluate the state of all boards
                evaluations = Helper.evaluate_all_boards(models[turn % 2], possible_boards)
                # if playing white, choose the best board for white
                if turn % 2 == 0:
                    board = possible_boards[evaluations.index(max(evaluations))]
                # if playing black, choose the worst board for white
                else:
                    board = possible_boards[evaluations.index(min(evaluations))]

                # check if the game is over
                if board.is_checkmate():
                    winner = (turn % 2)
                    checkmate = True
                    material_values = Helper.calculate_material(board)
                    summed_checkmates += 1
                    break

                if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                    material_values = Helper.calculate_material(board)
                    winner = material_values.index(max(material_values))
                    break

                turn = turn + 1
            summed_moves += turn
            games_played = games_played + 1
            summed_material += material_values[0] + material_values[1]
            # copy the winner and slightly modify the copy
            models[(winner + 1) % 2] = models[winner].create_modified_copy(ConfigReader.read_modification_factor())

            # safe every now and then
            if games_played % safe_frequency == 0:
                StorageHandler.save_model(models[0], model_name_1)
                StorageHandler.save_model(models[1], model_name_2)
                Helper.append_integers_to_file(ConfigReader.read_model_storage_directory() + "\\data_2",summed_moves,summed_checkmates,summed_material,safe_frequency)
                summed_moves = 0
                summed_checkmates = 0
                summed_material = 0

            Helper.print_game_result(games_played, turn, material_values, winner, checkmate)
