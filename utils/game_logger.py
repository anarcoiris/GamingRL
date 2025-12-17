
import json
import uuid
import datetime
import numpy as np
from typing import Dict, Any, List

class GameLogger:
    """
    Logs game events and saves them to JSON format compatibility.
    """
    def __init__(self, metadata: Dict[str, Any] = None):
        self.game_id = str(uuid.uuid4())
        self.metadata = metadata or {}
        self.metadata["timestamp"] = datetime.datetime.now().isoformat()
        self.steps = []
        self.winner = None
        self.termination_reason = None
        
    def log_step(self, board: np.ndarray, action: Dict, player: int, step_count: int):
        """
        Log a single game step.
        """
        step_data = {
            "step_count": step_count,
            "current_player": player,
            "board": board.tolist(), # Convert numpy to list for JSON
            "action": action
        }
        self.steps.append(step_data)
        
    def log_game_over(self, winner: int, reason: str = None):
        """
        Log the end of the game.
        """
        self.winner = winner
        self.termination_reason = reason
        
    def get_game_data(self) -> Dict:
        """
        Return the complete game data structure.
        """
        return {
            "game_id": self.game_id,
            "metadata": self.metadata,
            "winner": self.winner,
            "termination_reason": self.termination_reason,
            "total_steps": len(self.steps),
            "steps": self.steps
        }
        
    def save(self, filepath: str):
        """
        Save game data to a JSON file.
        """
        data = self.get_game_data()
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

def load_game(filepath: str) -> Dict:
    """
    Load a game from JSON file.
    """
    with open(filepath, 'r') as f:
        return json.load(f)
