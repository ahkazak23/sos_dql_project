import os
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from game.game_env import SOSGameEnv
from models.dq_network import DQNetworkCNN
from training.replay_buffer import ReplayBuffer
from config.game_config import *

import random


def train():
    # Initialize the game environment
    env = SOSGameEnv()

    # Action space size
    action_size = env.board_size * env.board_size * 2  # Positions * Letters ('S' or 'O')

    # Initialize the networks
    policy_net = DQNetworkCNN(action_size)
    target_net = DQNetworkCNN(action_size)
    target_net.load_state_dict(policy_net.state_dict())
    target_net.eval()

    # Optimizer and loss
    optimizer = optim.Adam(policy_net.parameters(), lr=LEARNING_RATE)
    criterion = nn.MSELoss()

    # Replay buffer
    replay_buffer = ReplayBuffer(MEMORY_SIZE)

    # Epsilon-greedy strategy
    epsilon = EPSILON_START

    # Training loop
    for episode in range(NUM_EPISODES):
        state = env.reset()  # Reset the environment
        total_reward = 0

        for t in range(MAX_STEPS):
            # Select action using epsilon-greedy strategy
            if np.random.rand() <= epsilon:
                action_index = random_action(env)
            else:
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                with torch.no_grad():
                    q_values = policy_net(state_tensor)
                valid_actions = env.available_actions()
                if valid_actions:
                    valid_action_indices = [encode_action(a, env.board_size) for a in valid_actions]
                    q_values_valid = q_values[0, valid_action_indices]
                    max_q_index = torch.argmax(q_values_valid).item()
                    action_index = valid_action_indices[max_q_index]
                else:
                    break  # No valid actions available

            # Decode action and execute
            row, col, letter = decode_action(action_index, env.board_size)
            next_state, reward, done, info = env.step((row, col, letter))
            total_reward += reward

            # Store experience in replay buffer
            replay_buffer.push(state, action_index, reward, next_state, done)
            state = next_state

            # Train the network if enough experiences are in the buffer
            if len(replay_buffer) >= BATCH_SIZE:
                batch = replay_buffer.sample(BATCH_SIZE)
                train_batch(policy_net, target_net, optimizer, criterion, batch)

            if done:
                break

        # Update epsilon
        epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)

        # Update the target network periodically
        if (episode + 1) % TARGET_UPDATE_FREQ == 0:
            target_net.load_state_dict(policy_net.state_dict())

        # Logging
        print(f"Episode {episode + 1}/{NUM_EPISODES}, Total Reward: {total_reward}, Epsilon: {epsilon:.4f}")

    # Ensure the output directory exists
    model_dir = 'outputs/models'
    os.makedirs(model_dir, exist_ok=True)

    # Save the trained model
    torch.save(policy_net.state_dict(), os.path.join(model_dir, 'sos_dqn.pth'))
    print("Training completed and model saved!")


def random_action(env):
    """Select a random valid action from the environment."""
    actions = env.available_actions()
    action = random.choice(actions)
    return encode_action(action, env.board_size)


def encode_action(action, board_size):
    """Encode an action (row, col, letter) into a single index."""
    row, col, letter = action
    position = row * board_size + col
    letter_index = 0 if letter == 'S' else 1
    return position * 2 + letter_index


def decode_action(action_index, board_size):
    """Decode an action index back into (row, col, letter)."""
    position = action_index // 2
    letter_index = action_index % 2
    row = position // board_size
    col = position % board_size
    letter = 'S' if letter_index == 0 else 'O'
    return row, col, letter


def train_batch(policy_net, target_net, optimizer, criterion, batch):
    """Train the policy network using a batch of experiences."""
    states, actions, rewards, next_states, dones = zip(*batch)

    # Convert lists of NumPy arrays to tensors
    states = torch.FloatTensor(np.array(states))
    actions = torch.LongTensor(actions).unsqueeze(1)
    rewards = torch.FloatTensor(rewards).unsqueeze(1)
    next_states = torch.FloatTensor(np.array(next_states))
    dones = torch.FloatTensor(dones).unsqueeze(1)

    # Compute Q-values for the current states and selected actions
    q_values = policy_net(states).gather(1, actions)

    # Compute the target Q-values
    with torch.no_grad():
        max_next_q_values = target_net(next_states).max(1)[0].unsqueeze(1)
        target_q_values = rewards + (GAMMA * max_next_q_values * (1 - dones))

    # Compute loss
    loss = criterion(q_values, target_q_values)

    # Backpropagation and optimization
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


if __name__ == '__main__':
    train()
