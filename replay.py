"""Replay saved game JSON files with visual rendering."""

import argparse
import sys
import os
import json
import time
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from viz.board_renderer import EpisodeReplayRenderer
from utils.game_logger import load_game

def main():
    parser = argparse.ArgumentParser(description="GamingRL - Game Replayer")
    parser.add_argument("file", type=str, help="Path to game JSON file")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between moves")
    parser.add_argument("--no_rich", action="store_true", help="Disable Rich rendering")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File not found {args.file}")
        return

    print(f"Loading game: {args.file}")
    game_data = load_game(args.file)
    
    # Replay
    renderer = EpisodeReplayRenderer(use_rich=not args.no_rich)
    renderer.replay(game_data, delay=args.delay)

if __name__ == "__main__":
    main()
