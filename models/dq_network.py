import torch
import torch.nn as nn
import torch.nn.functional as F

class DQNetwork(nn.Module):
    def __init__(self, state_size, action_size):
        """
        Deep Q-Network to approximate Q-values for each action.
        :param state_size: Number of features in the input state.
        :param action_size: Number of possible actions.
        """
        super(DQNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, action_size)

    def forward(self, x):
        """
        Forward pass to calculate Q-values for each action.
        :param x: Input state as a tensor.
        :return: Q-values for all actions.
        """
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
