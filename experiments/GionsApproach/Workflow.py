import chess

from experiments.Gions2ndApproach.ConfigReader import ConfigReader
from experiments.Gions2ndApproach.Encoder import Converter
from experiments.GionsApproach.Helper import Helper
from experiments.GionsApproach.ModelFactory import ModelFactory
from experiments.GionsApproach.StorageHandler import StorageHandler


class Workflow:
    @staticmethod
    def Work():
        model_0 = StorageHandler.load_model_0()
        model_1 = StorageHandler.load_model_1()

        # if models are not initialized, create new ones
        if model_0 is None:
            model_0 = ModelFactory.create()
        if model_1 is None:
            model_1 = ModelFactory.create()

        # store models in an array
        models = [model_0, model_1]

        # how often the models should be saved to a json file
        save_frequency = ConfigReader.read_save_frequency()

        # let them play against each other infinitely many times
        turn = 0
        matches_played = 0
        total_turns_played = 0
        longest_game = 0
        while True:
            # start a new game
            # initialize a new chess board
            board = chess.Board()

            # Make the move to switch the positions of the black king and queen
            board.remove_piece_at(chess.E8)
            board.set_piece_at(chess.E8, chess.Piece(chess.QUEEN, chess.BLACK))
            board.remove_piece_at(chess.D8)
            board.set_piece_at(chess.D8, chess.Piece(chess.KING, chess.BLACK))

            if turn > longest_game:
                longest_game = turn
            turn = 0
            loser = None
            draw = False
            print("starting match number: " + str(matches_played) + "\n")
            print("total (legal) turns played: " + str(total_turns_played))
            print("number of turns of longest game so far:  " + str(longest_game))
            while True:
                encoded_board = Converter.board_to_int_array(board)
                # if its blacks turn, rotate the board
                if turn % 2 == 1:
                    encoded_board = encoded_board[:, ::-1]

                # let the model who´s turn it is run
                move = Helper.make_move(models[turn % 2], encoded_board, board, turn)

                if board.is_legal(move):
                    board.push(move)
                else:
                    # if a model tries to make an illegal move, it lost immediately
                    loser = turn % 2
                    break

                if board.is_checkmate():
                    loser = (turn % 2) + 1
                    break

                if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                    draw = True
                    break
                turn = turn + 1
                total_turns_played = total_turns_played + 1

            print("Match over! Turns played: " + str(turn) + "\n")
            matches_played = matches_played + 1

            # delete the losing model, and replace it with a slightly modified version of the winner model
            # if it´s a draw, the losing model is chosen at random
            if draw:
                loser = Helper.generate_random_integer()

            winner = (loser + 1) % 2

            if turn == 0:
                models[0] = ModelFactory.create()
                models[1] = ModelFactory.create()
                models[0].build((1, 768))
                models[1].build((1, 768))

            models[0] = models[winner]
            models[1] = Helper.create_deep_copy(models[0])
            Helper.modify_model_weights(models[1])

            if matches_played % save_frequency == 0:
                print("Saving models to json files..." + "\n")
                StorageHandler.save_model_0(models[0])
                StorageHandler.save_model_1(models[1])
                print("Done" + "\n")














