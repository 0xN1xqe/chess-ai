import torch
import torch.nn as nn


class NeuralNetwork(nn.Module):
    def __init__(self, input_size, output_size, hidden_sizes):
        super(NeuralNetwork, self).__init__()

        self.hidden_layers = nn.ModuleList()
        input_dim = input_size

        for hidden_size in hidden_sizes:
            self.hidden_layers.append(nn.Linear(input_dim, hidden_size))
            input_dim = hidden_size

        self.output_layer = nn.Linear(input_dim, output_size)

    def forward(self, x):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Check if GPU is available
        device = torch.device('cpu')
        # Move the network and input data to the GPU
        self.to(device)
        # Convert input data to PyTorch tensor and float type
        x = torch.from_numpy(x).float().to(device)

        for hidden_layer in self.hidden_layers:
            x = torch.relu(hidden_layer(x))

        x = self.output_layer(x)
        return x

    def load_to_gpu(self):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Check if GPU is available
        # Move the network and input data to the GPU
        self.to(device)

    def evaluate_all_boards(self, encoded_boards):
        evaluations = []
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')  # Check if GPU is available

        # Convert input data to PyTorch tensors and float type
        encoded_boards_tensor = torch.tensor(encoded_boards).float().to(device)

        # Apply ReLU activation to all hidden layers at once
        for hidden_layer in self.hidden_layers:
            encoded_boards_tensor = torch.relu(encoded_boards_tensor)

        # Compute evaluations in batches
        output = self.output_layer(encoded_boards_tensor)
        evaluations = output.squeeze().tolist()

        if isinstance(evaluations, float):
            evaluations = [evaluations]

        return evaluations

    def create_copy(self):
        net = NeuralNetwork(
            input_size=self.hidden_layers[0].in_features,
            output_size=self.output_layer.out_features,
            hidden_sizes=[layer.out_features for layer in self.hidden_layers]
        )

        # Copy the weights and biases from the current network to the modified network
        for modified_param, param in zip(net.parameters(), self.parameters()):
            modified_param.data.copy_(param.data.clone())

        return net

    def create_modified_copy(self, modification_factor):
        modified_net = NeuralNetwork(
            input_size=self.hidden_layers[0].in_features,
            output_size=self.output_layer.out_features,
            hidden_sizes=[layer.out_features for layer in self.hidden_layers]
        )

        # Copy the weights and biases from the current network to the modified network
        for modified_param, param in zip(modified_net.parameters(), self.parameters()):
            modified_param.data.copy_(param.data.clone())

            # Modify the weights and biases of the modified network
            modified_param.data += modification_factor * torch.randn_like(modified_param.data)

        return modified_net
