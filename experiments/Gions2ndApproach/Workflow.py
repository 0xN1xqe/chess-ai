import chess

from experiments.Gions2ndApproach.ConfigReader import ConfigReader
from experiments.Gions2ndApproach.Helper import Helper
from experiments.Gions2ndApproach.StorageHandler import StorageHandler


class Workflow:
    @staticmethod
    def work():
        Helper.print_device()

        model_name_1 = "m1"
        model_name_2 = "m2"
        models = [StorageHandler.load_model(model_name_1), StorageHandler.load_model(model_name_2)]

        safe_frequency = ConfigReader.read_save_frequency()
        games_played = 0

        while True:
            # start a new game
            # initialize a new chess board
            board = chess.Board()
            turn = 0
            winner = None
            draw = False
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
                    break

                if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                    winner = Helper.generate_random_integer()
                    draw = True
                    break

                turn = turn + 1

            games_played = games_played + 1
            # copy the winner and slightly modify the copy
            models[(winner + 1) % 2] = models[winner].create_modified_copy(ConfigReader.read_save_frequency())

            # safe every now and then
            if games_played % safe_frequency == 0:
                StorageHandler.save_model(models[0], model_name_1)
                StorageHandler.save_model(models[1], model_name_2)

            msg = "Done playing round number " + str(games_played) + "; " + str(turn + 1) + " moves were played. \t"
            if draw:
                msg += "Game ended in a draw"
            else:
                msg += Helper.int_to_color(winner) + " won"
            print(msg)
