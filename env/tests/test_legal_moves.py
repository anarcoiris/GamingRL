"""Tests for legal moves generation."""

import pytest
import numpy as np
import json
import os
from pathlib import Path

from env.rules import CheckersRules, Move
from env.checkers_env import CheckersEnv


def load_test_case(test_id: str) -> dict:
    """Load test case from JSON file.

    Args:
        test_id: Test ID (e.g., 'test_001')

    Returns:
        Test case dictionary
    """
    test_dir = Path(__file__).parent / "test_cases"
    test_file = test_dir / f"{test_id}.json"
    
    if not test_file.exists():
        pytest.skip(f"Test case {test_id} not found")
    
    with open(test_file, "r") as f:
        return json.load(f)


def board_from_list(board_list: list) -> np.ndarray:
    """Convert board from list format to numpy array.

    Args:
        board_list: List of lists representing board

    Returns:
        Numpy array board
    """
    return np.array(board_list, dtype=np.int8)


def action_to_tuple(action_dict: dict) -> tuple:
    """Convert action dict to tuple for comparison.

    Args:
        action_dict: Action dictionary

    Returns:
        Tuple (from, to, captures_set)
    """
    return (
        tuple(action_dict["from"]),
        tuple(action_dict["to"]),
        frozenset(tuple(c) for c in action_dict.get("captures", [])),
    )


class TestLegalMoves:
    """Test legal moves generation."""

    def test_simple_move(self):
        """Test simple move generation."""
        test_case = load_test_case("test_001")
        board = board_from_list(test_case["board_state"])
        current_player = test_case["current_player"]

        config = {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
        }
        rules = CheckersRules(config)
        legal_moves = rules.get_legal_moves(board, current_player)

        # Convert to comparable format
        legal_tuples = {action_to_tuple(m.to_dict()) for m in legal_moves}
        expected_tuples = {
            action_to_tuple(a) for a in test_case["expected_legal_moves"]
        }

        # Check that all expected moves are present
        assert expected_tuples.issubset(
            legal_tuples
        ), f"Expected moves not all found. Expected: {expected_tuples}, Got: {legal_tuples}"

    def test_forced_capture(self):
        """Test forced capture rule."""
        test_case = load_test_case("test_002")
        board = board_from_list(test_case["board_state"])
        current_player = test_case["current_player"]

        config = {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
        }
        rules = CheckersRules(config)
        legal_moves = rules.get_legal_moves(board, current_player)

        # All moves must be captures
        assert all(
            len(m.captures) > 0 for m in legal_moves
        ), "All moves should be captures when capture is forced"

        # Check expected move is present
        expected_move = test_case["expected_legal_moves"][0]
        expected_tuple = action_to_tuple(expected_move)
        legal_tuples = {action_to_tuple(m.to_dict()) for m in legal_moves}

        assert (
            expected_tuple in legal_tuples
        ), f"Expected capture move not found: {expected_move}"

    def test_multi_jump(self):
        """Test multi-jump sequence."""
        test_case = load_test_case("test_003")
        board = board_from_list(test_case["board_state"])
        current_player = test_case["current_player"]

        config = {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
        }
        rules = CheckersRules(config)
        legal_moves = rules.get_legal_moves(board, current_player)

        # Should have multi-jump move
        expected_move = test_case["expected_legal_moves"][0]
        assert expected_move["sequence_length"] > 1, "Should have multi-jump"

        expected_tuple = action_to_tuple(expected_move)
        legal_tuples = {action_to_tuple(m.to_dict()) for m in legal_moves}

        assert (
            expected_tuple in legal_tuples
        ), f"Expected multi-jump not found: {expected_move}"

    def test_prefer_longest_capture(self):
        """Test preference for longest capture."""
        test_case = load_test_case("test_004")
        board = board_from_list(test_case["board_state"])
        current_player = test_case["current_player"]

        config = {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
        }
        rules = CheckersRules(config)
        legal_moves = rules.get_legal_moves(board, current_player)

        # All moves should have same (maximum) capture length
        if legal_moves:
            max_captures = max(len(m.captures) for m in legal_moves)
            assert all(
                len(m.captures) == max_captures for m in legal_moves
            ), "All moves should have maximum capture length"

    def test_king_promotion_during_capture(self):
        """Test king promotion during capture sequence."""
        test_case = load_test_case("test_006")
        board = board_from_list(test_case["board_state"])
        current_player = test_case["current_player"]

        config = {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
        }
        rules = CheckersRules(config)
        legal_moves = rules.get_legal_moves(board, current_player)

        # Should have move with promotion
        expected_move = test_case["expected_legal_moves"][0]
        assert expected_move["promotion"], "Should have promotion"

        expected_tuple = action_to_tuple(expected_move)
        legal_tuples = {action_to_tuple(m.to_dict()) for m in legal_moves}

        assert (
            expected_tuple in legal_tuples
        ), f"Expected promotion move not found: {expected_move}"

    def test_initial_board_moves(self):
        """Test legal moves from initial board position."""
        test_case = load_test_case("test_013")
        board = board_from_list(test_case["board_state"])
        current_player = test_case["current_player"]

        config = {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
        }
        rules = CheckersRules(config)
        legal_moves = rules.get_legal_moves(board, current_player)

        # Should have some legal moves
        if "expected_legal_moves_count" in test_case:
            expected_count = test_case["expected_legal_moves_count"]
            assert (
                len(legal_moves) == expected_count
            ), f"Expected {expected_count} moves, got {len(legal_moves)}"
        else:
            assert len(legal_moves) > 0, "Should have legal moves from initial position"

    def test_blocked_piece(self):
        """Test terminal state when piece is blocked."""
        test_case = load_test_case("test_008")
        board = board_from_list(test_case["board_state"])
        current_player = test_case["current_player"]

        config = {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
        }
        rules = CheckersRules(config)
        legal_moves = rules.get_legal_moves(board, current_player)

        # Should have no legal moves (terminal state)
        assert len(legal_moves) == 0, "Should have no legal moves when blocked"

        # Check terminal state
        is_terminal, winner = rules.is_terminal(board, current_player)
        assert is_terminal, "Should be terminal state"
        if test_case.get("expected_outcome") == "win":
            assert winner == -current_player, "Opponent should win"

    def test_no_pieces(self):
        """Test terminal state when opponent has no pieces."""
        test_case = load_test_case("test_009")
        board = board_from_list(test_case["board_state"])
        current_player = test_case["current_player"]

        config = {
            "board_size": 8,
            "capture_forced": True,
            "prefer_longest_capture": True,
        }
        rules = CheckersRules(config)
        
        # Check terminal state
        is_terminal, winner = rules.is_terminal(board, current_player)
        assert is_terminal, "Should be terminal state"
        if test_case.get("expected_outcome") == "win":
            assert winner == current_player, "Current player should win"

