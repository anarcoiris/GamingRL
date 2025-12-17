"""Tests for replay buffer."""

import pytest
import numpy as np
from agent.replay_buffer import ReplayBuffer


class TestReplayBuffer:
    """Test replay buffer functionality."""

    def test_push_and_sample(self):
        """Test pushing and sampling experiences."""
        buffer = ReplayBuffer(capacity=100)

        # Push some experiences
        for i in range(10):
            state = np.random.rand(4, 8, 8).astype(np.float32)
            action = {"from": [5, 0], "to": [4, 1], "captures": []}
            reward = 0.1 * i
            next_state = np.random.rand(4, 8, 8).astype(np.float32)
            done = i % 2 == 0

            buffer.push(state, action, reward, next_state, done)

        assert len(buffer) == 10

        # Sample batch
        batch = buffer.sample(5)
        assert len(batch) == 5

        # Check batch structure
        for exp in batch:
            assert "state" in exp
            assert "action" in exp
            assert "reward" in exp
            assert "next_state" in exp
            assert "done" in exp

    def test_capacity_limit(self):
        """Test that buffer respects capacity limit."""
        buffer = ReplayBuffer(capacity=10)

        # Push more than capacity
        for i in range(20):
            state = np.random.rand(4, 8, 8).astype(np.float32)
            action = {"from": [5, 0], "to": [4, 1], "captures": []}
            buffer.push(state, action, 0.0, state, False)

        assert len(buffer) == 10

    def test_sample_smaller_than_buffer(self):
        """Test sampling when requesting more than buffer size."""
        buffer = ReplayBuffer(capacity=100)

        # Push only 3 experiences
        for i in range(3):
            state = np.random.rand(4, 8, 8).astype(np.float32)
            action = {"from": [5, 0], "to": [4, 1], "captures": []}
            buffer.push(state, action, 0.0, state, False)

        # Request more than available
        batch = buffer.sample(10)
        assert len(batch) == 3  # Should return only available

