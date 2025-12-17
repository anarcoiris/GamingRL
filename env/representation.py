"""State representation conversion utilities."""

import numpy as np
from typing import Tuple


def board_to_observation(board: np.ndarray, current_player: int = 1) -> np.ndarray:
    """Convert board state to observation tensor.

    Args:
        board: Board state (8x8) with values:
            0 = empty
            1 = player1 man
            2 = player1 king
            -1 = player2 man
            -2 = player2 king
        current_player: Current player (1 or -1)

    Returns:
        Observation tensor of shape (4, 8, 8) with channels:
        - Channel 0: own men
        - Channel 1: own kings
        - Channel 2: opponent men
        - Channel 3: opponent kings
    """
    obs = np.zeros((4, 8, 8), dtype=np.float32)

    for row in range(8):
        for col in range(8):
            piece = board[row, col]

            if piece == 0:
                continue

            if current_player == 1:
                # Player 1's perspective
                if piece == 1:  # Own man
                    obs[0, row, col] = 1.0
                elif piece == 2:  # Own king
                    obs[1, row, col] = 1.0
                elif piece == -1:  # Opponent man
                    obs[2, row, col] = 1.0
                elif piece == -2:  # Opponent king
                    obs[3, row, col] = 1.0
            else:
                # Player -1's perspective (flip)
                if piece == -1:  # Own man
                    obs[0, row, col] = 1.0
                elif piece == -2:  # Own king
                    obs[1, row, col] = 1.0
                elif piece == 1:  # Opponent man
                    obs[2, row, col] = 1.0
                elif piece == 2:  # Opponent king
                    obs[3, row, col] = 1.0

    return obs


def create_initial_board() -> np.ndarray:
    """Create initial checkers board state.

    Returns:
        Board state (8x8) with initial piece positions
    """
    board = np.zeros((8, 8), dtype=np.int8)

    # Player 1 (red) pieces in first 3 rows
    for row in range(3):
        for col in range(8):
            if (row + col) % 2 == 1:  # Dark squares
                board[row, col] = 1  # Player 1 man

    # Player -1 (black) pieces in last 3 rows
    for row in range(5, 8):
        for col in range(8):
            if (row + col) % 2 == 1:  # Dark squares
                board[row, col] = -1  # Player -1 man

    return board


def board_hash(board: np.ndarray) -> int:
    """Generate hash of board state for repetition detection.

    Args:
        board: Board state (8x8)

    Returns:
        Hash value
    """
    return hash(board.tobytes())

