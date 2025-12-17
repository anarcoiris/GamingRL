"""Checkers environment compatible with Gym/Gymnasium API."""

import numpy as np
import random
from typing import Dict, Tuple, Optional, List, Any
import gymnasium as gym
from gymnasium import spaces

from env.rules import CheckersRules, Move
from env.representation import (
    board_to_observation,
    create_initial_board,
    board_hash,
)


class CheckersEnv(gym.Env):
    """Checkers environment compatible with Gymnasium API.

    This environment implements American checkers (8x8) with standard rules:
    - Forced captures
    - Prefer longest capture
    - King promotion on last row
    - Multi-jump sequences
    """

    metadata = {"render_modes": ["ascii", "human", "rgb_array"], "render_fps": 4}

    def __init__(self, config: Optional[Dict] = None, render_mode: Optional[str] = None):
        """Initialize checkers environment.

        Args:
            config: Configuration dictionary. If None, uses default config.
            render_mode: Rendering mode ('ascii', 'human', 'rgb_array')
        """
        super().__init__()

        # Load default config if not provided
        if config is None:
            config = self._default_config()

        self.config = config
        self.render_mode = render_mode

        # Initialize rules
        self.rules = CheckersRules(config)

        # Game state
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.current_player = 1
        self.step_count = 0
        self.move_history = []
        self.position_history = []  # For repetition detection

        # Configuration values
        self.max_episode_steps = config.get("max_episode_steps", 200)
        self.draw_repetition_threshold = config.get("draw_repetition_threshold", 3)
        self.draw_move_threshold = config.get("draw_move_threshold", 100)

        # Reward configuration
        self.reward_config = config.get("reward", {
            "win": 1.0,
            "loss": -1.0,
            "draw": 0.0,
            "capture": 0.01,
            "king_promotion": 0.02,
            "time_penalty": -0.001,
        })

        # Seed for reproducibility
        self._seed = None
        self.np_random = None

        # Observation and action spaces
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(4, 8, 8), dtype=np.float32
        )
        # Action space is dynamic (variable number of legal actions)
        self.action_space = spaces.Discrete(1)  # Placeholder, actual actions are dynamic

    def _default_config(self) -> Dict:
        """Return default configuration."""
        return {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
            "king_on_last_row": True,
            "max_episode_steps": 200,
            "draw_repetition_threshold": 3,
            "draw_move_threshold": 100,
            "reward": {
                "win": 1.0,
                "loss": -1.0,
                "draw": 0.0,
                "capture": 0.01,
                "king_promotion": 0.02,
                "time_penalty": -0.001,
            },
        }

    def seed(self, seed: Optional[int] = None):
        """Set seed for reproducibility.

        Args:
            seed: Random seed
        """
        self._seed = seed
        random.seed(seed)
        np.random.seed(seed)
        self.np_random = np.random.RandomState(seed)

    def reset(
        self,
        seed: Optional[int] = None,
        options: Optional[Dict] = None,
    ) -> Tuple[np.ndarray, Dict]:
        """Reset environment to initial state.

        Args:
            seed: Optional seed for reproducibility
            options: Optional dictionary with reset options

        Returns:
            Observation and info dictionary
        """
        if seed is not None:
            self.seed(seed)

        # Initialize board
        self.board = create_initial_board()
        self.current_player = 1
        self.step_count = 0
        self.move_history = []
        self.position_history = [board_hash(self.board)]

        # Build observation
        obs = self._build_observation()

        info = {
            "current_player": self.current_player,
            "legal_actions_count": len(self.get_legal_actions()),
        }

        return obs, info

    def step(self, action: Dict) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """Execute one step in the environment.

        Args:
            action: Action dictionary with keys: from, to, captures, promotion

        Returns:
            observation, reward, terminated, truncated, info
        """
        # Validate action
        legal_actions = self.get_legal_actions()
        action_from = tuple(action["from"])
        action_to = tuple(action["to"])
        action_captures = set(tuple(c) for c in action.get("captures", []))

        # Check if action is legal
        action_is_legal = False
        selected_move = None
        for move_dict in legal_actions:
            move_from = tuple(move_dict["from"])
            move_to = tuple(move_dict["to"])
            move_captures = set(tuple(c) for c in move_dict.get("captures", []))
            
            if (move_from == action_from) and (move_to == action_to):
                # Check captures match
                if move_captures == action_captures:
                    action_is_legal = True
                    # Convert back to Move object for application
                    selected_move = Move(
                        from_pos=move_from,
                        to_pos=move_to,
                        captures=list(move_captures),
                        promotion=move_dict.get("promotion", False),
                    )
                    break

        if not action_is_legal:
            raise ValueError(
                f"Action {action} is not legal. Legal actions: {len(legal_actions)}"
            )

        # Apply move
        reward = self._compute_step_reward(selected_move)
        self.board = self.rules.apply_move(self.board, selected_move, self.current_player)
        self.move_history.append(selected_move.to_dict())
        self.step_count += 1

        # Switch player
        self.current_player = -self.current_player

        # Check terminal state
        terminated, winner = self.rules.is_terminal(self.board, self.current_player)

        # Check for draw conditions
        truncated = False
        draw_reason = None

        # Check repetition
        current_hash = board_hash(self.board)
        self.position_history.append(current_hash)
        repetition_count = self.position_history.count(current_hash)
        if repetition_count >= self.draw_repetition_threshold:
            terminated = True
            winner = 0  # Draw
            draw_reason = "repetition"

        # Check max steps
        if self.step_count >= self.max_episode_steps:
            truncated = True
            if not terminated:
                terminated = True
                winner = 0  # Draw
                draw_reason = "max_steps"

        # Final reward if terminal
        if terminated:
            if winner == 1:
                reward += self.reward_config["win"]
            elif winner == -1:
                reward += self.reward_config["loss"]
            else:
                reward += self.reward_config["draw"]

        # Build observation
        obs = self._build_observation()

        # Info dictionary
        info = {
            "current_player": self.current_player,
            "legal_actions_count": len(self.get_legal_actions()) if not terminated else 0,
            "captured": len(selected_move.captures),
            "promotion": selected_move.promotion,
            "step_count": self.step_count,
            "winner": winner if terminated else None,
            "draw_reason": draw_reason,
        }

        return obs, reward, terminated, truncated, info

    def get_legal_actions(self) -> List[Dict]:
        """Get list of legal actions in current state.

        Returns:
            List of action dictionaries
        """
        moves = self.rules.get_legal_moves(self.board, self.current_player)
        return [move.to_dict() for move in moves]

    def _build_observation(self) -> np.ndarray:
        """Build observation tensor from current board state.

        Returns:
            Observation tensor of shape (4, 8, 8)
        """
        return board_to_observation(self.board, self.current_player)

    def _compute_step_reward(self, move: Move) -> float:
        """Compute reward for a step.

        Args:
            move: Move that was executed

        Returns:
            Reward value
        """
        reward = 0.0

        # Capture reward
        if move.captures:
            reward += len(move.captures) * self.reward_config["capture"]

        # Promotion reward
        if move.promotion:
            reward += self.reward_config["king_promotion"]

        # Time penalty
        reward += self.reward_config["time_penalty"]

        return reward

    def render(self, mode: str = "ascii"):
        """Render the environment.

        Args:
            mode: Rendering mode ('ascii', 'human', 'rgb_array')
        """
        if mode == "ascii" or mode == "human":
            return self._render_ascii()
        elif mode == "rgb_array":
            return self._render_rgb_array()
        else:
            raise ValueError(f"Unknown render mode: {mode}")

    def _render_ascii(self) -> str:
        """Render board as ASCII.

        Returns:
            ASCII string representation
        """
        lines = []
        lines.append("  " + " ".join(str(i) for i in range(8)))
        lines.append("  " + "-" * 15)

        piece_chars = {
            0: ".",
            1: "r",  # Player 1 man
            2: "R",  # Player 1 king
            -1: "b",  # Player -1 man
            -2: "B",  # Player -1 king
        }

        for row in range(8):
            line = f"{row}| "
            for col in range(8):
                if (row + col) % 2 == 0:
                    line += " "  # Light square
                else:
                    piece = self.board[row, col]
                    line += piece_chars.get(piece, "?")
                line += " "
            lines.append(line)

        lines.append(f"\nCurrent player: {self.current_player} ({'Red' if self.current_player == 1 else 'Black'})")
        lines.append(f"Step: {self.step_count}")

        return "\n".join(lines)

    def _render_rgb_array(self) -> np.ndarray:
        """Render board as RGB array.

        Returns:
            RGB array representation (for future implementation)
        """
        # Placeholder for RGB rendering
        return np.zeros((8, 8, 3), dtype=np.uint8)

    def serialize(self) -> Dict:
        """Serialize current game state.

        Returns:
            Dictionary with game state
        """
        return {
            "board": self.board.tolist(),
            "current_player": self.current_player,
            "step_count": self.step_count,
            "move_history": self.move_history,
            "position_history": self.position_history[-10:],  # Last 10 positions
        }

    def deserialize(self, state: Dict):
        """Deserialize and load game state.

        Args:
            state: Dictionary with game state
        """
        self.board = np.array(state["board"], dtype=np.int8)
        self.current_player = state["current_player"]
        self.step_count = state["step_count"]
        self.move_history = state["move_history"]
        self.position_history = state.get("position_history", [])

