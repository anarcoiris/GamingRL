"""Minimal training example to verify DQN works."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from env.checkers_env import CheckersEnv
from agent.dqn import DQNAgent
import numpy as np


def main():
    """Run minimal training to verify everything works."""
    # Load config
    config_path = Path(__file__).parent.parent / "config" / "checkers_rules.json"
    with open(config_path, "r") as f:
        config = json.load(f)

    # Create environment
    env = CheckersEnv(config)
    env.seed(42)

    # Create agent
    agent = DQNAgent(
        state_shape=(4, 8, 8),
        learning_rate=1e-4,
        batch_size=32,  # Smaller for quick test
        buffer_size=1000,
    )

    print("Starting minimal training test...")
    print(f"Device: {agent.device}")
    print("-" * 50)

    # Run a few episodes
    obs, info = env.reset()
    episode_count = 0
    total_steps = 0

    for step in range(500):  # Just 500 steps for quick test
        legal_actions = env.get_legal_actions()
        if not legal_actions:
            obs, info = env.reset()
            continue

        # Select action
        action = agent.select_action(obs, legal_actions)

        # Step
        next_obs, reward, done, truncated, info = env.step(action)

        # Store transition
        agent.store_transition(obs, action, reward, next_obs, done or truncated)

        # Train
        loss = agent.train_step()
        if loss is not None and step % 50 == 0:
            print(f"Step {step}: Loss={loss:.4f}, Epsilon={agent.epsilon:.3f}, Buffer={len(agent.replay_buffer)}")

        obs = next_obs
        total_steps += 1

        if done or truncated:
            episode_count += 1
            obs, info = env.reset()

    print("\n" + "=" * 50)
    print("Minimal training test complete!")
    print(f"Total steps: {total_steps}")
    print(f"Episodes: {episode_count}")
    print(f"Final epsilon: {agent.epsilon:.3f}")
    print(f"Buffer size: {len(agent.replay_buffer)}")
    print("=" * 50)


if __name__ == "__main__":
    main()

