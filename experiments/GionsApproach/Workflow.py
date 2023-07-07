import chess
import numpy as np

from experiments.GionsApproach.ConfigReader import ConfigReader
from experiments.GionsApproach.Converter import Converter
from experiments.GionsApproach.Helper import Helper
from experiments.GionsApproach.ModelFactory import ModelFactory
from experiments.GionsApproach.StorageHandler import StorageHandler


class Workflow:
    @staticmethod
    def Work():
        model_0 = StorageHandler.load_model_0()
        model_1 = StorageHandler.load_model_1()

        # if models are not initialized, create new ones
        if model_0 is None or True:
            model_0 = ModelFactory.create()
        if model_1 is None or True:
            model_1 = ModelFactory.create()

        # store models in an array
        models = [model_0, model_1]

        # how often the models should be saved to a json file
        save_frequency = ConfigReader.read_save_frequency()

        # let them play against each other infinitely many times
        matches_played = 0
        while True:
            # start a new game
            # initialize a new chess board
            board = chess.Board()
            turn = 0
            loser = None
            draw = False
            start_all_over = False
            print("starting match number: " + str(matches_played) + "\n")
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

                    # if the invalid move is made in the first turn, let the other model make a move as well
                    if turn == 0:
                        # rotate the board so the other player can move
                        encoded_board = encoded_board[:, ::-1]
                        move = Helper.make_move(models[(loser + 1) % 2], encoded_board, board, turn)
                        # if the others models move is illegal as well create both new from scratch
                        if not board.is_legal(move):
                            models[0] = ModelFactory.create()
                            models[1] = ModelFactory.create()
                            start_all_over = True
                    break

                if board.is_checkmate():
                    loser = (turn % 2) + 1
                    break

                if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
                    draw = True
                    break
                turn = turn + 1

            print("Match over! Turns played: " + str(turn) + "\n")
            matches_played = matches_played + 1

            # if both models try to make an illegal move, there was no progress made, so no reason to safe anything
            if not start_all_over:
                # delete the losing model, and replace it with a slightly modified version of the winner model
                # if it´s a draw, the losing model is chosen at random
                if draw:
                    loser = Helper.generate_random_integer()

                winner = (loser + 1) % 2
                models[loser] = Helper.create_deep_copy(models[winner])
                Helper.modify_model_weights(models[loser])

                if matches_played % save_frequency == 0:
                    print("Saving models to json files..." + "\n")
                    StorageHandler.save_model_0(models[0])
                    StorageHandler.save_model_1(models[1])
                    print("Done" + "\n")














