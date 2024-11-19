import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import torch
import torch.optim as optim
import random
from game.game_env import SOSGame
from models.dq_network import DQNetwork
from training.replay_buffer import ReplayBuffer
from config.game_config import *

def train():
    # Initialize environment, networks, optimizer, and replay buffer
    env = SOSGame()
    state_size = env.size * env.size  # 5x5 board flattened
    action_size = state_size  # 25 possible actions
    policy_net = DQNetwork(state_size, action_size)
    target_net = DQNetwork(state_size, action_size)
    target_net.load_state_dict(policy_net.state_dict())  # Sync target with policy net
    target_net.eval()
    optimizer = optim.Adam(policy_net.parameters(), lr=LR)
    replay_buffer = ReplayBuffer(BUFFER_SIZE)

    epsilon = EPSILON_START
    all_rewards = []

    for episode in range(MAX_EPISODES):
        state = env.reset()  # Reset the game
        state = torch.FloatTensor(state).unsqueeze(0)  # Add batch dimension
        total_reward = 0
        done = False

        while not done:
            # Choose action: epsilon-greedy policy
            if random.random() < epsilon:
                action = random.randint(0, action_size - 1)
            else:
                with torch.no_grad():
                    q_values = policy_net(state)
                    action = q_values.argmax().item()

            # Execute action in the environment
            row, col = divmod(action, env.size)
            letter = random.choice(["S", "O"])  # Randomly pick "S" or "O"
            # In train() function, after executing the action:
            valid_move = env.make_move(row, col, letter)

            if valid_move is None:
                reward = -1  # Penalty for invalid move
                done = True
            else:
                reward = env.check_sos(row, col)
                next_state = torch.FloatTensor(valid_move).unsqueeze(0)  # Use valid_move as next_state
                done = " " not in env.board  # Game ends when board is full

                # Store experience in replay buffer
                replay_buffer.add((state, action, reward, next_state, done))
                state = next_state  # Update state

            total_reward += reward

            # Train the network if replay buffer is sufficiently full
            if len(replay_buffer) >= BATCH_SIZE:
                batch = replay_buffer.sample(BATCH_SIZE)
                states, actions, rewards, next_states, dones = zip(*batch)
                states = torch.cat(states)
                next_states = torch.cat(next_states)
                actions = torch.LongTensor(actions).unsqueeze(1)
                rewards = torch.FloatTensor(rewards)
                dones = torch.FloatTensor(dones)

                # Compute Q-values
                q_values = policy_net(states).gather(1, actions).squeeze()
                with torch.no_grad():
                    next_q_values = target_net(next_states).max(1)[0]
                    targets = rewards + GAMMA * next_q_values * (1 - dones)

                # Update the policy network
                loss = torch.nn.functional.mse_loss(q_values, targets)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

        # Update target network periodically
        if episode % TARGET_UPDATE_FREQ == 0:
            target_net.load_state_dict(policy_net.state_dict())

        # Decay epsilon
        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
        all_rewards.append(total_reward)

        print(f"Episode {episode + 1}/{MAX_EPISODES}, Reward: {total_reward}, Epsilon: {epsilon:.4f}")

    # Save the trained model
    torch.save(policy_net.state_dict(), "outputs/models/sos_dqn.pth")
    print("Training complete. Model saved!")

if __name__ == "__main__":
    train()
