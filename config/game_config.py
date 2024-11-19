# config/game_config.py

BOARD_SIZE = 5

# DQL Hyperparameters
GAMMA = 0.99            # Higher discount factor
EPSILON_START = 1.0
EPSILON_MIN = 0.05      # Allow some exploration even later in training
EPSILON_DECAY = 0.995   # Adjusted decay rate
LEARNING_RATE = 0.0001  # Lower learning rate for stability
BATCH_SIZE = 64
MEMORY_SIZE = 20000     # Increase replay buffer size
TARGET_UPDATE_FREQ = 5  # Update target network more frequently
NUM_EPISODES = 5000     # Train for more episodes
MAX_STEPS = BOARD_SIZE * BOARD_SIZE  # Maximum steps equal to the number of cells
