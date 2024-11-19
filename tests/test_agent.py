import torch
import matplotlib.pyplot as plt
from models.dq_network import DQNetworkCNN
from game.game_env import SOSGameEnv
from training.train import decode_action, encode_action


def test_agent(policy_net, env):
    """
    Runs a single test game and returns the total reward and the final scores.
    """
    state = env.reset()  # Reset the environment
    done = False
    total_reward = 0

    while not done:
        state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Convert state to tensor
        with torch.no_grad():
            q_values = policy_net(state_tensor)

        # Determine valid actions
        valid_actions = env.available_actions()
        if not valid_actions:
            break

        # Select the best valid action
        valid_action_indices = [encode_action(a, env.board_size) for a in valid_actions]
        q_values_valid = q_values[0, valid_action_indices]
        max_q_index = torch.argmax(q_values_valid).item()
        action_index = valid_action_indices[max_q_index]

        # Decode the selected action and execute it
        row, col, letter = decode_action(action_index, env.board_size)
        state, reward, done, _ = env.step((row, col, letter))
        total_reward += reward

    return total_reward, env.scores  # Return total reward and final scores


def evaluate_agent(num_games=10):
    """
    Evaluates the agent over multiple games and visualizes performance.
    """
    # Initialize the game environment and the trained policy network
    env = SOSGameEnv()
    action_size = env.board_size * env.board_size * 2
    policy_net = DQNetworkCNN(action_size)
    policy_net.load_state_dict(torch.load('../training/outputs/models/sos_dqn.pth'))
    policy_net.eval()  # Set the model to evaluation mode

    # Metrics to track
    rewards = []
    scores = []

    # Run multiple test games
    for game in range(num_games):
        print(f"--- Game {game + 1}/{num_games} ---")
        total_reward, final_scores = test_agent(policy_net, env)
        rewards.append(total_reward)
        scores.append(final_scores)
        print(f"Total Reward: {total_reward}, Final Scores: {final_scores}")

    # Visualize the results
    plt.plot(rewards, marker='o')
    plt.xlabel('Game')
    plt.ylabel('Total Reward')
    plt.title('Agent Performance Over Multiple Games')
    plt.show()

    return rewards, scores


if __name__ == '__main__':
    evaluate_agent(num_games=10)  # Run 10 games for evaluation
