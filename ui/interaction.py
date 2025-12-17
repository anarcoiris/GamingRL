"""Interaction module for human player input and coordinate parsing."""

import re
from typing import List, Dict, Optional, Tuple

def coord_to_index(coord_str: str) -> Optional[Tuple[int, int]]:
    """
    Convert coordinate string like 'a3' or '5,0' to (row, col) indices.
    """
    coord_str = coord_str.strip().lower()
    
    # Try alphanumeric format like 'a3'
    alpha_match = re.match(r'^([a-h])([1-8])$', coord_str)
    if alpha_match:
        col = ord(alpha_match.group(1)) - ord('a')
        row = 8 - int(alpha_match.group(2))
        return (row, col)
    
    # Try numeric format like '5,0' or '5 0'
    num_match = re.findall(r'\d+', coord_str)
    if len(num_match) == 2:
        return (int(num_match[0]), int(num_match[1]))
        
    return None

def index_to_coord(row: int, col: int) -> str:
    """Convert (row, col) indices to alphanumeric 'a3' format."""
    return f"{chr(ord('a') + col)}{8 - row}"

def parse_human_move(input_str: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Parse moves like 'a3->b4', 'a3 b4', '5,0 4,1'.
    Returns (start_idx, end_idx) or None.
    """
    parts = re.split(r'[-\s>]+', input_str.strip())
    if len(parts) >= 2:
        start = coord_to_index(parts[0])
        end = coord_to_index(parts[1])
        if start and end:
            return (start, end)
    return None

def get_human_action(legal_actions: List[Dict], prompt: str = "Your move: ") -> Optional[Dict]:
    """
    Prompt user for a move and match against legal actions.
    
    Args:
        legal_actions: List of valid action dictionaries.
        prompt: CLI prompt string.
        
    Returns:
        Selected action dictionary or None if user quits.
    """
    print("\nValid moves notation: 'a3 b4' or enter index from list.")
    
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ['q', 'quit', 'exit']:
            return None
        
        # 1. Try matching by index
        if user_input.isdigit():
            idx = int(user_input)
            if 0 <= idx < len(legal_actions):
                return legal_actions[idx]
        
        # 2. Try matching by coordinate
        parsed = parse_human_move(user_input)
        if parsed:
            start_idx, end_idx = parsed
            matches = [
                a for a in legal_actions 
                if tuple(a["from"]) == start_idx and tuple(a["to"]) == end_idx
            ]
            
            if len(matches) == 1:
                return matches[0]
            elif len(matches) > 1:
                print("Ambiguous move (multiple jump paths). Please use index:")
                for i, m in enumerate(matches):
                    # Find the index in the original list
                    orig_idx = next(j for j, la in enumerate(legal_actions) if la == m)
                    print(f"  {orig_idx}: {m['from']} -> {m['to']} (captures {len(m.get('captures', []))})")
                continue
        
        print("Invalid move. Try 'a3 b4' or enter the move index.")

def list_legal_moves(legal_actions: List[Dict]):
    """Print legal moves in a readable format."""
    print("\nLegal Actions:")
    for i, a in enumerate(legal_actions):
        from_str = index_to_coord(a["from"][0], a["from"][1])
        to_str = index_to_coord(a["to"][0], a["to"][1])
        caps = len(a.get("captures", []))
        cap_str = f" [CAPS: {caps}]" if caps > 0 else ""
        print(f"  {i}: {from_str} -> {to_str}{cap_str}")
