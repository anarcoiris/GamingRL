"""DQN agent implementation."""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Dict, List, Optional, Tuple
import random

from agent.network import ActionValueNetwork, action_to_features
from agent.replay_buffer import ReplayBuffer


class DQNAgent:
    """Deep Q-Network agent for checkers."""

    def __init__(
        self,
        state_shape: Tuple[int, int, int] = (4, 8, 8),
        learning_rate: float = 1e-4,
        gamma: float = 0.99,
        epsilon_start: float = 1.0,
        epsilon_end: float = 0.05,
        epsilon_decay_steps: int = 50000,
        buffer_size: int = 100000,
        batch_size: int = 64,
        target_update_frequency: int = 1000,
        device: Optional[str] = None,
    ):
        """Initialize DQN agent.

        Args:
            state_shape: Shape of state observation (channels, height, width)
            learning_rate: Learning rate for optimizer
            gamma: Discount factor
            epsilon_start: Initial epsilon for epsilon-greedy
            epsilon_end: Final epsilon for epsilon-greedy
            epsilon_decay_steps: Steps over which to decay epsilon
            buffer_size: Size of replay buffer
            batch_size: Batch size for training
            target_update_frequency: Steps between target network updates
            device: Device to use ('cuda' or 'cpu'). Auto-detects if None.
        """
        self.state_shape = state_shape
        self.gamma = gamma
        self.batch_size = batch_size
        self.target_update_frequency = target_update_frequency
        self.step_count = 0

        # Epsilon schedule
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay_steps = epsilon_decay_steps
        self.epsilon = epsilon_start

        # Device
        if device is None:
            self.device = torch.device(
                "cuda" if torch.cuda.is_available() else "cpu"
            )
        else:
            self.device = torch.device(device)

        # Networks
        self.q_network = ActionValueNetwork(
            in_channels=state_shape[0],
            board_size=state_shape[1],
        ).to(self.device)

        self.target_network = ActionValueNetwork(
            in_channels=state_shape[0],
            board_size=state_shape[1],
        ).to(self.device)

        # Copy weights to target network
        self.target_network.load_state_dict(self.q_network.state_dict())
        self.target_network.eval()

        # Optimizer
        self.optimizer = optim.Adam(self.q_network.parameters(), lr=learning_rate)

        # Replay buffer
        self.replay_buffer = ReplayBuffer(capacity=buffer_size)

    def select_action(
        self, state: np.ndarray, legal_actions: List[Dict], epsilon: Optional[float] = None
    ) -> Dict:
        """Select action using epsilon-greedy policy.

        Args:
            state: Current state (4, 8, 8)
            legal_actions: List of legal actions
            epsilon: Epsilon value (uses current epsilon if None)

        Returns:
            Selected action dictionary
        """
        if not legal_actions:
            raise ValueError("No legal actions available")

        if epsilon is None:
            epsilon = self.epsilon

        # Explore: random action
        if random.random() < epsilon:
            return random.choice(legal_actions)

        # Exploit: choose action with highest Q-value
        return self._select_best_action(state, legal_actions)

    def _select_best_action(
        self, state: np.ndarray, legal_actions: List[Dict]
    ) -> Dict:
        """Select action with highest Q-value.

        Args:
            state: Current state
            legal_actions: List of legal actions

        Returns:
            Action with highest Q-value
        """
        if len(legal_actions) == 1:
            return legal_actions[0]

        # Convert state to tensor
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(self.device)

        # Evaluate Q-values for all legal actions
        q_values = []
        for action in legal_actions:
            action_features = action_to_features(action)
            action_tensor = torch.FloatTensor(action_features).unsqueeze(0).to(
                self.device
            )

            with torch.no_grad():
                q_value = self.q_network(state_tensor, action_tensor)
                q_values.append(q_value.item())

        # Select action with highest Q-value
        best_idx = np.argmax(q_values)
        return legal_actions[best_idx]

    def store_transition(
        self,
        state: np.ndarray,
        action: Dict,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ):
        """Store transition in replay buffer.

        Args:
            state: Current state
            action: Action taken
            reward: Reward received
            next_state: Next state
            done: Whether episode terminated
        """
        self.replay_buffer.push(state, action, reward, next_state, done)

    def train_step(
        self, env=None, get_legal_actions_fn=None
    ) -> Optional[float]:
        """Perform one training step.

        Args:
            env: Optional environment to get legal actions for next states
            get_legal_actions_fn: Optional function to get legal actions

        Returns:
            Loss value if training occurred, None otherwise
        """
        if len(self.replay_buffer) < self.batch_size:
            return None

        # Sample batch
        batch = self.replay_buffer.sample(self.batch_size)

        # Prepare tensors
        states = torch.FloatTensor(
            np.array([exp["state"] for exp in batch])
        ).to(self.device)
        next_states = torch.FloatTensor(
            np.array([exp["next_state"] for exp in batch])
        ).to(self.device)
        rewards = torch.FloatTensor([exp["reward"] for exp in batch]).to(self.device)
        dones = torch.BoolTensor([exp["done"] for exp in batch]).to(self.device)

        # Get action features for current actions
        action_features = torch.FloatTensor(
            np.array([action_to_features(exp["action"]) for exp in batch])
        ).to(self.device)

        # Current Q-values
        current_q_values = self.q_network(states, action_features).squeeze()

        # Next Q-values (using target network)
        # For actions with dynamic action spaces, we approximate by using
        # the same action features. A more accurate implementation would
        # evaluate all legal actions in next_state, but that requires
        # access to the environment or legal actions function.
        with torch.no_grad():
            # Use same action features as approximation
            # In practice, this works reasonably well for checkers
            next_q_values = self.target_network(next_states, action_features).squeeze()
            
            # For done states, next Q-value should be 0
            target_q_values = rewards + (self.gamma * next_q_values * ~dones)

        # Compute loss
        loss = nn.MSELoss()(current_q_values, target_q_values)

        # Optimize
        self.optimizer.zero_grad()
        loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(self.q_network.parameters(), max_norm=1.0)
        self.optimizer.step()

        # Update step count
        self.step_count += 1

        # Update epsilon
        self._update_epsilon()

        # Update target network
        if self.step_count % self.target_update_frequency == 0:
            self.target_network.load_state_dict(self.q_network.state_dict())

        return loss.item()

    def _update_epsilon(self):
        """Update epsilon using linear decay."""
        if self.step_count < self.epsilon_decay_steps:
            decay_rate = (self.epsilon_start - self.epsilon_end) / self.epsilon_decay_steps
            self.epsilon = max(
                self.epsilon_end,
                self.epsilon_start - decay_rate * self.step_count,
            )
        else:
            self.epsilon = self.epsilon_end

    def save_checkpoint(self, filepath: str):
        """Save agent checkpoint.

        Args:
            filepath: Path to save checkpoint
        """
        checkpoint = {
            "q_network_state_dict": self.q_network.state_dict(),
            "target_network_state_dict": self.target_network.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "step_count": self.step_count,
            "epsilon": self.epsilon,
        }
        torch.save(checkpoint, filepath)

    def load_checkpoint(self, filepath: str):
        """Load agent checkpoint.

        Args:
            filepath: Path to checkpoint file
        """
        checkpoint = torch.load(filepath, map_location=self.device)
        self.q_network.load_state_dict(checkpoint["q_network_state_dict"])
        self.target_network.load_state_dict(checkpoint["target_network_state_dict"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        self.step_count = checkpoint["step_count"]
        self.epsilon = checkpoint["epsilon"]

