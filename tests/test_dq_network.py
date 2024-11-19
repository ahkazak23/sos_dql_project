import unittest
import torch
from models.dq_network import DQNetworkCNN

class TestDQNetwork(unittest.TestCase):
    def setUp(self):
        self.state_size = 25  # 5x5 board flattened
        self.action_size = 25  # 25 possible actions (one for each cell)
        self.model = DQNetworkCNN(self.state_size, self.action_size)

    def test_forward_pass(self):
        state = torch.randn(1, self.state_size)  # Random input state
        q_values = self.model(state)
        self.assertEqual(q_values.shape, (1, self.action_size))  # Ensure correct output shape
