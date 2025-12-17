
import pytest
import numpy as np
from agent.heuristic_agent import HeuristicAgent
from env.rules import CheckersRules, Move

# Mock config
TEST_CONFIG = {
    "board_size": 8,
    "capture_forced": True,
    "prefer_longest_capture": True,
    "king_on_last_row": True
}

@pytest.fixture
def rules():
    return CheckersRules(TEST_CONFIG)

@pytest.fixture
def agent():
    return HeuristicAgent(config=TEST_CONFIG, depth=2)

def create_board(pieces):
    """
    Helper to create a board from a list of pieces.
    pieces: list of (row, col, value)
    """
    board = np.zeros((8, 8), dtype=np.int8)
    for r, c, v in pieces:
        board[r, c] = v
    return board

def test_evaluate_material_balance(agent):
    # Equal material
    board = create_board([(0, 1, 1), (7, 0, -1)])
    # 1 vs -1 -> score 0 (relative to perspective, simplified)
    # Heuristic usually returns score for 'maximizing_player' or always for Player 1?
    # Standard: Score is always from perspective of Player 1 (Red).
    # Positive = Good for P1, Negative = Good for P2.
    
    score = agent.evaluate_board(board)
    assert score == 0

    # P1 has advantage (2 men vs 1 man)
    board = create_board([(0, 1, 1), (0, 3, 1), (7, 0, -1)])
    score = agent.evaluate_board(board)
    assert score > 0

    # P2 has advantage (1 man vs 1 king)
    board = create_board([(0, 1, 1), (7, 0, -2)])
    score = agent.evaluate_board(board)
    assert score < 0

def test_select_action_forced_capture(agent, rules):
    # Scene: P1 at (2,1), P2 at (3,2). P1 MUST capture (2,1)->(4,3).
    pieces = [
        (2, 1, 1),  # P1
        (3, 2, -1)  # P2
    ]
    board = create_board(pieces)
    
    # Env would pass legal actions. We simulate getting them from rules.
    legal_moves = [m.to_dict() for m in rules.get_legal_moves(board, 1)]
    assert len(legal_moves) == 1
    assert legal_moves[0]["captures"] != []
    
    action = agent.select_action(board, legal_moves, player=1)
    
    # Heuristic agent must select the only legal move (if forced)
    assert action == legal_moves[0]

def test_eval_center_control(agent):
    # Validates that center pieces are valued slightly higher
    # Board A: P1 piece in corner (7,0), P2 piece at (0,7) (to prevent win detection)
    board_a = create_board([(7, 0, 1), (0, 7, -1)])
    # Board B: P1 piece in center (4,2), P2 piece at (0,7) (Notice: (4,3)/(3,4) are center squares in logic)
    # let's use (3,4) which is in center_rows={3,4}, center_cols={3,4}
    board_b = create_board([(3, 4, 1), (0, 7, -1)])
    
    score_a = agent.evaluate_board(board_a)
    score_b = agent.evaluate_board(board_b)
    
    assert score_b > score_a

def test_minimax_find_win_in_one(agent, rules):
    # P1 at (5,2), P2 at (4,3). Cap -> (3,4).
    # But let's set up a choice.
    # Choice A: Move (5,0) -> (4,1) (Safe)
    # Choice B: Move (5,6) -> (4,7) (Results in getting captured next turn)
    # Actually simpler: Find a move that leads to better eval.
    pass

