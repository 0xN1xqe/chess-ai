from experiments.Gions2ndApproach.NN import NeuralNetwork


class NNFactory:
    @staticmethod
    def create_v1():
        return NeuralNetwork(768, 1, [3000, 3000])

    @staticmethod
    def create_v2():
        return NeuralNetwork(768, 1, [500, 500, 500, 500])

    @staticmethod
    def create_v3():
        return NeuralNetwork(384, 1, [250, 250, 250, 250])
