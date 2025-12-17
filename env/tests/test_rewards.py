"""Tests for reward computation."""

import pytest
import numpy as np
from env.checkers_env import CheckersEnv
from env.rules import Move


class TestRewards:
    """Test reward computation."""

    def test_capture_reward(self):
        """Test reward for capturing a piece."""
        config = {
            "reward": {
                "capture": 0.01,
                "time_penalty": -0.001,
            }
        }
        env = CheckersEnv(config)
        env.reset()

        # Create a move with capture
        move = Move(
            from_pos=(5, 0),
            to_pos=(3, 2),
            captures=[(4, 1)],
            promotion=False,
        )

        reward = env._compute_step_reward(move)
        assert reward == pytest.approx(0.01 - 0.001), "Should reward capture"

    def test_promotion_reward(self):
        """Test reward for king promotion."""
        config = {
            "reward": {
                "king_promotion": 0.02,
                "time_penalty": -0.001,
            }
        }
        env = CheckersEnv(config)
        env.reset()

        move = Move(
            from_pos=(1, 0),
            to_pos=(0, 1),
            captures=[],
            promotion=True,
        )

        reward = env._compute_step_reward(move)
        assert reward == pytest.approx(0.02 - 0.001), "Should reward promotion"

    def test_time_penalty(self):
        """Test time penalty is applied."""
        config = {
            "reward": {
                "time_penalty": -0.001,
            }
        }
        env = CheckersEnv(config)
        env.reset()

        move = Move(
            from_pos=(5, 0),
            to_pos=(4, 1),
            captures=[],
            promotion=False,
        )

        reward = env._compute_step_reward(move)
        assert reward == pytest.approx(-0.001), "Should apply time penalty"

