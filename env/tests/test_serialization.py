"""Tests for serialization and deserialization."""

import pytest
import numpy as np
from env.checkers_env import CheckersEnv


class TestSerialization:
    """Test serialization and deserialization."""

    def test_serialize_deserialize(self):
        """Test that serialize/deserialize preserves state."""
        config = {"max_episode_steps": 50}
        env = CheckersEnv(config)
        obs, info = env.reset(seed=42)
        
        # Make a few moves
        for _ in range(3):
            legal_actions = env.get_legal_actions()
            if not legal_actions:
                break
            env.step(legal_actions[0])

        # Serialize
        state = env.serialize()
        
        # Create new env and deserialize
        env2 = CheckersEnv(config)
        env2.deserialize(state)
        
        # Check state matches
        assert np.array_equal(env.board, env2.board), "Boards should match"
        assert env.current_player == env2.current_player, "Current player should match"
        assert env.step_count == env2.step_count, "Step count should match"
        assert len(env.move_history) == len(env2.move_history), "Move history length should match"

    def test_serialize_preserves_game_state(self):
        """Test that serialization preserves all game state."""
        config = {"max_episode_steps": 50}
        env = CheckersEnv(config)
        env.reset(seed=42)
        
        # Make some moves
        for _ in range(5):
            legal_actions = env.get_legal_actions()
            if not legal_actions:
                break
            env.step(legal_actions[0])

        state = env.serialize()
        
        # Check all important fields are present
        assert "board" in state
        assert "current_player" in state
        assert "step_count" in state
        assert "move_history" in state
        assert "position_history" in state

