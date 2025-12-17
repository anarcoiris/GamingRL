"""Example script: Play random games to test environment."""

import json
import random
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from env.checkers_env import CheckersEnv


def main():
    """Play random games and show statistics."""
    # Load config
    config_path = Path(__file__).parent.parent / "config" / "checkers_rules.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    # Create environment
    env = CheckersEnv(config)
    env.seed(42)

    # Statistics
    wins = {1: 0, -1: 0, 0: 0}
    episode_lengths = []
    total_rewards = []

    num_episodes = 100

    print(f"Playing {num_episodes} random games...")
    print("-" * 50)

    for episode in range(num_episodes):
        obs, info = env.reset()
        done = False
        truncated = False
        episode_reward = 0.0
        steps = 0

        while not done and not truncated:
            # Get legal actions
            legal_actions = env.get_legal_actions()
            
            if not legal_actions:
                break

            # Choose random action
            action = random.choice(legal_actions)
            
            # Step
            obs, reward, done, truncated, info = env.step(action)
            episode_reward += reward
            steps += 1

        # Record statistics
        winner = info.get("winner", 0)
        wins[winner] += 1
        episode_lengths.append(steps)
        total_rewards.append(episode_reward)

        if (episode + 1) % 10 == 0:
            print(f"Episode {episode + 1}/{num_episodes}")

    # Print statistics
    print("\n" + "=" * 50)
    print("Statistics:")
    print(f"  Player 1 wins: {wins[1]} ({wins[1]/num_episodes*100:.1f}%)")
    print(f"  Player -1 wins: {wins[-1]} ({wins[-1]/num_episodes*100:.1f}%)")
    print(f"  Draws: {wins[0]} ({wins[0]/num_episodes*100:.1f}%)")
    print(f"  Average episode length: {sum(episode_lengths)/len(episode_lengths):.1f} steps")
    print(f"  Average reward: {sum(total_rewards)/len(total_rewards):.3f}")
    print("=" * 50)


if __name__ == "__main__":
    main()

