
import sys
import os
import re

# Ensure root is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from env.checkers_env import CheckersEnv
from agent.heuristic_agent import HeuristicAgent
from utils.game_logger import GameLogger

def parse_move_input(input_str):
    """
    Parse string like '5,0 4,1' or '5,0->4,1' or '5 0 4 1'
    Returns ((r1, c1), (r2, c2)) or None
    """
    # Extract all numbers
    nums = [int(n) for n in re.findall(r'\d+', input_str)]
    if len(nums) == 4:
        return (nums[0], nums[1]), (nums[2], nums[3])
    return None

def get_human_move(legal_actions):
    """
    Ask user for move until valid.
    """
    print("\nLegal Moves:")
    for i, move in enumerate(legal_actions):
        print(f"{i}: {move['from']} -> {move['to']} (Captures: {len(move.get('captures', []))})")
        
    while True:
        try:
            user_input = input("\nEnter move (e.g., '5,0 4,1') or move index (e.g., '0'): ")
            if user_input.lower() in ['q', 'quit', 'exit']:
                return None
            
            # Check if index
            if user_input.isdigit():
                idx = int(user_input)
                if 0 <= idx < len(legal_actions):
                    return legal_actions[idx]
            
            # Check if coordinates
            coords = parse_move_input(user_input)
            if coords:
                start, end = coords
                # Find matching action
                matches = [m for m in legal_actions if tuple(m['from']) == start and tuple(m['to']) == end]
                if matches:
                    if len(matches) > 1:
                        print("Ambiguous move (maybe multiple capture paths). Please select by index.")
                    else:
                        return matches[0]
            
            print("Invalid move format or illegal move. Try again.")
            
        except KeyboardInterrupt:
            return None
        except Exception as e:
            print(f"Error: {e}")

def play_game(outdir="data/generated"):
    env = CheckersEnv()
    
    # Human is Player 1 (Red), Bot is Player -1 (Black)
    # Or let user choose? Let's default Human=P1.
    human_player = 1
    bot = HeuristicAgent(env.config, depth=4) # Stronger bot for play
    
    logger = GameLogger(metadata={"p1": "human", "p2": "heuristic_depth_4"})
    
    obs, info = env.reset()
    print("Game Started! You are Player 1 (Red/r). Bot is Player -1 (Black/b).")
    
    done = False
    truncated = False
    
    while not (done or truncated):
        print("\n" + env.render())
        current_player = env.current_player
        legal_actions = env.get_legal_actions()
        
        if current_player == human_player:
            print(f"\nYour turn (Player {current_player})")
            action = get_human_move(legal_actions)
            if action is None:
                print("Game Aborted.")
                return
        else:
            print(f"\nBot turn (Player {current_player})...")
            action = bot.select_action(env.board, legal_actions, player=current_player)
            print(f"Bot chose: {action['from']} -> {action['to']}")
            
        logger.log_step(env.board, action, current_player, env.step_count)
        obs, reward, done, truncated, info = env.step(action)
        
    print("\n" + env.render())
    winner = info.get("winner")
    
    if winner == human_player:
        print("CONGRATULATIONS! You Won!")
    elif winner == -human_player:
        print("GAME OVER. Bot Won.")
    else:
        print("GAME OVER. Draw.")
        
    reason = info.get("draw_reason") if winner == 0 else "checkmate"
    logger.log_game_over(winner, reason)
    
    os.makedirs(outdir, exist_ok=True)
    filename = f"human_vs_bot_{logger.metadata['timestamp'].replace(':','-')}.json"
    save_path = os.path.join(outdir, filename)
    logger.save(save_path)
    print(f"Game saved to {save_path}")

if __name__ == "__main__":
    play_game()
