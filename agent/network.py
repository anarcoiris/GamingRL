"""Neural network architectures for DQN agent."""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Dict, Tuple
import numpy as np


class QNetwork(nn.Module):
    """Q-Network for checkers using CNN architecture.

    Takes board state (4, 8, 8) and evaluates Q-values for legal actions.
    """

    def __init__(
        self,
        in_channels: int = 4,
        board_size: int = 8,
        hidden_dim: int = 256,
        conv_channels: Tuple[int, int] = (32, 64),
    ):
        """Initialize Q-Network.

        Args:
            in_channels: Number of input channels (4 for checkers)
            board_size: Size of board (8x8)
            hidden_dim: Hidden dimension for fully connected layers
            conv_channels: Tuple of (conv1_channels, conv2_channels)
        """
        super().__init__()

        self.in_channels = in_channels
        self.board_size = board_size
        self.hidden_dim = hidden_dim

        # Convolutional layers
        self.conv1 = nn.Conv2d(
            in_channels, conv_channels[0], kernel_size=3, padding=1
        )
        self.conv2 = nn.Conv2d(
            conv_channels[0], conv_channels[1], kernel_size=3, padding=1
        )

        # Calculate flattened size
        conv_out_size = conv_channels[1] * board_size * board_size

        # Fully connected layers
        self.fc1 = nn.Linear(conv_out_size, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        # Output layer will be added dynamically based on action space
        # For now, we'll use a flexible approach

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through network.

        Args:
            x: Input tensor of shape (batch_size, 4, 8, 8)

        Returns:
            Feature representation of shape (batch_size, hidden_dim // 2)
        """
        # Convolutional layers
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))

        # Flatten
        x = x.view(x.size(0), -1)

        # Fully connected layers
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))

        return x


class ActionValueNetwork(nn.Module):
    """Network that evaluates Q-values for specific actions.

    This network takes board state and action embeddings to produce Q-values.
    """

    def __init__(
        self,
        in_channels: int = 4,
        board_size: int = 8,
        hidden_dim: int = 256,
        action_embed_dim: int = 32,
    ):
        """Initialize Action-Value Network.

        Args:
            in_channels: Number of input channels
            board_size: Size of board
            hidden_dim: Hidden dimension
            action_embed_dim: Dimension for action embeddings
        """
        super().__init__()

        # State encoder (CNN)
        self.state_encoder = QNetwork(
            in_channels=in_channels,
            board_size=board_size,
            hidden_dim=hidden_dim,
        )

        # Action embedding: encode action as (from_row, from_col, to_row, to_col, num_captures)
        self.action_embed = nn.Linear(5, action_embed_dim)

        # Combine state and action
        combined_dim = hidden_dim // 2 + action_embed_dim
        self.q_head = nn.Sequential(
            nn.Linear(combined_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(
        self, state: torch.Tensor, action_features: torch.Tensor
    ) -> torch.Tensor:
        """Forward pass.

        Args:
            state: Board state tensor (batch_size, 4, 8, 8)
            action_features: Action features (batch_size, 5) = [from_row, from_col, to_row, to_col, num_captures]

        Returns:
            Q-values (batch_size, 1)
        """
        # Encode state
        state_features = self.state_encoder(state)

        # Encode action
        action_emb = F.relu(self.action_embed(action_features))

        # Combine
        combined = torch.cat([state_features, action_emb], dim=1)

        # Q-value
        q_value = self.q_head(combined)

        return q_value


def action_to_features(action: Dict, board_size: int = 8) -> np.ndarray:
    """Convert action dictionary to feature vector.

    Args:
        action: Action dictionary with keys: from, to, captures
        board_size: Size of board

    Returns:
        Feature vector: [from_row, from_col, to_row, to_col, num_captures]
        Normalized to [0, 1] range
    """
    from_pos = action["from"]
    to_pos = action["to"]
    num_captures = len(action.get("captures", []))

    features = np.array(
        [
            from_pos[0] / board_size,  # Normalized from_row
            from_pos[1] / board_size,  # Normalized from_col
            to_pos[0] / board_size,  # Normalized to_row
            to_pos[1] / board_size,  # Normalized to_col
            num_captures / 10.0,  # Normalized num_captures (assuming max ~10)
        ],
        dtype=np.float32,
    )

    return features

