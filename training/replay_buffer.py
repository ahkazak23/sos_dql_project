import random
from collections import deque

class ReplayBuffer:
    def __init__(self, buffer_size):
        """
        Replay buffer to store experiences for training.
        :param buffer_size: Maximum number of experiences to store.
        """
        self.buffer = deque(maxlen=buffer_size)

    def add(self, experience):
        """
        Add an experience to the buffer.
        :param experience: Tuple (state, action, reward, next_state, done).
        """
        self.buffer.append(experience)

    def sample(self, batch_size):
        """
        Sample a batch of experiences.
        :param batch_size: Number of experiences to sample.
        :return: A batch of experiences.
        """
        return random.sample(self.buffer, batch_size)

    def __len__(self):
        return len(self.buffer)
