"""Tests for DQN agent."""

import pytest
import numpy as np
import torch
from agent.dqn import DQNAgent


class TestDQNAgent:
    """Test DQN agent functionality."""

    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = DQNAgent(state_shape=(4, 8, 8))
        assert agent.state_shape == (4, 8, 8)
        assert agent.epsilon == agent.epsilon_start
        assert len(agent.replay_buffer) == 0

    def test_select_action_random(self):
        """Test random action selection (exploration)."""
        agent = DQNAgent(state_shape=(4, 8, 8))
        agent.epsilon = 1.0  # Always explore

        state = np.random.rand(4, 8, 8).astype(np.float32)
        legal_actions = [
            {"from": [5, 0], "to": [4, 1], "captures": []},
            {"from": [5, 2], "to": [4, 3], "captures": []},
        ]

        # Should select random action
        action = agent.select_action(state, legal_actions, epsilon=1.0)
        assert action in legal_actions

    def test_select_action_greedy(self):
        """Test greedy action selection (exploitation)."""
        agent = DQNAgent(state_shape=(4, 8, 8))

        state = np.random.rand(4, 8, 8).astype(np.float32)
        legal_actions = [
            {"from": [5, 0], "to": [4, 1], "captures": []},
        ]

        # Should select action (only one available)
        action = agent.select_action(state, legal_actions, epsilon=0.0)
        assert action == legal_actions[0]

    def test_store_transition(self):
        """Test storing transitions."""
        agent = DQNAgent(state_shape=(4, 8, 8))

        state = np.random.rand(4, 8, 8).astype(np.float32)
        action = {"from": [5, 0], "to": [4, 1], "captures": []}
        reward = 0.1
        next_state = np.random.rand(4, 8, 8).astype(np.float32)
        done = False

        agent.store_transition(state, action, reward, next_state, done)
        assert len(agent.replay_buffer) == 1

    def test_train_step_insufficient_samples(self):
        """Test train_step with insufficient samples."""
        agent = DQNAgent(state_shape=(4, 8, 8), batch_size=64)

        # Don't add enough samples
        for i in range(10):
            state = np.random.rand(4, 8, 8).astype(np.float32)
            action = {"from": [5, 0], "to": [4, 1], "captures": []}
            agent.store_transition(state, action, 0.1, state, False)

        # Should return None (not enough samples)
        loss = agent.train_step()
        assert loss is None

    def test_epsilon_decay(self):
        """Test epsilon decay."""
        agent = DQNAgent(
            state_shape=(4, 8, 8),
            epsilon_start=1.0,
            epsilon_end=0.05,
            epsilon_decay_steps=100,
        )

        initial_epsilon = agent.epsilon
        assert initial_epsilon == 1.0

        # Simulate steps
        for _ in range(50):
            agent.step_count += 1
            agent._update_epsilon()

        # Epsilon should have decreased
        assert agent.epsilon < initial_epsilon
        assert agent.epsilon >= agent.epsilon_end

    def test_save_load_checkpoint(self, tmp_path):
        """Test saving and loading checkpoints."""
        agent1 = DQNAgent(state_shape=(4, 8, 8))
        agent1.step_count = 100
        agent1.epsilon = 0.5

        # Save checkpoint
        checkpoint_path = tmp_path / "test_checkpoint.pt"
        agent1.save_checkpoint(str(checkpoint_path))
        assert checkpoint_path.exists()

        # Load checkpoint
        agent2 = DQNAgent(state_shape=(4, 8, 8))
        agent2.load_checkpoint(str(checkpoint_path))

        assert agent2.step_count == agent1.step_count
        assert agent2.epsilon == agent1.epsilon

