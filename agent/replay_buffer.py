"""Replay buffer for storing and sampling experiences."""

import numpy as np
import random
from typing import Dict, List, Optional, Tuple
from collections import deque


class ReplayBuffer:
    """Circular buffer for storing experiences (state, action, reward, next_state, done)."""

    def __init__(self, capacity: int = 100000):
        """Initialize replay buffer.

        Args:
            capacity: Maximum number of experiences to store
        """
        self.capacity = capacity
        self.buffer = deque(maxlen=capacity)
        self.position = 0

    def push(
        self,
        state: np.ndarray,
        action: Dict,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ):
        """Add experience to buffer.

        Args:
            state: Current state (4, 8, 8)
            action: Action dictionary
            reward: Reward received
            next_state: Next state (4, 8, 8)
            done: Whether episode terminated
        """
        experience = {
            "state": state.copy(),
            "action": action.copy(),
            "reward": reward,
            "next_state": next_state.copy(),
            "done": done,
        }
        self.buffer.append(experience)

    def sample(self, batch_size: int) -> List[Dict]:
        """Sample a batch of experiences.

        Args:
            batch_size: Number of experiences to sample

        Returns:
            List of experience dictionaries
        """
        if len(self.buffer) < batch_size:
            batch_size = len(self.buffer)

        return random.sample(self.buffer, batch_size)

    def __len__(self) -> int:
        """Return current size of buffer."""
        return len(self.buffer)

    def clear(self):
        """Clear the buffer."""
        self.buffer.clear()
        self.position = 0

