
import pytest
import numpy as np
import os
import json
from utils.game_logger import GameLogger, load_game

def test_logger_flow(tmp_path):
    # Setup
    logger = GameLogger(metadata={"p1": "heuristic", "p2": "random"})
    
    # Log step
    board = np.zeros((8, 8), dtype=np.int8)
    action = {"from": [0,0], "to": [1,1]}
    logger.log_step(board, action, player=1, step_count=0)
    
    # Log outcome
    logger.log_game_over(winner=1, reason="capture")
    
    # Save
    filepath = tmp_path / "test_game.json"
    logger.save(str(filepath))
    
    # Verify file exists
    assert os.path.exists(filepath)
    
    # Load and verify content
    data = load_game(str(filepath))
    assert data["game_id"] == logger.game_id
    assert data["winner"] == 1
    assert data["metadata"]["p1"] == "heuristic"
    assert len(data["steps"]) == 1
    assert data["steps"][0]["action"]["from"] == [0, 0]
    
    # Verify numpy conversion
    assert isinstance(data["steps"][0]["board"], list)
