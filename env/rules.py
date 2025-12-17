"""Rules and move generation for checkers game."""

import numpy as np
from typing import List, Dict, Tuple, Optional
import copy


class Move:
    """Represents a move in checkers."""

    def __init__(
        self,
        from_pos: Tuple[int, int],
        to_pos: Tuple[int, int],
        captures: List[Tuple[int, int]] = None,
        promotion: bool = False,
    ):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.captures = captures if captures is not None else []
        self.promotion = promotion
        self.sequence_length = len(self.captures) + (1 if not self.captures else 0)

    def to_dict(self) -> Dict:
        """Convert move to dictionary format."""
        return {
            "from": list(self.from_pos),
            "to": list(self.to_pos),
            "captures": [list(c) for c in self.captures],
            "promotion": self.promotion,
            "sequence_length": self.sequence_length,
        }

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return (
            self.from_pos == other.from_pos
            and self.to_pos == other.to_pos
            and self.captures == other.captures
            and self.promotion == other.promotion
        )

    def __hash__(self):
        return hash(
            (self.from_pos, self.to_pos, tuple(self.captures), self.promotion)
        )

    def __repr__(self):
        return f"Move(from={self.from_pos}, to={self.to_pos}, captures={len(self.captures)}, promotion={self.promotion})"


class CheckersRules:
    """Handles checkers game rules and move generation."""

    # Board values
    EMPTY = 0
    PLAYER1_MAN = 1
    PLAYER1_KING = 2
    PLAYER2_MAN = -1
    PLAYER2_KING = -2

    def __init__(self, config: Dict):
        """Initialize rules with configuration.

        Args:
            config: Configuration dictionary with game rules
        """
        self.board_size = config.get("board_size", 8)
        self.capture_forced = config.get("capture_forced", True)
        self.prefer_longest_capture = config.get("prefer_longest_capture", True)
        self.king_on_last_row = config.get("king_on_last_row", True)

    def is_valid_square(self, row: int, col: int) -> bool:
        """Check if square is valid and playable (dark squares only).

        Args:
            row: Row index (0-7)
            col: Column index (0-7)

        Returns:
            True if square is valid and playable
        """
        if not (0 <= row < self.board_size and 0 <= col < self.board_size):
            return False
        # Only dark squares are playable (row + col is odd)
        return (row + col) % 2 == 1

    def get_move_directions(self, piece_value: int, is_king: bool = False) -> List[Tuple[int, int]]:
        """Get valid move directions for a piece.

        Args:
            piece_value: Piece value (1, 2, -1, -2)
            is_king: Whether piece is a king

        Returns:
            List of (row_delta, col_delta) directions
        """
        if is_king:
            # Kings can move in all 4 diagonal directions
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        else:
            # Men can only move forward (toward opponent)
            if piece_value > 0:  # Player 1 moves down (positive row)
                return [(1, -1), (1, 1)]
            else:  # Player -1 moves up (negative row)
                return [(-1, -1), (-1, 1)]

    def get_simple_moves(
        self, board: np.ndarray, row: int, col: int, player: int
    ) -> List[Move]:
        """Get simple (non-capture) moves for a piece.

        Args:
            board: Board state (8x8 array)
            row: Row of piece
            col: Column of piece
            player: Player (1 or -1)

        Returns:
            List of simple moves
        """
        moves = []
        piece_value = board[row, col]
        is_king = abs(piece_value) == 2

        directions = self.get_move_directions(piece_value, is_king)

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc

            if not self.is_valid_square(new_row, new_col):
                continue

            if board[new_row, new_col] == self.EMPTY:
                # Check for promotion
                promotion = False
                if not is_king:
                    if player == 1 and new_row == self.board_size - 1:
                        promotion = True
                    elif player == -1 and new_row == 0:
                        promotion = True

                moves.append(
                    Move(
                        from_pos=(row, col),
                        to_pos=(new_row, new_col),
                        captures=[],
                        promotion=promotion,
                    )
                )

        return moves

    def get_capture_moves(
        self, board: np.ndarray, row: int, col: int, player: int
    ) -> List[Move]:
        """Get capture moves (including multi-jump) for a piece.

        Args:
            board: Board state (8x8 array)
            row: Row of piece
            col: Column of piece
            player: Player (1 or -1)

        Returns:
            List of capture moves (including multi-jump sequences)
        """
        return self._generate_captures_recursive(
            board, row, col, player, captures_so_far=[]
        )

    def _generate_captures_recursive(
        self,
        board: np.ndarray,
        row: int,
        col: int,
        player: int,
        captures_so_far: List[Tuple[int, int]],
    ) -> List[Move]:
        """Recursively generate all capture sequences from a position.

        Args:
            board: Current board state
            row: Current row
            col: Current column
            player: Current player
            captures_so_far: List of positions captured so far in sequence

        Returns:
            List of complete capture moves
        """
        moves = []
        piece_value = board[row, col]
        is_king = abs(piece_value) == 2

        directions = self.get_move_directions(piece_value, is_king)

        for dr, dc in directions:
            # Check if we can jump over an opponent piece
            jump_row = row + dr
            jump_col = col + dc

            if not self.is_valid_square(jump_row, jump_col):
                continue

            # Must jump over opponent piece
            jumped_piece = board[jump_row, jump_col]
            if jumped_piece == self.EMPTY or (jumped_piece * player > 0):
                continue  # Empty or own piece

            # Landing square
            land_row = jump_row + dr
            land_col = jump_col + dc

            if not self.is_valid_square(land_row, land_col):
                continue

            if board[land_row, land_col] != self.EMPTY:
                continue  # Landing square must be empty

            # Create new board state after this capture
            new_board = board.copy()
            new_board[land_row, land_col] = new_board[row, col]
            new_board[row, col] = self.EMPTY
            new_board[jump_row, jump_col] = self.EMPTY

            # Check for promotion during capture sequence
            new_promotion = False
            new_is_king = is_king
            if not is_king:
                if player == 1 and land_row == self.board_size - 1:
                    new_promotion = True
                    new_is_king = True
                    new_board[land_row, land_col] = self.PLAYER1_KING if player == 1 else self.PLAYER2_KING
                elif player == -1 and land_row == 0:
                    new_promotion = True
                    new_is_king = True
                    new_board[land_row, land_col] = self.PLAYER1_KING if player == 1 else self.PLAYER2_KING

            # Update directions if piece was promoted
            if new_is_king and not is_king:
                directions = self.get_move_directions(
                    self.PLAYER1_KING if player == 1 else self.PLAYER2_KING, True
                )

            new_captures = captures_so_far + [(jump_row, jump_col)]

            # Check for additional captures from new position
            additional_moves = self._generate_captures_recursive(
                new_board, land_row, land_col, player, new_captures
            )

            if additional_moves:
                # Extend current sequence with additional captures
                moves.extend(additional_moves)
            else:
                # This is a complete capture sequence
                moves.append(
                    Move(
                        from_pos=(row, col),
                        to_pos=(land_row, land_col),
                        captures=new_captures,
                        promotion=new_promotion or (len(captures_so_far) == 0 and new_promotion),
                    )
                )

        return moves

    def get_legal_moves(
        self, board: np.ndarray, player: int
    ) -> List[Move]:
        """Get all legal moves for a player.

        Args:
            board: Board state (8x8 array)
            player: Player (1 or -1)

        Returns:
            List of legal moves
        """
        all_moves = []
        capture_moves = []

        # Find all pieces for this player
        for row in range(self.board_size):
            for col in range(self.board_size):
                if not self.is_valid_square(row, col):
                    continue

                piece_value = board[row, col]
                if piece_value == 0:
                    continue

                # Check if piece belongs to player
                if (player == 1 and piece_value > 0) or (
                    player == -1 and piece_value < 0
                ):
                    # Get simple moves
                    simple_moves = self.get_simple_moves(board, row, col, player)
                    all_moves.extend(simple_moves)

                    # Get capture moves
                    captures = self.get_capture_moves(board, row, col, player)
                    capture_moves.extend(captures)

        # If captures are available and forced, only return captures
        if self.capture_forced and capture_moves:
            if self.prefer_longest_capture:
                # Find maximum capture length
                max_captures = max(len(m.captures) for m in capture_moves)
                # Return only moves with maximum captures
                return [m for m in capture_moves if len(m.captures) == max_captures]
            else:
                return capture_moves

        # No captures or captures not forced, return all moves
        return all_moves

    def apply_move(self, board: np.ndarray, move: Move, player: int) -> np.ndarray:
        """Apply a move to the board.

        Args:
            board: Current board state
            move: Move to apply
            player: Player making the move

        Returns:
            New board state
        """
        new_board = board.copy()

        # Remove captured pieces
        for cap_row, cap_col in move.captures:
            new_board[cap_row, cap_col] = self.EMPTY

        # Move piece
        piece_value = new_board[move.from_pos[0], move.from_pos[1]]
        new_board[move.to_pos[0], move.to_pos[1]] = piece_value
        new_board[move.from_pos[0], move.from_pos[1]] = self.EMPTY

        # Handle promotion
        if move.promotion:
            if player == 1:
                new_board[move.to_pos[0], move.to_pos[1]] = self.PLAYER1_KING
            else:
                new_board[move.to_pos[0], move.to_pos[1]] = self.PLAYER2_KING

        return new_board

    def is_terminal(self, board: np.ndarray, current_player: int) -> Tuple[bool, Optional[int]]:
        """Check if game is in terminal state.

        Args:
            board: Board state
            current_player: Current player (1 or -1)

        Returns:
            (is_terminal, winner) where winner is 1, -1, 0 (draw), or None
        """
        opponent = -current_player

        # Check if opponent has no pieces
        opponent_has_pieces = False
        player_has_pieces = False

        for row in range(self.board_size):
            for col in range(self.board_size):
                if not self.is_valid_square(row, col):
                    continue
                piece = board[row, col]
                if piece > 0:
                    player_has_pieces = True
                elif piece < 0:
                    opponent_has_pieces = True

        if not opponent_has_pieces:
            return True, current_player  # Current player wins
        if not player_has_pieces:
            return True, opponent  # Opponent wins

        # Check if opponent has legal moves
        opponent_moves = self.get_legal_moves(board, opponent)
        if not opponent_moves:
            return True, current_player  # Opponent has no moves, current player wins

        # Check if current player has legal moves
        player_moves = self.get_legal_moves(board, current_player)
        if not player_moves:
            return True, opponent  # Current player has no moves, opponent wins

        return False, None

