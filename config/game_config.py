# Training Hyperparameters
GAMMA = 0.99  # Discount factor
LR = 0.001  # Learning rate
BUFFER_SIZE = 10000  # Replay buffer size
BATCH_SIZE = 64  # Mini-batch size
EPSILON_START = 1.0  # Initial exploration rate
EPSILON_END = 0.01  # Final exploration rate
EPSILON_DECAY = 0.995  # Decay rate for epsilon
TARGET_UPDATE_FREQ = 10  # Update target network every N episodes
MAX_EPISODES = 500  # Maximum number of episodes to train
