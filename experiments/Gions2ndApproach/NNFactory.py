from experiments.Gions2ndApproach.NN import NeuralNetwork


class NNFactory:
    @staticmethod
    def create_v1():
        return NeuralNetwork(768, 1, [3000, 3000])
