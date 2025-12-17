"""Training script for DQN agent."""

import argparse
import json
import random
from pathlib import Path
import numpy as np
import torch

from env.checkers_env import CheckersEnv
from agent.dqn import DQNAgent


def train_dqn(
    config_path: str,
    output_dir: str = "checkpoints",
    num_steps: int = 100000,
    eval_frequency: int = 5000,
    eval_episodes: int = 10,
    seed: int = 42,
):
    """Train DQN agent.

    Args:
        config_path: Path to environment configuration
        output_dir: Directory to save checkpoints
        num_steps: Number of training steps
        eval_frequency: Steps between evaluations
        eval_episodes: Number of episodes for evaluation
        seed: Random seed
    """
    # Set seeds
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    # Load config
    with open(config_path, "r") as f:
        env_config = json.load(f)

    # Create environment
    env = CheckersEnv(env_config)
    env.seed(seed)

    # Create agent
    agent = DQNAgent(
        state_shape=(4, 8, 8),
        learning_rate=1e-4,
        gamma=0.99,
        epsilon_start=1.0,
        epsilon_end=0.05,
        epsilon_decay_steps=50000,
        buffer_size=100000,
        batch_size=64,
        target_update_frequency=1000,
    )

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Training statistics
    episode_rewards = []
    episode_lengths = []
    losses = []
    wins = {1: 0, -1: 0, 0: 0}

    print("Starting DQN training...")
    print(f"Device: {agent.device}")
    print(f"Total steps: {num_steps}")
    print("-" * 50)

    # Training loop
    obs, info = env.reset()
    episode_reward = 0.0
    episode_length = 0
    episode_count = 0

    for step in range(num_steps):
        # Select action
        legal_actions = env.get_legal_actions()
        if not legal_actions:
            # No legal actions, reset
            obs, info = env.reset()
            continue

        action = agent.select_action(obs, legal_actions)

        # Step environment
        next_obs, reward, done, truncated, info = env.step(action)

        # Store transition
        agent.store_transition(obs, action, reward, next_obs, done or truncated)

        # Train agent
        loss = agent.train_step()
        if loss is not None:
            losses.append(loss)

        # Update statistics
        episode_reward += reward
        episode_length += 1

        # Update observation
        obs = next_obs

        # Handle episode end
        if done or truncated:
            episode_rewards.append(episode_reward)
            episode_lengths.append(episode_length)

            winner = info.get("winner")
            if winner is not None:
                wins[winner] += 1

            episode_count += 1

            # Print progress
            if episode_count % 10 == 0:
                avg_reward = np.mean(episode_rewards[-10:]) if episode_rewards else 0
                avg_length = np.mean(episode_lengths[-10:]) if episode_lengths else 0
                avg_loss = np.mean(losses[-100:]) if losses else 0
                print(
                    f"Step {step}/{num_steps} | "
                    f"Episode {episode_count} | "
                    f"Epsilon: {agent.epsilon:.3f} | "
                    f"Avg Reward: {avg_reward:.3f} | "
                    f"Avg Length: {avg_length:.1f} | "
                    f"Avg Loss: {avg_loss:.4f}"
                )

            # Reset environment
            obs, info = env.reset()
            episode_reward = 0.0
            episode_length = 0

        # Evaluation
        if step > 0 and step % eval_frequency == 0:
            eval_reward, eval_wins = evaluate_agent(env, agent, eval_episodes)
            print(
                f"\nEvaluation at step {step}: "
                f"Avg Reward: {eval_reward:.3f} | "
                f"Wins: {eval_wins[1]}/{eval_episodes}"
            )
            print("-" * 50)

        # Save checkpoint
        if step > 0 and step % 10000 == 0:
            checkpoint_path = output_path / f"checkpoint_{step}.pt"
            agent.save_checkpoint(str(checkpoint_path))
            print(f"Checkpoint saved: {checkpoint_path}")

    # Final checkpoint
    final_checkpoint = output_path / "checkpoint_final.pt"
    agent.save_checkpoint(str(final_checkpoint))
    print(f"\nFinal checkpoint saved: {final_checkpoint}")

    # Print final statistics
    print("\n" + "=" * 50)
    print("Training Complete!")
    print(f"Total episodes: {episode_count}")
    print(f"Average reward: {np.mean(episode_rewards):.3f}")
    print(f"Average episode length: {np.mean(episode_lengths):.1f}")
    print(f"Win rate (Player 1): {wins[1]/(wins[1]+wins[-1]+wins[0])*100:.1f}%")
    print("=" * 50)


def evaluate_agent(
    env: CheckersEnv, agent: DQNAgent, num_episodes: int = 10
) -> Tuple[float, Dict]:
    """Evaluate agent performance.

    Args:
        env: Environment
        agent: DQN agent
        num_episodes: Number of episodes to evaluate

    Returns:
        Average reward and win statistics
    """
    agent.q_network.eval()
    episode_rewards = []
    wins = {1: 0, -1: 0, 0: 0}

    for _ in range(num_episodes):
        obs, info = env.reset()
        episode_reward = 0.0
        done = False
        truncated = False

        while not done and not truncated:
            legal_actions = env.get_legal_actions()
            if not legal_actions:
                break

            # Use epsilon=0 for evaluation (no exploration)
            action = agent.select_action(obs, legal_actions, epsilon=0.0)
            obs, reward, done, truncated, info = env.step(action)
            episode_reward += reward

        episode_rewards.append(episode_reward)
        winner = info.get("winner")
        if winner is not None:
            wins[winner] += 1

    agent.q_network.train()

    return np.mean(episode_rewards), wins


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train DQN agent for checkers")
    parser.add_argument(
        "--config",
        type=str,
        default="config/checkers_rules.json",
        help="Path to environment configuration",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="checkpoints",
        help="Directory to save checkpoints",
    )
    parser.add_argument(
        "--num_steps",
        type=int,
        default=100000,
        help="Number of training steps",
    )
    parser.add_argument(
        "--eval_frequency",
        type=int,
        default=5000,
        help="Steps between evaluations",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed",
    )

    args = parser.parse_args()

    train_dqn(
        config_path=args.config,
        output_dir=args.output_dir,
        num_steps=args.num_steps,
        eval_frequency=args.eval_frequency,
        seed=args.seed,
    )

