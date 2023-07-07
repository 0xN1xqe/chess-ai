import numpy as np


class Converter:
    @staticmethod
    def board_string_to_int_array(board):
        int_array = []
        int_array_e = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        int_array_p = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        int_array_r = [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        int_array_n = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        int_array_b = [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
        int_array_k = [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
        int_array_q = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0]

        int_array_P = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        int_array_R = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
        int_array_N = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
        int_array_B = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0]
        int_array_K = [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
        int_array_Q = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
        for x in board:
            if x == "p":
                int_array.append(int_array_p)
            if x == "n":
                int_array.append(int_array_n)
            if x == "b":
                int_array.append(int_array_b)
            if x == "r":
                int_array.append(int_array_r)
            if x == "k":
                int_array.append(int_array_k)
            if x == "q":
                int_array.append(int_array_q)
            if x == "P":
                int_array.append(int_array_P)
            if x == "N":
                int_array.append(int_array_N)
            if x == "B":
                int_array.append(int_array_B)
            if x == "Q":
                int_array.append(int_array_Q)
            if x == "K":
                int_array.append(int_array_K)
            if x == "R":
                int_array.append(int_array_R)
            if x == ".":
                int_array.append(int_array_e)
        return int_array

    @staticmethod
    def board_to_int_array(board):
        state = str(board).replace("\n", "")
        encoded_board = np.array(Converter.board_string_to_int_array(state)).reshape(1, 768)
        return encoded_board
