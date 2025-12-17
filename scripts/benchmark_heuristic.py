
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import random
from env.checkers_env import CheckersEnv
from agent.heuristic_agent import HeuristicAgent
from tqdm import tqdm

def benchmark(num_games=50):
    env = CheckersEnv()
    
    # Initialize heuristic agent for Player 1
    heuristic_agent = HeuristicAgent(env.config, depth=2)
    
    results = {"win": 0, "loss": 0, "draw": 0}
    
    print(f"Running {num_games} games: Heuristic (P1) vs Random (P2)...")
    
    for _ in tqdm(range(num_games)):
        obs, info = env.reset()
        done = False
        truncated = False
        
        while not (done or truncated):
            current_player = env.current_player
            legal_actions = env.get_legal_actions()
            
            if current_player == 1:
                # Heuristic
                action = heuristic_agent.select_action(env.board, legal_actions, player=1)
            else:
                # Random
                if not legal_actions:
                    break # Should be handled by env step
                action = random.choice(legal_actions)
                
            obs, reward, done, truncated, info = env.step(action)
            
        winner = info.get("winner")
        if winner == 1:
            results["win"] += 1
        elif winner == -1:
            results["loss"] += 1
        else:
            results["draw"] += 1
            
    print("\nBenchmark Results:")
    print(f"Wins (Heuristic): {results['win']}")
    print(f"Losses (Random):  {results['loss']}")
    print(f"Draws:            {results['draw']}")
    
    win_rate = results["win"] / num_games
    print(f"Win Rate: {win_rate*100:.2f}%")
    
    if win_rate >= 0.90:
        print("SUCCESS: Heuristic agent achievement unlocked (>90% win rate)")
    else:
        print("WARNING: Heuristic agent underperforming")

if __name__ == "__main__":
    benchmark(num_games=20) # Start small for quick check
