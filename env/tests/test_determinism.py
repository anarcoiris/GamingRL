"""Tests for determinism and reproducibility."""

import pytest
import numpy as np
from env.checkers_env import CheckersEnv


class TestDeterminism:
    """Test determinism and reproducibility."""

    def test_seed_reproducibility(self):
        """Test that same seed produces same results."""
        config = {"max_episode_steps": 50}
        
        # Run episode 1
        env1 = CheckersEnv(config)
        obs1, info1 = env1.reset(seed=42)
        actions1 = []
        rewards1 = []
        
        for _ in range(10):
            legal_actions = env1.get_legal_actions()
            if not legal_actions:
                break
            action = legal_actions[0]  # Take first legal action
            actions1.append(action)
            obs, reward, done, truncated, info = env1.step(action)
            rewards1.append(reward)
            if done or truncated:
                break

        # Run episode 2 with same seed
        env2 = CheckersEnv(config)
        obs2, info2 = env2.reset(seed=42)
        actions2 = []
        rewards2 = []
        
        for _ in range(10):
            legal_actions = env2.get_legal_actions()
            if not legal_actions:
                break
            action = legal_actions[0]  # Take first legal action
            actions2.append(action)
            obs, reward, done, truncated, info = env2.step(action)
            rewards2.append(reward)
            if done or truncated:
                break

        # Should produce same results
        assert np.array_equal(obs1, obs2), "Initial observations should match"
        assert len(actions1) == len(actions2), "Should have same number of actions"
        assert actions1 == actions2, "Actions should match"
        assert rewards1 == rewards2, "Rewards should match"

    def test_board_state_reproducibility(self):
        """Test that board state is reproducible with seed."""
        config = {"max_episode_steps": 50}
        
        env1 = CheckersEnv(config)
        env1.reset(seed=123)
        env1.step(env1.get_legal_actions()[0])
        board1 = env1.board.copy()

        env2 = CheckersEnv(config)
        env2.reset(seed=123)
        env2.step(env2.get_legal_actions()[0])
        board2 = env2.board.copy()

        assert np.array_equal(board1, board2), "Board states should match"

