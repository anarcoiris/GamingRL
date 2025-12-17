
import numpy as np
import copy
from typing import Dict, List, Tuple, Optional
from env.rules import CheckersRules, Move

class HeuristicAgent:
    """
    A Minimax-based Heuristic Agent for Checkers.
    uses Alpha-Beta pruning to decide the best move.
    """

    def __init__(self, config: Dict, depth: int = 3):
        """
        Args:
            config: Game configuration dictionary.
            depth: Search depth for Minimax (default: 3).
        """
        self.config = config
        self.depth = depth
        self.rules = CheckersRules(config)
        self.search_player = 1 # Assigned during select_action

        # Weights
        self.W_MAN = 10.0
        self.W_KING = 15.0
        self.W_CENTER = 1.0

    def evaluate_board(self, board: np.ndarray) -> float:
        """
        Evaluate board state from perspective of Player 1.
        Positive score favors Player 1 (Red).
        Negative score favors Player 2 (Black).
        """
        score = 0.0
        p1_pieces = 0
        p2_pieces = 0

        rows, cols = board.shape
        center_rows = {3, 4}
        center_cols = {3, 4}

        for r in range(rows):
            for c in range(cols):
                piece = board[r, c]
                if piece == 0:
                    continue

                abs_piece = abs(piece)
                is_king = abs_piece == 2
                
                # Material Value
                value = self.W_KING if is_king else self.W_MAN
                
                # Positional Value (Center Control)
                if r in center_rows and c in center_cols:
                    value += self.W_CENTER

                # Add to total (P1 adds, P2 subtracts)
                if piece > 0:
                    score += value
                    p1_pieces += 1
                else:
                    score -= value
                    p2_pieces += 1
        
        # Win/Loss Check (Soft check, usually handled by terminal check in minimax)
        if p1_pieces == 0 and p2_pieces > 0:
            return -10000.0
        if p2_pieces == 0 and p1_pieces > 0:
            return 10000.0

        return score

    def select_action(self, board: np.ndarray, legal_actions: List[Dict], player: int = 1) -> Dict:
        """
        Select the best action from legal_actions.
        
        Args:
            board: Current board state (numpy array)
            legal_actions: List of legal actions (dicts)
            player: Current player (1 or -1)
            
        Returns:
            The selected action dictionary.
        """
        if not legal_actions:
            return None
        
        # If only one action, take it (forced)
        if len(legal_actions) == 1:
            return legal_actions[0]

        best_score = -float('inf') if player == 1 else float('inf')
        best_action = random_choice(legal_actions) # Fallback
        
        self.search_player = player
        
        # Shuffle actions to add randomness when scores are equal
        # But for 'Deterministic' bot, we might want fixed order?
        # User requested "Deterministic Algorithmic Bot".
        # We should NOT shuffle or seed it strictly.
        # Let's simple iterate. To be deterministic, input order matters.
        # CheckersRules returns deterministic order usually.

        for action_dict in legal_actions:
            # Reconstruct Move object
            move = self._dict_to_move(action_dict)
            
            # Apply move sim
            next_board = self.rules.apply_move(board, move, player)
            
            # Minimax search on next board
            # Next is opponent's turn -> player * -1
            score = self.minimax(next_board, self.depth - 1, -float('inf'), float('inf'), player * -1)
            
            if player == 1:
                # Maximizing
                if score > best_score:
                    best_score = score
                    best_action = action_dict
            else:
                # Minimizing
                if score < best_score:
                    best_score = score
                    best_action = action_dict
                    
        return best_action
    
    def minimax(self, board: np.ndarray, depth: int, alpha: float, beta: float, current_player_eval: int) -> float:
        """
        Minimax with Alpha-Beta Pruning.
        Returns the best score for the current board state.
        """
        # Check terminal
        is_terminal, winner = self.rules.is_terminal(board, current_player_eval)
        if is_terminal:
            if winner == 1:
                return 10000.0 + depth # Prefer winning faster
            elif winner == -1:
                return -10000.0 - depth # Prefer losing slower
            else:
                return 0.0 # Draw

        if depth == 0:
            return self.evaluate_board(board)

        legal_moves = self.rules.get_legal_moves(board, current_player_eval)
        if not legal_moves:
             # Should be caught by is_terminal usually, but strictly:
             # If no moves, you lose.
             return -10000.0 if current_player_eval == 1 else 10000.0

        if current_player_eval == 1:
            max_eval = -float('inf')
            for move in legal_moves:
                next_board = self.rules.apply_move(board, move, 1)
                eval = self.minimax(next_board, depth - 1, alpha, beta, -1)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                next_board = self.rules.apply_move(board, move, -1)
                eval = self.minimax(next_board, depth - 1, alpha, beta, 1)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def _dict_to_move(self, d: Dict) -> Move:
        return Move(
            from_pos=tuple(d['from']),
            to_pos=tuple(d['to']),
            captures=[tuple(c) for c in d.get('captures', [])],
            promotion=d.get('promotion', False)
        )

def random_choice(lst):
    # Deterministic fallback: take first
    return lst[0]
