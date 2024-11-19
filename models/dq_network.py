# models/dq_network.py

import torch
import torch.nn as nn
import torch.nn.functional as F
from config.game_config import BOARD_SIZE


class DQNetworkCNN(nn.Module):
    def __init__(self, action_size):
        super(DQNetworkCNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(64 * BOARD_SIZE * BOARD_SIZE, 256)
        self.fc2 = nn.Linear(256, action_size)

    def forward(self, x):
        x = x.unsqueeze(1)  # Add channel dimension: [batch_size, 1, BOARD_SIZE, BOARD_SIZE]
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = x.view(-1, 64 * BOARD_SIZE * BOARD_SIZE)  # Flatten
        x = F.relu(self.fc1(x))
        return self.fc2(x)
